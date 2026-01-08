import pytest

from sentinel_ai_v2.v3 import SentinelV3
from sentinel_ai_v2.config import CircuitBreakerThresholds
from sentinel_ai_v2.contracts import ReasonCode, canonical_hash_v3
from tests.fixtures_v3 import make_valid_v3_request


def test_context_hash_success_matches_contract_payload():
    """
    Regression lock: SUCCESS/WARN/BLOCK context_hash MUST equal canonical_hash_v3 of:
      component, contract_version, telemetry, thresholds fingerprint, model_used
    """
    s = SentinelV3(thresholds=CircuitBreakerThresholds())

    # Use the repo's known-valid v3 request fixture (top-level allowlist compliant).
    req = make_valid_v3_request(
        request_id="r1",
        telemetry={"block_height": 10, "mempool_size": 1, "entropy": {"score": 0.1}},
        max_latency_ms=2500,
    )

    out = s.evaluate(req)
    assert out["contract_version"] == 3
    assert out["component"] == "sentinel"
    assert out["decision"] in {"ALLOW", "WARN", "BLOCK"}  # must not be ERROR for valid input
    assert isinstance(out["context_hash"], str)
    assert len(out["context_hash"]) == 64  # sha256 hex

    expected = canonical_hash_v3(
        {
            "component": "sentinel",
            "contract_version": 3,
            "telemetry": req["telemetry"],
            "thresholds": s._thresholds_fingerprint(s.thresholds),
            "model_used": False,  # default: no model loaded
        }
    )

    assert out["context_hash"] == expected


def test_context_hash_error_non_dict_request_matches_contract_payload():
    """
    Regression lock: non-dict request must fail-closed with ERROR context_hash payload:
      component, contract_version, request_id, reason_code
    """
    s = SentinelV3(thresholds=CircuitBreakerThresholds())

    out = s.evaluate("not a dict")  # type: ignore[arg-type]
    assert out["decision"] == "ERROR"
    assert out["contract_version"] == 3
    assert out["component"] == "sentinel"

    expected = canonical_hash_v3(
        {
            "component": "sentinel",
            "contract_version": 3,
            "request_id": "unknown",
            "reason_code": ReasonCode.SNTL_ERROR_INVALID_REQUEST.value,
        }
    )

    assert out["context_hash"] == expected


def test_context_hash_error_bad_version_matches_contract_payload():
    """
    Regression lock: wrong contract_version must fail-closed with ERROR context_hash payload:
      component, contract_version, request_id, reason_code
    """
    s = SentinelV3(thresholds=CircuitBreakerThresholds())

    req = make_valid_v3_request(request_id="r-badver", contract_version=2)

    out = s.evaluate(req)
    assert out["decision"] == "ERROR"
    assert out["contract_version"] == 3
    assert out["component"] == "sentinel"

    expected = canonical_hash_v3(
        {
            "component": "sentinel",
            "contract_version": 3,
            "request_id": "r-badver",
            "reason_code": ReasonCode.SNTL_ERROR_SCHEMA_VERSION.value,
        }
    )

    assert out["context_hash"] == expected
