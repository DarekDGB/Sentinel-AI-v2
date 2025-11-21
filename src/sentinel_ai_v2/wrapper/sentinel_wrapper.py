import time
from .workflow import run_full_workflow
from .monitor import Monitor

class SentinelWrapper:
    """
    High-level orchestrator: wraps the entire Sentinel AI v2 engine.
    Provides: start(), stop(), health(), run_once()
    """

    def __init__(self):
        self.monitor = Monitor()
        self.running = False

    def run_once(self):
        """Executes a single run cycle."""
        result = run_full_workflow()
        self.monitor.update(result)
        return result

    def start(self, interval=10):
        """Starts an automated loop."""
        self.running = True
        print("[SentinelWrapper] Starting loop...")

        while self.running:
            result = self.run_once()
            print(f"[SentinelWrapper] Result: {result}")
            time.sleep(interval)

    def stop(self):
        """Stops the automated loop."""
        self.running = False
        print("[SentinelWrapper] Stopped.")

    def health(self):
        """Returns last known health state."""
        return self.monitor.last_status()
