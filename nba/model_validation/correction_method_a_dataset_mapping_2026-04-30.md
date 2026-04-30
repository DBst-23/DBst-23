# Correction Log — Method-A Dataset Mapping

## Correction Label
`METHOD_A_DATASET_MAPPING_CORRECTION_2026-04-30`

## Issue
A prior interpretation mislabeled the Method-A visual/output that showed 1,176 converted single legs as the full NBA dataset.

## Correct Mapping

| File | Scope | Converted Single Legs |
|---|---|---:|
| `NBA_bets_rebounds_11-1-25_4-30-26` | NBA rebounds only | 1,176 |
| `NBA_bets_11-1-25_4-30-26` | All NBA bet types | 2,052 |

## Correct Rebound-Only Output

The graphic/output with these values belongs to the rebounds-only batch:

| Metric | Value |
|---|---:|
| Profit Method-A | +$132.48 |
| Units | +26.50u |
| ROI | +5.29% |
| Avg. Risk | $2.13 |
| Converted Single Legs | 1,176 |
| Record Legs | 628-548 |
| Leg Hit Rate | 53.40% |
| Max Win | $58.46 |
| Max Loss | -$25.54 |
| Avg. CLV | +1.01% |

## Correct Card vs Method-A Comparison

| Format | Profit | Units | ROI | Hit Rate | Count |
|---|---:|---:|---:|---:|---:|
| Parlay Cards | -$73.16 | -11.31u | -4.5% | 33.33% | 278 |
| Method-A Legs | +$132.48 | +26.50u | +5.29% | 53.40% | 1,176 |

## Updated Interpretation

The rebounds model is not the core leak when viewed as individual single-fire legs. The negative card-format ROI appears to be driven by execution structure:

- multi-leg rebound cards,
- shared rebound pools,
- same-game correlation,
- one-leg failure wiping out the entire card,
- parlay volatility tax.

## Operational Impact

This strengthens the B.004 transition case:

- Rebounds should remain a core market.
- Default execution should shift to single-fire.
- Rebound parlays require strict correlation checks.
- 2-leg rebound cards need higher thresholds.
- 3+ leg rebound cards should be boost-only.

## Status
Correction logged and dataset mapping clarified.
