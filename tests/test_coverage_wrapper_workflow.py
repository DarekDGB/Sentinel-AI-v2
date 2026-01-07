from sentinel_ai_v2.wrapper import workflow


class _DummyClient:
    def __init__(self):
        self.seen = None

    def evaluate_snapshot(self, raw_telemetry):
        self.seen = raw_telemetry
        # Return a SentinelResult-like object (duck typing)
        class _R:
            status = "OK"
            risk_score = 0.12
            details = ["x"]

        return _R()


def test__get_client_returns_provided_client():
    dummy = _DummyClient()
    got = workflow._get_client(dummy)  # type: ignore[arg-type]
    assert got is dummy


def test_run_full_workflow_uses_provided_client_and_passes_telemetry():
    dummy = _DummyClient()
    tel = {"block_height": 123, "mempool_size": 7}

    res = workflow.run_full_workflow(tel, client=dummy)  # type: ignore[arg-type]

    assert dummy.seen == tel
    assert res.status == "OK"
    assert res.risk_score == 0.12
    assert res.details == ["x"]
