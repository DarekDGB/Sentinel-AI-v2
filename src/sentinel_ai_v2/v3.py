"""
Sentinel AI — Shield Contract v3 entrypoint

Archangel Michael invariants enforced:
- contract_version must be exactly 3 (fail-closed)
- strict input validation (fail-closed)
- single v3 entrypoint
- NO caller-supplied shortcuts (no cached verdicts, no skip flags)
- uses existing v2 scoring pipeline WITHOUT changing behavior
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional
import hashlib
import json
import time

from .config import CircuitBreakerThresholds
from .data_intake import TelemetrySnapshot, normalize_raw_telemetry
from .model_loader import LoadedModel, run_model_inference
from .scoring import SentinelScore, compute_risk_score


@dataclass(frozen=True)
class SentinelV3:
    """
    Single supported v3 entrypoint (component-level gate).

    NOTE:
    - This is NOT a network server.
    - This is a pure evaluator (given telemetry + thresholds + optional model).
    """

    thresholds: CircuitBreakerThresholds
    model: Optional[LoadedModel] = None

    COMPONENT: str = "sentinel"
    CONTRACT_VERSION: int = 3

    def evaluate(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a Shield Contract v3 request and return a v3-shaped response.

        Fail-closed:
        - invalid version -> ERROR (fail_closed=True)
        - missing/invalid telemetry -> ERROR (fail_closed=True)

        Behavior:
        - Uses the existing v2 scoring pipeline (normalize -> features -> compute_risk_score)
          so results match v2 behavior.
        """
        start = time.time()

        # 1) Type guard
        if not isinstance(request, dict):
            return self._error_response(
                request_id="unknown",
                reason_code="SNTL_ERROR_INVALID_REQUEST",
                details={"error": "request must be a dict"},
                latency_ms=self._latency_ms(start),
            )

        request_id = str(request.get("request_id", "unknown"))

        # 2) Strict version check
        contract_version = request.get("contract_version", None)
        if contract_version != self.CONTRACT_VERSION:
            return self._error_response(
                request_id=request_id,
                reason_code="SNTL_ERROR_SCHEMA_VERSION",
                details={"error": "contract_version must be 3"},
                latency_ms=self._latency_ms(start),
            )

        # 3) Telemetry must exist and be a dict
        raw_telemetry = request.get("telemetry", None)
        if raw_telemetry is None or not isinstance(raw_telemetry, dict):
            return self._error_response(
                request_id=request_id,
                reason_code="SNTL_ERROR_INVALID_REQUEST",
                details={"error": "telemetry must exist and be a dict"},
                latency_ms=self._latency_ms(start),
            )

        # 4) Run the existing v2 pipeline (no behavior change)
        snapshot: TelemetrySnapshot = normalize_raw_telemetry(raw_telemetry)

        features: Dict[str, Any] = {
            "entropy_score": (snapshot.entropy or {}).get("score", 0.0),
            "mempool_score": (snapshot.mempool or {}).get("score", 0.0),
            "reorg_score": (snapshot.reorg or {}).get("score", 0.0),
            "entropy_drop": (snapshot.entropy or {}).get("drop", 0.0),
            "mempool_anomaly": (snapshot.mempool or {}).get("anomaly", 0.0),
            "reorg_depth": (snapshot.reorg or {}).get("depth", 0),
        }

        model_used = False
        if self.model is not None:
            # Keep v2 behavior: model contributes if available
            model_score = run_model_inference(self.model, features)
            features["model_score"] = model_score
            model_used = True

        sentinel_score: SentinelScore = compute_risk_score(
            features=features,
            thresholds=self.thresholds,
        )

        # 5) Build deterministic context hash
        context_hash = self._context_hash(
            component=self.COMPONENT,
            contract_version=self.CONTRACT_VERSION,
            telemetry=raw_telemetry,
            # thresholds matter for determinism of decision; include a stable view
            thresholds=self._thresholds_fingerprint(self.thresholds),
            model_used=model_used,
        )

        # 6) Map to v3 response
        # We keep v2 result fields inside evidence so v2 can map back exactly.
        decision = self._map_status_to_decision(sentinel_score.status)

        response = {
            "contract_version": self.CONTRACT_VERSION,
            "component": self.COMPONENT,
            "request_id": request_id,
            "context_hash": context_hash,
            "decision": decision,
            "risk": {
                "score": float(sentinel_score.risk_score),
                "tier": self._tier_from_score(float(sentinel_score.risk_score)),
            },
            # Keep reason codes stable and minimal in v3 for now
            "reason_codes": self._reason_codes_from_details(sentinel_score.details),
            "evidence": {
                "features": {},  # keep empty for now (avoid leaking internals)
                "details": {
                    # v2 compatibility payload (internal bridging only)
                    "v2_status": sentinel_score.status,
                    "v2_risk_score": float(sentinel_score.risk_score),
                    "v2_details": list(sentinel_score.details),
                },
            },
            "meta": {
                "model_used": bool(model_used),
                "latency_ms": self._latency_ms(start),
                "fail_closed": True,
            },
        }

        return response

    # ----------------------------
    # Helpers (deterministic + safe)
    # ----------------------------

    @staticmethod
    def _latency_ms(start: float) -> int:
        return int((time.time() - start) * 1000)

    @staticmethod
    def _tier_from_score(score: float) -> str:
        # Simple stable bucketing (can be refined later without breaking v2 mapping)
        if score < 0.25:
            return "LOW"
        if score < 0.50:
            return "MEDIUM"
        if score < 0.75:
            return "HIGH"
        return "CRITICAL"

    @staticmethod
    def _map_status_to_decision(status: str) -> str:
        s = (status or "").strip().upper()
        if s in {"OK", "ALLOW", "SAFE", "GREEN"}:
            return "ALLOW"
        if s in {"WARN", "WARNING", "CAUTION", "YELLOW"}:
            return "WARN"
        if s in {"ERROR"}:
            return "ERROR"
        # Default: treat unknown as BLOCK (deny-by-default)
        return "BLOCK"

    @staticmethod
    def _reason_codes_from_details(details: list[str]) -> list[str]:
        # Stable, contract-facing codes only. Keep minimal to avoid churn.
        if not details:
            return ["SNTL_OK"]
        # If v2 details exist, surface one stable umbrella code.
        return ["SNTL_V2_SIGNAL"]

    @staticmethod
    def _thresholds_fingerprint(thresholds: CircuitBreakerThresholds) -> Dict[str, Any]:
        # Best-effort stable representation for hashing.
        # Avoid relying on dataclass internals; use vars() which is stable for dataclasses.
        try:
            return dict(vars(thresholds))
        except Exception:
            return {"_": "unavailable"}

    @staticmethod
    def _context_hash(
        component: str,
        contract_version: int,
        telemetry: Dict[str, Any],
        thresholds: Dict[str, Any],
        model_used: bool,
    ) -> str:
        payload = {
            "component": component,
            "contract_version": contract_version,
            "telemetry": telemetry,
            "thresholds": thresholds,
            "model_used": bool(model_used),
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    def _error_response(
        self,
        request_id: str,
        reason_code: str,
        details: Dict[str, Any],
        latency_ms: int,
    ) -> Dict[str, Any]:
        payload = {
            "component": self.COMPONENT,
            "contract_version": self.CONTRACT_VERSION,
            "request_id": str(request_id),
            "reason_code": reason_code,
        }
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        context_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()

        return {
            "contract_version": self.CONTRACT_VERSION,
            "component": self.COMPONENT,
            "request_id": str(request_id),
            "context_hash": context_hash,
            "decision": "ERROR",
            "risk": {"score": 0.0, "tier": "LOW"},
            "reason_codes": [reason_code],
            "evidence": {"features": {}, "details": details},
            "meta": {"model_used": False, "latency_ms": int(latency_ms), "fail_closed": True},
        }
