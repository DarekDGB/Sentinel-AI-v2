# src/sentinel_ai_v2/heartbeat.py

from __future__ import annotations

from typing import Optional

from .adaptive_core_bridge import SentinelAdaptiveCoreBridge


def shield_heartbeat(
    *,
    min_severity: int = 0,
    bridge: Optional[SentinelAdaptiveCoreBridge] = None,
) -> str:
    """
    Returns a combined health + intelligence heartbeat for the shield.

    When Adaptive Core is available:
      - returns immune report text
      - prints adaptive state (weights + threshold) in the output

    When not available:
      - returns a simple status message
    """
    bridge = bridge or SentinelAdaptiveCoreBridge()

    if not bridge.is_available:
        return "Shield heartbeat: Adaptive Core not available."

    # Pull immune report text
    report_text = bridge.get_immune_report_text(min_severity=min_severity)

    # Pull adaptive state
    state = bridge._interface.get_adaptive_state()  # type: ignore

    lines = []
    lines.append("=== DigiByte Quantum Shield — Heartbeat ===")
    lines.append("")
    lines.append(">> Immune Report:")
    lines.append(report_text)
    lines.append("")
    lines.append(">> Adaptive State:")
    lines.append(f"  Global Threshold: {state.global_threshold:.3f}")
    lines.append("  Layer Weights:")
    for layer, weight in state.layer_weights.items():
        lines.append(f"    - {layer}: {weight:.3f}")

    return "\n".join(lines)
