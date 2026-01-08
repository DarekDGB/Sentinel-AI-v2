# Sentinel AI v3 — Adaptive Core Integration (DONE Criteria)

Status: **integration-ready**

This document defines the **single supported integration surface** between
**Adaptive Core v3** (caller) and **Sentinel AI v3** (analyzer).

---

## 1) Single Supported Entrypoint

Adaptive Core **must** call exactly one function:

- `sentinel_ai_v2.api.evaluate_v3(request: dict) -> dict`

Any other import path (including instantiating internal classes directly) is
**unsupported** and may break compatibility.

---

## 2) Request Shape (Shield Contract v3)

Adaptive Core sends a Shield Contract v3 request that includes only allowlisted
top-level fields:

- `contract_version` (int, must be 3)
- `component` (str, must be `"sentinel"`)
- `request_id` (str)
- `telemetry` (object / dict)
- `constraints` (object / dict)

Unknown top-level keys are **rejected** (fail-closed).

---

## 3) Response Shape (Contract-Stable)

Sentinel AI returns a deterministic response containing contract-stable fields:

- `contract_version` (always 3)
- `component` (`"sentinel"`)
- `request_id` (echoed)
- `context_hash` (sha256 hex, deterministic per contract)
- `decision` (`ALLOW|WARN|BLOCK|ERROR`)
- `risk` (object, includes at least `score` and `tier` when applicable)
- `reason_codes` (list of stable codes)
- `meta.fail_closed` (always true)

Adaptive Core must treat:

- `decision == "ERROR"` as **BLOCK**
- `meta.fail_closed == true` as **fail-closed** (never allow on ambiguity)

---

## 4) Fail-Closed Integration Rules

Adaptive Core **must** block execution if any of the following occur:

- invalid `contract_version`
- unknown top-level fields
- telemetry too large / exceeds limits
- NaN/Inf numeric fields
- any schema validation error

Sentinel AI will return `decision="ERROR"` with stable `reason_codes`.

---

## 5) What This Module Does NOT Do

Sentinel AI does **not**:

- sign transactions
- execute wallet actions
- enforce policy
- modify blockchain state

It only **analyzes telemetry and signals risk**.

---

## 6) Regression Locks

Integration is considered **DONE** when:

- The single entrypoint exists (`sentinel_ai_v2.api.evaluate_v3`)
- A caller-shaped test proves:
  - valid request returns non-ERROR decision
  - toxic inputs fail-closed with ERROR
  - `context_hash` determinism is stable

These are enforced in CI via tests.
