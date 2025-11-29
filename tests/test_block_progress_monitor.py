import time
from datetime import datetime, timezone

from sentinel_ai_v2.telemetry_monitor import (
    BlockProgressMonitor,
    BlockProgressStatus,
)


class FakeRpc:
    """
    Fake RPC client for testing.
    You control block height manually.
    """
    def __init__(self, heights):
        self.heights = heights
        self.index = 0

    def get_block_count(self):
        # return next height in array
        h = self.heights[self.index]
        # do not overflow
        if self.index < len(self.heights) - 1:
            self.index += 1
        return h


def test_monitor_detects_normal_progress():
    rpc = FakeRpc([100, 101, 102])
    monitor = BlockProgressMonitor(rpc, stall_threshold_seconds=1)

    s1 = monitor.check_block_progress()
    s2 = monitor.check_block_progress()
    s3 = monitor.check_block_progress()

    assert s1.status == "ok"
    assert s2.status == "ok"
    assert s3.status == "ok"
    assert s3.current_height == 102


def test_monitor_detects_stall():
    # height stays the same
    rpc = FakeRpc([200, 200, 200])
    monitor = BlockProgressMonitor(rpc, stall_threshold_seconds=0)

    s1 = monitor.check_block_progress()
    s2 = monitor.check_block_progress()

    assert s2.status == "stalled"
    assert s2.stalled_for_seconds >= 0
