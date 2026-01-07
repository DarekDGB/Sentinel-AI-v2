import math
import pytest

from sentinel_ai_v2.contracts.v3_types import SentinelV3Request
from sentinel_ai_v2.contracts.v3_reason_codes import ReasonCode
import sentinel_ai_v2.contracts.v3_types as t


def _base():
    return {
        "contract_version": 3,
        "component": "sentinel",
        "request_id": "r1",
        "telemetry": {"block_height": 1, "mempool_size": 2},
        "constraints": {"max_latency_ms": 2500},
    }


def test_bad_number_nan_rejected():
    req = _base()
    req["telemetry"] = {"x": float("nan")}
    with pytest.raises(ValueError) as e:
        SentinelV3Request.from_dict(req)
    assert ReasonCode.SNTL_ERROR_BAD_NUMBER.value in str(e.value)


def test_bad_number_infinity_rejected():
    req = _base()
    req["telemetry"] = {"x": float("inf")}
    with pytest.raises(ValueError) as e:
        SentinelV3Request.from_dict(req)
    assert ReasonCode.SNTL_ERROR_BAD_NUMBER.value in str(e.value)


def test_non_string_dict_key_rejected():
    req = _base()
    req["telemetry"] = {1: "x"}  # invalid JSON-like key
    with pytest.raises(ValueError) as e:
        SentinelV3Request.from_dict(req)
    assert ReasonCode.SNTL_ERROR_INVALID_REQUEST.value in str(e.value)


def test_node_limit_guard_triggers(monkeypatch):
    # Force a tiny node limit to hit the guard deterministically
    monkeypatch.setattr(t.SentinelV3Request, "MAX_TELEMETRY_NODES", 3)
    req = _base()
    req["telemetry"] = {"a": {"b": {"c": {"d": 1}}}}
    with pytest.raises(ValueError) as e:
        SentinelV3Request.from_dict(req)
    assert ReasonCode.SNTL_ERROR_TELEMETRY_TOO_LARGE.value in str(e.value)


def test_constraints_bad_latency_falls_back_to_default():
    req = _base()
    req["constraints"] = {"max_latency_ms": "not-an-int"}
    parsed = SentinelV3Request.from_dict(req)
    assert parsed.constraints.fail_closed is True
    assert parsed.constraints.max_latency_ms == 2500


def test_schema_version_type_mismatch():
    req = _base()
    req["contract_version"] = "3"
    with pytest.raises(ValueError) as e:
        SentinelV3Request.from_dict(req)
    assert ReasonCode.SNTL_ERROR_SCHEMA_VERSION.value in str(e.value)
