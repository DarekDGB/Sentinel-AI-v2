# 🛡 Sentinel AI v2 --- Monitoring & Anomaly Detection Layer

### *DigiByte External Telemetry Layer (Layer 1 of the Monitoring Stack)*

## 1. Project Intent

Sentinel AI v2 is **not** a protocol-layer security system and does
**not** modify DigiByte consensus, cryptography, or core rules.\
It is an **external monitoring, analytics, and anomaly-detection layer**
designed to *observe* DigiByte node behaviour and surface useful risk
signals.

Its purpose is to help node operators and developers gain deeper
visibility into:

-   node health\
-   mempool behaviour\
-   chain stability\
-   reorg patterns\
-   oracle / price-feed deviations\
-   anomaly trends over time

All cryptographic upgrades and consensus decisions remain the
responsibility of the DigiByte Core (C++).\
Sentinel AI v2 only **reads, analyses, and reports**.

------------------------------------------------------------------------

## 2. Architecture Overview

Sentinel sits *outside* the node and consumes data via RPC/logs:

``` mermaid
flowchart LR
    A[DigiByte Core Node (C++)] -->|RPC / Logs / Telemetry| B[Sentinel AI v2 (Python)]
    B --> C[Analytics Engine]
    C --> D[Anomaly Flags / Logs / Dashboards]
```

------------------------------------------------------------------------

## 3. Key Modules

-   `telemetry_monitor.py` -- collects RPC data\
-   `anomaly_engine.py` -- detects unusual chain or mempool behaviour\
-   `adaptive_core_bridge.py` -- *optional* integration with Adaptive
    Layer for research\
-   `heartbeat.py` -- generates basic health metadata\
-   `log_utils.py` -- structured logging for dashboards

------------------------------------------------------------------------

## 4. Threat Model & Scope

### 🔍 **What Sentinel AI v2 DOES**

-   monitors node & chain behaviour\
-   analyses RPC/mempool/log data\
-   detects potential anomalies\
-   emits warning signals / logs\
-   supports dashboards & analytics

### 🚫 **What Sentinel AI v2 DOES NOT**

-   change protocol rules\
-   modify signature algorithms\
-   isolate wallets or nodes\
-   provide cryptographic protection\
-   stop attacks at the node level

This tool is **read-only** and focused entirely on visibility.

------------------------------------------------------------------------

## 5. Example Anomaly Signal API

``` python
report_reorg_anomaly(
    block_height=123456,
    score=0.92,
    details={"peers_observed": 8}
)
```

------------------------------------------------------------------------

## 6. Functional Monitoring Example

A simple block-progress monitor:

``` python
from sentinel_ai_v2.telemetry_monitor import check_block_progress

status = check_block_progress()
print(status)
```

If the chain appears stalled beyond a threshold, an anomaly flag is
logged.

------------------------------------------------------------------------

## 7. Heartbeat Metadata

``` python
from sentinel_ai_v2.heartbeat import shield_heartbeat
print(shield_heartbeat())
```

Outputs general diagnostic information (version, timestamps, last
checks).

------------------------------------------------------------------------

## 8. Current Functional Coverage

-   [x] Basic telemetry structure\
-   [x] Heartbeat metadata output\
-   [x] Initial anomaly-signal API\
-   [ ] Block-progress anomaly detector\
-   [ ] Mempool deviation detector\
-   [ ] Chain-health metrics\
-   [ ] Price-feed deviation checker

------------------------------------------------------------------------

## 9. Safety Properties

-   External, non-intrusive architecture\
-   Read-only interaction with the node\
-   Optional integration with Adaptive Layer\
-   Modular, test-friendly design

------------------------------------------------------------------------

## 10. License

MIT License -- free to use, modify, and distribute.

------------------------------------------------------------------------

## 11. Author

Created by **Darek (@Darek_DGB)**\
Visionary architect of the DigiByte Monitoring Stack.
