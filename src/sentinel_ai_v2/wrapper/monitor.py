from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Dict, Any

from ..api import SentinelResult


@dataclass
class Monitor:
    """
    Simple in-memory monitor storing the last SentinelResult.
    """

    last_result: Optional[SentinelResult] = None

    def update(self, result: SentinelResult) -> None:
        self.last_result = result

    def last_status(self) -> Dict[str, Any]:
        """
        Return a compact status snapshot suitable for health checks / dashboards.
        """
        if self.last_result is None:
            return {"status": "NO_DATA", "risk_score": 0.0, "details": []}

        return {
            "status": self.last_result.status,
            "risk_score": self.last_result.risk_score,
            "details": self.last_result.details,
        }
