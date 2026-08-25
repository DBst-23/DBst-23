# WNBA LIVE-FLOW Investment Log — Golden State Valkyries at Minnesota Lynx

- Date: 2026-08-24
- Checkpoint: Halftime
- Score at entry decision: Golden State 34, Minnesota 32
- Combined at halftime: 66
- Market-blind model projection: MIN 72, GSV 70, full-game total 142
- Market revealed: Over 149.5 points
- Position: NO on Over 149.5 (equivalent to Under 149.5)
- Platform: Kalshi
- Entry probability / price: 59%
- Cost: $40.00
- Max payout: $65.99
- Gross profit if correct: $25.99
- Implied break-even probability: 59.0%
- Model edge vs market line: 7.5 points toward the Under
- Status: OPEN

## Rationale
The first-half total of 66 was not projected to continue linearly. SharpEdge expected a materially higher-scoring second half because both teams had positive regression signals, but the frozen halftime projection called for roughly 76 second-half points, producing a full-game center of 142. The live market at 149.5 required approximately 84 second-half points, eight points above the model's remaining-game center.

Golden State's first-half 25.0% three-point shooting and zero free-throw attempts created upside, while Minnesota's 11 first-half turnovers created strong shot-volume normalization pressure. Even after incorporating those upward scoring forces, the model remained materially below the market.

## Market Comparison
- SharpEdge fair total: 142
- Kalshi strike: 149.5
- Difference: 7.5 points Under
- Position purchased: NO on Over 149.5

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
- OPEN_INVESTMENT

```yaml
game_id: WNBA_2026-08-24_GSV_MIN
checkpoint: halftime
score_at_checkpoint:
  GSV: 34
  MIN: 32
model_total: 142
market_line: 149.5
position: NO_OVER_149_5
platform: Kalshi
entry_probability: 0.59
cost: 40.00
max_payout: 65.99
profit_if_win: 25.99
edge_points: 7.5
status: OPEN
```
