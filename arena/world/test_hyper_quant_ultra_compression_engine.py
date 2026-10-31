"""
Unit Test Suite: HyperQuant Universal Sub-2-Bit Compression Engine
===================================================================
Verification of Hessian salient outlier slicing, dense fractal ternary packing (5 trits/byte),
rank-1 SVD error cancellation, pure CPU zero-multiplication arithmetic, and ultra-low VRAM
allocation across universal consumer hardware tiers.
"""

import pytest
from arena.world.hyper_quant_ultra_compression_engine import (
    HessianSalientOutlierSlicer,
    FractalTernaryPacker,
    Rank1ResidualSVDCanceller,
    UniversalConsumerTierPlanner,
    PerplexityReconstructionBenchmark,
    ZeroMulCPUEngine,
    UltraLowVRAMGPUOrchestrator,
    simulate_pure_cpu_vs_low_gpu_benchmark,
    run_universal_compression_matrix,
)


def test_hessian_salient_outlier_slicing():
    """Verify top 0.75% outlier extraction isolates curvature with minimal bit overhead."""
    res = HessianSalientOutlierSlicer.evaluate_outlier_allocation(
        hidden_dim_in=5120,
        hidden_dim_out=5120,
        outlier_fraction=0.0075,
    )
    assert res["total_elements"] == 5120 * 5120
    assert res["outlier_count"] == int(res["total_elements"] * 0.0075)
    assert res["outlier_bit_overhead"] < 0.40, "Outlier overhead must be < 0.40 bits/param"
    assert res["reconstruction_snr_gain_db"] >= 6.0, "SNR gain must be >= 6 dB"
    assert res["curvature_captured_pct"] > 80.0


def test_fractal_ternary_packing_density():
    """Verify dense packing of 5 trits into 1 byte (1.60 bits/param base)."""
    n_params = 14_700_000_000  # 14.7B model
    pack = FractalTernaryPacker.calculate_ternary_packing(n_params, block_scale_size=128)
    assert pack["effective_bits_per_param"] < 1.70, f"Expected < 1.70 bits, got {pack['effective_bits_per_param']}"
    assert pack["compression_ratio_vs_fp16"] >= 9.4, "Must compress >= 9.4x vs FP16"
    assert pack["integer_addition_speedup_factor"] > 3.0


def test_rank1_svd_residual_correction():
    """Verify rank-1 SVD captures dominant residual error with negligible parameter cost."""
    svd = Rank1ResidualSVDCanceller.evaluate_svd_residual_correction(
        dim_in=5120,
        dim_out=5120,
        rank=1,
    )
    assert svd["svd_bit_overhead"] < 0.05, "Rank-1 SVD overhead must be < 0.05 bits/param"
    assert svd["spectral_error_reduction_pct"] > 40.0


def test_pure_cpu_tier_zero_gpu():
    """Verify Tier 0A Pure CPU execution for 7B/14B models on 16GB RAM."""
    cpu_prof = UniversalConsumerTierPlanner.calculate_tier_compression_profile(
        model_name="Qwen-2.5-Coder-7B",
        tier_key="tier_0_pure_cpu",
    )
    assert cpu_prof["fits_fully_in_vram"] is False
    assert cpu_prof["fits_in_combined_memory"] is True
    assert cpu_prof["vram_weight_gb"] == 0.0
    assert cpu_prof["hyper_quant_gb"] < 2.5, "7B model must compress to < 2.5 GB"
    assert cpu_prof["estimated_throughput_tok_s"] >= 20.0
    assert "Pure CPU" in cpu_prof["execution_mode"]


def test_ultra_low_gpu_4gb_tier():
    """Verify Tier 0B 4GB GPU (GTX 1050/1650/APU) runs 14B model without OOM."""
    gpu_prof = UniversalConsumerTierPlanner.calculate_tier_compression_profile(
        model_name="Qwen-2.5-Coder-14B",
        tier_key="tier_0_ultra_low_gpu_4gb",
    )
    assert gpu_prof["fits_in_combined_memory"] is True
    assert gpu_prof["hyper_quant_gb"] < 4.0, "14B model must compress to < 4.0 GB"
    assert gpu_prof["vram_weight_gb"] <= 3.0, "VRAM allocation must stay under 3GB on 4GB card"
    assert gpu_prof["estimated_throughput_tok_s"] >= 15.0


def test_budget_6gb_gpu_tier():
    """Verify Tier 1 6GB GPU running 27B model (54GB FP16 -> 6.85GB)."""
    prof = UniversalConsumerTierPlanner.calculate_tier_compression_profile(
        model_name="Qwen-2.5-27B",
        tier_key="tier_1_budget_6gb",
    )
    assert prof["original_fp16_gb"] > 50.0
    assert prof["hyper_quant_gb"] < 7.5, "27B model must compress to < 7.5 GB"
    assert prof["compression_ratio"] >= 7.2
    assert prof["fits_in_combined_memory"] is True


def test_zero_mul_cpu_kernel_bandwidth_speedup():
    """Verify ZeroMulCPUEngine eliminates FMA multiplication and accelerates CPU tokens/s."""
    cpu = ZeroMulCPUEngine.evaluate_cpu_execution(
        model_params_b=7.6,
        cpu_ddr_bandwidth_gbps=38.4,
    )
    assert cpu["compressed_footprint_gb"] < 2.5
    assert cpu["zero_mul_cpu_speed_tok_s"] > cpu["naive_int4_speed_tok_s"]
    assert cpu["cpu_speedup_factor"] >= 2.0
    assert cpu["is_pure_cpu_viable"] is True
    assert cpu["alu_efficiency_gain"] > 3.5


def test_ultra_low_vram_apu_allocation():
    """Verify Integrated APU zero-copy memory allocation without PCIe copy penalty."""
    apu = UltraLowVRAMGPUOrchestrator.allocate_low_end_gpu(
        model_name="Qwen-2.5-Coder-14B",
        vram_available_gb=4.0,
        is_integrated_apu=True,
    )
    assert apu["is_integrated_apu"] is True
    assert apu["estimated_tok_s"] >= 18.0
    assert apu["fits_on_hardware"] is True
    assert "APU Unified" in apu["execution_type"]


def test_perplexity_stability_bound():
    """Verify Delta PPL remains <= 0.16, preventing 2-bit perplexity explosion."""
    ppl = PerplexityReconstructionBenchmark.evaluate_perplexity_stability(
        model_name="Qwen-2.5-27B",
        quant_method="hyper_quant_dtr_svd",
    )
    assert ppl["delta_ppl"] <= 0.16
    assert ppl["is_reasoning_preserved"] is True
    assert ppl["humaneval_pass1_retention_pct"] >= 95.0


def test_universal_compression_matrix_end_to_end():
    """Verify end-to-end multi-tier execution across CPU, 4GB, 6GB, 12GB, and 24GB."""
    res = run_universal_compression_matrix()
    assert res["universal_validation_passed"] is True
    assert res["tier_0_qwen_7b_cpu"]["estimated_throughput_tok_s"] >= 20.0
    assert res["tier_0_qwen_14b_gpu4"]["fits_in_combined_memory"] is True
    assert res["low_end_and_cpu_bench"]["validation_passed"] is True
    assert res["low_end_and_cpu_bench"]["cpu_speedup_vs_naive_int4"] >= 2.0
