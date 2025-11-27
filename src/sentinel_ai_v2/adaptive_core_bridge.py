# src/sentinel_ai_v2/adaptive_core_bridge.py

from __future__ import annotations

from typing import Any, Optional

try:
    # These imports will only work when the Adaptive Core package
    # is available in the same environment. If not, we handle it
    # gracefully and keep Sentinel AI v2 fully functional.
    from adaptive_core.interface import AdaptiveCoreInterface  # type: ignore
    from adaptive_core.threat_packet import ThreatPacket  # type: ignore
except ImportError:  # pragma: no cover - optional integration
    AdaptiveCoreInterface = None  # type: ignore
    ThreatPacket = None  # type: ignore


class SentinelAdaptiveCoreBridge:
    """
    Optional bridge between Sentinel AI v2 and the DigiByte Quantum
    Adaptive Core.

    Design goals:
      - Do NOT break Sentinel AI v2 if the adaptive_core package
        is not installed.
      - When adaptive_core *is* available, allow Sentinel to:
          * submit ThreatPacket objects to the Adaptive Core
          * later: request immune reports

    This keeps Sentinel "adaptive-ready" without introducing a hard
    runtime dependency.
    """

    def __init__(self, interface: Optional["AdaptiveCoreInterface"] = None) -> None:
        # If AdaptiveCoreInterface is not available, this bridge becomes
        # a no-op and Sentinel can still run normally.
        if AdaptiveCoreInterface is None:
            self._available = False
            self._interface = None
        else:
            self._available = True
            self._interface = interface or AdaptiveCoreInterface()

    @property
    def is_available(self) -> bool:
        """
        Returns True if the adaptive_core integration is available
        in the current environment.
        """
        return self._available and self._interface is not None

    def submit_simple_threat(
        self,
        source_layer: str,
        threat_type: str,
        severity: int,
        description: str,
        *,
        node_id: Optional[str] = None,
        wallet_id: Optional[str] = None,
        tx_id: Optional[str] = None,
        block_height: Optional[int] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Convenience helper for Sentinel to send a basic threat signal
        into the Adaptive Core.

        Example usage (future, inside Sentinel):

            bridge.submit_simple_threat(
                source_layer="sentinel_ai_v2",
                threat_type="reorg_pattern",
                severity=8,
                description="Abnormal reorg pattern detected.",
                block_height=1234567,
                metadata={"score": 0.94},
            )
        """
        if not self.is_available:
            # Adaptive Core is not installed / wired in this environment.
            # We silently no-op to avoid breaking Sentinel.
            return

        assert ThreatPacket is not None  # for type checkers

        packet = ThreatPacket(
            source_layer=source_layer,
            threat_type=threat_type,
            severity=severity,
            description=description,
            node_id=node_id,
            wallet_id=wallet_id,
            tx_id=tx_id,
            block_height=block_height,
            metadata=metadata,
        )

        self._interface.submit_threat_packet(packet)  # type: ignore[arg-type]

    def get_immune_report_text(self, min_severity: int = 0) -> str:
        """
        Optional helper for Sentinel to fetch a human-readable immune report
        for logging or debugging, when the Adaptive Core is available.
        """
        if not self.is_available:
            return "Adaptive Core integration not available in this environment."

        return self._interface.get_immune_report_text(min_severity=min_severity)
