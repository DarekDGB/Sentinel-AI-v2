# Contributing to Sentinel AI (Shield Contract v3)

> **Shield Contract v3 Notice**
>
> Sentinel AI is now a **Shield Contract v3 signal-generation component**.
> Contributions must not weaken:
> - contract strictness
> - determinism
> - fail-closed behavior
> - Sentinel’s read-only, non-consensus role
>
> Authoritative specifications live in **`docs/INDEX.md`**.

---

## 🚀 Project Scope (v3)

**Sentinel AI** is the *external, non-consensus* threat detection and signal-generation
layer of the **DigiByte Quantum Shield**.

Its responsibilities are strictly limited to:

- observing network telemetry
- detecting anomalous or hostile patterns
- producing **structured Shield Contract v3 signals**
- remaining fully **read-only**

Sentinel AI **must never**:
- sign transactions
- modify blockchain state
- influence consensus rules
- act as an enforcement or policy engine

Legacy v2 concepts are preserved in `docs/legacy/` for historical reference only.

---

## ✅ What Contributions Are Welcome

### ✔️ Detection & Analysis Improvements
- Improved anomaly detection logic
- Better feature engineering (entropy, topology, propagation, forks)
- Refinements to risk scoring models
- Performance and reliability improvements

### ✔️ Contract & Security Hardening
- Strengthening Shield Contract v3 validation
- Improving fail-closed handling
- Tightening determinism and replay safety
- Additional regression or invariance tests

### ✔️ Testing & Verification
- Attack simulations
- Property-based or fuzz testing
- CI hardening
- No-drift regression coverage

### ✔️ Documentation
- Clarifying v3 behavior or invariants
- Improving explanations in authoritative docs
- Correcting ambiguity or drift

---

## ❌ What Will Not Be Accepted

### 🚫 Weakening Shield Contract v3
- Making validation permissive
- Allowing partial or best-effort parsing
- Softening fail-closed behavior
- Introducing silent fallbacks

### 🚫 Decision or Enforcement Logic
Sentinel AI must not:
- override upstream or downstream decisions
- act as a policy engine
- downgrade or reinterpret signals after evaluation

### 🚫 Consensus Interaction
Sentinel AI must never:
- modify DigiByte consensus rules
- influence block acceptance or difficulty
- interact with private keys or signing flows

### 🚫 Opaque or Unreviewable Complexity
Avoid introducing:
- opaque ML pipelines without explainability
- heavy frameworks that reduce auditability
- logic that obscures determinism or reproducibility

---

## 🧱 Design Principles (Non-Negotiable)

All contributions must respect:

1. **Read-Only by Design**  
   Sentinel observes and signals — nothing more.

2. **Fail-Closed First**  
   Invalid input must result in `ERROR`, never silent acceptance.

3. **Determinism**  
   Same input → same output → same `context_hash`.

4. **Auditability**  
   Security reviewers must be able to reason about behavior from code alone.

5. **Separation of Authority**  
   Sentinel signals; DQSN transports; ADN decides.

6. **History Preservation**  
   Legacy concepts may be referenced, not re-introduced.

---

## 🔄 Pull Request Expectations

A pull request should include:

- A clear explanation of **what changed and why**
- Tests for any contract, detection, or logic changes
- No weakening of v3 invariants
- Documentation updates where applicable

Additional rules:
- Contract changes **require tests**
- Determinism changes require **regression coverage**
- Fail-closed behavior must be preserved or strengthened

The architect (**@DarekDGB**) reviews **direction and invariants**.  
Contributors and DigiByte developers review **technical correctness**.

---

## 📝 License

By contributing, you agree that your work is released under the **MIT License**.

© 2026 **DarekDGB**
