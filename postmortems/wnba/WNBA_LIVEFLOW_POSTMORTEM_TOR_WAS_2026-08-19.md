# WNBA LIVE-FLOW Postmortem — Toronto Tempo at Washington Mystics

## Game Identity
- Date: 2026-08-19
- Venue: CareFirst Arena, Washington, DC
- Final: Washington 93, Toronto 82
- Final total: **175**
- End 3Q: Washington 69, Toronto 56
- End-3Q total: **125**
- Game ID: `WNBA_2026-08-19_TOR_WAS`

## Pre-Market SharpEdge Freeze — End 3Q
The market-blind end-3Q checkpoint projected a final total around **162-163**, with a working fair total of **162.5**.

### End-3Q state
- Score: Washington 69, Toronto 56
- Combined through 3Q: **125**
- Toronto through 3Q: 21/51 FG (41.2%), 9/22 3PT (40.9%), 5/8 FT (62.5%), 7 turnovers
- Washington through 3Q: 21/46 FG (45.7%), 8/19 3PT (42.1%), 19/23 FT (82.6%), 14 turnovers
- SharpEdge expected Q4 scoring: approximately **37-38 points**
- SharpEdge fair final total: **162.5**

### Core end-3Q thesis
- The game had already reached 125 points, but the model expected the fourth quarter to settle near the high-30s.
- Washington's 29.4% third-quarter FG rate created some positive-regression pressure, but the model still expected overall scoring to cool enough to keep the game in the low-160s.
- Toronto had scored 23 in Q3 after only 9 in Q2, but the model did not project another high-scoring quarter.
- Washington held a 13-point lead, which was expected to reduce extreme late-game volatility relative to a one-possession game.

## Wager Logged

| Checkpoint | Market | Line | Odds | Stake | Result | Final Total | Net |
|---|---|---:|---:|---:|---|---:|---:|
| End 3Q | Full-game total | Under 166.5 | -113 | $10.00 | LOSS | 175 | -$10.00 |

**Total risk:** $10.00  
**Net result:** **-$10.00**

## Market Comparison
- SharpEdge fair total: **162.5**
- William Hill total: **166.5**
- Nominal edge: **4.0 points to the Under**
- Book implied Q4 scoring from current total: **41.5 points**
- SharpEdge expected Q4 scoring: **37.5 points**
- Actual Q4 scoring: **50 points**
- Final total: **175**
- Wager miss versus line: **8.5 points Over**
- Model miss versus final: **12.5 points high-side miss**

## Quarter-4 Reconstruction
Toronto won Q4 scoring **26-24**.

### Toronto Q4
From the end-3Q cumulative box to the final box:
- FG: 7/14
- 3PT: 2/5
- FT: **10/15**
- Points: **26**

### Washington Q4
From the end-3Q cumulative box to the final box:
- FG: 9/20
- 3PT: 1/8
- FT: **5/5**
- Points: **24**

### Key scoring driver
The fourth quarter produced **15 made free throws on 20 attempts combined**. That free-throw expansion was the largest structural reason the final quarter blew through both the SharpEdge expectation and the sportsbook's implied Q4 scoring requirement.

## Projection Accuracy

| Metric | SharpEdge | Market | Actual |
|---|---:|---:|---:|
| End-3Q total | 125 | 125 | 125 |
| Expected remaining scoring | ~37.5 | 41.5 | **50** |
| Final total | **162.5** | **166.5** | **175** |
| Error vs actual | -12.5 | -8.5 | — |

### Interpretation
This was not a case where the market simply posted an obviously bad number and the game landed near the model center. Both the model and the market underestimated fourth-quarter scoring, but SharpEdge underestimated it more aggressively.

The Under thesis therefore fails the postmortem on outcome and on calibration. The miss came primarily from a late-game free-throw environment that the end-3Q projection did not sufficiently price.

## What the Model Read Correctly
1. **The line was not wildly detached from the game state.** The market's 166.5 required 41.5 fourth-quarter points, only four points above the SharpEdge Q4 center.
2. **Washington remained in control.** The Mystics won 93-82 after leading by 13 entering Q4.
3. **Toronto did not need an extreme shooting eruption to break the Under.** The decisive scoring acceleration came largely through foul shots rather than unsustainable 3-point shooting.

## What Failed / What Must Change

### 1. Late-game free-throw environment was underweighted
Toronto went from **5/8 FT through 3Q** to **15/23 final**, meaning it attempted **15 free throws in Q4 alone**. Washington added another 5/5.

**Correction:** Add a `Q4_FT_PRESSURE_GATE` to end-3Q total projections. The model must explicitly estimate fourth-quarter free-throw volume from:
- score margin,
- foul counts,
- bonus proximity,
- aggressive rim pressure,
- trailing-team urgency,
- intentional-foul probability.

### 2. End-3Q Under edge threshold was too permissive
A 4-point model-market difference was treated as actionable even though the wager had only one quarter remaining. With only 10 minutes left, a single foul-heavy stretch can erase four points of theoretical edge quickly.

**Correction:** Raise the minimum edge threshold for end-3Q full-game totals. A 4-point edge should be treated as marginal unless supported by a strong possession/FT/foul-state confirmation.

### 3. Range width was too narrow for one-quarter tail risk
The projection centered near 162.5, effectively requiring only about 37-38 Q4 points. The realized 50-point quarter was not an absurd outlier in WNBA late-game conditions once foul pressure emerged.

**Correction:** End-3Q projections must output a Q4 scoring distribution, not only a center. Track at minimum:
- median Q4 points,
- 75th percentile,
- 90th percentile,
- probability of clearing the live total.

### 4. Toronto's comeback pressure was underpriced
Toronto entered Q4 down 13. A trailing team still close enough to press can create faster possessions, more rim attacks, and late fouling even if it never fully closes the gap.

**Correction:** Add `TRAILING_TEAM_URGENCY` as a pace and foul-volume modifier for margins roughly 8-15 points entering Q4.

## Revised LIVE-FLOW Rules From This Game

### `Q4_FT_PRESSURE_GATE`
Before an end-3Q Under strike, explicitly model likely Q4 free-throw attempts and bonus/intentional-foul risk.

### `END3Q_EDGE_FLOOR`
A nominal 4-point total edge is not automatically sufficient with only one quarter remaining. Require either a larger edge or stronger structural confirmation.

### `Q4_DISTRIBUTION_REQUIRED`
Every end-3Q total must include a remaining-points distribution, not only a point estimate.

### `TRAILING_TEAM_URGENCY`
A team trailing by roughly 8-15 points entering Q4 receives an upward adjustment to pace/foul-tail risk unless the game state clearly indicates surrender rotations.

## Classification
- End-3Q U166.5: **LOSS / MODEL CALIBRATION MISS**
- Directional Under read: **FAIL**
- Market disagreement quality: **MARGINAL — 4.0 points**
- Q4 scoring projection: **FAIL — actual 50 vs ~37.5 expected**
- Free-throw tail modeling: **FAIL — requires upgrade**
- Logging discipline: **PASS — checkpoint and wager preserved**

## Machine-Readable Summary
```yaml
game_id: WNBA_2026-08-19_TOR_WAS
final:
  TOR: 82
  WAS: 93
  total: 175
end_3q:
  TOR: 56
  WAS: 69
  total: 125
model:
  fair_total: 162.5
  expected_q4_points: 37.5
market:
  total: 166.5
  implied_q4_points: 41.5
wager:
  checkpoint: end_3q
  market: full_game_total
  selection: under
  line: 166.5
  odds_american: -113
  stake_usd: 10.00
  result: loss
  net_usd: -10.00
actual_q4:
  TOR: 26
  WAS: 24
  total: 50
  combined_ftm: 15
  combined_fta: 20
errors:
  model_vs_final: -12.5
  market_vs_final: -8.5
process:
  directional_read: fail
  q4_projection: fail
  free_throw_tail_modeling: fail
  checkpoint_persistence: pass
new_tags:
  - Q4_FT_PRESSURE_GATE
  - END3Q_EDGE_FLOOR
  - Q4_DISTRIBUTION_REQUIRED
  - TRAILING_TEAM_URGENCY
status: POSTMORTEM_COMPLETE
```
