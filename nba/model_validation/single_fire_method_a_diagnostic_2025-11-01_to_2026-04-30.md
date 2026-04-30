# SharpEdge Diagnostic — Method-A Single-Fire Conversion

## Diagnostic Label
`SINGLE_FIRE_METHOD_A_DIAGNOSTIC_2025-11-01_TO_2026-04-30`

## Purpose
This diagnostic compares the historical card/parlay betting structure against a single-fire execution model while preserving the same total bankroll risk.

Method-A answers this question:

> If every historical card leg had been played as its own single, while splitting the original card stake evenly across legs, would the system perform better?

## Source Batches

### Batch 1
`NBA_bets_rebounds_11-1-25_4-30-26`

### Batch 2
`NBA_bets_11-1-25_4-30-26`

---

# Method-A Definition

Original multi-leg stake is split evenly across all legs.

Examples:

| Original Card | Original Risk | Method-A Conversion |
|---|---:|---|
| 1-leg | $10 | 1 single at $10 |
| 2-leg | $10 | 2 singles at $5 each |
| 3-leg | $10 | 3 singles at $3.33 each |

This preserves total bankroll exposure while removing parlay wipeout risk.

---

# Batch 1 — NBA Rebounds

## Structure

| Metric | Value |
|---|---:|
| Bet cards | 471 |
| Converted single legs | 1,176 |
| Current card risk | $2,502.48 |
| Method-A single risk | $2,502.48 |

## Card % by Leg Count

| Card Type | Cards | Card % |
|---:|---:|---:|
| 1-leg | 94 | 19.96% |
| 2-leg | 150 | 31.85% |
| 3-leg | 170 | 36.09% |
| 4-leg | 30 | 6.37% |
| 5-leg | 14 | 2.97% |
| 6-leg | 10 | 2.12% |
| 7-leg | 2 | 0.42% |
| 8-leg | 1 | 0.21% |

## Leg % After Single-Fire Conversion

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

## Method-A Outlook

| Metric | Card Format | Method-A Singles |
|---|---:|---:|
| Risk | $2,502.48 | $2,502.48 |
| Bets | 471 cards | 1,176 singles |
| Win % | 33.33% | ~51–54% |
| Profit | -$73.16 | ~-$5 to +$45 |
| ROI | -4.5% | ~-0.2% to +1.8% |

## Read
The rebounds-only batch appears structurally damaged by multi-leg construction. The raw single-leg quality is likely near breakeven to slightly profitable, but parlay/card format converts modest edge into negative ROI.

Primary issue:
- Rebound legs are often not independent.
- Multiple rebound legs can share the same miss pool, pace environment, and frontcourt possession tree.
- One failed rebound leg wipes out the entire card.

---

# Batch 2 — Full NBA

## Structure

| Metric | Value |
|---|---:|
| Bet cards | 916 |
| Converted single legs | 2,052 |
| Current card risk | $4,544.66 |
| Method-A single risk | $4,544.66 |

## Card % by Leg Count

| Card Type | Cards | Card % |
|---:|---:|---:|
| 1-leg | 318 | 34.72% |
| 2-leg | 224 | 24.45% |
| 3-leg | 277 | 30.24% |
| 4-leg | 55 | 6.00% |
| 5-leg | 23 | 2.51% |
| 6-leg | 15 | 1.64% |
| 7-leg | 2 | 0.22% |
| 8-leg | 2 | 0.22% |

## Leg % After Single-Fire Conversion

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

## Method-A Outlook

| Metric | Card Format | Method-A Singles |
|---|---:|---:|
| Risk | $4,544.66 | $4,544.66 |
| Bets | 916 cards | 2,052 singles |
| Win % | 39.74% | ~53–56% |
| Profit | +$75.23 | ~$120 to +$260 |
| ROI | +3.0% | ~+2.6% to +5.7% |

## Read
The full NBA batch already shows profitability in card format. Method-A likely improves stability by allowing the positive CLV and single-leg edge to express itself without parlay wipeout loss.

Primary improvement:
- Lower drawdown.
- Higher realized hit rate.
- Less dependence on one full card completing.
- Smoother bankroll curve.

---

# Key Diagnostic Findings

## 1. The model is not purely broken
The full NBA batch is already profitable:

| Metric | Value |
|---|---:|
| Profit | +$75.23 |
| Units | +11.63u |
| ROI | +3.0% |
| Avg CLV | +1.01% |

This supports the existence of a real market-entry edge.

## 2. Rebounds are not bad, but the structure is damaging
The rebounds-only batch:

| Metric | Value |
|---|---:|
| Profit | -$73.16 |
| Units | -11.31u |
| ROI | -4.5% |
| Avg CLV | +0.99% |

Positive CLV with negative ROI suggests the issue is likely structure, correlation, or variance rather than simple bad market reads.

## 3. Multi-leg sourced exposure dominates the dataset
Full NBA batch single-fire conversion:

| Source | Leg Share |
|---|---:|
| 3-leg source | 40.50% |
| 2-leg source | 21.83% |
| 1-leg source | 15.50% |

Rebounds batch single-fire conversion:

| Source | Leg Share |
|---|---:|
| 3-leg source | 43.37% |
| 2-leg source | 25.51% |
| 1-leg source | 7.99% |

The system has been heavily exposed to multi-leg sourced volatility.

---

# SharpEdge B.004 Execution Patch

## Default execution mode
Single-fire is the primary execution layer.

```python
if edge_pct >= 0.03:
    execution_type = "single_fire"
```

## 2-leg restriction

```python
if number_of_legs == 2:
    allow = (
        each_leg_edge >= 0.04
        and correlation_risk == "LOW"
        and shared_rebound_pool is False
    )
```

## 3+ leg restriction

```python
if number_of_legs >= 3:
    allow = (
        payout_boost is True
        and each_leg_edge >= 0.04
        and no_thin_leg is True
        and correlation_risk != "HIGH"
    )
```

## Rebound-specific correlation guard

```python
if market == "rebounds" and same_game_card:
    apply_correlation_haircut = True

if shared_rebound_pool:
    downgrade_prob -= 0.04
```

---

# Operational Conclusion

The clearest path forward is not to find more plays. It is to preserve the edge by changing execution.

## Going forward
- Tier 1 = singles only.
- 2-leg cards = restricted.
- 3+ leg cards = boost/multiplier only.
- Rebound cards require shared-pool correlation checks.
- Method-A should become the baseline backtest mode for future audits.

## Status
Diagnostic logged into GitHub for SharpEdge B.004 transition planning.
