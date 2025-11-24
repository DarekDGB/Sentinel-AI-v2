"""
Basic import test for Sentinel AI v2.

Goal:
- Make sure core package modules import without error.
"""

import importlib
import sys
from pathlib import Path

def _add_src_to_path():
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))

_add_src_to_path()

modules = [
    "sentinel_ai_v2",
    "sentinel_ai_v2.api",
    "sentinel_ai_v2.client",
    "sentinel_ai_v2.wrapper",
]

def test_modules_importable():
    for mod in modules:
        m = importlib.import_module(mod)
        assert m is not None, f"Failed to import {mod}"
