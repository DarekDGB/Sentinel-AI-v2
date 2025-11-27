# 🛡 Sentinel AI v2 — Technical Documentation  
### Quantum-Resistant Detection Layer (Layer 1 of 5)

## 1. Purpose  
Sentinel AI v2 is the **detection layer** of the DigiByte Quantum Shield.  
It monitors blockchain behaviour, generates structured ThreatPackets, emits feedback signals, and integrates optionally with the Adaptive Core v2 without creating hard dependencies.

## 2. Architecture Overview  
```
┌──────────────────────────────┐
│   Sentinel AI v2 (Detection) │
└──────────────┬───────────────┘
               │ ThreatPacket
               ▼
┌──────────────────────────────┐
│ Adaptive Core v2 (Learning)  │
└──────────────┬───────────────┘
               │ Immune Report
               ▼
         Heartbeat Output
```

## 3. Key Modules  
- `adaptive_core_bridge.py` – optional interface to Adaptive Core  
- `adaptive_hooks.py` – converts detections to ThreatPackets  
- `feedback_hooks.py` – sends TP/FP/missed feedback  
- `heartbeat.py` – retrieves immune state + metadata  

## 4. Threat Signal API  
```python
report_reorg_anomaly_to_adaptive(
    block_height=123456,
    score=0.92,
    details={"peers": 8}
)
```

## 5. Feedback API  
```python
send_feedback_to_adaptive(
    layer="sentinel_ai_v2",
    event_id="abc123",
    feedback="TRUE_POSITIVE"
)
```

## 6. Heartbeat  
```python
from sentinel_ai_v2.heartbeat import shield_heartbeat
print(shield_heartbeat())
```

## 7. Safety Properties  
- Fully optional integration  
- No crashes if Adaptive Core not installed  
- 100% test-safe  
- Modular, clean, professional
