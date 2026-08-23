# WNBA LIVE-FLOW Postmortem — Atlanta Dream at Phoenix Mercury

**Date:** 2026-08-22  
**Checkpoint:** End of 3rd Quarter  
**Market:** Full Game Total — Live  
**Sportsbook:** William Hill  
**Decision:** NO BET  
**Final:** Atlanta Dream 99, Phoenix Mercury 89  
**Final Total:** 188

---

## 1. Trigger State

**End of 3Q:** Atlanta 73, Phoenix 68  
**Combined:** 141

SharpEdge projected the line **before sportsbook comparison**.

### Frozen SharpEdge read

- Fair full-game total: **185.0**
- Expected 4Q scoring: approximately **44 combined points**
- Fair spread: approximately **Atlanta -2 to -3**

The sportsbook then showed:

- Full-game total: **186.5** (-115 both sides)
- Atlanta team total: **97.5**
- Phoenix team total: **89.5**
- Atlanta live spread: **-7.5 (+100)**
- Phoenix live spread: **+7.5 (-130)**

The full-game total gap was only **1.5 points toward the Under**.

**Classification:** PASS / NO BET  
**Reason:** Model-market separation below strike threshold.

---

## 2. Why the Pass Was Correct

The third quarter was extremely high scoring: Phoenix won the period **33-23**, creating **56 combined points** and pulling the game from 85 at halftime to 141 through three quarters.

Phoenix's Q3 scoring was powered by an efficiency burst:

- Phoenix FG: **13/22 (59.1%)**
- Phoenix 3PT: **5/7 (71.4%)**
- Kahleah Copper: **18 Q3 points**

That made regression a reasonable component of the 4Q projection. But the market had already adjusted upward to **186.5**. With SharpEdge at **185.0**, the available edge was only **1.5 points**.

That was not enough separation to justify paying -115 into a volatile end-game state.

The correct decision was therefore not to force an Under simply because the projection sat slightly below market.

---

## 3. What Actually Happened

The fourth quarter produced **47 points**:

- Atlanta: **26**
- Phoenix: **21**

Final score:

**Atlanta 99, Phoenix 89 — 188 total**

The actual fourth quarter finished approximately **3 points above** the 44-point central expectation, enough to push the game above both the 185 SharpEdge fair and the 186.5 sportsbook line.

Had SharpEdge forced the Under 186.5, it would have lost by **1.5 points**.

Because the system passed, bankroll exposure was **$0**.

---

## 4. Projection Audit

| Metric | SharpEdge | Sportsbook | Actual |
|---|---:|---:|---:|
| Full-game total | 185.0 | 186.5 | 188 |
| Remaining 4Q points | ~44 | ~45.5 implied | 47 |
| End-3Q combined | 141 | — | 141 |

### Errors

- Actual vs SharpEdge fair: **+3.0 points**
- Actual vs sportsbook total: **+1.5 points**
- Sportsbook vs SharpEdge fair: **+1.5 points**

The sportsbook was slightly closer to the realized outcome, but the key process result is that **neither side offered enough pre-wager separation to qualify as a strike**.

---

## 5. Fourth-Quarter Mechanics

Atlanta's offense remained efficient enough to prevent the hoped-for regression from producing a low-scoring close.

### Atlanta Q4

- 26 points
- 8/15 FG (**53.3%**)
- 2/8 from three
- 8/9 FT
- only 1 turnover

Angel Reese was the decisive interior scoring driver:

- **13 Q4 points**
- 5/5 FG
- 3/4 FT

She finished with a career-high **31 points** and 14 rebounds.

### Phoenix Q4

- 21 points
- 6/11 FG (**54.5%**)
- 1/2 from three
- 8/10 FT

Phoenix did regress from its 33-point third quarter, but not enough. Both teams shot above 53% from the field in Q4 and combined for **16 made free throws**, keeping the scoring floor elevated.

---

## 6. What SharpEdge Got Right

1. **Projection first, market second.** The 185 fair total was frozen before viewing William Hill's 186.5.
2. **No forced wager.** A 1.5-point edge at -115 was correctly rejected.
3. **Volatility was respected.** The 56-point Q3 created uncertainty rather than becoming an automatic fade signal.
4. **The pass protected capital.** The Under would have lost, but outcome is secondary to the fact that the pre-wager edge did not meet strike standards.
5. **Regression thesis was directionally reasonable but incomplete.** Phoenix cooled from 33 to 21 in Q4, yet Atlanta's efficiency and free throws offset that regression.

---

## 7. What the Model Should Learn

### `LIVEFLOW_END3Q_EDGE_THRESHOLD_v1`

- Do not attack a live total merely because SharpEdge differs from market by 1-2 points.
- At end-of-3Q checkpoints, require a larger cushion because one quarter carries high variance from fouling, free throws, possession compression, star concentration and game-state urgency.
- A prior-quarter shooting spike can regress while the total still goes Over if the opposing offense remains efficient or the foul environment rises.
- Separate **team-level regression** from **game-total regression**. Phoenix regressed materially from 33 Q3 points to 21 Q4 points, yet Atlanta rose from 23 to 26.
- Late free-throw volume must be treated as an upside tail for totals. The teams combined for 19 Q4 free-throw attempts and made 16.
- Continue logging passes with the same rigor as wagers. A disciplined no-bet is model information, not an empty event.

---

## 8. Tags

- `NO_BET_DISCIPLINE`
- `MARKET_BLIND_PROJECTION`
- `EDGE_BELOW_THRESHOLD`
- `END3Q_VOLATILITY`
- `PHOENIX_Q3_EFFICIENCY_SPIKE`
- `PARTIAL_REGRESSION_ONLY`
- `ATLANTA_INTERIOR_SCORING_PERSISTED`
- `LATE_FREE_THROW_PRESSURE`
- `CAPITAL_PRESERVED`

---

## Final Grade

**CORRECT_PASS / PROCESS_WIN**

SharpEdge projected **185.0** against William Hill **186.5**, only a **1.5-point gap**. That was not enough to justify a live Under at -115.

The game finished **188**, meaning a forced Under would have lost. More importantly, the process did exactly what it was supposed to do: **project first, compare second, and decline the market when the edge is too thin**.

This game belongs in the library as a clean example that a correct LIVE-FLOW system is defined as much by the bets it refuses as by the bets it makes.
