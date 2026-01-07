from __future__ import annotations

from typing import Any, Dict, Optional


def make_valid_telemetry(
    *,
    block_height: int = 1,
    mempool_size: int = 2,
    entropy_score: float = 0.1,
) -> Dict[str, Any]:
    """
    Minimal telemetry dict that should pass SentinelV3Request.from_dict().
    Keep this small and stable for deterministic tests.
    """
    return {
        "block_height": block_height,
        "mempool_size": mempool_size,
        "entropy": {"score": entropy_score},
    }


def make_valid_v3_request(
    telemetry: Optional[Dict[str, Any]] = None,
    *,
    request_id: str = "r1",
    component: str = "sentinel",
    contract_version: int = 3,
    max_latency_ms: int = 2500,
) -> Dict[str, Any]:
    """
    Build a valid v3 request dict (top-level allowlist compliant).
    """
    return {
        "contract_version": contract_version,
        "component": component,
        "request_id": request_id,
        "telemetry": telemetry if telemetry is not None else make_valid_telemetry(),
        "constraints": {"max_latency_ms": max_latency_ms},
    }
