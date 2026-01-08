# Sentinel AI Documentation Index

This index lists **authoritative, supporting, and legacy documentation**
for **DGB Sentinel AI (Shield Contract v3)**.

---

## 🚀 Start Here (Authoritative — v3)

These documents define **binding behavior** of Sentinel AI v3.
Audits, integrations, and reviews must rely on these.

- **Shield Contract (binding):** `CONTRACT.md`
- **Architecture (role + flow):** `ARCHITECTURE.md`
- **Upgrade Plan:** `upgrade/SENTINEL_AI_V3_UPGRADE_PLAN.md`
- **Changelog:** `../CHANGELOG.md`
- **Security Policy:** `../SECURITY.md`
- **Auditor Summary:** `../AUDITOR_SUMMARY.md`

---

## 🧩 Integration & Usage

These documents help integrators and partners use Sentinel AI correctly.

- **README (public entry point):** `../README.md`
- **Integration Guide:** `../INTEGRATION.md`
- **Troubleshooting:** `../TROUBLESHOOTING.md`
- **Migration v2 → v3:** `../MIGRATION_V2_TO_V3.md`

---

## 🧪 Testing & Guarantees

These describe how guarantees are enforced.

- CI workflow: `.github/workflows/tests.yml`
- Coverage gate: ≥90% enforced in CI
- Determinism & toxic telemetry regression tests (see `tests/`)

---

## 🕰️ Legacy References (Non‑Authoritative)

The following documents are preserved **for historical context only**.
They do **not** define current behavior.

- `legacy/technical-spec.md`
- `legacy/whitepaper-sentinel-ai-v2.md`

Legacy documents must **not** be used for:
- integration decisions
- security assumptions
- audits of v3 behavior

---

## ✅ Status

- Shield Contract v3 enforced
- CI green
- Coverage gate active
- Legacy paths regression‑locked

This index reflects the **current, supported surface** of Sentinel AI.
