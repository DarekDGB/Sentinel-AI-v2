from __future__ import annotations

from typing import Any, Dict, Optional

from ..api import SentinelClient, SentinelResult
from ..config import load_config
from .workflow import run_full_workflow
from .monitor import Monitor


class SentinelWrapper:
    """
    Thin convenience wrapper around SentinelClient + Monitor.

    Usage example:

        wrapper = SentinelWrapper()
        result = wrapper.evaluate(snapshot)
        status = wrapper.last_status()
    """

    def __init__(self, client: Optional[SentinelClient] = None) -> None:
        if client is None:
            cfg = load_config()
            client = SentinelClient(config=cfg)

        self._client = client
        self._monitor = Monitor()

    def evaluate(self, raw_telemetry: Dict[str, Any]) -> SentinelResult:
        """
        Evaluate one telemetry snapshot and update internal monitor.
        """
        result = run_full_workflow(raw_telemetry, client=self._client)
        self._monitor.update(result)
        return result

    def last_status(self) -> Dict[str, Any]:
        """
        Get last known status summary (for dashboards / health checks).
        """
        return self._monitor.last_status()
