# Security Policy

**Project:** DGB Sentinel AI  
**Component:** Sentinel AI (Shield Layer v3)  
**Author:** DarekDGB  
**License:** MIT

---

## Scope of This Security Policy

This security policy applies **only** to the Sentinel AI codebase and its
documented interfaces under **Shield Contract v3**.

Sentinel AI is a **read-only, non-authoritative security component**.
It does **not** hold private keys, execute transactions, or modify blockchain
state.

Reports that assume Sentinel has execution or enforcement authority are
considered **out of scope** by design.

---

## Reporting a Vulnerability

If you believe you have found a security issue:

1. **Do not publish exploit details in a public issue.**
2. Prefer **GitHub Security Advisories** (private reporting), if available.
3. If advisories are not available, open an issue clearly marked **SECURITY**
   with **minimal details** and wait for further instructions.

Please allow reasonable time for triage before requesting updates.

---

## What to Include in a Report

To help validate and fix issues efficiently, include:

- **Impact**  
  What an attacker could realistically achieve *within Sentinelâs scope*.

- **Reproduction steps**  
  Clear, minimal steps (safe and non-destructive if possible).

- **Expected vs actual behavior**  
  Especially regarding fail-closed semantics or determinism.

- **Evidence**  
  Logs, screenshots, or test cases that support the claim.

---

## In-Scope Vulnerabilities

Examples of valid security reports include:

- Contract validation bypasses
- Non-deterministic behavior for identical inputs
- Incorrect `context_hash` generation
- Fail-open conditions on malformed input
- DoS vectors via unbounded recursion, payload size, or numeric edge cases
- Inconsistencies between documented and implemented Shield Contract v3 rules

---

## Out-of-Scope Reports

The following are **explicitly out of scope**:

- Requests for new features or expanded authority
- Issues related to transaction signing or fund control
- Consensus, mining, or DigiByte Core behavior
- Hypothetical attacks requiring Sentinel to execute actions it does not support
- Vulnerabilities in external systems consuming Sentinel outputs

Such reports may be closed without action.

---

## Disclosure Philosophy

This repository follows **responsible disclosure** principles:

- Validated issues are fixed promptly
- Weaponized details are not published before a patch exists
- Public disclosure occurs only after remediation or mitigation guidance

Security fixes may include:
- Contract tightening
- Additional validation
- New regression tests
- CI enforcement updates

---

## Security References

- **Shield Contract v3:** `docs/CONTRACT.md`
- **Auditor Summary:** `docs/AUDITOR_SUMMARY.md`
- **Architecture:** `docs/ARCHITECTURE.md`

These documents define Sentinel AIâs security boundaries and guarantees.

---

## Final Note

Any change that weakens **determinism**, **fail-closed behavior**, or
**non-authoritative design** will be treated as a **security regression**
and rejected.

This policy is binding for contributors and integrators.
