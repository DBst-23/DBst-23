# NBA Postmortem — MIA @ CHA Rebound Cards

**Date:** 2026-04-14  
**Game:** Miami Heat @ Charlotte Hornets  
**Final:** Hornets 127, Heat 126 (OT)  
**Market Focus:** Rebounds  
**Postmortem Type:** Pregame prop card review

---

## Logged Cards

### Card A — 3 Pick Champions (Late card)
- **LaMelo Ball UNDER 5.5 rebounds** ✅
- **Brandon Miller UNDER 5.5 rebounds** ✅
- **Andrew Wiggins UNDER 4.5 rebounds** ❌
- **Stake:** $10.00
- **Boosted payout shown:** $64.70
- **Result:** Loss
- **Card hit rate:** 2/3

### Card B — 3 Pick Card
- **Brandon Miller UNDER 5.5 rebounds** ✅
- **LaMelo Ball UNDER 5.5 rebounds** ✅
- **Andrew Wiggins UNDER 4.5 rebounds** ❌
- **Stake:** $5.50
- **Potential payout:** $23.37
- **Odds shown:** +325
- **Result:** Loss
- **Card hit rate:** 2/3

### Card C — 3 Pick Card
- **LaMelo Ball UNDER 5.5 rebounds** ✅
- **Andrew Wiggins UNDER 4.5 rebounds** ❌
- **Moussa Diabate OVER 8.5 rebounds** ✅
- **Stake:** $10.00
- **Potential payout:** $32.18
- **Odds shown:** +222
- **Result:** Loss
- **Card hit rate:** 2/3

---

## Final Results by Leg

### 1) LaMelo Ball UNDER 5.5 rebounds — **WIN**
- **Final rebounds:** 5
- **Needed:** 5 or fewer
- **Margin:** Cleared by 0.5

### 2) Brandon Miller UNDER 5.5 rebounds — **WIN**
- **Final rebounds:** 5
- **Needed:** 5 or fewer
- **Margin:** Cleared by 0.5

### 3) Andrew Wiggins UNDER 4.5 rebounds — **LOSS**
- **Final rebounds:** 7
- **Needed:** 4 or fewer
- **Miss margin:** 2.5 rebounds

### 4) Moussa Diabate OVER 8.5 rebounds — **WIN**
- **Final rebounds:** 14
- **Needed:** 9 or more
- **Margin:** Cleared by 5.5

---

## Game Context

### Final team stats
- **Miami rebounds:** 48 total, 12 offensive
- **Charlotte rebounds:** 54 total, 17 offensive
- **Charlotte second-chance points:** 25
- **Miami second-chance points:** 20
- **Charlotte field goal attempts:** 113
- **Miami field goal attempts:** 103

### Rotation / overtime effects
- Game went to **overtime**, which inflated rebound opportunity volume.
- Heavy-minute players gained extra accumulation windows.
- Charlotte’s 113 FGA and 17 OREB created strong sustained rebound volume across the game.

---

## Why Each Read Won or Lost

### LaMelo Ball UNDER 5.5 rebounds ✅
**Pregame thesis:** Ball rebound under due to backcourt role, lower interior responsibility, and stronger frontcourt rebound claim from Diabate/Bridges/Knueppel mix.

**What happened:**
- Ball finished with **5 rebounds in 40 minutes**.
- Despite OT, he still stayed under.
- His game tilted toward **usage and creation** instead of glass control:
  - **30 points, 10 assists, 31 FGA**
- Rebound share stayed concentrated elsewhere.

**Postmortem tag:**
- `HIT_REGISTERED`
- `ROLE_HELD_STABLE`
- `USAGE_OVER_REBOUND_PATH_CONFIRMED`

---

### Brandon Miller UNDER 5.5 rebounds ✅
**Pregame thesis:** Miller under was driven by expected wing shot volume and scoring role, with rebound competition from Diabate, Bridges, Knueppel, and bench bigs.

**What happened:**
- Miller finished with **5 rebounds in 37 minutes**.
- Another narrow but clean win.
- He remained mostly in a scoring/spacing role:
  - **23 points, 17 FGA, 10 3PA**
- He did not turn into a primary cleanup rebounder.

**Postmortem tag:**
- `HIT_REGISTERED`
- `WING_UNDER_HELD`
- `SHOT_PROFILE_MATCHED`

---

### Andrew Wiggins UNDER 4.5 rebounds ❌
**Pregame thesis:** Wiggins under was based on modest recent rebound rates, lineup competition, and expectation that Miami’s bigs plus guards would absorb more rebound share.

**What happened:**
- Wiggins finished with **7 rebounds in 42 minutes**.
- The leg failed decisively, not by a hook.
- He logged elevated floor time in a highly competitive OT environment and picked up **2 offensive rebounds**, which hurt the under immediately.
- Miami’s long-possession, high-volume game and extra OT rebound chances pushed him beyond the number.

**Failure factors:**
1. **Minutes inflation** — 42 minutes gave him a larger accumulation runway than a normal median game.
2. **OT environment** — extra possessions materially damaged thin rebound unders.
3. **Offensive rebound variance** — 2 OREB is a direct under-killer for a wing at 4.5.
4. **Game competitiveness** kept core players on the floor deep.

**Postmortem tag:**
- `MISS_REGISTERED`
- `OT_INFLATION_BURN`
- `WING_OREB_SPIKE`
- `MINUTES_EXPANSION_FAILURE`

---

### Moussa Diabate OVER 8.5 rebounds ✅
**Pregame thesis:** Diabate over was the strongest structural rebound angle because of role, interior responsibility, and matchup volume.

**What happened:**
- Diabate finished with **14 rebounds in 36 minutes**.
- Massive clear.
- He dominated the glass with **8 offensive rebounds**, validating the center rebound edge call.
- Charlotte’s team-level rebound environment was strong all night.

**Postmortem tag:**
- `HIT_REGISTERED`
- `CENTER_EDGE_CONFIRMED`
- `OREB_DOMINANCE`
- `MATCHUP_VOLUME_VALIDATED`

---

## Card-Level Review

### Overall card performance
- All three invested cards finished **2/3**.
- The common failure point was **Andrew Wiggins UNDER 4.5 rebounds**.
- This means the portfolio read was directionally strong overall, but correlation to one fragile wing-under leg caused full-card loss.

### Key lesson
The board read on **Ball under**, **Miller under**, and **Diabate over** was solid. The weak point was pressing **Wiggins under** into multiple cards.

This was not a broad read failure. It was a **single-leg concentration failure**.

---

## SharpEdge Diagnostic Summary

### What the model got right
- Correctly identified **Charlotte center rebound strength**.
- Correctly identified that **Ball and Miller were not elite rebound roles** in this setup.
- Correctly leaned into **Diabate’s glass advantage**.

### What failed
- Wing under on Wiggins did not account enough for:
  - overtime probability cost,
  - close-game minutes extension,
  - offensive rebound volatility,
  - and rebound opportunity inflation in a 229-shot environment.

---

## Patch Recommendation

### Add / reinforce the following rule
**WING_UNDER_FRAGILITY_GATE**
- Downgrade wing rebound unders when all of the following are present:
  1. projected competitive spread / tight game script,
  2. thin line (4.5 or 5.5),
  3. player can collect opportunistic OREB,
  4. high rebound-volume environment,
  5. overtime risk materially damages under EV.

### Secondary rule
**CARD_CORRELATION_WARNING**
- When one thin prop appears in multiple cards, label it as a repeated dependency risk.
- Prevent one fragile leg from becoming a multi-card portfolio choke point.

---

## Final Grading

### Leg grades
- **LaMelo Ball U5.5 REB:** A
- **Brandon Miller U5.5 REB:** A-
- **Moussa Diabate O8.5 REB:** A+
- **Andrew Wiggins U4.5 REB:** D

### Portfolio grade
- **Read quality:** B+
- **Execution quality:** B-
- **Risk concentration:** C+

---

## MPZ Tracker Notes
- **Loss classification:** `Single-Leg Concentration Burn`
- **Variance tag:** `OT_INFLATION_BURN`
- **Structural note:** Good matchup read, weak diversification across cards.
- **Action item:** Reduce repeated exposure to one fragile wing rebound under in multi-card builds.

---

## Logbook Status
**Filed as:** `NBA_POSTMORTEM_2026-04-14_MIA_CHA_REBOUND_CARDS`  
**Status:** Finalized  
**Ready for:** Backtest_Logbook / MPZ Tracker ingestion
