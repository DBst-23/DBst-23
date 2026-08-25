# WNBA LIVE-FLOW Postmortem — Atlanta Dream at Los Angeles Sparks

## Game
- Date: 2026-08-24
- Venue: Crypto.com Arena, Los Angeles, CA
- Final: Atlanta Dream 78, Los Angeles Sparks 71
- Final total: 149
- Halftime: Los Angeles 37, Atlanta 36
- Halftime combined: 73

## Frozen Market-Blind Projection
SharpEdge projected the game before viewing the live market:

- Atlanta final: **78**
- Los Angeles final: **79**
- Full-game total: **157**
- Atlanta second half: **42**
- Los Angeles second half: **42**
- Atlanta fair team total: **78**

The halftime read centered on strong positive shooting-regression pressure for both teams, Atlanta turnover normalization, Atlanta offensive rebounding, sustainable Los Angeles interior scoring, and a competitive game state.

## Market Reveal
The primary Atlanta team-total market was:

- Atlanta over 87.5: +109
- Atlanta under 87.5: -263

SharpEdge's 78 projection created a **9.5-point raw gap toward the Under**, but the -263 price was far outside the normal **-125 maximum price threshold**.

## Execution
Instead of paying -263, SharpEdge deliberately laddered down:

- Market: NO on Atlanta Dream over 84.5
- Equivalent: Atlanta team total Under 84.5
- Platform: Kalshi
- Entry price: **+101**
- Cost: **$19.60**
- Payout: **$39.39**
- Profit: **+$19.79**
- ROI: **+101.02%**
- Effective break-even: **49.76%**
- Model gap at executed strike: **6.5 points Under**
- Result: **WIN**

## Result Audit
Atlanta finished with **78 points**, exactly matching the frozen SharpEdge Atlanta team-total projection.

Atlanta also scored **42 points in the second half**, exactly matching the frozen remaining-game projection.

Therefore:

- ATL TT projection error: **0**
- ATL 2H projection error: **0**
- Executed strike: 84.5
- Actual ATL total: 78
- Cover margin: **6.5 points**

The full-game projection was less accurate because Los Angeles underperformed the model:

- Projected: ATL 78, LAS 79 — 157
- Actual: ATL 78, LAS 71 — 149
- ATL error: 0
- LAS error: -8
- Total error: -8

This matters because the investment was not a full-game total position. The targeted variable — Atlanta scoring — was calibrated exactly.

## Why the Under Held
Atlanta's first-half profile suggested some scoring regression, but the model did not require an explosive second half. The Dream ultimately scored 42 after halftime, exactly as projected.

The underlying path was consistent with the model's restraint:

- Atlanta finished only 6/29 from three (20.7%).
- Rhyne Howard finished 2/12 from three and carried five fouls.
- Atlanta generated strong offensive-rebound volume, finishing with 15 offensive boards, but converted only nine second-chance points.
- Angel Reese dominated the glass with 26 rebounds, including eight offensive rebounds, yet finished with only 11 points on 4/14 shooting.
- Atlanta's second-half scoring came more from interior conversion and free throws than from perimeter normalization.
- The Dream scored 26 in the third quarter but only 16 in the fourth, preventing late-game acceleration above the model center.

The model correctly separated **opportunity generation** from **actual scoring efficiency**. Atlanta had enough volume to avoid collapsing, but not enough efficient perimeter production to threaten the 84.5 strike.

## Execution Postmortem — LADDER_DOWN_FOR_PRICE
This game is a strong validation of the **LADDER_DOWN_FOR_PRICE** concept.

The original 87.5 Under offered more cushion but demanded -263. The alternate 84.5 Under reduced the cushion by three points but preserved a 6.5-point gap to the frozen projection while improving the price all the way to +101.

The final score landing at 78 demonstrates why model-center distance matters. SharpEdge did not need the full 9.5-point cushion at 87.5. The alternate strike still sat far enough above the model center to preserve meaningful protection.

This does **not** mean every heavily juiced edge should be laddered. The rule remains conditional:

1. Freeze the model before viewing price.
2. Identify the primary directional edge.
3. Reject prices beyond the standard threshold unless a documented exception is justified.
4. Search alternate strikes only in the same direction.
5. Preserve a meaningful distance between the alternate strike and frozen model center.
6. Log the exact executed price, cost, payout, and break-even probability.

## Model-Learning Notes
### Positive
- Atlanta team-total center was exact.
- Atlanta second-half scoring was exact.
- The model correctly resisted overreacting to extreme first-half three-point inefficiency.
- Atlanta's offensive-rebound edge was correctly recognized as a floor-support mechanism rather than automatic scoring explosion.
- Howard foul trouble was appropriately tagged as volatility against aggressive upside assumptions.
- Price-sensitive execution materially improved expected economics versus the original -263 market.

### Calibration caution
The full-game total projection overestimated Los Angeles by eight points. Los Angeles finished 3/18 from three (16.7%), and several perimeter players remained inefficient rather than regressing toward neutral. Future LIVE-FLOW calibration should continue separating team-specific regression signals rather than forcing both sides toward symmetric shooting normalization.

## Classification
- Primary model call: Atlanta TT Under
- Executed derivative: Atlanta Under 84.5
- Price type: Plus money
- Price threshold: Within standard cap
- Execution style: Alternate-line ladder
- Projection quality on targeted variable: Exact
- Investment result: WIN
- Profit: +$19.79
- ROI: +101.02%

## Frozen Tags
- LIVE_FLOW_POSTMORTEM
- LIVE_FLOW_HALFTIME_STRIKE
- MARKET_BLIND_PROJECTION_FROZEN
- ATL_TEAM_TOTAL_UNDER
- ATL_MODEL_EXACT_HIT
- ATL_SECOND_HALF_EXACT_HIT
- ALT_LINE_EXECUTION
- LADDER_DOWN_FOR_PRICE
- MODEL_MARKET_DIVERGENCE_6_5
- PLUS_MONEY_ENTRY
- WITHIN_PRICE_THRESHOLD
- PRICE_LOGGING_REQUIRED
- KALSHI_POSITION
- TARGET_VARIABLE_CALIBRATION_EXACT
- LAS_REGRESSION_UNDERREALIZED
- CLOSED_WIN

```yaml
game_id: WNBA_2026-08-24_ATL_LAS
checkpoint: halftime
halftime_score:
  ATL: 36
  LAS: 37
market_blind: true
frozen_projection:
  ATL: 78
  LAS: 79
  total: 157
  ATL_2H: 42
  LAS_2H: 42
primary_market:
  ATL_TT: 87.5
  under_price: -263
executed_market:
  ATL_TT: 84.5
  position: UNDER
  kalshi_side: NO_OVER_84_5
  price: 101
  cost: 19.60
  payout: 39.39
  profit: 19.79
  roi: 1.0102
  break_even_probability: 0.4976
model_gap_at_entry: 6.5
final:
  ATL: 78
  LAS: 71
  total: 149
actual_ATL_2H: 42
projection_errors:
  ATL: 0
  LAS: -8
  total: -8
  ATL_2H: 0
result:
  side: WIN
  margin_to_executed_strike: -6.5
status: CLOSED
```
