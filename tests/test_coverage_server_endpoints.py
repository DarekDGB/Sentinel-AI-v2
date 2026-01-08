import pytest
from fastapi import HTTPException

import sentinel_ai_v2.server as s


def _run(coro):
    try:
        return coro.send(None)
    except StopIteration as e:
        return e.value


def test_health_ok():
    res = _run(s.health())
    assert res.ok is True
    assert isinstance(res.status, str)


def test_status_ok():
    res = _run(s.status())
    assert isinstance(res.status, str)
    assert isinstance(res.risk_score, float)


def test_evaluate_ok(monkeypatch):
    class R:
        status = "OK"
        risk_score = 0.0
        details = []

    def ok(_telemetry):
        return R()

    monkeypatch.setattr(s.wrapper, "evaluate", ok)
    req = s.EvaluateRequest(telemetry={"block_height": 1})
    res = _run(s.evaluate(req))
    assert res.status == "OK"
    assert res.risk_score == 0.0
    assert res.details == []


def test_evaluate_raises_http_500(monkeypatch):
    def boom(_telemetry):
        raise RuntimeError("fail")

    monkeypatch.setattr(s.wrapper, "evaluate", boom)
    req = s.EvaluateRequest(telemetry={"block_height": 1})

    with pytest.raises(HTTPException) as e:
        _run(s.evaluate(req))

    assert e.value.status_code == 500
    # Fail-closed: do not leak internal exception strings to clients
    assert e.value.detail == "internal_error"
