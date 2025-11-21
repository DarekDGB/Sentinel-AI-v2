from sentinel_ai_v2.data_intake import get_all_data
from sentinel_ai_v2.feature_engineering import build_features
from sentinel_ai_v2.threat_models import evaluate_threats
from sentinel_ai_v2.risk_aggregation import aggregate_risk
from sentinel_ai_v2.scoring import score_risk

def run_full_workflow():
    """
    Full Sentinel pipeline:
    1. Data intake
    2. Feature engineering
    3. Threat evaluation
    4. Risk aggregation
    5. Scoring
    """
    
    raw = get_all_data()
    features = build_features(raw)
    threats = evaluate_threats(features)
    aggregated = aggregate_risk(threats)
    score = score_risk(aggregated)

    return {
        "raw": raw,
        "features": features,
        "threats": threats,
        "risk": aggregated,
        "score": score
    }
