# 🛡️ Sentinel AI (Shield Contract v3)
### *DigiByte Quantum Shield — External Telemetry, Threat Modeling & Anomaly Detection Layer*  
**Architecture by @DarekDGB — MIT Licensed**

> **Repository note**  
> This repository was originally named `Sentinel-AI-v2`.  
> It now implements **Shield Contract v3**.  
> A repository rename (removing version suffixes) will occur in a future cleanup pass.

---

## 🚀 Purpose

**Sentinel AI** is the *external, non-consensus* security monitoring layer of the **DigiByte Quantum Shield**.

It operates under **Shield Contract v3**, enforcing strict versioning, deterministic evaluation, and fail-closed
semantics. Sentinel observes, analyzes, correlates, and surfaces emergent threats to the DigiByte network, but
**never interferes with consensus, signing, or execution**.

Sentinel is designed as a **reference-grade security component**, suitable for integration into higher shield layers
(DQSN, ADN, Adaptive Core) and for independent review by DigiByte Core developers and security engineers.

---

## 📚 Documentation Authority

All authoritative documentation for Sentinel AI v3 lives under:

```
docs/
├── INDEX.md          ← start here
├── CONTRACT.md       ← Shield Contract v3 (authoritative)
├── ARCHITECTURE.md   ← system design & invariants
└── upgrade/          ← v2 → v3 migration notes
```

Legacy v2 documents are preserved under `docs/legacy/` for historical reference only.

---

## 🛡️ Sentinel AI — Shield Contract v3

Sentinel AI is a **fully hardened Shield Contract v3 component**.

### Core guarantees

- **Contract v3 enforced**
  - `contract_version == 3` is the outermost gate
  - Invalid, unknown, or malformed input fails closed
- **Read-only**
  - No signing, no execution, no state mutation
- **Deterministic**
  - Same input → same output → same `context_hash`
- **Fail-closed**
  - NaN/Infinity values, unknown schema, or invalid versions → `ERROR`
- **Single authority**
  - All evaluation flows through the v3 contract gate

Sentinel AI does **not**:
- alter consensus
- modify blockchain state
- hold keys
- replace DigiByte Core or node software

---

## 🔥 Position in the DigiByte Quantum Shield (5-Layer Model)

```
        ┌────────────────────────────────────────┐
        │           Guardian Wallet             │
        │  User-side rules & policy enforcement │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        Quantum Wallet Guard (QWG)      │
        │  PQC checks, signature safety, filters │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        ADN v3 — Active Defence         │
        │  Network response & tactical controls │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        Sentinel AI (THIS REPO)         │
        │  Telemetry analysis & threat scoring  │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        DQSN v3 — Telemetry Layer       │
        │  Entropy, node health, chain signals  │
        └────────────────────────────────────────┘
```

Sentinel AI is the **eyes and ears** of the Quantum Shield.

---

## 🎯 Core Mission

### ✓ Observe  
Collect distributed measurements about the network: blocks, peers, latencies, forks, propagation.

### ✓ Identify  
Detect patterns correlated with attacks:
- chain reorg attempts  
- eclipse attacks  
- sudden miner dominance  
- timestamp manipulation  
- hashpower anomalies  
- low-entropy block sequences  
- suspicious geographic clustering  

### ✓ Signal  
Emit **risk scores** and **structured signals** to DQSN v3 and ADN v3.

### ✓ Never interfere with consensus  
Sentinel is **external**. Zero consensus impact.

---

## 🧠 Threat Model

Sentinel evaluates threats across five planes:

1. **Entropy Plane** — randomness quality, difficulty adjustments, timestamp divergence  
2. **Topology Plane** — peer distribution, clustering, asynchrony  
3. **Hashrate Plane** — dominance, sudden power shifts  
4. **Fork Plane** — fork depth, competitive chain behavior  
5. **Propagation Plane** — latency, bottlenecks, geographic imbalance  

Each plane contributes to a **multi-factor risk vector**.

---

## 📡 Data Flow Overview

```
[Network Activity]
        ↓
[Collectors]
        ↓
[Raw Telemetry]
        ↓
[Analytics Engines]
        ↓
[Threat Scores]
        ↓
[Shield Contract v3 Gate]
        ↓
[DQSN v3 / ADN v3 / Adaptive Core]
```

---

## 🛡️ Security Philosophy

1. **Zero Consensus Influence** — observes, never rules  
2. **Explainable Detection** — no black-box authority  
3. **Multi-source Validation** — no single metric decides  
4. **Fail-Closed by Design** — invalid input → `ERROR`  
5. **Deterministic & Auditable** — reproducible outputs  
6. **Signal, Not Authority** — higher layers decide

---

## ⚙️ Code Status

Sentinel AI implements:

- Shield Contract v3 enforcement
- Deterministic evaluation pipeline
- Fail-closed validation
- v2 → v3 compatibility adapter
- Regression locks preventing behavior drift
- CI pipeline with security-focused tests

This repository is **v3-complete and integration-ready**.

---

## 🧪 Tests

The test suite enforces:

- Contract version gating
- Fail-closed behavior
- NaN / Infinity rejection
- Unknown schema rejection
- v2 ↔ v3 no-drift regression lock

Passing CI is a **security requirement**, not a formality.

---

## 🤝 Contribution Policy

See `CONTRIBUTING.md`.

Key rules:
- Improvements are welcome
- Contract weakening is rejected
- Sentinel must remain **external, read-only, and non-consensus**

---

## 📜 License

MIT License  
© 2026 **DarekDGB**

This architecture is free to use with mandatory attribution.
