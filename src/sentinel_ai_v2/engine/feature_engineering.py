from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict

from ..data_intake import TelemetrySnapshot


@dataclass
class FeatureVector:
    """
    Structured feature vector derived from a TelemetrySnapshot.

    These features map 1:1 to the flat `features` dict used by the scoring
    engine, so devs can choose whether to work with objects or plain dicts.
    """

    entropy_score: float = 0.0
    mempool_score: float = 0.0
    reorg_score: float = 0.0

    entropy_drop: float = 0.0
    mempool_anomaly: float = 0.0
    reorg_depth: int = 0

    model_score: float | None = None  # optional, filled by AI model later

    def to_dict(self) -> Dict[str, Any]:
        """Convert to the flat dict format expected by `compute_risk_score`."""
        data = asdict(self)
        # remove None to keep feature dict clean
        return {k: v for k, v in data.items() if v is not None}


def build_feature_vector(snapshot: TelemetrySnapshot) -> FeatureVector:
    """
    Build a FeatureVector from a TelemetrySnapshot.

    This is an optional helper; the current API already builds a dict directly,
    but DigiByte devs can use this structured version if they prefer.
    """
    entropy = snapshot.entropy or {}
    mempool = snapshot.mempool or {}
    reorg = snapshot.reorg or {}

    return FeatureVector(
        entropy_score=float(entropy.get("score", 0.0)),
        mempool_score=float(mempool.get("score", 0.0)),
        reorg_score=float(reorg.get("score", 0.0)),
        entropy_drop=float(entropy.get("drop", 0.0)),
        mempool_anomaly=float(mempool.get("anomaly", 0.0)),
        reorg_depth=int(reorg.get("depth", 0)),
    )
