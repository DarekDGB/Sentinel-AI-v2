# Contributing to Sentinel AI v2

Sentinel AI v2 is a **reference architecture** and implementation skeleton for
DigiByte’s external telemetry and anomaly-detection layer.

It is part of the broader **DigiByte Quantum Shield & Adamantine** ecosystem and
is designed to stay:

- External to consensus  
- Transparent  
- Auditable  
- Focused on **monitoring, scoring, and signalling**, not on forcing protocol changes.

---

## What kind of contributions are welcome?

✅ **Improvements and extensions**, for example:

- Better feature engineering or risk scoring logic  
- Additional telemetry sources (peers, latency, geography, etc.)  
- Performance / reliability improvements in watchers and monitors  
- Extra tests, attack simulations, and documentation  
- Integrations with other DigiByte tools (nodes, dashboards, alerting stacks)

✅ **Bug fixes**, refactors, or clarity improvements that keep the design intact.

---

## What is **not** accepted?

❌ Changes that **remove or weaken** core architectural ideas, such as:

- Removing Sentinel’s role as an external telemetry / monitoring layer  
- Downgrading or deleting detection logic  
- Turning Sentinel into a consensus-modifying component  
- Replacing the DigiByte-focused model with something unrelated

If a change **dismantles the architecture** instead of improving it, it will be rejected.

---

## Design Principles

Contributions should respect the following principles:

- **No consensus changes** – Sentinel observes, it does not rule.  
- **Security first** – favour correctness and safety over micro-optimisations.  
- **Auditability** – keep logic understandable and reviewable.  
- **Modularity** – new functionality should be in clear, focused modules.  

---

## Code Review Expectations

The original author (@DarekDGB) acts as the **architect** of the system.

- Contributors and DigiByte developers are expected to review **technical details**.  
- Architectural review focuses on **direction and alignment with the shield vision**, not line-by-line code checking.

By opening a pull request, you confirm that:

- Tests pass locally (where applicable).  
- You have not removed or weakened core architecture.  
- Your change is documented where appropriate (README/docs).

---

## License

By contributing, you agree that your contributions are licensed under the
same MIT License as the rest of the project.
