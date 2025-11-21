from __future__ import annotations

from typing import Any, Dict, Optional

from ..api import SentinelClient, SentinelResult
from ..config import load_config


def _get_client(client: Optional[SentinelClient] = None) -> SentinelClient:
    """Return provided client or build a default one from config."""
    if client is not None:
        return client
    cfg = load_config()
    return SentinelClient(config=cfg)


def run_full_workflow(
    raw_telemetry: Dict[str, Any],
    client: Optional[SentinelClient] = None,
) -> SentinelResult:
    """
    High-level single-shot workflow.

    ADN or node operators pass one telemetry snapshot (dict) and get back
    a SentinelResult (status + risk_score + details).
    """
    sentinel = _get_client(client)
    return sentinel.evaluate_snapshot(raw_telemetry)
