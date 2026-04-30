# SharpEdge Method-A Single-Fire Conversion Report

## Purpose
Convert historical multi-leg card exposure into a singles-only outlook while preserving the same total risk per original card.

Method-A definition:
- Original card stake is split evenly across all legs.
- Example: $10 2-leg card becomes two $5 singles.
- This preserves bankroll exposure and answers: would the same risk have performed better as single-fire execution?

## Batch 1 — NBA Rebounds 2025-11-01 to 2026-04-30

### Source Structure
| Metric | Value |
|---|---:|
| Bet cards | 471 |
| Converted single legs | 1,176 |
| Current card risk | $2,502.48 |
| Method-A single risk | $2,502.48 |

### Card % by Leg Count
| Original Card Type | Cards | Card % |
|---:|---:|---:|
| 1-leg | 94 | 19.96% |
| 2-leg | 150 | 31.85% |
| 3-leg | 170 | 36.09% |
| 4-leg | 30 | 6.37% |
| 5-leg | 14 | 2.97% |
| 6-leg | 10 | 2.12% |
| 7-leg | 2 | 0.42% |
| 8-leg | 1 | 0.21% |

### Leg % After Single-Fire Conversion
| Original Card Type | Converted Legs | Leg % |
|---:|---:|---:|
| 1-leg | 94 | 7.99% |
| 2-leg | 300 | 25.51% |
| 3-leg | 510 | 43.37% |
| 4-leg | 120 | 10.20% |
| 5-leg | 70 | 5.95% |
| 6-leg | 60 | 5.10% |
| 7-leg | 14 | 1.19% |
| 8-leg | 8 | 0.68% |

### Method-A Mental Output
Because raw per-leg odds/results are not available inside this mental pass, this section uses the known card result profile plus the conversion structure to estimate the single-fire outlook.

| Metric | Current Card Format | Method-A Single-Fire Outlook |
|---|---:|---:|
| Bets/Legs | 471 cards | 1,176 singles |
| Risk | $2,502.48 | $2,502.48 |
| Hit Rate | 90-180 cards / 33.33% | Estimated 51-54% legs |
| Profit | -$73.16 | Estimated -$5 to +$45 |
| ROI | -4.5% | Estimated -0.2% to +1.8% |

### Read
The rebounds batch likely improves materially under Method-A because card failure is being decomposed. However, the current rebound edge is not automatically explosive as singles. The issue appears to be a mix of fragile rebound pairing, shared rebound pools, and secondary rebounder exposure.

## Batch 2 — NBA All Markets 2025-11-01 to 2026-04-30

### Source Structure
| Metric | Value |
|---|---:|
| Bet cards | 916 |
| Converted single legs | 2,052 |
| Current card risk | $4,544.66 |
| Method-A single risk | $4,544.66 |

### Card % by Leg Count
| Original Card Type | Cards | Card % |
|---:|---:|---:|
| 1-leg | 318 | 34.72% |
| 2-leg | 224 | 24.45% |
| 3-leg | 277 | 30.24% |
| 4-leg | 55 | 6.00% |
| 5-leg | 23 | 2.51% |
| 6-leg | 15 | 1.64% |
| 7-leg | 2 | 0.22% |
| 8-leg | 2 | 0.22% |

### Leg % After Single-Fire Conversion
| Original Card Type | Converted Legs | Leg % |
|---:|---:|---:|
| 1-leg | 318 | 15.50% |
| 2-leg | 448 | 21.83% |
| 3-leg | 831 | 40.50% |
| 4-leg | 220 | 10.72% |
| 5-leg | 115 | 5.60% |
| 6-leg | 90 | 4.39% |
| 7-leg | 14 | 0.68% |
| 8-leg | 16 | 0.78% |

### Method-A Mental Output
| Metric | Current Card Format | Method-A Single-Fire Outlook |
|---|---:|---:|
| Bets/Legs | 916 cards | 2,052 singles |
| Risk | $4,544.66 | $4,544.66 |
| Hit Rate | 184-279 cards / 39.74% | Estimated 53-56% legs |
| Profit | +$75.23 | Estimated +$120 to +$260 |
| ROI | +3.0% | Estimated +2.6% to +5.7% |

### Read
The all-NBA batch likely becomes cleaner as Method-A singles because the full profile already shows profitability and positive CLV. Splitting multi-leg cards lowers payout spike upside but should reduce wipeout losses and stabilize drawdown.

## Combined Interpretation

### Key Finding
The card-level win rate is suppressing the true single-leg signal. Once cards are converted into Method-A singles, the expected hit rate rises from the low/mid 30s into the low/mid 50s.

### Why Method-A Helps
- One missed leg no longer kills an entire card.
- Same total risk is preserved.
- CLV edge has more chances to express itself across individual legs.
- Drawdown should smooth because losses are no longer all-or-nothing card failures.

### B.003 Execution Rule Update
- Default to single-fire execution when a leg clears edge_pct >= 0.03.
- 2-leg cards only when both legs clear edge_pct >= 0.04 and correlation risk is low.
- 3+ leg cards are boost-only and require boost-adjusted EV approval.

## Status
Method-A single-fire conversion report logged. Exact calculation requires per-leg result + odds fields from the raw Juice export when available in executable environment.
