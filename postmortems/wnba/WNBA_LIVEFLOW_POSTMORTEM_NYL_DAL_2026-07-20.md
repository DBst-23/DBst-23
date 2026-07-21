# WNBA LiveFlow Postmortem — New York Liberty @ Dallas Wings

```yaml
postmortem_id: WNBA_LIVEFLOW_POSTMORTEM_NYL_DAL_2026-07-20
league: WNBA
date: 2026-07-20
matchup: New York Liberty @ Dallas Wings
venue: College Park Center
market: Live full-game total
position: Over 179.5
entry_price: -115
stake: 10.00
payout: 18.70
profit: 8.70
result: WIN
final_score: Liberty 99, Wings 98 (OT)
final_total: 197
regulation_score: 83-83
regulation_total: 166
overtime_total: 31
cover_margin_final: 17.5
cover_margin_regulation: -13.5
entry_timing: user-reported first portion of Q3
entry_method: blind line-watch investment; no full gamebook confirmation at entry
```

## Ticket

- **Position:** Over 179.5 live total
- **Price:** -115
- **Stake:** $10.00
- **Return:** $18.70
- **Profit:** +$8.70
- **Final:** 197 points after overtime
- **Settlement:** Win by 17.5 points

## Game Flow

| Segment | Liberty | Wings | Total | Read |
|---|---:|---:|---:|---|
| Q1 | 25 | 22 | 47 | Strong opening scoring environment |
| Q2 | 25 | 25 | 50 | First half remained efficient and competitive |
| 1H | 50 | 47 | 97 | Healthy over pace before the live entry window |
| Q3 | 9 | 21 | 30 | Liberty offensive collapse created the apparent live-total discount |
| Q4 | 24 | 15 | 39 | Regulation recovery was insufficient for 179.5 |
| Regulation | 83 | 83 | 166 | Ticket was 13.5 points short without overtime |
| OT | 16 | 15 | 31 | Overtime fully rescued and cleared the wager |
| Final | 99 | 98 | 197 | Official win |

## Core Diagnosis

The ticket won, but the underlying regulation thesis did not.

The line-watch read identified a live total that appeared compressed after New York's third-quarter scoring collapse. That instinct had a legitimate regression basis: New York entered halftime with 50 points, then produced only 9 in Q3 while shooting 3-of-18 from the field and 0-of-5 from three. A rebound from that extreme offensive trough was reasonable.

However, the wager still required 180 total points and regulation finished at only 166. The game needed a tie at 83-83 and a 31-point overtime period to cash. Therefore, this must be recorded as an **outcome win but regulation-process miss** rather than a clean predictive victory.

```yaml
tag_result:
  primary_tag: OT_RESCUE_OVER
  secondary_tags:
    - BLIND_LINE_WATCH_ENTRY
    - REGULATION_THESIS_FAILED
    - THIRD_QUARTER_TOTAL_COMPRESSION
    - OFFENSIVE_REGRESSION_SIGNAL
    - CLOSE_GAME_OT_OPTIONALITY
    - RESULT_PROCESS_DIVERGENCE
```

## What Supported the Over Read

### 1. Strong first-half scoring base

The teams scored 97 first-half points despite only 15 combined turnovers through halftime. Dallas shot 54.1% from the field and 50% from three, while New York produced 50 points with strong interior and second-chance creation.

### 2. New York's Q3 collapse was extreme

```yaml
new_york_q3:
  points: 9
  fg: 3/18
  fg_pct: 16.7
  three_pt: 0/5
  turnovers: 3
  offensive_rebounds: 4
  read: severe short-window offensive suppression with regression potential
```

New York still generated 18 field-goal attempts and four offensive rebounds in the quarter. The scoring collapse was driven more by conversion failure than by a complete loss of possessions.

### 3. Competitive game state preserved extension value

The game remained close enough to create late fouling, bonus free throws, and overtime optionality. It ultimately reached 83-83 after regulation and produced 31 overtime points.

## What the Blind Entry Missed

### 1. The line was not proven under-inflated

No pregame total, exact entry score, entry clock, possession count, or live projection was recorded. The conclusion that 179.5 was under-inflated was therefore subjective rather than model-confirmed.

### 2. Regulation scoring requirement remained demanding

Even with first-half pace, the ticket needed substantial second-half offense. The second half produced only 69 regulation points. The final regulation total of 166 demonstrates that the number was not actually beaten by normal game flow.

### 3. Third-quarter weakness was not isolated to one clean variable

New York's Q3 collapse offered regression upside, but Dallas also slowed. The teams combined for only 30 points in the quarter. A valid over entry required evidence that pace, shot quality, foul pressure, and primary scorers would all recover—not merely that the market number looked low.

### 4. Overtime dependency cannot be treated as repeatable edge

The game tied because of a rare late sequence involving fouls, offensive rebounds, missed shots, and free throws. Overtime counts for full-game basketball totals, but it is a high-variance settlement path, not a reliable base projection.

## Process Grade

```yaml
result_grade: A
price_grade: B
read_grade: C
execution_grade: C-
repeatability_grade: D+
overall_process_grade: C-
classification: profitable outcome; variance-assisted process
```

## Edge Audit

```yaml
market_line: 179.5
price: -115
break_even_probability: 53.49
final_total: 197
regulation_total: 166
overtime_total: 31
final_edge_realized: +17.5_points
regulation_edge_realized: -13.5_points
model_probability_at_entry: not recorded
model_mean_at_entry: not recorded
model_median_at_entry: not recorded
true_pre_bet_edge: unverified
```

Because no simulation or fair-line projection was recorded before the wager, probability, mean, median, and EV cannot be reconstructed honestly. The only defensible conclusion is that the ticket won while the regulation scoring path failed.

## Engine Patch — Live Over Compression Gate

```yaml
LIVE_OVER_COMPRESSION_GATE:
  purpose: prevent blind over entries based only on a falling live total

  required_inputs:
    - exact_score_and_clock
    - live_total_and_price
    - pregame_total_or_prior_live_peak
    - estimated_remaining_possessions
    - current_fg_and_3pt_profile
    - free_throw_and_bonus_state
    - turnover_rate
    - offensive_rebound_rate
    - active_closing_lineups

  minimum_confirmation_rules:
    - projected_mean >= market_line + 4.0
    - projected_median >= market_line + 2.5
    - over_probability >= 57_percent_at_minus_115
    - at_least_two_regression_signals_present
    - pace_or_possession_environment_not_collapsing
    - no_major_offensive_lineup_downgrade

  valid_regression_signals:
    - team_fg_pct <= 30_with_normal_shot_volume
    - team_3pt_pct <= 20_with_quality_attempt_volume
    - missed_open_shots_or_rim_attempts
    - strong_offensive_rebounding_sustaining_possessions
    - primary_creators_active_and_not_in_foul_trouble

  danger_filters:
    - both_teams_halfcourt_stagnation
    - live_total_requires_top_decile_remaining_scoring
    - entry_based_only_on_visual_line_drop
    - one_team_missing_primary_creator
    - blowout_risk_reducing_late_foul_extension

  overtime_treatment:
    - include_only_as_tail_probability
    - never_use_as_base_case
    - tag_any_ticket_that_needs_ot_as_variance_assisted
```

## Model-Sharpening Takeaway

The useful instinct was recognizing that a 9-point New York quarter was unlikely to represent its true remaining-game scoring level. The mistake was converting that instinct directly into a wager without recording a fair total, probability distribution, or remaining-possession projection.

For future LIVE-FLOW entries, the line itself is only an alert. It is not the edge. The wager becomes actionable only after the model produces the mean, median, over probability, and EV against the exact live number.

## Final Assessment

**Official result:** Win.

**Model verdict:** Do not promote this as a clean LIVE-FLOW success. Regulation finished 13.5 points below the ticket line, and overtime supplied all of the winning margin. Preserve the observational skill—spotting compressed totals after an extreme cold stretch—but patch the workflow so no future investment is approved without exact clock, score, market, pace, and distributional confirmation.