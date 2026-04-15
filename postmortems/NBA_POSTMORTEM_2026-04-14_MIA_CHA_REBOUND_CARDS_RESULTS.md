# NBA Postmortem — MIA @ CHA Rebound Cards Results

**Date:** 2026-04-14  
**Game:** Miami Heat @ Charlotte Hornets  
**Final:** Hornets 127, Heat 126 (OT)  
**Postmortem Focus:** Invested rebound cards and end-of-game failure analysis  
**Status:** Finalized

---

## 1. Invested Cards Logged

### Card A — Champions 3 Pick (Play-In Boost)
- LaMelo Ball **UNDER 5.5 REB** ✅
- Brandon Miller **UNDER 5.5 REB** ✅
- Andrew Wiggins **UNDER 4.5 REB** ❌
- **Stake:** $10.00
- **Boosted payout shown:** $64.70
- **Displayed multiplier:** 6.47x
- **Result:** Loss
- **Hit rate:** 2/3

### Card B — 3 Pick Card (+325)
- Brandon Miller **UNDER 5.5 REB** ✅
- LaMelo Ball **UNDER 5.5 REB** ✅
- Andrew Wiggins **UNDER 4.5 REB** ❌
- **Stake:** $5.50
- **Potential payout:** $23.37
- **Displayed odds:** +325
- **Result:** Loss
- **Hit rate:** 2/3

### Card C — 3 Pick Card (+222)
- LaMelo Ball **UNDER 5.5 REB** ✅
- Andrew Wiggins **UNDER 4.5 REB** ❌
- Moussa Diabate **OVER 8.5 REB** ✅
- **Stake:** $10.00
- **Potential payout:** $32.18
- **Displayed odds:** +222
- **Result:** Loss
- **Hit rate:** 2/3

---

## 2. Final Leg Results

### Winning legs
- **LaMelo Ball UNDER 5.5 rebounds** → **5 rebounds** ✅
- **Brandon Miller UNDER 5.5 rebounds** → **5 rebounds** ✅
- **Moussa Diabate OVER 8.5 rebounds** → **14 rebounds** ✅

### Losing leg
- **Andrew Wiggins UNDER 4.5 rebounds** → **7 rebounds** ❌

---

## 3. Portfolio Summary

### Raw read accuracy
- Total unique prop reads invested: **4**
- Correct reads: **3**
- Wrong reads: **1**
- **Unique read win rate:** **75.0%**

### Financial summary
- Total staked: **$25.50**
- Total returned: **$0.00**
- Net: **-$25.50**

### Core lesson
This was **not** a board-read collapse. This was a **single-leg concentration failure**. One repeated fragile leg — **Wiggins U4.5 REB** — killed every card.

---

## 4. Game Environment Review

### Final team rebound and opportunity profile
- **Miami:** 48 rebounds, 12 offensive
- **Charlotte:** 54 rebounds, 17 offensive
- **Charlotte field goal attempts:** 113
- **Miami field goal attempts:** 103
- **Charlotte second-chance points:** 25
- **Miami second-chance points:** 20
- **Game went to overtime**

### What that means
This was a **high-volume rebound environment**:
- 216 total FGA
- 29 combined offensive rebounds
- overtime added extra possession/rebound windows
- competitive game preserved heavy starter minutes

That environment is favorable for **center overs** and hostile to **thin wing unders**.

---

## 5. Player-by-Player Postmortem

### LaMelo Ball UNDER 5.5 REB — WIN ✅
**Final:** 5 rebounds in 40 minutes

#### Why it held
- Ball’s role stayed tilted toward **shot creation and playmaking**.
- He finished with **30 points, 10 assists**, and did not become a major cleanup rebounder.
- Charlotte’s rebound share stayed concentrated more heavily with **Diabate** and **Miles Bridges**, while Ball remained more perimeter/usage driven.
- Even with overtime, he still stayed under.

#### Tags
- `HIT_REGISTERED`
- `USAGE_OVER_REBOUND_PATH_CONFIRMED`
- `ROLE_HELD_STABLE`

---

### Brandon Miller UNDER 5.5 REB — WIN ✅
**Final:** 5 rebounds in 37 minutes

#### Why it held
- Miller remained a **shot-first scoring wing**:
  - 23 points
  - 17 FGA
  - 10 3PA
- Rebound competition around him stayed real with Diabate, Bridges, Knueppel, and bench big involvement.
- He landed exactly below the number despite solid minutes.

#### Tags
- `HIT_REGISTERED`
- `WING_UNDER_HELD`
- `SHOT_PROFILE_MATCHED`

---

### Moussa Diabate OVER 8.5 REB — WIN ✅
**Final:** 14 rebounds in 36 minutes

#### Why it smashed
- This was the strongest structural read on the board.
- Diabate completely owned the glass, especially with **8 offensive rebounds**.
- Charlotte’s center rebound environment and team rebound distribution fully supported the over thesis.
- High miss volume plus sustained interior activity created a ceiling game.

#### Tags
- `HIT_REGISTERED`
- `CENTER_EDGE_CONFIRMED`
- `OREB_DOMINANCE`
- `MATCHUP_VOLUME_VALIDATED`

---

### Andrew Wiggins UNDER 4.5 REB — LOSS ❌
**Final:** 7 rebounds in 42 minutes

#### Why it failed
This miss was the entire portfolio breaker.

##### Main causes
1. **Minutes expansion**
   - Wiggins logged **42 minutes**, far above a comfortable under environment.

2. **Overtime inflation**
   - Extra possessions damaged a thin wing under immediately.

3. **Offensive rebound variance**
   - He grabbed **2 offensive rebounds**, which is devastating for a 4.5 under.

4. **Competitive script**
   - Tight game meant core players never got natural minute suppression.

5. **Volume environment**
   - 216 total FGA and constant second-chance sequences increased random wing rebound opportunity.

#### Tags
- `MISS_REGISTERED`
- `OT_INFLATION_BURN`
- `WING_OREB_SPIKE`
- `MINUTES_EXPANSION_FAILURE`
- `PORTFOLIO_CHOKE_LEG`

---

## 6. Halftime Read vs Full-Game Outcome

### Halftime snapshot
At halftime:
- Wiggins had **3 rebounds**
- Ball had **1 rebound**
- Miller had **2 rebounds**
- Diabate had **4 rebounds**

### What changed in the second half / OT
- Ball under still held comfortably.
- Miller under still held by the narrow half-board margin.
- Diabate over accelerated with elite second-half and OT rebound accumulation.
- Wiggins under failed due to **late-game accumulation + OT + OREB variance**.

This means the board read stayed largely intact after halftime; the failure was still isolated to one prop type.

---

## 7. Model / Process Review

### What the model got right
- Correctly identified **Diabate over** as a structural edge.
- Correctly identified **LaMelo under** as non-primary rebound role.
- Correctly identified **Brandon Miller under** as a scoring-wing profile rather than dominant rebound role.

### What the model/process got wrong
- Underestimated the fragility of **Wiggins U4.5** in a tight-game, overtime-capable environment.
- Allowed the same fragile leg to be **reused across multiple cards**, converting one miss into a full portfolio wipe.

---

## 8. MPZ Tagging

### Official MPZ classification
- **Primary tag:** `SINGLE_LEG_CONCENTRATION_BURN`
- **Secondary tag:** `OT_INFLATION_BURN`
- **Subtype:** `WING_UNDER_FRAGILITY_FAILURE`

### Tracker interpretation
This loss belongs in the MPZ tracker as a **process loss**, not a broad model failure. The board contained profitable information, but the exposure map was poor.

---

## 9. Patch Recommendations

### Patch 1 — WING_UNDER_FRAGILITY_GATE
Do not full-weight wing rebound unders when all or most are present:
- line is **4.5 or 5.5**
- game projects competitive
- player can collect opportunistic OREB
- high total shot volume / rebound environment exists
- overtime risk meaningfully harms the under

### Patch 2 — CARD_CORRELATION_WARNING
If one prop appears in more than one card:
- flag it as a **repeated dependency**
- cap repeated-card exposure for fragile props
- especially avoid duplicating thin unders across multiple cards

### Patch 3 — OT_SENSITIVITY_OVERLAY
Thin unders on rebounds should receive a downgrade in games where:
- live spread remains tight,
- both teams are generating extended possessions,
- or second-chance rate is elevated.

---

## 10. Final Grades

### Per-leg grades
- **LaMelo Ball U5.5 REB:** A
- **Brandon Miller U5.5 REB:** A-
- **Moussa Diabate O8.5 REB:** A+
- **Andrew Wiggins U4.5 REB:** D

### Overall portfolio grades
- **Edge identification:** A-
- **Prop selection quality:** B+
- **Risk structuring:** C
- **Final execution:** C+

---

## 11. Strategic Takeaway

The important conclusion is this:

> **The read engine worked better than the bankroll result suggests.**

Three of four unique prop reads won. The loss came from repeating one fragile under across the entire build.

That means the next edge jump is not just better picking — it is **better dependency control**.

---

## 12. Final Logbook Entry

**Filed as:** `NBA_POSTMORTEM_2026-04-14_MIA_CHA_REBOUND_CARDS_RESULTS`  
**Registry tags:** `MPZ_TRACKER`, `BACKTEST_LOGBOOK`, `EDGE_CALL_ACTIVE`  
**Ready for:** variance audit, bankroll workflow review, and future rebound under gating
