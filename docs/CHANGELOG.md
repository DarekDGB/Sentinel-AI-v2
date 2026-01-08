# Changelog

All notable changes to **DGB Sentinel AI** are documented in this file.

This project follows **semantic versioning** and enforces **contract stability**.
Breaking changes are only introduced with a **major version bump**.

---

## [v3.0.0] — 2026-01-07

### 🚀 Major Release — Shield Contract v3

This release marks the **formal stabilization of Sentinel AI v3** as a
deterministic, fail-closed, non-authoritative security component within the
DigiByte Quantum Immune Shield.

#### Added
- Shield Contract v3 with strict request/response schema
- Deterministic `context_hash` generation (SHA-256, canonical JSON)
- Explicit fail-closed validation semantics
- Stable, contract-facing reason codes
- Toxic telemetry regression test pack (DoS, NaN/Inf, size & depth limits)
- Shared v3 test fixtures for deterministic test construction
- Auditor Summary (`AUDITOR_SUMMARY.md`)
- Hardened Security Policy with explicit scope and non-goals
- CI enforcement with ≥90% test coverage gate
- Unicode hashing behavior explicitly tested and documented

#### Changed
- All request validation now occurs **before** any processing
- v2 behavior routed through v3 adapter (no bypass possible)
- Internal helpers hardened for determinism and safety
- Documentation rewritten to reflect strict non-authoritative boundaries

#### Fixed
- Edge cases in telemetry validation
- Inconsistent error handling paths
- Coverage gaps in adaptive bridges and hooks
- CI and packaging inconsistencies

#### Security
- Enforced deny-by-default behavior across all validation paths
- Added regression tests for adversarial input patterns
- Locked hashing behavior to prevent silent contract changes

---

## [v2.x] — Legacy Series (Maintenance Only)

### Notes
- v2 APIs remain available via internal adapter
- v2 behavior is regression-locked
- No new features will be added to v2
- All security guarantees are defined by Shield Contract v3

---

## Versioning Policy

- **MAJOR** — Contract or semantic breaking change
- **MINOR** — Backward-compatible feature additions
- **PATCH** — Bug fixes, tests, documentation, CI improvements

Any change that weakens determinism, fail-closed behavior, or non-authoritative
design will require a major version bump and explicit documentation.

---

*This changelog is authoritative. Undocumented changes are considered invalid.*
