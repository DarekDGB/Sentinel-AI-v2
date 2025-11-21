from __future__ import annotations
from typing import Dict, Any


class ThreatModel:
    """
    Base class for all structured threat models used by Sentinel AI v2.
    Each model returns a risk contribution between 0.0 and 1.0.
    """

    name: str = "base"

    def evaluate(self, features: Dict[str, Any]) -> float:
        """Override in subclasses."""
        raise NotImplementedError


class FiftyOneAttackModel(ThreatModel):
    name = "classic_51_attack"

    def evaluate(self, features: Dict[str, Any]) -> float:
        score = 0.0

        # Rapid entropy collapse is a direct 51% mining indicator
        if features.get("entropy_drop", 0) > 0.35:
            score += 0.4

        # Abnormally high reorg depth
        if features.get("reorg_depth", 0) >= 3:
            score += 0.4

        # Mempool anomalies
        if features.get("mempool_anomaly", 0) > 0.25:
            score += 0.2

        return min(score, 1.0)


class QuantumPreImageModel(ThreatModel):
    name = "quantum_preimage_attack"

    def evaluate(self, features: Dict[str, Any]) -> float:
        score = 0.0

        # Synthetic entropy strike patterns used by Shor-style simulations
        if features.get("entropy_score", 1.0) < 0.60:
            score += 0.5

        # Model prediction (if exists)
        if features.get("model_score", 0) > 0.75:
            score += 0.5

        return min(score, 1.0)


class MempoolFloodModel(ThreatModel):
    name = "mempool_flood"

    def evaluate(self, features: Dict[str, Any]) -> float:
        score = 0.0
        
        if features.get("mempool_anomaly", 0) > 0.5:
            score += 0.6
        
        if features.get("mempool_score", 0) < 0.4:
            score += 0.4
        
        return min(score, 1.0)


class EclipseAttackModel(ThreatModel):
    name = "eclipse_attack"

    def evaluate(self, features: Dict[str, Any]) -> float:
        score = 0.0
        
        # Depth-based isolation indicator
        if features.get("reorg_depth", 0) >= 2:
            score += 0.5
        
        # Combined with entropy stability (too stable = synthetic)
        if features.get("entropy_score", 1.0) > 0.95:
            score += 0.5
        
        return min(score, 1.0)


# Registry for all threat models
THREAT_MODELS = [
    FiftyOneAttackModel(),
    QuantumPreImageModel(),
    MempoolFloodModel(),
    EclipseAttackModel(),
]
