# WNBA LIVE-FLOW Investment Log — Atlanta Dream at Los Angeles Sparks

- Date: 2026-08-24
- Checkpoint: Halftime
- Score at checkpoint: Los Angeles 37, Atlanta 36
- Combined at halftime: 73
- Market-blind SharpEdge final projection: Los Angeles 79, Atlanta 78
- SharpEdge full-game total projection: 157
- SharpEdge Atlanta team-total projection: 78
- Initial market reveal: Atlanta team total 87.5, Under priced at -263
- Execution decision: Do not pay -263; ladder down to a lower strike for a materially better price
- Executed market: NO on Atlanta Dream over 84.5 points scored
- Equivalent position: Atlanta Dream Under 84.5
- Platform: Kalshi
- Entry price: +101
- Entry cost: $19.60
- Max payout: $39.39
- Potential profit: $19.79
- Effective all-in break-even from cost/payout: 49.76%
- Approx. American-odds equivalent from ticket economics: +101
- Current displayed market chance after entry in screenshot: 48%
- Standard SharpEdge max-price threshold: -125
- Price-threshold status: WITHIN THRESHOLD / FAVORABLE PLUS-MONEY ENTRY
- Model edge vs executed strike: 6.5 points toward the Under
- Status: OPEN

## Execution Rationale
SharpEdge froze Atlanta's fair final team total at **78** before viewing the live market. The first market reveal priced Atlanta at **87.5**, with the Under carrying a punitive **-263** price. Directionally, the model strongly preferred the Under, but paying -263 would have violated the normal SharpEdge price discipline.

Rather than chase the expensive 87.5 Under, the position was deliberately laddered down to **84.5** and purchased as **NO on Atlanta over 84.5 at +101**. That sacrificed three points of cushion in exchange for a dramatic improvement in price while still preserving a **6.5-point gap** between the executed strike and the frozen model center.

This is an important execution pattern for the LIVE-FLOW library: **when the correct side is prohibitively juiced, consider trading line cushion for price only if the alternate strike still remains materially separated from the frozen projection.**

## Price / Threshold Audit
The standard SharpEdge maximum price threshold is **-125**. This entry is not an exception. At **+101**, the position is substantially better than the threshold and requires only about **49.76%** break-even probability based on the ticket's $19.60 cost and $39.39 maximum payout.

The original 87.5 Under at -263 required roughly 72.5% break-even. By laddering to 84.5, SharpEdge reduced the raw line edge from 9.5 points to 6.5 points but improved the entry price from heavily juiced negative odds to plus money.

## Market Comparison
- SharpEdge Atlanta TT fair: 78
- Original market strike: 87.5
- Original raw edge: 9.5 points Under
- Original Under price: -263
- Executed strike: 84.5
- Executed raw edge: 6.5 points Under
- Executed price: +101
- Position: NO on ATL over 84.5 / ATL Under 84.5

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
- OPEN_POSITION

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
max_payout: 39.39
potential_profit: 19.79
effective_break_even_probability: 0.4976
current_displayed_probability_after_entry: 0.48
standard_max_price_american: -125
price_threshold_exception: false
edge_points: 6.5
status: OPEN
```
