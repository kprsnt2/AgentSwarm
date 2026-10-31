"""
HyperQuant: Universal Sub-2-Bit Dynamic Ternary-Residual SVD (DTR-SVD) Engine
================================================================================
Post-training extreme compression framework for LLMs on Pure CPU and Low-VRAM GPUs.
"""

from .core import (
    pack_trits_5_per_byte,
    unpack_trits_5_per_byte,
    HyperQuantDecomposer,
)

from .nn import (
    HyperQuantLinear,
    replace_linear_with_hyperquant,
)

__version__ = "1.0.0"
__all__ = [
    "pack_trits_5_per_byte",
    "unpack_trits_5_per_byte",
    "HyperQuantDecomposer",
    "HyperQuantLinear",
    "replace_linear_with_hyperquant",
]
