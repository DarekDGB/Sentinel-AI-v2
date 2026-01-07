from sentinel_ai_v2.wrapper.monitor import Monitor


class _DummyResult:
    status = "BLOCK"
    risk_score = 0.88
    details = ["a", "b"]


def test_monitor_last_status_no_data():
    m = Monitor()
    assert m.last_result is None
    assert m.last_status() == {"status": "NO_DATA", "risk_score": 0.0, "details": []}


def test_monitor_update_and_last_status():
    m = Monitor()
    m.update(_DummyResult())  # type: ignore[arg-type]
    out = m.last_status()
    assert out["status"] == "BLOCK"
    assert out["risk_score"] == 0.88
    assert out["details"] == ["a", "b"]
