# LAL @ OKC Postmortem — 2026-04-02

## Final Score
- **Oklahoma City Thunder 139**
- **Los Angeles Lakers 96**

## Closing Context
- **Close:** OKC favored heavily and validated it with a wire-to-wire blowout
- **Final rebound margin:** OKC **50**, LAL **38**
- **Offensive rebounds:** OKC **13**, LAL **8**
- **Game script:** extreme blowout, distorted minutes, rebound share, and rotation stability

## Invested Plays
### 1. LeBron James — Over 5.5 Rebounds
- **Result:** ✅ HIT
- **Final:** 6 rebounds in 26 minutes
- **Pre-game model read:** modest but playable over driven by stable rebound-chance volume
- **Postmortem note:** got there despite only 26 minutes because his base rebound role held.
- **Postmortem tags:** `HIT_REGISTERED`, `ROLE_STABLE_EDGE`, `BLOWOUT_RESILIENT_HIT`

### 2. Isaiah Hartenstein — Over 8.5 Rebounds
- **Result:** ❌ MISS
- **Final:** 6 rebounds in 20 minutes
- **Pre-game model read:** solid over based on rebound-chance rate, per-minute board profile, and matchup support
- **Failure mode:** game got out of hand, minutes were cut, and rebound opportunity distribution widened across the OKC bench and frontcourt rotation.
- **Postmortem tags:** `MISS_REGISTERED`, `MINUTES_SHARE_FAILURE`, `BLOWOUT_MINUTES_COLLAPSE`, `BENCH_REBOUND_DISTRIBUTION`

## Box Score Notes
- LeBron: **6 rebounds** in **26 minutes**
- Hartenstein: **6 rebounds** in **20 minutes** with **4 offensive rebounds**
- Jalen Williams: **9 rebounds**
- Shai Gilgeous-Alexander: **7 rebounds**
- Jaylin Williams: **6 rebounds** off bench
- Cason Wallace: **5 rebounds** off bench
- OKC team assists: **32**
- LAL turnovers: **18**
- OKC won points in paint **64–50** and second-chance points **18–3**

## Game Flow / Rebounding Notes
- This game was effectively broken by blowout script.
- Hartenstein’s per-minute rebound profile was not wrong, but the **minutes floor was wrong** for an over at 8.5.
- Once OKC gained total control, the rotation spread rebounds into secondary pieces rather than forcing starter volume continuation.
- LeBron survived because his line was lower and he reached 6 before the reduced-minute environment fully killed the projection window.

## Model Verdict
This was another example of **correct stronger leg / failed thinner support leg**, but here the main killer was **blowout and minutes truncation** rather than pure matchup misread.

### Correct Read
- LeBron’s over remained viable and cleared even in a poor game environment.

### Incorrect / Fragile Read
- Hartenstein over 8.5 was too exposed to blowout volatility for a two-leg pairing.
- The projection needed a stronger blowout minutes penalty before being paired.

## Actionable Patch
### Blowout Over Rule
Do **not** pair rebound overs on starters with lines above 8.5 unless one of the following is true:
- projected spread/game script keeps starter minutes stable
- player has a strong historical hit profile in sub-26 minute games
- rebound share remains highly concentrated even with bench rotation expansion

### New Detector Trigger
Add to NO BET ZONE DETECTOR:
- `BLOWOUT_OVEREXPOSURE_RISK`
- Trigger when starter rebound over depends on 28+ minutes and favorite has high blowout probability.

## Final Grading Summary
- **LeBron James O5.5 REB** → good hit, resilient to game script
- **Isaiah Hartenstein O8.5 REB** → miss driven by minutes/share collapse
- **Card verdict:** playable anchor + blowout-fragile second leg

## Registry Labels
- `ROLE_STABLE_EDGE`
- `BLOWOUT_RESILIENT_HIT`
- `MINUTES_SHARE_FAILURE`
- `BLOWOUT_MINUTES_COLLAPSE`
- `BENCH_REBOUND_DISTRIBUTION`
- `CARD_CONSTRUCTION_FAILURE`
