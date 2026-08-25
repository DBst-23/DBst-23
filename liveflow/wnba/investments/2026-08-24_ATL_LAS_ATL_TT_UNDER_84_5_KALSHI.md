# WNBA LIVE-FLOW Investment Log — Atlanta Dream at Los Angeles Sparks

- Date: 2026-08-24
- Checkpoint: Halftime
- Score at checkpoint: Los Angeles 37, Atlanta 36
- Combined at halftime: 73
- Market-blind SharpEdge final projection: Los Angeles 79, Atlanta 78
- SharpEdge full-game total projection: 157
- SharpEdge Atlanta team-total projection: 78
- SharpEdge Atlanta second-half projection: 42
- Initial market reveal: Atlanta team total 87.5, Under priced at -263
- Execution decision: Do not pay -263; ladder down to a lower strike for a materially better price
- Executed market: NO on Atlanta Dream over 84.5 points scored
- Equivalent position: Atlanta Dream Under 84.5
- Platform: Kalshi
- Entry price: +101
- Entry cost: $19.60
- Paid out: $39.39
- Net profit: +$19.79
- ROI on cost: +101.02%
- Effective all-in break-even from cost/payout: 49.76%
- Approx. American-odds equivalent from ticket economics: +101
- Displayed market chance after entry: 48%
- Standard SharpEdge max-price threshold: -125
- Price-threshold status: WITHIN THRESHOLD / FAVORABLE PLUS-MONEY ENTRY
- Model edge vs executed strike: 6.5 points toward the Under
- Final score: Atlanta 78, Los Angeles 71
- Final Atlanta team total: 78
- Result vs 84.5: Under by 6.5 points
- Projection error — Atlanta team total: 0 points
- Actual Atlanta second half: 42
- Projection error — Atlanta second half: 0 points
- Result: WIN
- Status: CLOSED — WON

## Execution Rationale
SharpEdge froze Atlanta's fair final team total at **78** before viewing the live market. The first market reveal priced Atlanta at **87.5**, with the Under carrying a punitive **-263** price. Directionally, the model strongly preferred the Under, but paying -263 would have violated the normal SharpEdge price discipline.

Rather than chase the expensive 87.5 Under, the position was deliberately laddered down to **84.5** and purchased as **NO on Atlanta over 84.5 at +101**. That sacrificed three points of cushion in exchange for a dramatic improvement in price while still preserving a **6.5-point gap** between the executed strike and the frozen model center.

The final Atlanta score landed at **78 exactly**, matching the frozen SharpEdge team-total projection point-for-point. Atlanta also scored **42 points in the second half**, exactly matching the frozen second-half Atlanta projection. The executed 84.5 strike therefore cleared by **6.5 points**, the same distance that separated the strike from the model center at entry.

## Price / Threshold Audit
The standard SharpEdge maximum price threshold is **-125**. This entry was not an exception. At **+101**, the position required only about **49.76%** break-even probability based on the ticket's $19.60 cost and $39.39 payout.

The original 87.5 Under at -263 required roughly 72.5% break-even. By laddering to 84.5, SharpEdge reduced the raw line edge from 9.5 points to 6.5 points but improved the entry price from heavily juiced negative odds to plus money.

The tradeoff worked exactly as intended: the model center remained sufficiently separated from the alternate strike, and the ticket produced **+$19.79 profit on $19.60 risk**, a **+101.02% ROI**.

## Market Comparison
- SharpEdge Atlanta TT fair: 78
- Original market strike: 87.5
- Original raw edge: 9.5 points Under
- Original Under price: -263
- Executed strike: 84.5
- Executed raw edge: 6.5 points Under
- Executed price: +101
- Final Atlanta total: 78
- Closing result versus executed strike: Under by 6.5
- Projection error versus Atlanta final: 0

## Projection Audit
- Projected final: ATL 78, LAS 79 — 157 total
- Actual final: ATL 78, LAS 71 — 149 total
- ATL error: 0
- LAS error: -8
- Full-game total error: -8
- Projected Atlanta second half: 42
- Actual Atlanta second half: 42
- Atlanta second-half error: 0

This is a high-quality team-total calibration result even though the full-game total overestimated Los Angeles by eight points. The targeted variable — Atlanta scoring — landed exactly on the frozen model center, both for the remaining half and the final team total.

## Execution Lesson
**LADDER_DOWN_FOR_PRICE** is validated as an execution concept, not as a blanket rule. When a directional edge is large but the primary line is prohibitively juiced, SharpEdge may trade some line cushion for a better price only when the alternate strike remains materially separated from the frozen projection.

In this case:
- 87.5 Under at -263: excellent line cushion, poor price.
- 84.5 Under at +101: still 6.5 points above the model center, dramatically superior economics.
- Actual: 78, exactly at the model center.

The better risk-adjusted execution was the alternate 84.5 strike.

## Frozen Tags
- LIVE_FLOW_HALFTIME_STRIKE
- MARKET_BLIND_PROJECTION_FROZEN
- ATL_TEAM_TOTAL_UNDER
- ALT_LINE_EXECUTION
- LADDER_DOWN_FOR_PRICE
- MODEL_MARKET_DIVERGENCE_6_5
- PLUS_MONEY_ENTRY
- WITHIN_PRICE_THRESHOLD
- PRICE_LOGGING_REQUIRED
- KALSHI_POSITION
- ATL_MODEL_EXACT_HIT
- ATL_SECOND_HALF_EXACT_HIT
- CLOSED_WIN

```yaml
game_id: WNBA_2026-08-24_ATL_LAS
checkpoint: halftime
score_at_checkpoint:
  ATL: 36
  LAS: 37
model_final:
  ATL: 78
  LAS: 79
model_total: 157
model_atl_team_total: 78
model_atl_second_half: 42
initial_market:
  atl_tt_line: 87.5
  under_price_american: -263
executed_market:
  line: 84.5
  position: NO_OVER_84_5
  equivalent: ATL_UNDER_84_5
  platform: Kalshi
entry_price_american: 101
cost: 19.60
payout: 39.39
profit: 19.79
roi: 1.0102
effective_break_even_probability: 0.4976
displayed_probability_after_entry: 0.48
standard_max_price_american: -125
price_threshold_exception: false
edge_points: 6.5
final_score:
  ATL: 78
  LAS: 71
final_total: 149
atl_final: 78
atl_second_half_actual: 42
atl_projection_error: 0
atl_second_half_projection_error: 0
result_margin_to_line: -6.5
result: WIN
status: CLOSED
```
