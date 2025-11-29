import requests


class SimpleRpcClient:
    """
    Very small DigiByte JSON-RPC client used by Sentinel AI v2
    to query basic node information (like block height).
    """

    def __init__(self, url: str, user: str, password: str) -> None:
        self.url = url
        self.auth = (user, password)

    def _rpc(self, method: str, params=None):
        payload = {
            "jsonrpc": "1.0",
            "id": "sentinel",
            "method": method,
            "params": params or [],
        }
        resp = requests.post(self.url, json=payload, auth=self.auth, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if data.get("error"):
            raise RuntimeError(data["error"])
        return data["result"]

    def get_block_count(self) -> int:
        """
        Returns the current chain height from the DigiByte node.
        """
        return int(self._rpc("getblockcount"))
