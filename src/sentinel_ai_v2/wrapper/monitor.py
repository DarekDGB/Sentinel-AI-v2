class Monitor:
    """
    Stores latest risk score / threat status.
    Useful for APIs, CLI, wrappers.
    """

    def __init__(self):
        self.state = None

    def update(self, result):
        """Save current result snapshot."""
        self.state = result

    def last_status(self):
        """Return latest status or fallback."""
        if self.state is None:
            return {"status": "no data yet"}
        return self.state
