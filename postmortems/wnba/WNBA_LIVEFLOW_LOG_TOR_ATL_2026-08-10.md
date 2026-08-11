# WNBA LIVE-FLOW Postmortem — Toronto Tempo at Atlanta Dream

## Final — Corrected Official Result
- Date: 2026-08-10
- Checkpoint: End of 3Q
- 3Q score: Atlanta 80, Toronto 67
- Final: Atlanta 107, Toronto 95
- Final total: 202
- Final margin: Atlanta +12
- Decision at checkpoint: PASS / NO STRIKE

## Frozen SharpEdge Projection
- 4Q: Atlanta 24, Toronto 22
- 4Q total: 46
- Projected 4Q margin: Atlanta +2
- Final: Atlanta 104, Toronto 89
- Full-game spread: Atlanta -15
- Full-game total: 193
- Atlanta team total: 104
- Toronto team total: 89

## William Hill Market at 3Q Checkpoint
- Spread: Atlanta -15.5
- Total: 192.5
- Atlanta team total: 104.5
- Toronto team total: 88.5

### Model vs Market at Decision Time
| Market | SharpEdge | William Hill | Separation |
|---|---:|---:|---:|
| Spread | ATL -15 | ATL -15.5 | 0.5 pt |
| Total | 193 | 192.5 | 0.5 pt |
| Atlanta TT | 104 | 104.5 | 0.5 pt |
| Toronto TT | 89 | 88.5 | 0.5 pt |

There was no qualifying edge. The market and model were effectively in equilibrium, so the PASS was correct process regardless of the eventual result.

## Actual 4Q
- Toronto 28
- Atlanta 27
- 4Q total: 55
- 4Q margin: Toronto +1

## Projection vs Actual
| Component | Projection | Actual | Error |
|---|---:|---:|---:|
| Atlanta 4Q | 24 | 27 | +3 |
| Toronto 4Q | 22 | 28 | +6 |
| 4Q total | 46 | 55 | +9 |
| 4Q margin | ATL +2 | TOR +1 | 3-point swing |
| Atlanta final | 104 | 107 | +3 |
| Toronto final | 89 | 95 | +6 |
| Full-game total | 193 | 202 | +9 |
| Final margin | ATL +15 | ATL +12 | 3 pts |

## Market Outcome
- Toronto +15.5 covered. Atlanta won by 12, so Toronto beat the spread by 3.5 points.
- Over 192.5 won. Final total 202 finished 9.5 points above the line.
- Atlanta Over 104.5 won. Atlanta scored 107, 2.5 points above the line.
- Toronto Over 88.5 won. Toronto scored 95, 6.5 points above the line.

## What Actually Happened
The previous automated postmortem was invalid because it used an incorrect final score and therefore produced the wrong grading, wrong 4Q scoring profile, and wrong model lesson. That record has been removed and replaced with this corrected version using the official final box supplied after the game.

The real 4th quarter was not a scoring-compression environment. It accelerated into a 55-point quarter despite Atlanta entering with a 13-point lead.

Toronto shot 9-for-14 from the field in the 4th quarter (64.3%) and went 9-for-11 at the line. Marina Mabrey scored 12 points in the quarter, Kiki Rice added 6, and Toronto produced 28 total points.

Atlanta also remained efficient, shooting 11-for-20 in the 4th quarter (55.0%) with four made threes. Rhyne Howard scored 12 in the period and Atlanta still added 27.

That combination drove the game nine points above the frozen 193 projection and 9.5 points above the live market total of 192.5.

## Evaluation of the PASS
**PASS = CORRECT PROCESS.**

This is an important distinction for the LIVE-FLOW database. The eventual winners do not retroactively create an actionable edge.

At the decision point:
- Our total was only 0.5 above market.
- Our spread was only 0.5 away from market.
- Both team totals were only 0.5 away from market.

Those gaps were far below a legitimate strike threshold. Taking Over 192.5, Toronto +15.5, Atlanta TT Over 104.5, or Toronto TT Over 88.5 would have won in hindsight, but none was supported by enough model-market separation when the decision had to be made.

## Model Diagnosis
### What SharpEdge got right
1. **No false edge:** The model correctly recognized an efficient market and stayed out.
2. **Game-side direction:** Atlanta remained the superior side and won comfortably.
3. **Broad scoring band:** A projected 193 was not structurally broken; the miss came from a high-efficiency 4Q tail rather than a completely wrong game script.

### What SharpEdge missed
1. **Toronto 4Q scoring tail:** Toronto exceeded its 22-point 4Q projection by 6.
2. **Late offensive sustainability:** Both teams remained highly efficient instead of regressing downward.
3. **Margin compression:** Toronto won the 4Q by one, reducing Atlanta's margin from +13 after 3Q to +12 final; SharpEdge expected Atlanta to win the quarter by two.
4. **High-total tail risk:** The model did not assign enough probability to a 55-point 4Q after Toronto had already shown strong 3Q shotmaking.

## Correct Model Lesson
Do **not** automatically apply stronger scoring compression merely because one team carries a double-digit lead into the 4th quarter.

For future WNBA LIVE-FLOW checkpoints, the 4Q layer should separately evaluate:
- current shot-quality and shotmaking persistence,
- foul/bonus environment,
- whether the trailing team still has primary creators actively attacking,
- rotation quality rather than assuming bench-induced slowdown,
- 3Q offensive momentum,
- comeback urgency and pace,
- probability of intentional fouling or extended late possessions if the game narrows.

A double-digit lead can create compression, but it should be a conditional input — not an automatic downward scoring adjustment.

## Classification
- PASS decision: **CORRECT PROCESS**
- Edge-threshold discipline: **CONFIRMED**
- Spread projection: **SOLID / 3-PT ERROR**
- Full-game total projection: **MISS LOW BY 9**
- Atlanta TT projection: **MISS LOW BY 3**
- Toronto TT projection: **MISS LOW BY 6**
- 4Q total projection: **MISS LOW BY 9**
- Primary calibration target: **high-efficiency 4Q tail / trailing-team offensive persistence**
- Previous automated postmortem: **INVALIDATED AND REMOVED**

```yaml
game_id: WNBA_2026-08-10_TOR_ATL
checkpoint: end_3q
score_at_checkpoint:
  TOR: 67
  ATL: 80
model:
  q4:
    TOR: 22
    ATL: 24
    total: 46
    margin: ATL_2
  final:
    TOR: 89
    ATL: 104
    total: 193
    margin: ATL_15
market:
  spread: ATL_-15.5
  total: 192.5
  atl_tt: 104.5
  tor_tt: 88.5
decision: PASS
actual:
  q4:
    TOR: 28
    ATL: 27
    total: 55
    margin: TOR_1
  final:
    TOR: 95
    ATL: 107
    total: 202
    margin: ATL_12
market_results:
  spread: TOR_+15.5_WIN
  total: OVER_192.5_WIN
  atl_tt: OVER_104.5_WIN
  tor_tt: OVER_88.5_WIN
errors:
  atl_q4: 3
  tor_q4: 6
  q4_total: 9
  atl_final: 3
  tor_final: 6
  full_total: 9
  final_margin: 3
postmortem:
  pass_decision: correct_process
  edge_threshold: confirmed
  total_model: miss_low
  calibration_target: high_efficiency_q4_tail_and_trailing_team_offensive_persistence
  prior_automated_postmortem: invalidated_and_removed
```