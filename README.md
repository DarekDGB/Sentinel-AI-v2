# 🛡️ DGB Sentinel AI (Shield Contract v3)

[![CI](https://github.com/DarekDGB/DGB-Sentinel-AI/actions/workflows/tests.yml/badge.svg)](https://github.com/DarekDGB/DGB-Sentinel-AI/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Contract](https://img.shields.io/badge/Shield%20Contract-v3-black.svg)](docs/CONTRACT.md)
[![Status](https://img.shields.io/badge/status-v3%20contract%20enforced-success.svg)](#)

### DigiByte Quantum Shield — External Telemetry Analysis & Threat Signal Generation
**Architecture by @DarekDGB — MIT Licensed**

---

## Overview

**Sentinel AI** is the **external, non-consensus telemetry analysis layer** of the DigiByte Quantum Shield.

It ingests **read-only signals** (telemetry, observations, monitors), evaluates them under **Shield Contract v3**
rules, and emits **deterministic threat signals**.

**Sentinel AI does not and must not:**
- change consensus
- sign transactions
- execute wallet actions
- gain authority over funds

> Glass-box rule: Sentinel can **observe and report**, never **execute or override**.

---

## Shield Contract v3 (what it guarantees)

Shield Contract v3 enforces:
- **Deterministic evaluation** (reproducible results)
- **Versioned contract semantics**
- **Fail-closed behavior** (unknown / malformed inputs are rejected)
- **Stable reason codes + hashing anchors** for auditability

Contract and rationale:
- `docs/CONTRACT.md`
- `docs/ARCHITECTURE.md`
- Upgrade plan: `docs/upgrade/SENTINEL_AI_V3_UPGRADE_PLAN.md`

---

## Code layout

- Source: `src/sentinel_ai_v2/`
- Contract helpers:
  - `src/sentinel_ai_v2/contracts/v3_hash.py`
  - `src/sentinel_ai_v2/contracts/v3_reason_codes.py`
- Wrapper / monitor tooling: `src/sentinel_ai_v2/wrapper/`
- Examples: `examples/`
- Tests: `tests/`

> Note: the internal Python package name remains `sentinel_ai_v2` for compatibility, while the repo enforces **v3 contract behavior**.

---

## Install (developer)

This repo is packaged via `pyproject.toml`.

```bash
python -m pip install -U pip
pip install -e .
pip install pytest
```

---

## Run tests

```bash
pytest -q
```

CI runs tests across multiple Python versions and treats failures as contract breakage.

---

## Documentation index

- `docs/INDEX.md` (starting point)
- `docs/CONTRACT.md` (Shield Contract v3)
- `docs/ARCHITECTURE.md` (how Sentinel fits the Shield)

Legacy references are kept in `docs/legacy/` for historical context only.

---

## Security

Please see `SECURITY.md` for responsible vulnerability disclosure guidance.

---

## License

MIT License  
© 2026 **DarekDGB**
