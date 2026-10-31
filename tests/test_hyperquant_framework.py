"""
Unit Tests for HyperQuant Framework
===================================
Verifies exactness of 5-trit packing/unpacking, DTR-SVD decomposition fidelity,
outlier extraction SNR gains, and rank-1 SVD error reduction.
"""

import pytest
import numpy as np
from hyperquant.core import (
    pack_trits_5_per_byte,
    unpack_trits_5_per_byte,
    HyperQuantDecomposer,
)


def test_pack_unpack_exactness():
    """Verify that 5-trit packing and unpacking is 100% reversible and exact."""
    np.random.seed(42)
    # Generate random trits {-1, 0, +1}
    for size in [5, 10, 128, 512, 1003, 4096]:
        trits = np.random.choice([-1, 0, 1], size=size).astype(np.int8)
        packed = pack_trits_5_per_byte(trits)
        # Expected packed length: ceil(size / 5)
        assert len(packed) == (size + 4) // 5
        # Packed values must be <= 242 (3^5 - 1)
        assert np.all(packed <= 242)
        # Unpack
        unpacked = unpack_trits_5_per_byte(packed, original_length=size)
        assert np.array_equal(trits, unpacked), f"Failed exact recovery for size {size}"


def test_hyperquant_decomposition_fidelity():
    """Verify weight matrix decomposition achieves >7.5x compression and >0.94 cosine similarity."""
    np.random.seed(1337)
    d_out, d_in = 512, 1024
    # Simulate LLM weight matrix with realistic distribution and heavy outliers
    W = np.random.normal(0, 0.02, size=(d_out, d_in)).astype(np.float32)
    # Inject heavy-tailed activation outliers
    outlier_idx = np.random.choice(d_out * d_in, size=int(d_out * d_in * 0.005), replace=False)
    W.ravel()[outlier_idx] *= 12.0

    decomp = HyperQuantDecomposer.decompose(
        W=W,
        outlier_ratio=0.0075,
        block_size=128,
        svd_rank=1,
    )

    assert decomp["effective_bits_per_param"] < 2.20, f"Expected < 2.20 bits, got {decomp['effective_bits_per_param']}"
    assert decomp["compression_ratio"] >= 7.5, f"Expected >= 7.5x, got {decomp['compression_ratio']}"
    assert decomp["cosine_similarity"] > 0.94, f"Expected cos_sim > 0.94, got {decomp['cosine_similarity']}"

    # Reconstruct dense weight
    W_rec = HyperQuantDecomposer.reconstruct_weight(decomp)
    assert W_rec.shape == W.shape
    
    # Cosine similarity between original and reconstructed
    cos_sim = np.sum(W * W_rec) / (np.linalg.norm(W) * np.linalg.norm(W_rec))
    assert cos_sim > 0.94


def test_outlier_slicing_snr_gain():
    """Verify that isolating top 0.75% outliers dramatically reduces reconstruction error."""
    np.random.seed(42)
    W = np.random.normal(0, 0.02, size=(256, 512)).astype(np.float32)
    # Inject extreme outliers
    W[0, 10] = 2.5
    W[50, 100] = -3.2
    W[120, 300] = 4.1

    # Without outlier slicing (ratio = 0.0)
    decomp_no_outlier = HyperQuantDecomposer.decompose(W, outlier_ratio=0.0, svd_rank=0)
    # With outlier slicing (ratio = 0.0075)
    decomp_outlier = HyperQuantDecomposer.decompose(W, outlier_ratio=0.0075, svd_rank=0)

    # Cosine similarity must be strictly higher with outlier slicing
    assert decomp_outlier["cosine_similarity"] > decomp_no_outlier["cosine_similarity"]
    assert decomp_outlier["relative_error"] < decomp_no_outlier["relative_error"]


def test_svd_residual_correction_gain():
    """Verify that rank-1 SVD captures residual error and improves fidelity."""
    np.random.seed(99)
    W = np.random.normal(0, 0.02, size=(256, 512)).astype(np.float32)

    decomp_rank0 = HyperQuantDecomposer.decompose(W, outlier_ratio=0.005, svd_rank=0)
    decomp_rank1 = HyperQuantDecomposer.decompose(W, outlier_ratio=0.005, svd_rank=1)

    assert decomp_rank1["cosine_similarity"] >= decomp_rank0["cosine_similarity"]
    assert decomp_rank1["relative_error"] <= decomp_rank0["relative_error"]


def test_non_standard_dimensions_padding():
    """Verify decomposition handles arbitrary non-multiple matrix dimensions."""
    np.random.seed(77)
    # Unaligned dimensions
    W = np.random.normal(0, 0.05, size=(137, 243)).astype(np.float32)

    decomp = HyperQuantDecomposer.decompose(W, outlier_ratio=0.01, block_size=128, svd_rank=1)
    W_rec = HyperQuantDecomposer.reconstruct_weight(decomp)

    assert W_rec.shape == (137, 243)
    assert decomp["cosine_similarity"] > 0.90
