"""
Unit Test Suite: HeteroFlash Unified-Memory Inference Engine
============================================================
Verification of PCIe double-buffered prefetching, DeepSeek-style MLA KV cache
compression, SpecDec-Split draft acceleration, and heterogeneous cluster partitioning.
"""

import pytest
from arena.world.hetero_flash_inference_engine import (
    PCIeAsyncPinnedRingBuffer,
    MLALatentKVCacheCompressor,
    SpeculativeDecSplitEngine,
    DistributedHeteroClusterOrchestrator,
    simulate_agentic_inference_benchmark,
)


def test_pcie_async_ring_buffer_overlap():
    """Verify asynchronous PCIe DMA prefetch latency and overlap calculation."""
    # 120 MB FFN layer weights over PCIe Gen 4 x4 (7.1 GB/s)
    prefetch = PCIeAsyncPinnedRingBuffer.evaluate_prefetch_overlap(
        layer_weights_mb=120.0,
        attention_compute_time_ms=18.0,
        pcie_bandwidth_gb_s=7.1,
    )
    assert prefetch["transfer_latency_ms"] < 20.0
    assert prefetch["overlap_efficiency_pct"] > 90.0, "Long attention compute should hide >90% of transfer latency"
    assert prefetch["pcie_stall_latency_ms"] < 2.0


def test_mla_latent_kv_cache_compression():
    """Verify DeepSeek Multi-Head Latent Attention (MLA) low-rank compression (>85% savings)."""
    # 8k context tokens
    res_8k = MLALatentKVCacheCompressor.compute_kv_cache_footprint(
        context_tokens=8192,
        num_layers=32,
        quant_bits=8,
    )
    assert res_8k["vram_savings_pct"] >= 85.0, f"Expected >= 85% savings, got {res_8k['vram_savings_pct']}%"
    assert res_8k["mla_compressed_mb"] < 200.0, "8k MLA cache must be < 200 MB"
    assert res_8k["fits_in_6gb_vram"] is True

    # 16k context tokens
    res_16k = MLALatentKVCacheCompressor.compute_kv_cache_footprint(
        context_tokens=16384,
        num_layers=32,
        quant_bits=8,
    )
    assert res_16k["mla_compressed_mb"] < 400.0, "16k MLA cache must be < 400 MB"
    assert res_16k["fits_in_6gb_vram"] is True


def test_speculative_dec_split_throughput():
    """Verify SpecDec-Split draft model acceleration over slow serial offloading."""
    spec = SpeculativeDecSplitEngine.evaluate_speculative_throughput(
        acceptance_rate=0.74,
        k_tokens=5,
        target_serial_speed_tok_s=5.2,
    )
    assert spec["expected_accepted_tokens"] >= 3.0, "At 74% acceptance, expect >= 3.0 accepted tokens"
    assert spec["speculative_speedup_factor"] >= 2.2, f"Expected speedup >= 2.2x, got {spec['speculative_speedup_factor']}"
    assert spec["effective_tokens_per_sec"] >= 11.5


def test_distributed_hetero_cluster_allocation():
    """Verify workload balance across Primary (3050 6GB + 16GB) and Secondary (8GB idle)."""
    cluster = DistributedHeteroClusterOrchestrator.allocate_workload(
        primary_vram_gb=6.0,
        primary_ram_gb=16.0,
        secondary_ram_gb=8.0,
    )
    assert cluster["total_cluster_memory_gb"] == 30.0
    assert cluster["primary_vram_allocation"]["draft_model_mb"] <= 1000.0
    assert cluster["secondary_node_allocation"]["embedding_model_mb"] == 350.0
    assert cluster["secondary_node_allocation"]["vector_store_chromadb_mb"] == 2500.0
    assert cluster["is_balanced"] is True


def test_end_to_end_agentic_benchmark_comparison():
    """Verify full agentic benchmark comparing Naive Offload vs. HeteroFlash."""
    naive = simulate_agentic_inference_benchmark(context_tokens=8192, use_hetero_flash=False)
    assert naive["vram_oom_risk"] is True, "Naive FP16 MHA at 8k context should flag VRAM OOM on 6GB card"
    assert naive["agentic_ready"] is False
    assert naive["decoding_speed_tok_s"] < 5.0

    hetero = simulate_agentic_inference_benchmark(context_tokens=8192, use_hetero_flash=True)
    assert hetero["vram_oom_risk"] is False
    assert hetero["agentic_ready"] is True
    assert hetero["decoding_speed_tok_s"] >= 18.0, f"Expected >= 18 tok/s, got {hetero['decoding_speed_tok_s']}"
    assert hetero["time_to_512_tokens_s"] < 80.0, "Turn latency must be < 80s (vs >300s naive)"
