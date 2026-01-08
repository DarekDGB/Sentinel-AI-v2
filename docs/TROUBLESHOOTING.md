# Troubleshooting — Sentinel AI v3

This guide helps diagnose common integration and validation errors when working
with **Sentinel AI (Shield Contract v3)**.

---

## General Rule

If Sentinel returns:

- `decision = ERROR`
- `meta.fail_closed = true`

**Upstream systems MUST treat this as BLOCK.**

Sentinel never attempts to repair malformed input.

---

## Common Errors

### SNTL_ERROR_UNKNOWN_TOP_LEVEL_KEY

**Cause:**  
Your request contains a field not defined by Shield Contract v3.

**Allowed top-level keys:**
- `contract_version`
- `component`
- `request_id`
- `telemetry`
- `constraints`

❌ Wrong:
```json
{
  "contract_version": 3,
  "component": "sentinel",
  "request_id": "x1",
  "telemetry": {},
  "extra": "not allowed"
}
```

✅ Correct:
```json
{
  "contract_version": 3,
  "component": "sentinel",
  "request_id": "x1",
  "telemetry": {}
}
```

---

### SNTL_ERROR_SCHEMA_VERSION

**Cause:**  
`contract_version` is missing or not equal to `3`.

**Fix:**  
Always send:
```json
"contract_version": 3
```

---

### SNTL_ERROR_BAD_NUMBER

**Cause:**  
Telemetry contains `NaN`, `Infinity`, or non-finite numbers.

**Fix:**  
Sanitize telemetry before sending. Sentinel rejects unsafe numbers.

---

### SNTL_ERROR_TELEMETRY_TOO_LARGE

**Cause:**  
Telemetry exceeds size or node limits.

**Fix:**  
Reduce payload size or depth. Sentinel enforces hard limits to prevent DoS.

---

## Determinism Issues

### “Why is my context_hash different?”

Sentinel hashes **exact input as-is**.

Differences may come from:
- Unicode normalization (NFC vs NFD)
- Key ordering before canonicalization
- Floating point representation

**Recommendation:**  
Normalize input to NFC before sending.

```python
import unicodedata
payload = unicodedata.normalize("NFC", payload)
```

---

## Debug Checklist

- [ ] contract_version == 3
- [ ] component == "sentinel"
- [ ] No extra top-level keys
- [ ] Telemetry JSON-serializable
- [ ] No NaN / Infinity
- [ ] Treat ERROR as BLOCK

---

If issues persist, review:
- `docs/CONTRACT.md`
- `docs/ARCHITECTURE.md`
