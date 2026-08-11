# WNBA LIVE-FLOW Postmortem — Toronto Tempo at Atlanta Dream

## Final
- Date: 2026-08-10
- 3Q checkpoint: Atlanta 80, Toronto 67
- Final: Atlanta 97, Toronto 83
- Final total: 180
- Final margin: Atlanta +14
- Decision at checkpoint: PASS / NO STRIKE

## Frozen SharpEdge Projection
- 4Q: Atlanta 24, Toronto 22
- 4Q total: 46
- Final: Atlanta 104, Toronto 89
- Full-game spread: Atlanta -15
- Full-game total: 193
- Atlanta team total: 104
- Toronto team total: 89

## William Hill at 3Q
- Spread: Atlanta -15.5
- Total: 192.5
- Atlanta TT: 104.5
- Toronto TT: 88.5
- Maximum model-market gap: 0.5 point

## Actual 4Q
- Atlanta 17, Toronto 16
- 4Q total: 33
- 4Q margin: Atlanta +1

## Projection vs Actual
| Component | Projection | Actual | Error |
|---|---:|---:|---:|
| Atlanta 4Q | 24 | 17 | -7 |
| Toronto 4Q | 22 | 16 | -6 |
| 4Q total | 46 | 33 | -13 |
| 4Q margin | ATL +2 | ATL +1 | 1 |
| Atlanta final | 104 | 97 | -7 |
| Toronto final | 89 | 83 | -6 |
| Full total | 193 | 180 | -13 |
| Final margin | ATL +15 | ATL +14 | 1 |

## Market Outcome
- Atlanta -15.5 did not cover; Toronto +15.5 covered by 1.5.
- Under 192.5 finished 12.5 points below the line.
- Atlanta finished 7.5 below 104.5.
- Toronto finished 5.5 below 88.5.

## Evaluation
The PASS was correct process. Every available market was only 0.5 point from the frozen model, so there was no meaningful pre-result separation. The final outcome should not be treated as a missed opportunity.

The strongest model hit was margin calibration: SharpEdge ATL +15 versus actual ATL +14, only a one-point error. The 4Q margin call was also strong: projected ATL +2, actual ATL +1.

The main miss was the scoring environment. The model projected 46 fourth-quarter points and got 33. Both team totals were therefore overstated: Atlanta by 7 and Toronto by 6. This was a shared pace/efficiency miss rather than a team-allocation miss.

## Model Lesson
Keep the market-blind workflow and no-action discipline when market and model are in equilibrium. Modify the fourth-quarter scoring layer by adding stronger late-game scoring compression when a team enters Q4 with a double-digit lead, especially after elevated 3-point shooting and large earlier free-throw volume.

## Classification
- PASS decision: CORRECT PROCESS
- Spread model: STRONG HIT
- 4Q margin model: STRONG HIT
- Full-game total model: MISS HIGH
- Team-total models: MISS HIGH
- Edge-threshold discipline: CONFIRMED
- Patch: strengthen fourth-quarter scoring compression

```yaml
game_id: WNBA_2026-08-10_TOR_ATL
checkpoint: end_3q
model:
  q4: {TOR: 22, ATL: 24, total: 46}
  final: {TOR: 89, ATL: 104, total: 193, margin: ATL_15}
market:
  spread: ATL_-15.5
  total: 192.5
  atl_tt: 104.5
  tor_tt: 88.5
actual:
  q4: {TOR: 16, ATL: 17, total: 33}
  final: {TOR: 83, ATL: 97, total: 180, margin: ATL_14}
errors:
  q4_total: -13
  full_total: -13
  final_margin: 1
postmortem:
  pass_decision: correct_process
  spread_model: strong_hit
  total_model: miss_high
  patch: stronger_q4_scoring_compression
```
