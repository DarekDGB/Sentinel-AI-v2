from sentinel_ai_v2.config import CircuitBreakerThresholds
from sentinel_ai_v2.v3 import SentinelV3
from sentinel_ai_v2.contracts import ReasonCode


def test_contract_v3_unknown_top_level_key_fails_closed():
    v3 = SentinelV3(thresholds=CircuitBreakerThresholds(), model=None)

    req = {
        "contract_version": 3,
        "component": "sentinel",
        "request_id": "x",
        "telemetry": {},
        "constraints": {"fail_closed": True},
        "unexpected": "nope",  # should trigger fail-closed
    }

    resp = v3.evaluate(req)
    assert resp["decision"] == "ERROR"
    assert resp["meta"]["fail_closed"] is True
    assert ReasonCode.SNTL_ERROR_UNKNOWN_TOP_LEVEL_KEY.value in resp["reason_codes"]
