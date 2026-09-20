# WNBA LIVE-FLOW Investment Log — Chicago Sky at Atlanta Dream

- Date: 2026-09-19
- Checkpoint: Halftime
- Score at checkpoint: Atlanta 51, Chicago 47
- Combined at halftime: 98
- Market-blind SharpEdge final projection: Atlanta 96, Chicago 90
- SharpEdge full-game total projection: 186
- SharpEdge Atlanta team-total projection: 96
- SharpEdge Chicago team-total projection: 90
- SharpEdge live spread projection: Atlanta -6
- Market reveal — full-game total: 188.5
- Market reveal — Atlanta team total: 100.5
- Market reveal — Chicago team total: 89.5
- Market reveal — live spread: Atlanta -10.5
- Primary model-market gap: 4.5 points toward Atlanta team-total Under
- Secondary full-game total gap: 2.5 points toward Under
- Execution decision: Attack the cleaner team-total discrepancy and avoid stacking correlated Under exposure
- Executed market: NO on Atlanta Dream over 100.5 points scored
- Equivalent position: Atlanta Dream Under 100.5
- Platform: Kalshi
- Entry cost: $10.00
- Max payout: $18.95
- Max profit if settled win: $8.95
- Displayed chance at entry: 51%
- Effective all-in break-even from cost/payout: 52.77%
- Approx. American-odds equivalent from ticket economics: -112
- Standard SharpEdge max-price threshold: -125
- Price-threshold status: WITHIN THRESHOLD
- Model edge vs executed strike: 4.5 points toward the Under
- Status: OPEN

## Execution Rationale
SharpEdge froze Atlanta's fair final team total at **96** before viewing the live market. The revealed Atlanta team-total strike was **100.5**, leaving a **4.5-point cushion toward the Under**.

The full-game total also leaned Under — SharpEdge **186** versus market **188.5** — but that separation was only **2.5 points**. Because the Atlanta team-total discrepancy was materially larger, the single-team market was selected as the primary strike rather than stacking correlated exposure across both Atlanta TT Under and full-game Under.

Atlanta had 51 points at halftime, so clearing 100.5 would require at least 50 additional second-half points. The market-blind model projected roughly **45 second-half Atlanta points**, consistent with the 96-point final center.

## Regression / Game-State Read
Atlanta's first-half scoring contained a meaningful perimeter-efficiency regression signal. The model did not assume a full collapse; it still allowed normal second-half scoring while discounting continuation of the first-half shotmaking environment.

The key distinction is that the position is not a generic fade of a hot shooting half. The strike is supported by:
- a market-blind 96-point Atlanta center,
- a 4.5-point model/market separation,
- a smaller and therefore less attractive edge on the correlated full-game Under,
- explicit avoidance of double-exposure to the same scoring thesis.

## Market Comparison
- SharpEdge full-game total: 186
- Market full-game total: 188.5
- Gap: 2.5 points Under
- SharpEdge Atlanta TT: 96
- Market Atlanta TT: 100.5
- Gap: 4.5 points Under
- SharpEdge Chicago TT: 90
- Market Chicago TT: 89.5
- Gap: 0.5 points Over — PASS
- SharpEdge spread: Atlanta -6
- Market spread: Atlanta -10.5
- Spread gap: 4.5 points toward Chicago, but not the primary scoring-model edge

## Price / Threshold Audit
The ticket costs **$10.00** for a maximum payout of **$18.95**, so the all-in break-even rate from the actual ticket economics is about **52.77%**. That is roughly equivalent to **-112 American odds**, which is inside the normal SharpEdge **-125 maximum price threshold**.

The screenshot displayed a **51% chance**, but SharpEdge records the effective break-even from actual cost and payout separately because platform display probability and all-in ticket economics can differ.

## Frozen Tags
- LIVE_FLOW_HALFTIME_STRIKE
- MARKET_BLIND_PROJECTION_FROZEN
- ATL_TEAM_TOTAL_UNDER
- MODEL_MARKET_DIVERGENCE_4_5
- CORRELATED_EXPOSURE_AVOIDED
- PRICE_LOGGING_REQUIRED
- WITHIN_PRICE_THRESHOLD
- KALSHI_POSITION
- OPEN_POSITION

```yaml
game_id: WNBA_2026-09-19_CHI_ATL
checkpoint: halftime
score_at_checkpoint:
  CHI: 47
  ATL: 51
model_final:
  CHI: 90
  ATL: 96
model_total: 186
model_atl_team_total: 96
model_chi_team_total: 90
model_live_spread: "ATL -6"
market_reveal:
  full_game_total: 188.5
  atl_tt: 100.5
  chi_tt: 89.5
  spread: "ATL -10.5"
executed_market:
  line: 100.5
  position: NO_ATL_OVER_100_5
  equivalent: ATL_UNDER_100_5
  platform: Kalshi
cost: 10.00
max_payout: 18.95
max_profit: 8.95
displayed_probability: 0.51
effective_break_even_probability: 0.5277
approx_american_odds: -112
standard_max_price_american: -125
price_threshold_exception: false
edge_points: 4.5
correlated_full_game_under_gap: 2.5
result: PENDING
status: OPEN
```
