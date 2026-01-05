# 🛡️ Sentinel AI (Shield Contract v3)
### *DigiByte Quantum Shield — External Telemetry Analysis & Threat Signal Generation Layer*  
**Architecture by @DarekDGB — MIT Licensed**

---

## 🚀 Purpose

**Sentinel AI** is the *external, non-consensus* **telemetry analysis and threat-signal generation** component of the **DigiByte Quantum Shield**.

It operates under **Shield Contract v3**, enforcing strict versioning, deterministic evaluation, and fail-closed
semantics. Sentinel **analyzes telemetry inputs**, evaluates threat patterns, and emits **structured, deterministic
security signals**, but **never interferes with consensus, signing, execution, or wallet behavior**.

Sentinel is designed as a **reference-grade security component**, suitable for:
- upstream telemetry producers (nodes, monitors, collectors)
- downstream consumers (DQSN v3, ADN v3, Adaptive Core)
- independent review by DigiByte Core developers and security engineers

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

Sentinel AI is a **Shield Contract v3–compliant component**.

### Core guarantees

- **Contract v3 enforced**
  - `contract_version == 3` is the outermost gate
  - Invalid, unknown, or malformed input fails closed
- **Read-only**
  - No signing
  - No execution
  - No state mutation
- **Deterministic**
  - Same input → same output → same `context_hash`
- **Fail-closed**
  - NaN / Infinity values
  - Unknown schemas
  - Invalid versions → `ERROR`
- **Single authority**
  - All evaluation flows through the v3 contract gate

Sentinel AI does **not**:
- alter consensus
- modify blockchain state
- hold private keys
- replace DigiByte Core or node software

---

## 🔥 Position in the DigiByte Quantum Shield (5-Layer Model)

> **Important:** Sentinel does **analysis**, not transport and not enforcement.

```
        ┌────────────────────────────────────────┐
        │           Guardian Wallet              │
        │  User-side rules & policy enforcement  │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        Quantum Wallet Guard (QWG)      │
        │  Signature safety & cryptographic gate │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        ADN v3 — Decision Layer         │
        │  Policy evaluation & defensive intent │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        DQSN v3 — Signal Network        │
        │  Aggregation, transport, normalization│
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        Sentinel AI (THIS REPO)         │
        │  Telemetry analysis & threat scoring  │
        └────────────────────────────────────────┘
```

Sentinel AI is the **analytical engine** of the Quantum Shield —  
it **produces signals**, it does **not** route or enforce them.

---

## 🎯 Core Mission

### ✓ Analyze  
Process structured telemetry inputs originating from nodes, monitors, or collectors.

### ✓ Identify  
Detect patterns correlated with network-level threats, including:
- chain reorg attempts  
- eclipse or isolation patterns  
- sudden miner dominance shifts  
- timestamp manipulation  
- hashpower anomalies  
- entropy degradation  
- suspicious geographic or topological clustering  

### ✓ Emit signals  
Produce **deterministic threat scores and structured signals** suitable for:
- aggregation by DQSN v3
- evaluation by ADN v3
- consumption by Adaptive Core logic

### ✓ Never interfere with consensus  
Sentinel is **external** and **advisory only**.

---

## 🧠 Threat Model

Sentinel evaluates threats across multiple analytical planes:

1. **Entropy Plane** — randomness quality, difficulty behavior, timestamp variance  
2. **Topology Plane** — peer distribution, clustering, network asymmetry  
3. **Hashrate Plane** — dominance detection, sudden power shifts  
4. **Fork Plane** — competing chains, fork depth, persistence  
5. **Propagation Plane** — latency patterns, bottlenecks, imbalance  

Each plane contributes to a **multi-factor, explainable risk vector**.

No single metric produces authority.

---

## 📡 Data Flow Overview

```
[Telemetry Sources]
        ↓
[Structured Inputs]
        ↓
[Sentinel Analysis Engines]
        ↓
[Deterministic Threat Scores]
        ↓
[Shield Contract v3 Gate]
        ↓
[DQSN v3 → ADN v3 → Adaptive Core]
```

---

## 🛡️ Security Philosophy

1. **Zero Consensus Influence** — observe and analyze only  
2. **Explainable Detection** — no black-box authority  
3. **Multi-signal Evaluation** — no single metric decides  
4. **Fail-Closed by Design** — invalid input → `ERROR`  
5. **Deterministic & Auditable** — reproducible outputs  
6. **Signal, Not Authority** — decisions belong upstream

---

## ⚙️ Code Status

Sentinel AI implements:

- Shield Contract v3 enforcement
- Deterministic evaluation pipeline
- Fail-closed validation logic
- v2 → v3 compatibility adapter
- Regression locks preventing behavioral drift
- Security-focused test suite

> CI workflows exist and are evolving; **test correctness is enforced by code and tests**, not by badges.

This repository is **v3-aligned and integration-ready**.

---

## 🧪 Tests

The test suite enforces:

- Contract version gating
- Fail-closed behavior
- NaN / Infinity rejection
- Unknown schema rejection
- v2 ↔ v3 no-drift guarantees

Tests are **security artifacts**, not optional checks.

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
