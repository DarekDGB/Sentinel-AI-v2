from sentinel_ai_v2.config import CircuitBreakerThresholds
from sentinel_ai_v2.v3 import SentinelV3


def test_contract_v3_invalid_version_fails_closed():
    """
    Archangel Michael invariant:
    Any request that is not contract_version == 3 MUST fail closed.
    """
    thresholds = CircuitBreakerThresholds()
    v3 = SentinelV3(thresholds=thresholds, model=None)

    request = {"contract_version": 2}  # invalid on purpose
    response = v3.evaluate(request)

    assert response["decision"] == "ERROR"
    assert response["meta"]["fail_closed"] is True
    assert "SNTL_ERROR_SCHEMA_VERSION" in response["reason_codes"]
