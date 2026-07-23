# WNBA LiveFlow Postmortem — Dallas Wings @ Portland Fire

```yaml
postmortem_id: WNBA_LIVEFLOW_POSTMORTEM_DAL_POR_2026-07-22
league: WNBA
date: 2026-07-22
matchup: Dallas Wings @ Portland Fire
venue: Moda Center
market: Live full-game spread
position: Portland Fire +3.5
entry_price: -115
stake: 8.99
payout: 0.00
profit: -8.99
result: LOSS
entry_score: Portland 42, Dallas 40
entry_timing: halftime
final_score: Dallas 101, Portland 97
final_margin_from_portland_perspective: -4
cover_margin: -0.5
settlement: lost by half a point
```

## Ticket

- **Position:** Portland Fire +3.5 live spread
- **Price:** -115
- **Stake:** $8.99
- **Potential return:** $16.81
- **Potential profit:** $7.82
- **Final:** Dallas 101, Portland 97
- **Settlement:** Loss by 0.5 points

## Halftime Snapshot

```yaml
halftime_score:
  Portland: 42
  Dallas: 40
halftime_market:
  Portland_spread: +3.5
  Portland_price: -115
  Dallas_spread: -3.5
  Dallas_price: -115
  live_total: 171.5
  Dallas_team_total: 87.5
  Portland_team_total: 84.5
```

## Game Flow

| Segment | Dallas | Portland | Margin from Portland view | Read |
|---|---:|---:|---:|---|
| Q1 | 18 | 17 | -1 | Competitive start |
| Q2 | 22 | 25 | +2 | Portland entered halftime ahead |
| 1H | 40 | 42 | +2 | Ticket entered with Portland effectively +5.5 relative to game state |
| Q3 | 36 | 27 | -7 | Dallas offensive surge flipped control |
| Q4 | 25 | 28 | -4 final | Portland rallied but missed cover by 0.5 |
| Final | 101 | 97 | -4 | +3.5 lost narrowly |

## Core Diagnosis

The halftime position was logically supported by the live game state. Portland led 42-40 and was offered +3.5, creating an effective 5.5-point cushion from the entry score. The wager was not defeated by a broad read failure; it was defeated by a single high-efficiency Dallas third quarter and a final margin that landed one half-point outside the number.

Dallas won Q3 36-27 while shooting 62.5% from the field. Arike Ogunbowale scored 15 points in the quarter, Jessica Shepard controlled the interior and distribution, and Dallas generated 10 second-chance points in the period. Portland recovered to win Q4 28-25 and cut the deficit to two with 32 seconds left, but Dallas converted late free throws and the game settled at four.

```yaml
tag_result:
  primary_tag: HALF_POINT_SPREAD_LOSS
  secondary_tags:
    - HALFTIME_LIVEFLOW_ENTRY
    - EFFECTIVE_ENTRY_CUSHION_5_5
    - THIRD_QUARTER_OPPONENT_SURGE
    - SECOND_CHANCE_POINT_SWING
    - LATE_COVER_NEAR_MISS
    - PROCESS_RESULT_DIVERGENCE
```

## What Supported the Portland +3.5 Read

### 1. Favorable entry geometry

At halftime, Portland led by two while receiving +3.5. The live position therefore held an effective 5.5-point cushion against the score state.

### 2. Portland offensive efficiency was real

Portland shot 50.0% from the field in the first half and finished at 56.9% for the game. Its offense did not collapse after entry. Portland scored 55 second-half points and 97 overall.

### 3. Ball movement and interior scoring remained stable

Portland finished with 24 assists and 48 points in the paint. Carla Leite produced 11 assists, and Portland generated efficient offense across multiple lineups.

### 4. The team remained competitive through the final possession

Portland won Q4 28-25, forced six Dallas turnovers in the quarter, and cut the margin to 99-97 with 32 seconds remaining. The wager remained live until the final sequence.

## What Defeated the Position

### 1. Dallas produced a top-end third-quarter scoring burst

```yaml
dallas_q3:
  points: 36
  fg: 15/24
  fg_pct: 62.5
  three_pt: 4/9
  assists: 13
  turnovers: 1
  second_chance_points: 10
```

This was the decisive segment. Dallas converted at an elite rate while committing only one turnover.

### 2. Offensive rebounding created the hidden margin

Dallas finished with 16 second-chance points compared with Portland's 4. The 12-point differential exceeded the final four-point margin and was the clearest structural reason the spread failed.

### 3. Portland's defensive rebounding did not protect the halftime edge

Jessica Shepard recorded 15 rebounds, including six offensive boards, and Dallas finished with nine offensive rebounds. Portland's efficient shooting masked a major possession disadvantage.

### 4. Late recovery stopped just short of the number

Portland rallied from a 12-point fourth-quarter deficit and cut the game to two, but Dallas scored the final two free throws. The closing sequence turned a potential +3.5 cover into a four-point loss.

## Model vs Market Audit

```yaml
market_line_at_entry: Portland +3.5
price: -115
break_even_probability: 53.49
entry_score_margin_portland: +2.0
effective_cushion_at_entry: +5.5
final_margin_portland: -4.0
realized_cover_margin: -0.5
model_probability_at_entry: not preserved in source record
model_mean_margin_at_entry: not preserved in source record
model_median_margin_at_entry: not preserved in source record
true_pre_bet_edge: not fully auditable
```

The exact pre-bet simulation mean, median, cover probability, and EV were not preserved in the available record. Therefore, the model edge cannot be reconstructed honestly beyond the observed game-state cushion.

## CLV Audit

```yaml
entry_line: Portland +3.5
entry_price: -115
closing_or_last_available_live_line: not recorded
clv_points: not verifiable
clv_price: not verifiable
clv_result: UNVERIFIED
```

This record does **not** claim positive or negative CLV because no later market snapshot was preserved. Future LIVE-FLOW tickets must record the entry line and at least one subsequent comparable market line before settlement.

## Process Grade

```yaml
result_grade: F
price_grade: C
read_grade: B-
execution_grade: B-
repeatability_grade: B
clv_grade: incomplete
risk_grade: C+
overall_process_grade: B-
classification: defensible halftime position; narrow loss driven by Q3 variance and rebounding disadvantage
```

## Engine Patch — Live Spread Cushion and Rebounding Gate

```yaml
LIVE_SPREAD_CUSHION_GATE:
  required_inputs:
    - exact_score_and_clock
    - live_spread_and_price
    - current_possession_estimate
    - halftime_or_segment_rebounding_split
    - offensive_rebound_rate
    - turnover_rate
    - shot_quality_and_efficiency
    - active_second_half_rotation
    - foul_state
    - subsequent_market_snapshot_for_clv

  minimum_confirmation_rules:
    - effective_score_adjusted_cushion >= 4.0_points
    - projected_cover_probability >= 57_percent_at_minus_115
    - projected_mean_margin clears_market_by >= 2.5_points
    - projected_median_margin clears_market_by >= 1.5_points
    - no_severe_defensive_rebounding_disadvantage
    - no_major_primary_scorer_or_rotation_downgrade

  danger_filters:
    - opponent_offensive_rebound_rate_above_30_percent
    - one_team_dominating_second_chance_points
    - first_half_lead_built_on_unsustainably_low_opponent_turnovers_or_shooting
    - live_favorite_with_multiple_high_usage_creators_heating_up
    - no_clv_capture_snapshot
```

## Model-Sharpening Takeaway

The halftime spread geometry was attractive, but score-adjusted cushion alone was insufficient. The missing variable was possession control. Portland shot efficiently enough to win the game offensively, yet Dallas' offensive rebounding and third-quarter shot creation created extra possessions and erased the cushion.

For future LIVE-FLOW halftime spread entries, the model must combine score-adjusted spread value with rebounding, turnover, and possession projections. A team can hold a favorable live number and still be vulnerable if the opponent owns the possession economy.

## Final Assessment

**Official result:** Loss.

**Model verdict:** The position was defensible and missed by only half a point. Do not classify it as a bad read solely because it lost. However, do not classify it as a fully validated edge either because the pre-bet distribution and CLV snapshot were not preserved. The principal patch is to add possession-economy and mandatory CLV capture to every halftime spread entry.