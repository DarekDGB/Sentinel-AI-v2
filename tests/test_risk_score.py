"""
Basic risk score logic test for Sentinel AI v2.
"""

from sentinel_ai_v2.scoring import compute_risk_score
from sentinel_ai_v2.config import CircuitBreakerThresholds

def test_trivial_normal_score():
    features = {
        "entropy_score": 0.0,
        "mempool_score": 0.0,
        "reorg_score": 0.0,
        "entropy_drop": 0.0,
        "mempool_anomaly": 0.0,
        "reorg_depth": 0,
    }
    thresholds = CircuitBreakerThresholds()
    result = compute_risk_score(features, thresholds)
    assert result.risk_score < 0.4
    assert result.status == "NORMAL"
