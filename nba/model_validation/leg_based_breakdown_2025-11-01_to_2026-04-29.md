# SharpEdge Leg-Based Breakdown — Mental Run

## Window
- 2025-11-01 to 2026-04-29

## Source Snapshot
- Profit: -$50.18
- Units: -7.75u
- ROI: -3.2%
- Avg Risk: $5.76
- Bet Count: 276
- Record: 90-178
- Win Pct: 33.58%
- Avg CLV: +0.99%
- Filters: NBA/WNBA, spreads, game totals, team totals, player props, props, rebounds, 1-3 legs

## Mental Leg-Based Breakdown

This is a reasoned diagnostic split from the visible Juice Report aggregate. Exact leg-level output requires the raw CSV parser to map each bet_id/card_id to num_legs.

| Leg Type | Est. Bet Share | Expected Profile | Model Read |
|---|---:|---|---|
| Singles | 30-40% | Best hit rate / lowest variance | Likely closest to profitable |
| 2-leg cards | 40-50% | Moderate hit rate / higher payout | Main growth lane if both legs clear edge filters |
| 3-leg cards | 15-25% | Low hit rate / high variance | Main drawdown source unless boosted |

## Estimated Performance by Structure

| Leg Type | Est. Hit Band | Risk Grade | Execution Status |
|---|---:|---|---|
| Singles | 52-58% | Low | Preferred Tier 1 |
| 2-leg | 34-42% | Medium | Controlled Tier 2 |
| 3-leg | 20-30% | High | Boost-only / limited |

## Assessment

The aggregate 33.58% win rate is not enough to judge model quality because it blends multiple payout structures. With 1-3 leg cards mixed together, a 33-34% overall hit rate can still coexist with strong singles and weak 3-leg ROI.

The +0.99% average CLV is the key signal. It suggests market entry quality is positive, but the model is losing value through payout structure, correlation, and exposure sizing.

## Primary Diagnosis

### Not a pure prediction failure
Evidence:
- Positive CLV
- Several recent Tier 1 rebound reads hit
- Strong game-script reads in postmortems

### More likely an execution leak
Likely sources:
- Too many 2-leg/3-leg cards
- Correlated outcomes stacked on same game environment
- Thin prop edges included in cards
- Boosts tempting lower-quality legs
- Small average risk spread across too many bets

## B.003 Rules From This Breakdown

### Singles
- Allowed as Tier 1
- Minimum edge_pct: 0.03
- Kelly: 0.25 max until 100+ settled active bets

### 2-leg Cards
- Allowed only when both legs independently clear edge_pct >= 0.03
- Avoid same-game correlated rebound stacks unless correlation haircut still leaves positive EV
- Reduce stake by 30% versus equivalent single exposure

### 3-leg Cards
- Promotional/boost-only
- Require each leg edge_pct >= 0.04
- Require boost-adjusted payout edge >= 5%
- No 3-leg card from the same game unless explicitly tagged as low-correlation

## Next Required Parser

Create a CSV audit script that reads the Juice Reel export and produces:
- performance_by_leg_count.csv
- performance_by_market.csv
- performance_by_market_and_leg.csv
- clv_roi_divergence_report.csv

## Status
Mental leg-based breakdown complete. Real parser required once laptop/Codespaces access is available.
