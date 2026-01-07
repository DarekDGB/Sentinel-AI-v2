from sentinel_ai_v2.adaptive_event import AdaptiveEvent
import sentinel_ai_v2.adaptive_bridge as b


def test_adaptive_event_timestamp_is_per_instance():
    a = AdaptiveEvent()
    b2 = AdaptiveEvent()
    assert a.created_at != b2.created_at


def test_build_adaptive_event_sets_fields():
    evt = b.build_adaptive_event(
        anomaly_type="entropy_drop",
        severity=0.8,
        qri_before=0.9,
        qri_after=0.7,
        block_height=123,
        txid="abc",
        details="x",
    )
    assert evt.layer == "sentinel"
    assert evt.anomaly_type == "entropy_drop"
    assert evt.severity == 0.8
    assert evt.qri_before == 0.9
    assert evt.qri_after == 0.7
    assert evt.block_height == 123
    assert evt.txid == "abc"
    assert evt.details == "x"


def test_emit_adaptive_event_from_signal_calls_export(monkeypatch):
    captured = {}

    def fake_export(evt):
        captured["evt"] = evt

    monkeypatch.setattr(b, "export_to_adaptive_core", fake_export)

    b.emit_adaptive_event_from_signal(
        signal_name="reorg_pattern",
        severity=0.6,
        qri_delta=-0.2,
        context={"window": "30s"},
        block_height=999,
        txid="tx1",
    )

    evt = captured["evt"]
    assert evt.anomaly_type == "reorg_pattern"
    assert evt.block_height == 999
    assert evt.txid == "tx1"
    assert evt.qri_after <= evt.qri_before
    assert evt.details is not None
