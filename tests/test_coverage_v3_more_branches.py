import sentinel_ai_v2.v3 as v3mod
from sentinel_ai_v2.v3 import SentinelV3
from sentinel_ai_v2.config import CircuitBreakerThresholds


def _base_req():
    return {
        "contract_version": 3,
        "component": "sentinel",
        "request_id": "r1",
        "telemetry": {"block_height": 10, "mempool_size": 1, "entropy": {"score": 0.1}},
        "constraints": {"max_latency_ms": 2500},
    }


def test_v3_schema_version_mismatch_returns_error():
    s = SentinelV3(thresholds=CircuitBreakerThresholds())
    req = _base_req()
    req["contract_version"] = 2
    out = s.evaluate(req)
    assert out["decision"] == "ERROR"
    assert "SNTL_ERROR_SCHEMA_VERSION" in out["reason_codes"][0]


def test_v3_contract_valueerror_path_is_error():
    s = SentinelV3(thresholds=CircuitBreakerThresholds())
    req = _base_req()
    req["evil"] = 1  # unknown top-level key -> ValueError
    out = s.evaluate(req)
    assert out["decision"] == "ERROR"
    assert "SNTL_ERROR_UNKNOWN_TOP_LEVEL_KEY" in out["reason_codes"][0]


def test_v3_component_mismatch_path(monkeypatch):
    s = SentinelV3(thresholds=CircuitBreakerThresholds())
    req = _base_req()
    req["component"] = "nope"  # parse ok (string), then mismatch
    out = s.evaluate(req)
    assert out["decision"] == "ERROR"
    assert "INVALID_REQUEST" in out["reason_codes"][0] or out["reason_codes"][0].startswith("SNTL_")


def test_v3_model_used_true_path(monkeypatch):
    # Force model inference path deterministically
    monkeypatch.setattr(v3mod, "run_model_inference", lambda model, features: 0.42)

    s = SentinelV3(thresholds=CircuitBreakerThresholds(), model=object())  # type: ignore[arg-type]
    out = s.evaluate(_base_req())
    assert out["meta"]["model_used"] is True
    assert out["contract_version"] == 3
    assert out["component"] == "sentinel"
    assert out["decision"] in ("ALLOW", "WARN", "ERROR", "BLOCK")
