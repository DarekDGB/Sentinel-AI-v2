from __future__ import annotations

import logging
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Protocol

logger = logging.getLogger(__name__)


class RpcClient(Protocol):
    """
    Minimal RPC client interface that Sentinel AI v2 expects.
    Your concrete implementation should call the DigiByte node's
    `getblockcount` RPC method.
    """
    def get_block_count(self) -> int:
        ...


@dataclass
class BlockProgressStatus:
    """
    Result of a single block-progress check.
    """
    timestamp: datetime
    current_height: int
    previous_height: Optional[int]
    status: str  # "ok" or "stalled"
    stalled_for_seconds: int


class BlockProgressMonitor:
    """
    Simple in-memory monitor that tracks whether the chain appears stalled.

    Usage:
        monitor = BlockProgressMonitor(rpc_client, stall_threshold_seconds=600)
        status = monitor.check_block_progress()
    """

    def __init__(self, rpc_client: RpcClient, stall_threshold_seconds: int = 600) -> None:
        self.rpc_client = rpc_client
        self.stall_threshold_seconds = stall_threshold_seconds

        self._last_height: Optional[int] = None
        self._last_seen_at: Optional[datetime] = None

    def check_block_progress(self) -> BlockProgressStatus:
        """
        Fetch current block height and compare with the previous check.

        Returns:
            BlockProgressStatus with:
              - status = "ok" or "stalled"
              - stalled_for_seconds >= threshold if stalled
        """
        now = datetime.now(timezone.utc)
        current_height = self.rpc_client.get_block_count()

        prev_height = self._last_height
        stalled_for_seconds = 0
        status = "ok"

        if self._last_height is not None and self._last_seen_at is not None:
            if current_height == self._last_height:
                stalled_for_seconds = int((now - self._last_seen_at).total_seconds())
                if stalled_for_seconds >= self.stall_threshold_seconds:
                    status = "stalled"

        # update internal state
        self._last_height = current_height
        self._last_seen_at = now

        result = BlockProgressStatus(
            timestamp=now,
            current_height=current_height,
            previous_height=prev_height,
            status=status,
            stalled_for_seconds=stalled_for_seconds,
        )

        log_level = logging.WARNING if status == "stalled" else logging.INFO
        logger.log(log_level, "Block progress status: %s", asdict(result))

        return result


# Optional: simple module-level helper for the README example

_monitor: Optional[BlockProgressMonitor] = None


def init_block_progress_monitor(rpc_client: RpcClient, stall_threshold_seconds: int = 600) -> None:
    """
    Initialise a global BlockProgressMonitor instance for simple usage.

    After calling this once, you can use `check_block_progress()` directly.
    """
    global _monitor
    _monitor = BlockProgressMonitor(rpc_client, stall_threshold_seconds)


def check_block_progress() -> BlockProgressStatus:
    """
    Convenience wrapper used in README examples.

    Make sure to call `init_block_progress_monitor(...)` once on startup.
    """
    if _monitor is None:
        raise RuntimeError("BlockProgressMonitor not initialised. "
                           "Call init_block_progress_monitor(rpc_client) first.")
    return _monitor.check_block_progress()
