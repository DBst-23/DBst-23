# NBA Patch Note — TEMPLATE

**Patch ID:** NBA_PATCH_YYYYMMDD_SHORTNAME  
**Created:** YYYY-MM-DD  
**Triggered By:** Game / Postmortem / Backtest / LiveFlow  
**Model Area:** Pace / Total / Rebound / Rotation / Market / Injury / Volatility  
**Status:** Proposed / Active / Deprecated  

---

## Problem

Describe the model miss, instability, or regression.

---

## Evidence

| Source | Signal | Impact |
|---|---|---|
|  |  |  |

---

## Patch Logic

```yaml
trigger:
  condition: 
  threshold: 

action:
  modifier: 
  cap: 
  confidence_adjustment: 
```

---

## Expected Effect

| Market | Expected Impact |
|---|---|
| Full Game Total |  |
| Team Total |  |
| Spread |  |
| Rebounds |  |

---

## Validation Plan

- Backtest on prior similar games.
- Run with patch ON/OFF.
- Compare mean, median, probability, and edge tier.
- Track hit/miss after next live use.
