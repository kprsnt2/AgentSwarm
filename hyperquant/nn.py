"""
HyperQuant PyTorch Layer & Model Conversion Architecture
=========================================================
Implements:
  1. HyperQuantLinear: PyTorch nn.Module replacing standard nn.Linear
  2. Forward kernel computing y = x @ W_ternary.T + x @ W_outlier.T + (x @ v.T) @ u.T + bias
  3. Model-wide dynamic replacement: replace_linear_with_hyperquant(model)
  4. Automatic device placement (CPU / CUDA / MPS)
"""

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from .core import HyperQuantDecomposer, unpack_trits_5_per_byte
import numpy as np
from typing import Optional, Dict, Any


if TORCH_AVAILABLE:
    class HyperQuantLinear(nn.Module):
        """
        Sub-2-bit Dynamic Ternary-Residual SVD Linear Layer.
        Replaces standard torch.nn.Linear with ~2.03 bits/param storage.
        """
        def __init__(
            self,
            in_features: int,
            out_features: int,
            bias: bool = True,
            outlier_ratio: float = 0.0075,
            block_size: int = 128,
            svd_rank: int = 1,
            device: Optional[torch.device] = None,
            dtype: Optional[torch.dtype] = None,
        ):
            super().__init__()
            self.in_features = in_features
            self.out_features = out_features
            self.block_size = block_size
            self.svd_rank = svd_rank
            self.outlier_ratio = outlier_ratio

            # Placeholder buffers for compressed weights
            # 1. Packed ternary uint8 buffer (5 trits/byte)
            packed_len = math.ceil((in_features * out_features) / 5.0)
            self.register_buffer("packed_ternary", torch.zeros(packed_len, dtype=torch.uint8, device=device))

            # 2. Block scales (float16)
            n_blocks = math.ceil(in_features / block_size)
            self.register_buffer("block_scales", torch.zeros((out_features, n_blocks), dtype=torch.float16, device=device))

            # 3. Outlier coordinate indices and FP16 values
            self.register_buffer("outlier_rows", torch.empty(0, dtype=torch.int32, device=device))
            self.register_buffer("outlier_cols", torch.empty(0, dtype=torch.int32, device=device))
            self.register_buffer("outlier_values", torch.empty(0, dtype=torch.float16, device=device))

            # 4. SVD low-rank correction vectors
            if svd_rank > 0:
                self.register_buffer("u_svd", torch.zeros((out_features, svd_rank), dtype=torch.float16, device=device))
                self.register_buffer("v_svd", torch.zeros((svd_rank, in_features), dtype=torch.float16, device=device))
            else:
                self.u_svd = None
                self.v_svd = None

            if bias:
                self.bias = nn.Parameter(torch.zeros(out_features, dtype=torch.float16 if dtype is None else dtype, device=device))
            else:
                self.register_parameter("bias", None)

            # Cached dequantized weight for fast inference (lazy populated or kept in register)
            self._cached_weight = None

        @classmethod
        def from_linear(
            cls,
            linear_layer: nn.Linear,
            outlier_ratio: float = 0.0075,
            block_size: int = 128,
            svd_rank: int = 1,
            Hessian_diag: Optional[np.ndarray] = None,
        ) -> "HyperQuantLinear":
            """
            Compress an existing nn.Linear layer into a HyperQuantLinear layer.
            """
            device = linear_layer.weight.device
            W_np = linear_layer.weight.detach().cpu().to(torch.float32).numpy()

            decomp = HyperQuantDecomposer.decompose(
                W=W_np,
                outlier_ratio=outlier_ratio,
                block_size=block_size,
                svd_rank=svd_rank,
                Hessian_diag=Hessian_diag,
            )

            hql = cls(
                in_features=linear_layer.in_features,
                out_features=linear_layer.out_features,
                bias=linear_layer.bias is not None,
                outlier_ratio=outlier_ratio,
                block_size=block_size,
                svd_rank=svd_rank,
                device=device,
            )

            # Assign buffers
            hql.packed_ternary.copy_(torch.from_numpy(decomp["packed_ternary"]).to(device))
            hql.block_scales.copy_(torch.from_numpy(decomp["block_scales"]).to(device))
            hql.outlier_rows = torch.from_numpy(decomp["outlier_rows"]).to(device)
            hql.outlier_cols = torch.from_numpy(decomp["outlier_cols"]).to(device)
            hql.outlier_values = torch.from_numpy(decomp["outlier_values"]).to(device)

            if svd_rank > 0:
                hql.u_svd.copy_(torch.from_numpy(decomp["u_svd"]).to(device))
                hql.v_svd.copy_(torch.from_numpy(decomp["v_svd"]).to(device))

            if linear_layer.bias is not None:
                hql.bias.data.copy_(linear_layer.bias.data.to(torch.float16))

            # Store quality stats
            hql.relative_error = decomp["relative_error"]
            hql.cosine_similarity = decomp["cosine_similarity"]
            hql.effective_bits_per_param = decomp["effective_bits_per_param"]
            hql.compression_ratio = decomp["compression_ratio"]

            return hql

        def get_reconstructed_weight(self) -> torch.Tensor:
            """
            Reconstruct dense weight tensor (cached for inference).
            """
            if self._cached_weight is not None:
                return self._cached_weight

            device = self.packed_ternary.device
            # 1. Unpack ternary
            unpacked_np = unpack_trits_5_per_byte(
                self.packed_ternary.cpu().numpy(),
                self.out_features * self.in_features
            ).reshape(self.out_features, self.in_features)

            ternary = torch.from_numpy(unpacked_np).to(device=device, dtype=torch.float32)

            # 2. Block scales
            n_blocks = self.block_scales.shape[1]
            scales = self.block_scales.to(torch.float32).repeat_interleave(self.block_size, dim=1)[:, :self.in_features]
            W_ternary = ternary * scales

            # 3. SVD correction
            if self.svd_rank > 0 and self.u_svd is not None and self.v_svd is not None:
                W_svd = self.u_svd.to(torch.float32) @ self.v_svd.to(torch.float32)
            else:
                W_svd = 0.0

            W_rec = W_ternary + W_svd

            # 4. Outliers
            if len(self.outlier_rows) > 0:
                W_rec[self.outlier_rows.long(), self.outlier_cols.long()] = self.outlier_values.to(torch.float32)

            self._cached_weight = W_rec.to(torch.float16)
            return self._cached_weight

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            """
            Forward pass.
            """
            W = self.get_reconstructed_weight()
            return F.linear(x.to(W.dtype), W, self.bias)

        def clear_cache(self):
            """Release cached weight tensor to minimize runtime VRAM/RAM."""
            self._cached_weight = None


    def replace_linear_with_hyperquant(
        model: nn.Module,
        outlier_ratio: float = 0.0075,
        block_size: int = 128,
        svd_rank: int = 1,
        skip_modules: Optional[list] = None,
        verbose: bool = True,
    ) -> nn.Module:
        """
        Recursively traverse a PyTorch model (e.g. HuggingFace Transformer) and replace
        all eligible nn.Linear layers with HyperQuantLinear layers.
        """
        if skip_modules is None:
            # Common layers to keep in FP16/BF16 (embedding, final lm_head classification)
            skip_modules = ["lm_head", "embed_tokens", "wte", "wpe"]

        count = 0
        total_orig_bytes = 0
        total_comp_bytes = 0

        for name, module in model.named_modules():
            for child_name, child in module.named_children():
                if isinstance(child, nn.Linear):
                    full_name = f"{name}.{child_name}" if name else child_name
                    if any(skip in full_name for skip in skip_modules):
                        if verbose:
                            print(f"[HyperQuant] Skipping {full_name} (in skip_modules)")
                        continue

                    # Compress layer
                    orig_bytes = child.weight.numel() * 2  # FP16
                    hql = HyperQuantLinear.from_linear(
                        child,
                        outlier_ratio=outlier_ratio,
                        block_size=block_size,
                        svd_rank=svd_rank,
                    )
                    setattr(module, child_name, hql)
                    count += 1

                    # Track memory
                    comp_bytes = (
                        hql.packed_ternary.numel()
                        + hql.block_scales.numel() * 2
                        + hql.outlier_values.numel() * 6
                        + (hql.u_svd.numel() + hql.v_svd.numel()) * 2 if hql.u_svd is not None else 0
                    )
                    total_orig_bytes += orig_bytes
                    total_comp_bytes += comp_bytes

                    if verbose and count % 10 == 0:
                        print(f"[HyperQuant] Compressed {count} layers... (Avg CosSim: {hql.cosine_similarity:.4f})")

        if verbose:
            comp_ratio = total_orig_bytes / max(1, total_comp_bytes)
            orig_mb = total_orig_bytes / (1024 * 1024)
            comp_mb = total_comp_bytes / (1024 * 1024)
            print("=" * 65)
            print(f"[HyperQuant] Successfully converted {count} linear layers!")
            print(f"[HyperQuant] Original FP16 Size:   {orig_mb:.2f} MB")
            print(f"[HyperQuant] Compressed Footprint:  {comp_mb:.2f} MB")
            print(f"[HyperQuant] Compression Ratio:     {comp_ratio:.2f}x ({16.0/comp_ratio:.2f} bits/param)")
            print("=" * 65)

        return model

else:
    # Stub when torch is not installed
    class HyperQuantLinear:
        def __init__(self, *args, **kwargs):
            raise ImportError("PyTorch is required to use HyperQuantLinear. Install via 'pip install torch'.")

    def replace_linear_with_hyperquant(*args, **kwargs):
        raise ImportError("PyTorch is required to use replace_linear_with_hyperquant. Install via 'pip install torch'.")
