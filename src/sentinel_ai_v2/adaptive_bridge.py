"""
Adaptive bridge helpers for Sentinel-AI v2.

This module does NOT change Sentinel's detection logic.
It only provides small helpers to turn anomalies into AdaptiveEvent objects
and a placeholder "emit" function.

Later, DigiByte-Quantum-Adaptive-Core can plug into this.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .adaptive_event import AdaptiveEvent

logger = logging.getLogger(__name__)


def build_adaptive_event(
    *,
    anomaly_type: str,
    severity: float,
    qri_before: float = 0.0,
    qri_after: float = 0.0,
    layer: str = "sentinel",
    block_height: Optional[int] = None,
    txid: Optional[str] = None,
    was_mitigated: bool = False,
    details: Optional[str] = None,
) -> AdaptiveEvent:
    """
    Factory helper to construct a normalized AdaptiveEvent from Sentinel anomaly data.

    This keeps the Sentinel → Adaptive Core interface clean:
    Sentinel passes only basic fields; Adaptive Core can evolve independently.
    """
    return AdaptiveEvent(
        layer=layer,
        anomaly_type=anomaly_type,
        severity=float(severity),
        qri_before=float(qri_before),
        qri_after=float(qri_after),
        block_height=block_height,
        txid=txid,
        was_mitigated=bool(was_mitigated),
        details=details,
        # NOTE: created_at is set by AdaptiveEvent default; we intentionally do not override it here.
    )


def emit_adaptive_event(event: AdaptiveEvent) -> None:
    """
    Placeholder sink for AdaptiveEvents.

    For v2 this only logs a structured JSON line.
    Later, DigiByte-Quantum-Adaptive-Core can replace this with:
      – HTTP/gRPC send
      – message queue push
      – file / DB logger, etc.
    """
    try:
        payload = asdict(event)
        # default=str ensures datetime is JSON-serializable
        logger.debug("AdaptiveEvent %s", json.dumps(payload, sort_keys=True, default=str))
    except Exception as e:  # pragma: no cover – defensive
        logger.error("Failed to log AdaptiveEvent: %s", e)


def export_to_adaptive_core(event: AdaptiveEvent) -> None:
    """
    Integration alias kept for readability.

    Today this simply calls emit_adaptive_event().
    Later this can become the single integration point for Adaptive Core transports.
    """
    emit_adaptive_event(event)


def emit_adaptive_event_from_signal(
    *,
    signal_name: str,
    severity: float,
    qri_delta: float = 0.0,
    layer: str = "sentinel",
    context: Optional[Dict[str, Any]] = None,
    block_height: Optional[int] = None,
    txid: Optional[str] = None,
) -> None:
    """
    Convenience helper: take any Sentinel signal name and push it into Adaptive Core.

    Example:

        emit_adaptive_event_from_signal(
            signal_name="entropy_drop",
            severity=0.82,
            qri_delta=-0.15,
            context={"window": "30s", "chain": "DigiByte"},
        )

    Notes:
    - severity is a float (0..1 suggested).
    - qri_delta is applied as: qri_after = max(0.0, qri_before + qri_delta)
    - context is stored in the `details` field as JSON (string) for v2 simplicity.
    """
    qri_before = float(severity)
    qri_after = qri_before + float(qri_delta)
    if qri_after < 0.0:
        qri_after = 0.0

    details_str: Optional[str] = None
    if context is not None:
        try:
            # Keep deterministic ordering
            details_str = json.dumps(context, sort_keys=True, separators=(",", ":"), default=str)
        except Exception:
            # Fail closed on details serialization? For v2 bridge we do not block event creation.
            details_str = str(context)

    evt = build_adaptive_event(
        layer=layer,
        anomaly_type=signal_name,
        severity=float(severity),
        qri_before=qri_before,
        qri_after=qri_after,
        block_height=block_height,
        txid=txid,
        was_mitigated=False,
        details=details_str,
    )

    export_to_adaptive_core(evt)
