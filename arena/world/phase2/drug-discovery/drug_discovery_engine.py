"""
drug_discovery_engine.py - Python module alias for drug-discovery_engine.py
Allows standard Python identifier imports: `import drug_discovery_engine`
"""

import importlib
import os
import sys

_engine = importlib.import_module("drug-discovery_engine")

# Re-export all public attributes
for _attr in dir(_engine):
    if not _attr.startswith("_"):
        globals()[_attr] = getattr(_engine, _attr)
