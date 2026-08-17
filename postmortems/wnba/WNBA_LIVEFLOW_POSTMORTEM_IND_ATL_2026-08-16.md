# WNBA LIVE-FLOW Postmortem — Indiana Fever at Atlanta Dream

## Game Identity
- Date: 2026-08-16
- Venue: State Farm Arena, Atlanta, GA
- Final: Indiana 95, Atlanta 91 (OT)
- Regulation: Indiana 81, Atlanta 81
- Regulation total: 162
- Final total including OT: 186
- Overtime scoring: Indiana 14, Atlanta 10 (24 total)
- Game ID: `WNBA_2026-08-16_IND_ATL`

## Pre-Market SharpEdge Freeze — Halftime
The market-blind halftime checkpoint was already persisted before market reveal.

### Halftime state
- Score: Atlanta 44, Indiana 40
- Indiana: 17/39 FG (43.6%), 3/13 3PT (23.1%), 3/8 FT (37.5%)
- Atlanta: 14/39 FG (35.9%), 4/15 3PT (26.7%), 12/13 FT (92.3%)

### Frozen SharpEdge fair lines
- Full-game total: **168**
- Indiana team total: **82**
- Atlanta team total: **86**
- Spread: **Atlanta -4**
- Central total range: **161-175**
- Central margin range: **Atlanta by 0 to 8**

### Core halftime thesis
- Indiana carried strong positive regression pressure from 23.1% 3PT, 37.5% FT, Kelsey Mitchell at 2/10, and productive interior offense.
- Atlanta also had room for FG improvement, but its 12/13 FT conversion carried negative regression pressure.
- The game remained highly competitive, with seven lead changes and eight ties through halftime.

## Wagers Logged

| Checkpoint | Market | Line | Odds | Stake | Result | Final Relevant Score | Net |
|---|---|---:|---:|---:|---|---:|---:|
| Halftime | Full-game total | Under 174.5 | -115 | $20.00 | LOSS | 186 | -$20.00 |
| Halftime | Indiana team total | Under 86.5 | -110 | $10.00 | LOSS | IND 95 | -$10.00 |
| End 3Q | Full-game total | Under 182.5 | -125 | $10.00 | LOSS | 186 | -$10.00 |

**Total risk:** $40.00  
**Net result:** **-$40.00**

## Checkpoint Audit

### Halftime — Under 174.5
- SharpEdge fair total: 168
- Book total: 174.5
- Nominal model edge: **6.5 points to the Under**
- Regulation outcome: 162
- Regulation cushion versus wager: **12.5 points Under**
- Final after OT: 186
- Grading outcome: LOSS

**Process verdict:** The regulation scoring read was directionally and numerically strong. The bet did not lose because the regulation game materially outscored the model; it lost because a tied 81-81 regulation game produced a 24-point overtime period. Because full-game sportsbook totals include overtime, this is not treated as a bad beat exemption. It is an overtime-tail risk that the LIVE-FLOW distribution must explicitly price.

### Halftime — Indiana TT Under 86.5
- SharpEdge fair Indiana TT: 82
- Book Indiana TT: 86.5
- Nominal model edge: **4.5 points to the Under**
- Indiana regulation score: 81
- Regulation cushion versus wager: **5.5 points Under**
- Indiana OT points: 14
- Final Indiana score: 95
- Grading outcome: LOSS

**Process verdict:** The numerical center supported the Under, and Indiana landed almost exactly on the frozen regulation projection (81 actual versus 82 projected). However, this derivative was structurally weaker than the full-game Under because the halftime model itself identified Indiana as the stronger positive-regression side. In a close game, an Indiana TT Under is directly exposed to both the expected regression and overtime extension. Future derivative ranking should penalize team-total Unders when that same team carries strong positive-regression tags.

### End 3Q — Under 182.5
- End 3Q score: Atlanta 72, Indiana 64 (136 total)
- Book total: 182.5
- Required fourth-quarter-plus scoring to beat the Under: 47+ points
- Regulation fourth quarter: Indiana 17, Atlanta 9 = 26 points
- Regulation total: 162
- Regulation cushion versus wager: **20.5 points Under**
- Overtime: 24 additional points
- Final total: 186
- Grading outcome: LOSS

**Process verdict:** The end-3Q Under thesis was strongly validated during regulation: only 26 points were scored in Q4. The loss again came entirely from overtime. However, the exact end-3Q market-blind SharpEdge fair total was not persisted in GitHub before market reveal, so this checkpoint cannot be audited with the same precision as the halftime freeze. That is a logging/process defect and should be corrected going forward.

## Projection Accuracy — Regulation vs Final

| Metric | Frozen HT Projection | Regulation Actual | Error vs Regulation | Final incl. OT |
|---|---:|---:|---:|---:|
| Indiana | 82 | 81 | -1 | 95 |
| Atlanta | 86 | 81 | -5 | 91 |
| Total | 168 | 162 | -6 | 186 |
| Margin | ATL by 4 | Tie | 4 pts | IND by 4 |

### Interpretation
The model's core regulation projection was substantially better than the final betting result suggests:
- Indiana finished regulation only **1 point** below its projection.
- The regulation total finished **6 points** below the fair total.
- Both full-game Under positions had comfortable regulation cushions.
- The decisive model miss was not ordinary scoring pace; it was failure to sufficiently account for the **overtime tail in a competitive game state**.

## What the Model Read Correctly
1. **Indiana positive regression arrived.** Kelsey Mitchell rose from 5 first-half points to 18 by the end of regulation and 20 after OT. Caitlin Clark rose from 10 at halftime to 24 through regulation and 26 final.
2. **Atlanta's first-half FT support did not translate into runaway regulation scoring.** Atlanta scored 37 points in the second half after 44 in the first half.
3. **The regulation total stayed below the halftime fair center.** Final regulation scoring was 162 against a frozen 168 projection.
4. **The End-3Q Under read was strong in Q4.** The teams combined for only 26 fourth-quarter points.
5. **Competitive-state risk was real.** The game finished regulation tied after 13 regulation lead changes and 11 ties, ultimately forcing OT.

## What Failed / What Must Change

### 1. Overtime tail was identified qualitatively but not priced quantitatively
The halftime log included `COMPETITIVE_ROTATIONS_SECURE` and a margin range reaching Atlanta by 0, but the total distribution did not carry an explicit overtime component. A close-game total cannot be modeled only as a regulation scoring distribution when the sportsbook grades through overtime.

**Correction:** Every LIVE-FLOW full-game total projection must now carry:
- regulation fair total,
- overtime probability estimate,
- overtime-adjusted fair total,
- tail probability of the wager losing specifically through OT.

### 2. Correlated exposure was too concentrated
All three wagers were effectively the same thesis:
- game Under,
- Indiana TT Under,
- later game Under.

This created **$40 of highly correlated downside**. When overtime occurred, every position was hit by the same event.

**Correction:** Treat multiple wagers on the same scoring thesis as one exposure bucket. Additional same-direction entries require materially improved price/edge and must not be sized as independent bets.

### 3. Indiana TT Under conflicted with the strongest regression signal
The model explicitly tagged:
- `IND_3P_REGRESSION_UP`
- `IND_FT_REGRESSION_UP`
- `KELSEY_MITCHELL_SHOOTING_REGRESSION_UP`
- `IND_PAINT_PROCESS_STRONG`

Taking Indiana TT Under 86.5 was numerically defensible from the 82 center, but qualitatively it faded the side with the strongest positive scoring-regression profile.

**Correction:** Add a derivative-consistency check. If a team carries multiple positive-regression tags, its TT Under must clear a higher edge threshold than a neutral derivative.

### 4. End-3Q independent line was not persisted
The market-blind halftime projection was frozen cleanly in GitHub. The end-3Q projection was not.

**Correction:** Before every market reveal at halftime or end 3Q, persist the exact SharpEdge lines and state tags. No later reconstruction from memory.

## Revised LIVE-FLOW Rules From This Game

### `OT_TAIL_GATE`
For full-game totals in competitive games, calculate an explicit overtime component before declaring an edge.

Trigger the gate when any of the following are present late:
- projected margin near one possession,
- repeated ties/lead changes,
- live spread near pick'em / one possession,
- high-probability close-game rotation state.

### `CORRELATED_EXPOSURE_BUCKET`
Full-game total + team total + later re-entry on the same directional scoring thesis count as one correlated position group.

### `DERIVATIVE_REGRESSION_CONSISTENCY`
Do not aggressively short a team total when the same model is flagging strong positive shooting/FT/player regression for that team unless the numerical edge is clearly large enough to overcome that conflict.

### `CHECKPOINT_FREEZE_REQUIRED`
Every halftime and end-3Q wager must have its own market-blind GitHub freeze before sportsbook pricing is viewed.

## Classification
- Halftime U174.5: **GOOD REGULATION READ / OT-TAIL LOSS**
- Halftime IND TT U86.5: **NUMERIC EDGE, WEAKER DERIVATIVE / OT-TAIL LOSS**
- End-3Q U182.5: **STRONG REGULATION READ / OT-TAIL LOSS / CHECKPOINT NOT FULLY PERSISTED**
- Overall model regulation read: **PASS**
- Overtime-tail modeling: **FAIL — requires upgrade**
- Exposure construction: **FAIL — excessive correlated stacking**
- Logging discipline: **PARTIAL PASS — halftime clean, end-3Q incomplete**

## Machine-Readable Summary
```yaml
game_id: WNBA_2026-08-16_IND_ATL
final:
  IND: 95
  ATL: 91
  total: 186
  overtime: true
regulation:
  IND: 81
  ATL: 81
  total: 162
overtime:
  IND: 14
  ATL: 10
  total: 24
halftime_model:
  IND: 82
  ATL: 86
  total: 168
  spread: ATL_-4
wagers:
  - checkpoint: halftime
    market: full_game_total
    selection: under
    line: 174.5
    odds_american: -115
    stake_usd: 20.00
    result: loss
    regulation_result: would_win
    loss_driver: overtime
  - checkpoint: halftime
    market: IND_team_total
    selection: under
    line: 86.5
    odds_american: -110
    stake_usd: 10.00
    result: loss
    regulation_result: would_win
    loss_driver: overtime
  - checkpoint: end_3q
    market: full_game_total
    selection: under
    line: 182.5
    odds_american: -125
    stake_usd: 10.00
    result: loss
    regulation_result: would_win
    loss_driver: overtime
risk_usd: 40.00
net_usd: -40.00
process:
  regulation_projection: pass
  overtime_tail_modeling: fail
  correlated_exposure_control: fail
  derivative_consistency: needs_improvement
  checkpoint_persistence: partial_pass
new_tags:
  - OT_TAIL_GATE
  - CORRELATED_EXPOSURE_BUCKET
  - DERIVATIVE_REGRESSION_CONSISTENCY
  - CHECKPOINT_FREEZE_REQUIRED
status: POSTMORTEM_COMPLETE
```
