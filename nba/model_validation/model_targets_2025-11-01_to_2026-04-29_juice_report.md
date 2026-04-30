# SharpEdge Model Target Audit — Juice Report

## Window
- Placed: 2025-11-01 to 2026-04-29
- Closed: 2025-11-01 to 2026-04-29
- Snapshot timestamp: 2026-04-29 8:10 PM PDT

## Filters Shown
- NBA
- WNBA
- Spread
- Game Total
- Team Total
- Player Prop
- Prop
- Rebounds
- Number of legs: 1 to 3

## Juice Report Metrics

| Metric | Value |
|---|---:|
| Profit | -$50.18 |
| Units | -7.75u |
| ROI | -3.2% |
| Avg. Risk | $5.76 |
| Bet Count | 276 |
| Record | 90-178 |
| Win Pct | 33.58% |
| Max Win | $58.46 |
| Max Loss | -$25.54 |
| Avg. CLV | +0.99% |

## Immediate Model Read
The filtered historical profile is negative ROI but positive average CLV. This is a critical split.

Interpretation:
- The market-beating component is present: +0.99% average CLV.
- Execution and card construction are leaking ROI: -3.2% ROI.
- The low win percentage is partly explained by 1-3 leg card construction, not necessarily single-bet prediction failure.
- The model should separate singles from 2-leg and 3-leg cards before judging true edge.

## Priority Diagnostics

### 1. Separate by leg count
Required reports:
- Singles only
- 2-leg cards
- 3-leg cards

Reason:
The record of 90-178 across mixed legs does not tell us whether the model has a single-market edge. It blends straight bets with multiplier volatility.

### 2. Separate by market type
Required reports:
- Rebounds
- Spreads
- Game totals
- Team totals
- Other player props

Reason:
The visible filter includes multiple market types. We need to isolate where the model wins and where it leaks.

### 3. Evaluate positive CLV but negative ROI bucket
Required flags:
- CLV_WIN_ROI_LOSS
- VARIANCE_OR_PAYOUT_STRUCTURE_LEAK
- CARD_CONSTRUCTION_AUDIT_REQUIRED

Reason:
Positive CLV with negative ROI can mean either variance, correlated-leg failure, or overexposure to low probability multipliers.

## Patch Direction

### Execution Rule
Until enough data proves otherwise:
- Singles are preferred for Tier 1.
- 2-leg cards require both legs to clear >= 3% edge.
- 3-leg cards are treated as promotional/boost-only unless the combined model EV clears a higher threshold.

### Minimum Edge Rules
- Single: edge_pct >= 0.03
- 2-leg: each leg edge_pct >= 0.03 and combined EV positive after correlation haircut
- 3-leg: each leg edge_pct >= 0.04 and boost-adjusted payout must beat fair price by >= 5%

### Bankroll Rule
- Keep quarter-Kelly max until at least 100 settled EDGE_CALL_ACTIVE bets are logged under the new B.003 filter set.

## Status
Logged for model validation and future filtering.
