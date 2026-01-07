from sentinel_ai_v2.v3 import SentinelV3
from sentinel_ai_v2.config import CircuitBreakerThresholds, SentinelConfig
from sentinel_ai_v2.api import SentinelClient


def test_v3_evaluate_happy_path_minimal():
    s = SentinelV3(thresholds=CircuitBreakerThresholds())
    req = {
        "contract_version": 3,
        "component": "sentinel",
        "request_id": "r1",
        "telemetry": {"block_height": 10, "mempool_size": 1},
        "fail_closed": True,
    }
    out = s.evaluate(req)
    assert out["contract_version"] == 3
    assert out["component"] == "sentinel"
    assert out["request_id"] == "r1"
    assert out["decision"] in ("ALLOW", "BLOCK", "ERROR")
    assert "context_hash" in out
    assert "reason_codes" in out
    assert "risk" in out


def test_v3_evaluate_invalid_request_is_error():
    s = SentinelV3(thresholds=CircuitBreakerThresholds())
    out = s.evaluate("not a dict")  # type: ignore[arg-type]
    assert out["decision"] == "ERROR"
    assert out["contract_version"] == 3
    assert out["component"] == "sentinel"


def test_api_client_constructs():
    # Smoke: construction should not crash
    client = SentinelClient(config=SentinelConfig())
    assert client is not None
