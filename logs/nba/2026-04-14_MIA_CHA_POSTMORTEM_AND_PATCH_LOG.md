# NBA Postmortem + Patch Log
## MIA @ CHA — 2026-04-14

### RESULT: ❌ Portfolio Loss (2/3 across all cards)

---

## 🔴 MPZ CLASSIFICATION

- PRIMARY: SINGLE_LEG_CONCENTRATION_BURN
- SECONDARY:
  - OT_INFLATION_BURN
  - WING_UNDER_FRAGILITY_FAILURE
  - PORTFOLIO_CHOKE_LEG

---

## 📊 TRUE EDGE PERFORMANCE

- Unique props: 4  
- Correct: 3  
- Accuracy: **75%**  
- Outcome: **-100% ROI (structure failure)**  

---

## 🎯 FAILURE POINT

**Andrew Wiggins UNDER 4.5 REB**

- Final: 7 rebounds  
- Minutes: 42  
- OREB: 2  
- Game: OT, 1-possession  

### Why it failed:
1. OT inflated rebound volume  
2. High possession environment (216 FGA)  
3. Offensive rebound spike  
4. Minutes expansion (no bench suppression)  

---

## 🧠 WHAT THE MODEL GOT RIGHT

- Ball UNDER → ✅
- Miller UNDER → ✅
- Diabate OVER → ✅ (14 rebounds, dominant)

👉 Core read was STRONG

---

## ❌ WHAT FAILED

> **Exposure architecture**

- Same fragile leg used across multiple cards  
- Turned 1 miss → total portfolio loss  

---

## 🔧 PATCHES ACTIVATED

### 1. WING_UNDER_FRAGILITY_GATE
- Blocks thin rebound unders (4.5 / 5.5) in:
  - close games
  - high rebound environments
  - OT-risk spots

---

### 2. CARD_CORRELATION_WARNING
- Prevents repeating same leg across cards  
- Stops portfolio choke scenarios  

---

### 3. OT_SENSITIVITY_OVERLAY
- Applies penalty to unders in:
  - tight spreads
  - high possession games
  - high OREB environments  

---

### 4. PORTFOLIO_DEPENDENCY_CHECK
- Blocks cards if:
  - same player/market reused
  - >1 fragile leg per card  

---

## 🏁 FINAL TAKEAWAY

> **Edge detection = WINNING**  
> **Edge distribution = LOSING**

This is a **structure leak, not a model leak**

---

## 📌 SYSTEM STATUS

- MPZ_TAGGED ✅  
- PATCH_APPLIED ✅  
- READY_FOR_NEXT_SLATE ✅