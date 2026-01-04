# 🛡️ Sentinel AI v3
### *DigiByte Quantum Shield — External Telemetry, Threat Modeling & Anomaly Detection Layer*  
**Architecture by @DarekDGB — MIT Licensed**

---

## 🚀 Purpose

**Sentinel AI v3** is the *external, non-consensus* security monitoring layer of the **DigiByte Quantum Shield**.

It operates under **Shield Contract v3**, enforcing strict versioning, fail-closed semantics, and deterministic outputs.
Sentinel observes, analyzes, correlates, and surfaces emergent threats to the DigiByte network, but **never interferes
with consensus, signing, or execution**.

Sentinel is designed as a **reference-grade security component**, suitable for integration into higher shield layers
(DQSN, ADN, Adaptive Core) and for independent review by DigiByte Core developers and security researchers.

---

## 🛡️ Sentinel AI — Shield Contract v3

Sentinel AI is now a **fully hardened Shield Contract v3 component**.

### Core guarantees

- **Contract v3 enforced**
  - `contract_version == 3` is the outermost gate
  - Invalid or unknown inputs fail closed
- **Read-only**
  - No signing, no execution, no state mutation
- **Deterministic**
  - Same input → same output → same `context_hash`
- **Fail-closed**
  - Unknown schema, NaN/Infinity values, oversized telemetry → `ERROR`
- **Single authority**
  - All evaluation flows through the v3 contract gate

Sentinel AI **does not**:
- alter consensus
- modify blockchain state
- hold keys
- replace DigiByte Core or node software

---

# 🔥 Position in the Quantum Shield (5-Layer Model)

```
        ┌────────────────────────────────────────┐
        │           Guardian Wallet             │
        │  (User-Side Defence, Rules Engine)    │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        Quantum Wallet Guard (QWG)      │
        │ Filters, PQC Safety, Behavioural Logic │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │        ADN v3 — Active Defence         │
        │  Network Response, Isolation, Tactics  │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │      Sentinel AI v3 (THIS REPO)        │
        │  Telemetry, Threat Intel, AI Scoring   │
        └────────────────────────────────────────┘
                        ▲
                        │
        ┌────────────────────────────────────────┐
        │  DQSN v3 — DigiByte Quantum Shield Net │
        │  Entropy, Node Health, UTXO Patterns   │
        └────────────────────────────────────────┘
```

Sentinel is the **eyes and ears** of the Quantum Shield.

---

# 🎯 Core Mission

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

# 🧠 Threat Model (Formal)

Sentinel evaluates threats across five planes:

1. **Entropy Plane** — randomness quality, difficulty adjustments, timestamp divergence  
2. **Topology Plane** — peer distribution, clustering, asynchrony  
3. **Hashrate Plane** — dominance, sudden power shifts  
4. **Fork Plane** — fork depth, competitive chain behavior  
5. **Propagation Plane** — latency, bottlenecks, geographic imbalance  

Each plane contributes to a **multi-factor risk vector**.

---

# 🧩 Internal Architecture (Reference)

```
sentinel_ai_v2/
│
├── collectors/
├── analytics/
├── outputs/
└── utils/
```

This repository provides a **reference architecture**.  
Concrete implementations may extend modules, but **contract rules and read-only guarantees must remain intact**.

---

# 📡 Data Flow Overview

```
[Attacker → Network Activity]
          ↓
   (Collectors)
          ↓
  [Raw Telemetry Streams]
          ↓
   (Analytics Engines)
          ↓
   [Threat Scores + Vectors]
          ↓
   (Shield Contract v3 Gate)
          ↓
 [DQSN v3 / ADN v3 / Adaptive Core]
```

---

# 🛡️ Security Philosophy

Sentinel follows six principles:

1. **Zero Consensus Influence**  
   Observes—never rules.

2. **Explainable Detection**  
   AI assists but never becomes a black box.

3. **Multi‑Source Validation**  
   No single metric determines a threat.

4. **Fail‑Closed by Design**  
   Invalid input results in `ERROR`, never silent acceptance.

5. **Deterministic & Auditable**  
   Outputs are reproducible and hash-addressable.

6. **Signal, Not Authority**  
   Sentinel informs; higher layers decide.

---

# ⚙️ Code Status

Sentinel AI v3 includes:

- Shield Contract v3 enforcement
- Deterministic evaluation pipeline
- Fail-closed validation and hardening
- v2 → v3 compatibility adapter
- Regression locks preventing behavior drift
- CI pipeline with security-focused tests

This repository is **v3-complete and integration-ready**.

---

# 🧪 Tests

The test suite enforces:

- Contract version gating
- Fail-closed behavior
- NaN / Infinity rejection
- Unknown schema rejection
- v2 ↔ v3 no-drift regression lock

Passing CI is a **security requirement**, not a formality.

---

# 🤝 Contribution Policy

Please see `CONTRIBUTING.md`.

Key rules:
- Improvements are welcome
- Contract weakening is rejected
- Sentinel must always remain **external, read-only, and non-consensus**

---

# 📜 License

MIT License  
© 2026 **DarekDGB**

This architecture is free to use with mandatory attribution.
