import pytest

from sentinel_ai_v2.rpc_client import SimpleRpcClient


class _Resp:
    def __init__(self, payload, status_ok=True):
        self._payload = payload
        self._status_ok = status_ok

    def raise_for_status(self):
        if not self._status_ok:
            raise RuntimeError("http error")

    def json(self):
        return self._payload


def test_rpc_client_success(monkeypatch):
    calls = {}

    def fake_post(url, json, auth, timeout):
        calls["url"] = url
        calls["payload"] = json
        calls["auth"] = auth
        calls["timeout"] = timeout
        return _Resp({"result": 123, "error": None})

    import sentinel_ai_v2.rpc_client as m
    monkeypatch.setattr(m.requests, "post", fake_post)

    c = SimpleRpcClient("http://node", "u", "p")
    assert c.get_block_count() == 123

    assert calls["url"] == "http://node"
    assert calls["payload"]["method"] == "getblockcount"
    assert calls["auth"] == ("u", "p")
    assert calls["timeout"] == 10


def test_rpc_client_raises_on_rpc_error(monkeypatch):
    def fake_post(url, json, auth, timeout):
        return _Resp({"result": None, "error": {"code": -1, "message": "boom"}})

    import sentinel_ai_v2.rpc_client as m
    monkeypatch.setattr(m.requests, "post", fake_post)

    c = SimpleRpcClient("http://node", "u", "p")
    with pytest.raises(RuntimeError):
        c.get_block_count()


def test_rpc_client_raises_on_http_error(monkeypatch):
    def fake_post(url, json, auth, timeout):
        return _Resp({"result": 1, "error": None}, status_ok=False)

    import sentinel_ai_v2.rpc_client as m
    monkeypatch.setattr(m.requests, "post", fake_post)

    c = SimpleRpcClient("http://node", "u", "p")
    with pytest.raises(RuntimeError):
        c.get_block_count()
