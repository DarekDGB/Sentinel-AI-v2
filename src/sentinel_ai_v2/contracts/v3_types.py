from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, FrozenSet, Optional
import math

from .v3_reason_codes import ReasonCode


def _safe_is_finite_number(x: Any) -> bool:
    # Accept ints/floats only; reject bool (bool is subclass of int).
    if isinstance(x, bool):
        return False
    if isinstance(x, (int, float)):
        return math.isfinite(float(x))
    return True  # non-numbers OK here


def _walk_check_finite(obj: Any, max_nodes: int) -> Optional[ReasonCode]:
    """
    Walk JSON-like structures and reject NaN/Infinity.
    Also provides a node limit to avoid pathological recursion/DoS.
    """
    seen = 0
    stack = [obj]
    while stack:
        seen += 1
        if seen > max_nodes:
            # Treat as too large; caller can map to telemetry too large
            return ReasonCode.SNTL_ERROR_TELEMETRY_TOO_LARGE

        cur = stack.pop()
        if isinstance(cur, dict):
            for k, v in cur.items():
                # keys must be strings in JSON-like telemetry
                if not isinstance(k, str):
                    return ReasonCode.SNTL_ERROR_INVALID_REQUEST
                if not _safe_is_finite_number(v):
                    return ReasonCode.SNTL_ERROR_BAD_NUMBER
                stack.append(v)
        elif isinstance(cur, list):
            for v in cur:
                if not _safe_is_finite_number(v):
                    return ReasonCode.SNTL_ERROR_BAD_NUMBER
                stack.append(v)
        else:
            if not _safe_is_finite_number(cur):
                return ReasonCode.SNTL_ERROR_BAD_NUMBER

    return None


@dataclass(frozen=True)
class SentinelV3Constraints:
    fail_closed: bool = True
    max_latency_ms: int = 2500


@dataclass(frozen=True)
class SentinelV3Request:
    contract_version: int
    component: str
    request_id: str
    telemetry: Dict[str, Any]
    constraints: SentinelV3Constraints = SentinelV3Constraints()

    # Hard allowlist for v3 top-level keys
    TOP_LEVEL_KEYS: FrozenSet[str] = frozenset(
        {"contract_version", "component", "request_id", "telemetry", "constraints"}
    )

    # Hard limits (tune later with tests)
    MAX_TELEMETRY_BYTES: int = 200_000     # 200KB
    MAX_TELEMETRY_NODES: int = 20_000      # structure nodes upper bound

    @staticmethod
    def from_dict(obj: Dict[str, Any]) -> "SentinelV3Request":
        if not isinstance(obj, dict):
            raise ValueError(ReasonCode.SNTL_ERROR_INVALID_REQUEST.value)

        # Unknown top-level keys -> fail-closed
        unknown = set(obj.keys()) - set(SentinelV3Request.TOP_LEVEL_KEYS)
        if unknown:
            raise ValueError(ReasonCode.SNTL_ERROR_UNKNOWN_TOP_LEVEL_KEY.value)

        cv = obj.get("contract_version", None)
        comp = obj.get("component", None)
        rid = obj.get("request_id", "unknown")
        tel = obj.get("telemetry", None)
        con = obj.get("constraints", {}) or {}

        if not isinstance(rid, str):
            rid = str(rid)

        if not isinstance(cv, int):
            raise ValueError(ReasonCode.SNTL_ERROR_SCHEMA_VERSION.value)

        if not isinstance(comp, str):
            raise ValueError(ReasonCode.SNTL_ERROR_INVALID_REQUEST.value)

        if not isinstance(tel, dict):
            raise ValueError(ReasonCode.SNTL_ERROR_INVALID_REQUEST.value)

        # Approx byte limit (canonical JSON)
        try:
            import json
            canonical = json.dumps(tel, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            if len(canonical.encode("utf-8")) > SentinelV3Request.MAX_TELEMETRY_BYTES:
                raise ValueError(ReasonCode.SNTL_ERROR_TELEMETRY_TOO_LARGE.value)
        except ValueError:
            raise
        except Exception:
            # If telemetry can't be serialized deterministically -> reject
            raise ValueError(ReasonCode.SNTL_ERROR_INVALID_REQUEST.value)

        # NaN/Infinity + node limit guard
        rc = _walk_check_finite(tel, max_nodes=SentinelV3Request.MAX_TELEMETRY_NODES)
        if rc is not None:
            raise ValueError(rc.value)

        # Constraints (ignore caller attempts to disable fail_closed)
        max_latency_ms = con.get("max_latency_ms", 2500)
        try:
            max_latency_ms = int(max_latency_ms)
        except Exception:
            max_latency_ms = 2500

        constraints = SentinelV3Constraints(fail_closed=True, max_latency_ms=max_latency_ms)

        return SentinelV3Request(
            contract_version=cv,
            component=comp,
            request_id=rid,
            telemetry=tel,
            constraints=constraints,
        )


@dataclass(frozen=True)
class SentinelV3Response:
    contract_version: int
    component: str
    request_id: str
    context_hash: str
    decision: str
    risk: Dict[str, Any]
    reason_codes: list[str]
    evidence: Dict[str, Any]
    meta: Dict[str, Any]
