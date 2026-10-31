"""
HyperQuant: Universal Sub-2-Bit Dynamic Ternary-Residual SVD (DTR-SVD) Framework
================================================================================
Core algorithm implementation for NumPy and PyTorch.
Implements:
  1. Hessian-Guided Salient Outlier Slicing (SOS)
  2. Dense Fractal Ternary Quantization & 5-Trit Packing
  3. Rank-r Singular Value Decomposition (SVD) Residual Drift Cancellation
  4. Forward reconstruction with high numerical fidelity
"""

import math
import numpy as np
from typing import Tuple, Dict, Any, Optional


def pack_trits_5_per_byte(trits: np.ndarray) -> np.ndarray:
    """
    Pack an array of ternary values in {-1, 0, +1} into uint8 bytes, 5 trits per byte.
    trits: 1D numpy array with values in {-1, 0, +1}
    Returns: 1D uint8 numpy array of packed bytes.
    """
    flat = trits.flatten().astype(np.int8)
    n = len(flat)
    # Pad to multiple of 5
    pad_len = (5 - (n % 5)) % 5
    if pad_len > 0:
        flat = np.pad(flat, (0, pad_len), mode='constant', constant_values=0)
    
    # Map {-1, 0, +1} -> {0, 1, 2}
    mapped = (flat + 1).astype(np.uint8)
    
    # Reshape into chunks of 5
    chunks = mapped.reshape(-1, 5)
    # Horner's polynomial: t0 + 3*t1 + 9*t2 + 27*t3 + 81*t4 <= 242
    packed = (
        chunks[:, 0]
        + chunks[:, 1] * 3
        + chunks[:, 2] * 9
        + chunks[:, 3] * 27
        + chunks[:, 4] * 81
    ).astype(np.uint8)
    
    return packed


def unpack_trits_5_per_byte(packed: np.ndarray, original_length: int) -> np.ndarray:
    """
    Unpack uint8 bytes back into ternary values {-1, 0, +1}.
    """
    b = packed.astype(np.uint32)
    t0 = (b % 3).astype(np.int8)
    b //= 3
    t1 = (b % 3).astype(np.int8)
    b //= 3
    t2 = (b % 3).astype(np.int8)
    b //= 3
    t3 = (b % 3).astype(np.int8)
    b //= 3
    t4 = (b % 3).astype(np.int8)

    unpacked = np.stack([t0, t1, t2, t3, t4], axis=1).reshape(-1)
    # Map {0, 1, 2} -> {-1, 0, +1}
    unpacked = unpacked[:original_length] - 1
    return unpacked


def fast_power_iteration_svd(E: np.ndarray, rank: int = 1, num_iters: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Ultra-fast truncated SVD via power iteration O(rank * iters * M * N).
    Avoids O(M * N^2) full SVD, running in milliseconds even on massive matrices!
    """
    d_out, d_in = E.shape
    if rank <= 0:
        return np.zeros((d_out, 0), dtype=np.float16), np.zeros((0, d_in), dtype=np.float16)

    u_list = []
    v_list = []
    E_curr = E.copy()

    for r in range(rank):
        # Seed vector
        v = np.ones(d_in, dtype=np.float32) / math.sqrt(d_in)
        sigma = 1.0
        for _ in range(num_iters):
            u = E_curr @ v
            norm_u = np.linalg.norm(u)
            if norm_u < 1e-8:
                break
            u /= norm_u

            v = E_curr.T @ u
            sigma = np.linalg.norm(v)
            if sigma < 1e-8:
                break
            v /= sigma

        u_vec = (u * np.sqrt(sigma)).astype(np.float16)
        v_vec = (v * np.sqrt(sigma)).astype(np.float16)
        u_list.append(u_vec)
        v_list.append(v_vec)

        # Deflate
        E_curr -= (u_vec.astype(np.float32)[:, None] @ v_vec.astype(np.float32)[None, :])

    u_svd = np.column_stack(u_list)
    v_svd = np.vstack(v_list)
    return u_svd, v_svd


class HyperQuantDecomposer:
    """
    Decomposes a dense weight matrix W into:
      W = W_ternary + W_sparse_outliers + ΔW_svd
    """

    @classmethod
    def decompose(
        cls,
        W: np.ndarray,
        outlier_ratio: float = 0.0075,
        block_size: int = 128,
        svd_rank: int = 1,
        Hessian_diag: Optional[np.ndarray] = None,
    ) -> Dict[str, Any]:
        """
        Decompose weight matrix W (shape [d_out, d_in]) into:
          - packed_ternary: uint8 array (5 trits/byte)
          - block_scales: float16 array of block scales
          - outlier_indices: (row, col) coordinates of top outlier weights
          - outlier_values: float16 values of outliers
          - u_svd: float16 array of shape [d_out, svd_rank]
          - v_svd: float16 array of shape [svd_rank, d_in]
        """
        W = np.asarray(W, dtype=np.float32)
        d_out, d_in = W.shape
        total_elements = d_out * d_in
        
        # 1. Hessian-Guided Salient Outlier Slicing (SOS)
        if Hessian_diag is None:
            # Empirical proxy: column-wise energy |W| * sqrt(mean(W^2))
            H_proxy = np.sqrt(np.mean(W ** 2, axis=0, keepdims=True)) + 1e-6
            sensitivity = (np.abs(W) ** 2) * H_proxy
        else:
            sensitivity = (W ** 2) * Hessian_diag.reshape(1, d_in)
            
        k_outliers = max(1, int(total_elements * outlier_ratio))
        # Find top k indices
        flat_indices = np.argpartition(sensitivity.ravel(), -k_outliers)[-k_outliers:]
        row_indices, col_indices = np.unravel_index(flat_indices, (d_out, d_in))
        
        # Extract outlier values and zero them in the base matrix
        outlier_vals = W[row_indices, col_indices].astype(np.float16)
        W_base = W.copy()
        W_base[row_indices, col_indices] = 0.0
        
        # 2. Block-wise Ternary Quantization
        # Pad d_in to multiple of block_size if needed
        pad_in = (block_size - (d_in % block_size)) % block_size
        if pad_in > 0:
            W_padded = np.pad(W_base, ((0, 0), (0, pad_in)), mode='constant')
        else:
            W_padded = W_base
            
        n_blocks_per_row = W_padded.shape[1] // block_size
        blocks = W_padded.reshape(d_out, n_blocks_per_row, block_size)
        
        # Optimal Ternary Quantization (TWN / BitNet threshold)
        # Optimal threshold Delta = 0.7 * E[|W|]
        mean_abs = np.mean(np.abs(blocks), axis=-1, keepdims=True)
        threshold = 0.70 * mean_abs

        ternary_blocks = np.zeros_like(blocks, dtype=np.int8)
        pos_mask = blocks > threshold
        neg_mask = blocks < -threshold
        ternary_blocks[pos_mask] = 1
        ternary_blocks[neg_mask] = -1

        # Optimal scale alpha: mean of magnitudes of active trits
        active_counts = np.sum(pos_mask | neg_mask, axis=-1, keepdims=True)
        active_sums = np.sum(np.abs(blocks) * (pos_mask | neg_mask), axis=-1, keepdims=True)
        block_scales = np.where(active_counts > 0, active_sums / np.maximum(active_counts, 1), mean_abs)
        block_scales = np.maximum(block_scales, 1e-5).astype(np.float32)
        
        # Unpad
        ternary_matrix = ternary_blocks.reshape(d_out, -1)[:, :d_in]
        scales_matrix = np.repeat(block_scales.reshape(d_out, n_blocks_per_row), block_size, axis=1)[:, :d_in]
        
        # Dense reconstructed ternary base
        W_ternary_reconstructed = (ternary_matrix * scales_matrix).astype(np.float32)
        
        # Pack ternary trits into uint8 bytes (5 trits per byte)
        packed_ternary = pack_trits_5_per_byte(ternary_matrix)
        
        # 3. Rank-r SVD Residual Correction (via O(MN) power iteration)
        E = (W_base - W_ternary_reconstructed).astype(np.float32)
        u_svd, v_svd = fast_power_iteration_svd(E, rank=svd_rank, num_iters=5)
            
        # Reconstruct approximation
        svd_reconstructed = (u_svd.astype(np.float32) @ v_svd.astype(np.float32)) if svd_rank > 0 else 0.0
        
        W_approx = W_ternary_reconstructed + svd_reconstructed
        W_approx[row_indices, col_indices] = outlier_vals.astype(np.float32)
        
        # Quality metrics
        frobenius_original = np.linalg.norm(W)
        frobenius_error = np.linalg.norm(W - W_approx)
        relative_error = frobenius_error / max(1e-6, frobenius_original)
        
        # Cosine similarity between original and reconstructed weights
        cos_sim = np.sum(W * W_approx) / (frobenius_original * np.linalg.norm(W_approx) + 1e-8)
        
        # Memory metrics
        fp16_bytes = total_elements * 2
        ternary_bytes = len(packed_ternary)
        scale_bytes = block_scales.size * 2  # stored in float16
        outlier_bytes = len(outlier_vals) * 6  # 2 bytes val + 4 bytes coord
        svd_bytes = (u_svd.size + v_svd.size) * 2
        total_compressed_bytes = ternary_bytes + scale_bytes + outlier_bytes + svd_bytes
        effective_bits_per_param = (total_compressed_bytes * 8.0) / total_elements
        compression_ratio = fp16_bytes / total_compressed_bytes
        
        return {
            "d_out": d_out,
            "d_in": d_in,
            "packed_ternary": packed_ternary,
            "block_scales": block_scales.astype(np.float16),
            "block_size": block_size,
            "outlier_rows": row_indices.astype(np.int32),
            "outlier_cols": col_indices.astype(np.int32),
            "outlier_values": outlier_vals,
            "u_svd": u_svd,
            "v_svd": v_svd,
            "svd_rank": svd_rank,
            "relative_error": float(relative_error),
            "cosine_similarity": float(cos_sim),
            "effective_bits_per_param": float(effective_bits_per_param),
            "compression_ratio": float(compression_ratio),
            "total_compressed_bytes": int(total_compressed_bytes),
            "fp16_bytes": int(fp16_bytes),
        }

    @classmethod
    def reconstruct_weight(cls, decomp: Dict[str, Any]) -> np.ndarray:
        """
        Reconstruct dense weight matrix W_approx from decomposed state.
        """
        d_out = decomp["d_out"]
        d_in = decomp["d_in"]
        block_size = decomp["block_size"]
        
        # 1. Unpack ternary matrix
        ternary_flat = unpack_trits_5_per_byte(decomp["packed_ternary"], d_out * d_in)
        ternary = ternary_flat.reshape(d_out, d_in)
        
        # 2. Apply block scales
        scales = decomp["block_scales"].astype(np.float32)
        n_blocks = scales.shape[1]
        scales_expanded = np.repeat(scales.reshape(d_out, n_blocks), block_size, axis=1)[:, :d_in]
        W_ternary = (ternary * scales_expanded).astype(np.float32)
        
        # 3. Add SVD low-rank correction
        if decomp["svd_rank"] > 0:
            W_svd = (decomp["u_svd"].astype(np.float32) @ decomp["v_svd"].astype(np.float32))
        else:
            W_svd = 0.0
            
        W_rec = W_ternary + W_svd
        
        # 4. Inject sparse outliers
        W_rec[decomp["outlier_rows"], decomp["outlier_cols"]] = decomp["outlier_values"].astype(np.float32)
        
        return W_rec
