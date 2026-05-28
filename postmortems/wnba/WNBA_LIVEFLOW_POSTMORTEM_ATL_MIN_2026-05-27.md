# WNBA LiveFlow Postmortem — ATL Dream @ MIN Lynx

**Game ID:** WNBA_ATL_MIN_2026-05-27  
**Date:** 2026-05-27  
**Venue:** Target Center, Minneapolis, MN  
**Final:** MIN 96, ATL 81  
**Logged Folder:** `postmortems/wnba/`  
**LiveFlow Result:** WIN ✅  
**Ticket:** No — Atlanta wins by over 1.5 points  
**Entry:** $5 at -104  
**Payout:** $9.81  
**Net:** +$4.81 / +96.2%

---

## 1. LiveFlow Position Summary

### Bet Logged

```yaml
market: Dream vs Lynx Spread
position: No — Atlanta wins by over 1.5 points
entry_price: -104
stake: 5.00
payout: 9.81
result: WIN
final_score:
  ATL: 81
  MIN: 96
margin: MIN +15
```

### Model Read at Entry

The LiveFlow strike was made after Atlanta erased Minnesota’s early control and tied the game at **26–26** in the 2nd quarter. Despite the tie, the model read was not Atlanta momentum — it was **Minnesota stabilization risk**.

Primary reasons:

- Minnesota opened with a dominant 23–14 first quarter.
- Atlanta’s comeback was three-point driven, not paint/control driven.
- Minnesota still had stronger interior efficiency and starter creation.
- Atlanta’s turnover profile remained fragile.
- The wager was not Minnesota moneyline; it was fading Atlanta by 2+ points.

---

## 2. Score Phase Breakdown

| Segment | ATL | MIN | Margin | Key Read |
|---|---:|---:|---:|---|
| 1Q | 14 | 23 | MIN +9 | Minnesota controlled opening script |
| 2Q | 23 | 19 | MIN +5 at half | Atlanta three-point correction closed gap |
| 3Q | 19 | 28 | MIN +14 | Decisive Lynx separation phase |
| 4Q | 25 | 26 | MIN +15 final | Minnesota maintained cushion |

### Critical Swing

The key phase was early 3Q. Minnesota led **44–40** before producing a **13–0 run**, extending the game to **57–40**. That run validated the LiveFlow fade of Atlanta’s comeback sustainability.

---

## 3. Team Efficiency + Game Environment

### Minnesota Lynx

```yaml
points: 96
fg: 40-67
fg_pct: 59.7
three_pt: 7-19
three_pct: 36.8
ft: 9-10
ft_pct: 90.0
assists: 26
turnovers: 14
points_in_paint: 52
second_chance_points: 15
fastbreak_points: 6
```

Minnesota’s edge was not volume. It was execution. The Lynx generated **26 assists on 40 made field goals**, shot nearly **60%**, and created **52 paint points**. That is a premium half-court offensive signal, especially because Atlanta could not force Minnesota into enough empty possessions.

### Atlanta Dream

```yaml
points: 81
fg: 29-65
fg_pct: 44.6
three_pt: 11-31
three_pct: 35.5
ft: 12-16
ft_pct: 75.0
assists: 23
turnovers: 16
points_in_paint: 36
second_chance_points: 11
fastbreak_points: 4
```

Atlanta’s scoring profile leaned heavily on perimeter makes. They hit **11 threes**, but Minnesota dominated the interior scoring gap by **+16 paint points** and won the shot quality battle.

---

## 4. Player Driver Review

### Minnesota Primary Drivers

| Player | Final Line | Model Impact |
|---|---:|---|
| Courtney Williams | 25 PTS, 7 AST, 10-15 FG | Primary shot creator; late-clock closer |
| Natasha Howard | 22 PTS, 8 REB, 5 AST, 11-16 FG | Interior efficiency engine |
| Olivia Miles | 16 PTS, 8 AST, 5 REB | Stabilized pace and creation |
| Nia Coffey | 14 PTS, 5 REB, 2-5 3PT | Early spacing + tone-setting |
| Kayla McBride | 12 PTS, 3 STL | 4Q separation support |

### Atlanta Primary Drivers

| Player | Final Line | Model Impact |
|---|---:|---|
| Allisha Gray | 21 PTS, 5-8 3PT | Main reason Atlanta stayed live |
| Naz Hillmon | 15 PTS, 8 REB | Interior support but not enough rim pressure |
| Angel Reese | 10 PTS, 8 REB, 5 AST | Active but did not own glass enough |
| Rhyne Howard | 10 PTS, 4-14 FG | Inefficiency capped Atlanta ceiling |
| Jordin Canada | 9 PTS, 5 AST, 4 TOV | Playmaking offset by turnover pressure |

---

## 5. LiveFlow Edge Validation

### Why the Bet Won

The position won because the model correctly separated **scoreboard tie** from **true game control**.

At 26–26, Atlanta had regained score parity, but the underlying structure still favored Minnesota:

```yaml
liveflow_signal:
  atlanta_comeback_type: perimeter_make_driven
  minnesota_advantage_type: paint_efficiency_and_assist_quality
  atlanta_risk: turnover_fragility
  minnesota_risk: temporary ball-security dip
  model_call: fade_atlanta_by_2_plus
  result: confirmed
```

### Market Edge

The price at **-104** was within threshold. The market was giving near-even pricing on Atlanta not winning by 2+ despite Minnesota showing superior interior shot quality and opening control.

```yaml
entry_price: -104
estimated_live_probability: 58-62%
implied_probability: 51.0%
estimated_edge: +7% to +11%
confidence_tier: strong
```

---

## 6. Rebound Environment Analysis

### Team Rebounds

| Team | Total REB | OREB | DREB |
|---|---:|---:|---:|
| ATL | 27 | 10 | 17 |
| MIN | 24 | 5 | 19 |

Atlanta technically won raw rebounds, but this was not a positive game-control signal. Their rebound edge came from Minnesota’s high efficiency reducing available defensive boards and Atlanta’s missed-shot volume creating more offensive rebound chances.

### Rebound Interpretation

```yaml
rebound_signal: misleading_raw_edge
atl_rebounds: inflated_by_missed_shot_environment
min_rebounds: suppressed_by_high_fg_efficiency
true_control: minnesota_paint_efficiency
```

### Patch Note

For future WNBA LiveFlow reads, raw rebound edge should be downgraded when:

- Opponent shoots 58%+ from field.
- Rebound edge is paired with a double-digit deficit.
- Offensive rebound chances are created by inefficient offense rather than physical control.

Recommended tag:

```yaml
RAW_REBOUND_EDGE_MISLEADING_WHEN_OPP_EFG_SPIKE: ACTIVE
```

---

## 7. Momentum + Tactical Notes

### Minnesota

- Controlled the first quarter with early shot quality and defense.
- Lost some control in Q2 due to turnovers and Atlanta three-point variance.
- Re-established dominance immediately in Q3.
- Closed with enough offensive stability to prevent Atlanta from threatening spread outcome.

### Atlanta

- Comeback was sharp but fragile.
- Relied on Gray perimeter shooting.
- Could not generate enough rim pressure or force enough misses.
- Turnovers directly fueled the 3Q collapse.

---

## 8. Patch Evaluation

### Keep

```yaml
LIVEFLOW_SCOREBOARD_PARITY_FILTER: KEEP
```

This game strongly supports not overreacting to a tied score when the underlying shot quality and possession control still lean the other side.

### Modify

```yaml
RAW_REBOUND_EDGE_WEIGHTING: MODIFY
```

Atlanta’s rebound profile looked competitive, but the environment showed it was partly miss-volume driven. Add efficiency context before treating rebound margin as control.

### Add

```yaml
THIRD_QUARTER_REASSERTION_GATE_WNBA: ADD
```

Minnesota’s 13–0 third-quarter run was the decisive validation. When a home favorite/quality side controls Q1, gets tied in Q2, then opens Q3 with paint touches + forced turnovers, LiveFlow should raise probability sharply.

---

## 9. Retraining Flags

```yaml
retraining_flags:
  - LIVEFLOW_TIE_SCORE_NOT_EQUAL_CONTROL
  - PERIMETER_COMEBACK_VOLATILITY
  - RAW_REBOUND_EDGE_MISLEADING
  - THIRD_QUARTER_REASSERTION_GATE
  - PAINT_POINTS_CONTROL_SIGNAL
  - TURNOVER_TO_RUN_CONVERSION
```

---

## 10. Final Status

```yaml
final_status: KEEP_WITH_MODIFICATION
bet_result: WIN
model_result: SIGNAL_CONFIRMED
confidence: HIGH
folder: postmortems/wnba/
file: WNBA_LIVEFLOW_POSTMORTEM_ATL_MIN_2026-05-27.md
```

## Summary

This was a clean LiveFlow win. The model correctly identified that Atlanta’s comeback to 26–26 was not a true control flip. Minnesota’s superior shot quality, paint scoring, assist creation, and third-quarter reassertion produced a decisive 96–81 final. The main model improvement is to treat raw rebound edges carefully when they are created by missed-shot volume rather than actual board dominance.