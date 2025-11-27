# src/sentinel_ai_v2/feedback_hooks.py

from __future__ import annotations

from typing import Optional

from .adaptive_core_bridge import SentinelAdaptiveCoreBridge


def send_feedback_to_adaptive(
    *,
    layer: str,
    event_id: str,
    feedback: str,
    bridge: Optional[SentinelAdaptiveCoreBridge] = None,
) -> None:
    """
    Small helper used by Sentinel AI v2 to send feedback signals
    back to the Adaptive Core.

    Supported feedback values:
        - "TRUE_POSITIVE"
        - "FALSE_POSITIVE"
        - "MISSED_ATTACK"

    This function centralises the logic so detection modules can simply call:

        send_feedback_to_adaptive(
            layer="sentinel_ai_v2",
            event_id="abc123",
            feedback="TRUE_POSITIVE",
        )
    """
    bridge = bridge or SentinelAdaptiveCoreBridge()

    if not bridge.is_available:
        # No adaptive core installed; safe no-op.
        return

    tag = feedback.upper()

    bridge.submit_feedback_label(
        layer=layer,
        event_id=event_id,
        feedback=tag,
    )
