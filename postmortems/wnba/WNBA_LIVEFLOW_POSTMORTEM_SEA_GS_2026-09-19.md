# WNBA LIVE-FLOW Postmortem — Seattle Storm at Golden State Valkyries

## Game
- Date: 2026-09-19
- Venue: Chase Center, San Francisco, CA
- Final: Golden State Valkyries 70, Seattle Storm 57
- Final total: **127**
- Halftime: Golden State 49, Seattle 25
- End 3Q: Golden State 64, Seattle 46
- Q4: Golden State 6, Seattle 11
- Attendance: 18,064 (sellout)

## Executive Summary
SharpEdge's end-of-third-quarter LIVE-FLOW process correctly identified **Golden State team total Under 90.5** as the preferred execution.

The position won comfortably:
- Golden State entered Q4 with 64 points.
- The 90.5 line required **27+ fourth-quarter points** to lose the Under.
- Golden State scored only **6 points** in Q4.
- Final Golden State total: **70**.
- Market cushion at settlement: **20.5 points under 90.5**.

The direction was correct, but the postmortem also exposes a calibration issue: SharpEdge's frozen projection of Golden State 87 was still **17 points too high**. The model recognized blowout/rotation suppression, but it did not apply nearly enough fourth-quarter scoring decay.

This is therefore a **winning execution with a meaningful projection miss**. Both truths must be preserved.

## Locked Position
- Platform: Kalshi
- Contract: **No · Golden State over 90.5 points scored**
- Sportsbook equivalent: **Golden State TT Under 90.5**
- Cost: **$9.60**
- Paid out: **$9.69**
- Profit: **+$0.09**
- ROI on cost: **+0.94%**
- Result: **WIN**

Important: Kalshi's displayed **99% chance** was the contract market quote at the time of capture, not a SharpEdge-generated model probability.

## End-3Q Market-Blind Freeze
Score at checkpoint:
- Golden State 64
- Seattle 46
- Combined 110
- Golden State lead: 18

Frozen SharpEdge projection:
- Golden State final: **87**
- Seattle final: **60**
- Full-game total: **147**
- Final margin: Golden State **+27**

Frozen fair lines:
- Spread: Golden State -27.5
- Total: 146.5
- Golden State TT: 87.0
- Seattle TT: 59.5

Observed market:
- Golden State -18.5
- Full-game total 145.5
- Golden State TT 90.5
- Seattle TT 65.5

The full-game total was correctly passed because SharpEdge's 146.5 fair total was only one point away from market. The team-total allocation layer created the actionable difference.

## Why the Golden State TT Under Was Correct
### 1. Required scoring was too aggressive for the game state
Golden State needed at least 27 Q4 points to clear 90.5 after entering the period at 64.

That requirement was large for a team already leading by 18 in a game that had reached a 32-point maximum margin.

### 2. Blowout state materially changed offensive incentives
Golden State no longer needed aggressive transition offense or starter-heavy shot creation. The fourth-quarter environment became substantially lower leverage.

### 3. Team-total isolation was cleaner than the aggregate total
SharpEdge did **not** force a full-game total bet. That was important. The aggregate total had largely converged to market, while Golden State's individual scoring requirement still looked inflated.

### 4. Correlation discipline was preserved
Seattle TT Under 65.5 also showed model separation, but both unders were substantially driven by the same low-Q4/blowout-decay regime. The system chose one primary expression instead of stacking correlated positions.

## Fourth-Quarter Audit
Actual Q4:
- Golden State: **6**
- Seattle: **11**
- Combined: **17**

Golden State Q4 shooting:
- 3/16 FG — **18.8%**
- 0/6 3PT — **0%**
- 0 FT attempts
- 5 turnovers

Seattle Q4 shooting:
- 4/16 FG — **25.0%**
- 2/8 3PT — **25.0%**
- 1/2 FT

The quarter was not merely slow. It was an extreme scoring collapse on both sides.

## Projection Error Audit
### Golden State
- Frozen final projection: 87
- Actual: 70
- Error: **-17**

### Seattle
- Frozen final projection: 60
- Actual: 57
- Error: **-3**

### Full game
- Frozen total projection: 147
- Actual: 127
- Error: **-20**

### Fourth quarter
- Projected Golden State Q4: 23
- Actual: 6
- Error: **-17**

- Projected Seattle Q4: 14
- Actual: 11
- Error: **-3**

- Projected Q4 total: 37
- Actual: 17
- Error: **-20**

This was an **asymmetric projection miss**. Nearly the entire error came from overestimating Golden State's remaining offense.

## Model Diagnosis
### What worked
- Market-blind projection occurred before viewing the live market.
- Team-allocation analysis found a better angle than the aggregate total.
- The system ranked Golden State TT Under 90.5 as the primary execution.
- The full-game total was passed when separation was insufficient.
- Correlated team-total exposure was not stacked.
- The actual ticket won with a 20.5-point settlement cushion.

### What missed
- Golden State's blowout-state scoring decay was still dramatically underweighted.
- The model projected 23 Q4 points for Golden State; actual was 6.
- Rotation suppression was recognized qualitatively but not converted into enough quantitative downward adjustment.
- The model did not fully price the possibility that a large-lead favorite could enter a near-offensive-shutdown state.

## Key Learning — BLOWOUT_SCORING_DECAY Needs a Stronger Tail
This game validates the direction of the existing blowout suppression concept but shows that a simple moderate reduction is not enough.

When a favorite enters Q4 with:
- lead of 18+
- prior maximum lead of 30+
- no need for pace acceleration
- bench/low-usage units likely to absorb minutes
- aggregate market already compressed

the remaining scoring distribution should include a much fatter lower tail.

The lesson is **not** to hard-code six-point quarters. The lesson is to increase probability mass on extreme low-scoring favorite outcomes in noncompetitive fourth quarters.

## Proposed Patch — BLOWOUT_DECAY_TAIL_v2
For end-3Q LIVE-FLOW totals and team totals, add an explicit lower-tail adjustment when all of the following are present:

1. Current lead >= 18.
2. Maximum prior lead >= 24.
3. Leading team has already shown second-half pace/efficiency cooling.
4. Market requires the leading team to score at or above a normal full-strength Q4 rate.
5. Rotation risk is elevated.

### Test requirement
Backtest historical WNBA end-3Q checkpoints by lead buckets:
- 12-17
- 18-23
- 24-29
- 30+

For each bucket, compare:
- actual leading-team Q4 points
- baseline projected Q4 points
- projection error
- starter minute share in Q4
- field-goal attempts
- free-throw attempts
- turnover rate

Then compare MAE before and after the decay-tail adjustment.

## Market-Selection Lesson
This game is a strong example of why LIVE-FLOW should ask:

**Which market is mispriced?**

rather than:

**Is the game going Over or Under?**

At end 3Q:
- Full total: near fair → pass.
- Golden State TT: meaningful Under separation → strike.
- Seattle TT: larger raw separation but greater garbage-time uncertainty → secondary.
- Spread: theoretical value, but not the cleanest scoring-state expression.

That market-selection hierarchy worked.

## Final Classification
- Primary checkpoint: End 3Q
- Market-blind freeze: YES
- Primary execution: Golden State TT Under 90.5 equivalent
- Platform: Kalshi
- Ticket result: WIN
- Cost: $9.60
- Payout: $9.69
- Profit: +$0.09
- ROI: +0.94%
- Final GS points: 70
- Settlement cushion: 20.5 points
- Model GS projection: 87
- GS projection error: -17
- Full-game projection error: -20
- Execution quality: GOOD
- Projection calibration: TOO HIGH
- Primary model lesson: stronger blowout-scoring lower tail required

## Frozen Tags
- LIVE_FLOW_POSTMORTEM
- WNBA_2026_09_19_SEA_GS
- END3_MARKET_BLIND_PROJECTION_FROZEN
- GS_TEAM_TOTAL_UNDER_90_5
- KALSHI_NO_GS_OVER_90_5
- CLOSED_WIN
- TEAM_TOTAL_MARKET_SELECTION_WIN
- FULL_TOTAL_PASS_CORRECT
- CORRELATION_DISCIPLINE
- BLOWOUT_SCORING_DECAY
- ROTATION_SUPPRESSION
- BLOWOUT_DECAY_TAIL_v2
- FAVORITE_Q4_OFFENSIVE_COLLAPSE
- PROJECTION_WIN_DIRECTION_MISS_MAGNITUDE
- CALIBRATION_REVIEW_REQUIRED

```yaml
postmortem_id: WNBA_LIVEFLOW_POSTMORTEM_SEA_GS_2026-09-19
game_id: WNBA_2026-09-19_SEA_GS
league: WNBA
date: 2026-09-19
checkpoint: end_3q
score_at_checkpoint:
  SEA: 46
  GS: 64
  total: 110
  margin: GS_18
market_seen_before_projection: false
frozen_projection:
  q4:
    SEA: 14
    GS: 23
    total: 37
  final:
    SEA: 60
    GS: 87
    total: 147
    margin: GS_27
fair_lines:
  spread: GS_-27.5
  total: 146.5
  GS_TT: 87.0
  SEA_TT: 59.5
market:
  spread: GS_-18.5
  total: 145.5
  GS_TT: 90.5
  SEA_TT: 65.5
execution:
  platform: Kalshi
  contract: NO_GS_OVER_90.5
  equivalent_market: GS_TT_UNDER_90.5
  displayed_market_probability_pct: 99
  cost_usd: 9.60
  payout_usd: 9.69
  profit_usd: 0.09
  roi_pct: 0.94
  result: WIN
final:
  SEA: 57
  GS: 70
  total: 127
  margin: GS_13
q4_actual:
  SEA: 11
  GS: 6
  total: 17
projection_errors:
  SEA: -3
  GS: -17
  total: -20
  q4_SEA: -3
  q4_GS: -17
  q4_total: -20
settlement:
  GS_TT_line: 90.5
  GS_actual: 70
  under_cushion_points: 20.5
patch_candidate: BLOWOUT_DECAY_TAIL_v2
status: CLOSED_WIN
```
