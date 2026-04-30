# SharpEdge Method-A Output — Full NBA Batch

## Dataset
`NBA_bets_11-1-25_4-30-26`

## Scope
All NBA bet types from 2025-11-01 to 2026-04-30.

## Correct Dataset Mapping

| File | Scope | Converted Single Legs |
|---|---|---:|
| `NBA_bets_rebounds_11-1-25_4-30-26` | NBA rebounds only | 1,176 |
| `NBA_bets_11-1-25_4-30-26` | All NBA bet types | 2,052 |

---

# Full NBA Method-A Single-Fire Output

## True Leg Performance

| Metric | Value |
|---|---:|
| Profit Method-A | +$260.92 |
| Units | +52.18u |
| ROI | +5.74% |
| Avg. Risk | $2.21 |
| Converted Single Legs | 2,052 |
| Record Legs | 1,111-941 |
| Leg Hit Rate | 54.14% |
| Max Win | $78.36 |
| Max Loss | -$25.54 |
| Avg. CLV | +1.01% |

## Card vs Method-A Comparison

| Format | Profit | Units | ROI | Hit Rate | Count |
|---|---:|---:|---:|---:|---:|
| Parlay Cards | +$75.23 | +11.63u | +3.0% | 39.74% | 471 |
| Method-A Legs | +$260.92 | +52.18u | +5.74% | 54.14% | 2,052 |

---

# Diagnostic Read

The full NBA batch is already profitable in card format, but Method-A single-fire execution materially improves the profile.

## Key Improvements
- Profit improves from +$75.23 to approximately +$260.92.
- ROI improves from +3.0% to approximately +5.74%.
- Hit rate normalizes from card-level 39.74% to leg-level 54.14%.
- Total exposure is preserved by splitting original card risk evenly across legs.
- Positive CLV remains aligned at approximately +1.01%.

## Interpretation
The full NBA model is showing a valid positive-EV profile. The all-market engine appears stronger than the rebounds-only subset, but both improve significantly when converted to single-fire Method-A execution.

This confirms that the core model does not require a full rebuild. The bigger upgrade is execution architecture.

---

# Operational Conclusion

## B.004 Single-Fire Default

```python
if edge_pct >= 0.03:
    execution_type = "single_fire"
```

## Multi-Leg Restriction

```python
if number_of_legs >= 2:
    allow = (
        each_leg_edge >= 0.04
        and correlation_risk == "LOW"
        and no_thin_leg is True
    )
```

## 3+ Leg Rule

```python
if number_of_legs >= 3:
    allow = (
        payout_boost is True
        and boost_adjusted_ev >= 0.05
        and correlation_risk != "HIGH"
    )
```

---

# Status
Full NBA Method-A output logged for B.004 execution transition.
