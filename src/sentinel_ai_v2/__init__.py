"""
Sentinel AI v2 – Quantum-Resistant Threat Engine for DigiByte.

This package provides a reference implementation skeleton for the adversarial-
hardened detection layer in the 3-layer DigiByte defense architecture:

    DQSN → Sentinel AI v2 → ADN
"""

from .api import SentinelClient  # re-export for convenience

__all__ = ["SentinelClient"]
__version__ = "2.0.0"
