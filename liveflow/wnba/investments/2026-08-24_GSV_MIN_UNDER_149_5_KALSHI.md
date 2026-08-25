# WNBA LIVE-FLOW Investment Log — Golden State Valkyries at Minnesota Lynx

- Date: 2026-08-24
- Checkpoint: Halftime
- Score at entry decision: Golden State 34, Minnesota 32
- Combined at halftime: 66
- Market-blind model projection: MIN 72, GSV 70, full-game total 142
- Model second-half projection: 76 combined points
- Market revealed: Over 149.5 points
- Position: NO on Over 149.5 (equivalent to Under 149.5)
- Platform: Kalshi
- Displayed market chance at entry: 59%
- Cost: $40.00
- Paid out: $65.90
- Net profit: +$25.90
- ROI on cost: +64.75%
- Effective all-in break-even from cost/payout: 60.70%
- Approx. American-odds equivalent of effective break-even: -154
- Standard SharpEdge max-price threshold: -125
- Price-threshold status: EXCEPTION — accepted outside normal cap
- Exception rationale: 7.5-point market-blind model gap toward the Under
- Model edge vs market line: 7.5 points toward the Under
- Final score: Golden State 80, Minnesota 66
- Final total: 146
- Result vs 149.5: Under by 3.5 points
- Result: WIN
- Status: CLOSED — WON

## Rationale
The first-half total of 66 was not projected to continue linearly. SharpEdge expected a materially higher-scoring second half because both teams had positive regression signals, but the frozen halftime projection called for roughly 76 second-half points, producing a full-game center of 142. The live market at 149.5 required 84 second-half points to finish Over, eight points above the model's remaining-game center.

Golden State's first-half 25.0% three-point shooting and zero free-throw attempts created upside, while Minnesota's 11 first-half turnovers created strong shot-volume normalization pressure. Even after incorporating those upward scoring forces, the model remained materially below the market.

## Price / Execution Audit
The Kalshi screen displayed a **59% chance** when the position was entered. The settled ticket shows **$40.00 cost** and **$65.90 paid out**. Those realized ticket economics imply an all-in break-even of approximately **60.70%**, roughly **-154 American odds**.

SharpEdge's standard maximum price threshold is **-125**. This investment was an explicit **threshold exception**, not a permanent rule change. The exception was accepted because the market-blind fair total of **142** sat **7.5 points below** the 149.5 strike.

Future logs must preserve both the displayed market probability/price and the realized cost-to-payout economics whenever available.

## Market Comparison
- SharpEdge fair total: 142
- Kalshi strike: 149.5
- Difference: 7.5 points Under
- Position purchased: NO on Over 149.5
- Actual final total: 146
- Closing result versus strike: Under by 3.5

## Projection Audit
- Projected final: GSV 70, MIN 72 — 142 total
- Actual final: GSV 80, MIN 66 — 146 total
- GSV error: +10
- MIN error: -6
- Total error: +4
- Projected second half: 76
- Actual second half: 80
- Second-half error: +4

The direction was correct, but the team-level distribution was not. Golden State's second-half offense exceeded the model while Minnesota remained materially below its projected scoring center.

## Frozen Tags
- LIVE_FLOW_HALFTIME_STRIKE
- MARKET_BLIND_PROJECTION_FROZEN
- FULL_GAME_TOTAL_UNDER
- MODEL_MARKET_DIVERGENCE_7_5
- BOTH_TEAMS_SCORING_REGRESSION_UP
- MIN_TURNOVER_REGRESSION_UP_STRONG
- GSV_3P_REGRESSION_UP
- GSV_ZERO_FTA_FIRST_HALF
- KALSHI_POSITION
- PRICE_THRESHOLD_EXCEPTION
- PRICE_LOGGING_REQUIRED
- CLOSED_WIN

```yaml
game_id: WNBA_2026-08-24_GSV_MIN
checkpoint: halftime
score_at_checkpoint:
  GSV: 34
  MIN: 32
model_final:
  GSV: 70
  MIN: 72
model_total: 142
model_second_half_total: 76
market_line: 149.5
position: NO_OVER_149_5
platform: Kalshi
displayed_market_probability: 0.59
cost: 40.00
payout: 65.90
profit: 25.90
roi: 0.6475
effective_break_even_probability: 0.6070
approx_american_odds_equivalent: -154
standard_max_price_american: -125
price_threshold_exception: true
edge_points: 7.5
final_score:
  GSV: 80
  MIN: 66
final_total: 146
result_margin_to_line: -3.5
result: WIN
status: CLOSED
```
