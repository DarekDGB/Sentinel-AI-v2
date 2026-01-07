import pytest

import sentinel_ai_v2.server as s
from fastapi import HTTPException


@pytest.mark.asyncio
async def test_health_uses_wrapper_last_status(monkeypatch):
    monkeypatch.setattr(s.wrapper, "last_status", lambda: {"status": "OK"})
    resp = await s.health()
    assert resp.ok is True
    assert resp.status == "OK"


@pytest.mark.asyncio
async def test_status_returns_defaults(monkeypatch):
    monkeypatch.setattr(
        s.wrapper,
        "last_status",
        lambda: {"status": "NO_DATA", "risk_score": 0.0, "details": []},
    )
    resp = await s.status()
    assert resp.status == "NO_DATA"
    assert resp.risk_score == 0.0
    assert resp.details == []


@pytest.mark.asyncio
async def test_evaluate_success(monkeypatch):
    class _R:
        status = "OK"
        risk_score = 0.12
        details = ["x"]

    monkeypatch.setattr(s.wrapper, "evaluate", lambda telemetry: _R())
    req = s.EvaluateRequest(telemetry={"block_height": 1})
    resp = await s.evaluate(req)
    assert resp.status == "OK"
    assert resp.risk_score == 0.12
    assert resp.details == ["x"]


@pytest.mark.asyncio
async def test_evaluate_raises_http_500(monkeypatch):
    def boom(_telemetry):
        raise RuntimeError("fail")

    monkeypatch.setattr(s.wrapper, "evaluate", boom)
    req = s.EvaluateRequest(telemetry={"block_height": 1})

    with pytest.raises(HTTPException) as e:
        await s.evaluate(req)

    assert e.value.status_code == 500
    assert "fail" in str(e.value.detail)
