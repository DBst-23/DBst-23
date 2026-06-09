# WNBA LiveFlow Postmortem — Portland Fire @ Los Angeles Sparks

```yaml
postmortem_id: WNBA_LIVEFLOW_POSTMORTEM_POR_LAS_2026-06-07
league: WNBA
date: 2026-06-07
matchup: Portland Fire @ Los Angeles Sparks
venue: Crypto.com Arena
market: No / Over 168.5 total points
entry_price: +158
stake: 5.00
payout: 12.94
profit: 7.94
result: WIN
final_score: Sparks 89, Fire 72
final_total: 161
closing_margin_vs_ticket: 7.5 points under
```

## Ticket

- **Position:** No — Over 168.5 points scored
- **Entry:** +158
- **Cost:** $5.00
- **Payout:** $12.94
- **Profit:** +$7.94
- **Outcome:** 161 final total
- **Result:** Win by 7.5 points under the ticket line

## Game Flow

| Segment | Fire | Sparks | Total | Read |
|---|---:|---:|---:|---|
| Q1 | 21 | 24 | 45 | Inflated by FT + second-chance scoring |
| Q2 | 22 | 17 | 39 | Pace cooled; under still live |
| 1H | 43 | 41 | 84 | Needed 84.5 or fewer in 2H |
| Q3 | 12 | 23 | 35 | Under thesis confirmed |
| Q4 | 17 | 25 | 42 | Comfortable close |
| Final | 72 | 89 | 161 | No Over cashed |

## Core Diagnosis

This was not a pure blowout total collapse. It was an **early total inflation fade**. The market held an elevated live total after a 45-point first quarter, but Portland’s scoring profile was not sustainable.

Portland scored 21 in Q1 despite shooting only **5-of-21 FG**, **2-of-9 from three**, and relying heavily on **9-of-9 free throws** plus **10 second-chance points**. That profile created scoreboard inflation without stable shot quality.

```yaml
tag_result:
  primary_tag: LIVE_TOTAL_INFLATION_FADE
  secondary_tags:
    - EARLY_FT_INFLATION
    - FALSE_PACE_Q1
    - POOR_SHOT_QUALITY_MASKED_BY_LINE
    - SECOND_CHANCE_NOISE
    - THIRD_QUARTER_OFFENSIVE_REGRESSION
```

## Q1 Signal Profile

```yaml
portland_q1_profile:
  points: 21
  fg: 5/21
  fg_pct: 23.8
  three_pt: 2/9
  three_pt_pct: 22.2
  free_throws: 9/9
  offensive_rebounds: 5
  second_chance_points: 10
  read: unstable scoring; fade inflated total
```

## Halftime Read

At halftime the total sat at 84. The ticket still needed the second half to stay at 84.5 or lower, but the underlying shot environment favored the No Over side.

```yaml
halftime_read:
  total: 84
  needed_to_beat_ticket: 85
  portland_3pt: 2/18
  sparks_3pt: 4/15
  combined_3pt: 6/33
  total_turnovers: 6
  main_risk: free_throw_volume
  model_read: hold
```

## Second-Half Separation

The third quarter was the kill shot. Portland scored only 12 points, shot 0-of-4 from three, and committed 9 turnovers. Los Angeles won the quarter 23-12 and flipped the game state from coin-flip into Sparks control.

```yaml
second_half:
  fire: 29
  sparks: 48
  total: 77
  note: Under won because Portland collapsed enough to absorb a strong Sparks second half.
```

## Engine Patch

```yaml
LIVE_TOTAL_INFLATION_FADE:
  description: >
    Live total inflates or remains elevated after an early scoring quarter,
    but underlying shot quality shows unstable scoring caused by free throws,
    offensive rebounds, or temporary shooting rather than sustainable offense.

  trigger_conditions:
    - q1_total >= 43
    - live_total >= pregame_total - 2
    - one_team_fg_pct <= 35
    - one_team_3pt_pct <= 25
    - one_team_points_supported_by_ft_or_second_chance >= 40_percent
    - combined_turnovers <= 6

  preferred_action:
    - attack_no_over
    - prioritize_plus_money
    - hold_through_halftime_if_live_total_requires <= 85_second_half_points

  confidence_boost:
    base: +6%
    if_primary_scoring_team_fg_pct <= 30: +4%
    if_primary_scoring_team_3pt_pct <= 25: +3%
    if_q1_free_throw_rate_is_unsustainably_high: +3%
    if_second_chance_points_make_up_25_percent_or_more_of_team_points: +3%

  danger_filters:
    - both_teams_3pt_volume_elite_and_making_shots
    - both_teams_in_bonus_early_multiple_quarters
    - close_game_with_late_foul_extension_risk
    - live_total_already_corrected_down_by_8_plus_points
```

## Edge Summary

```yaml
entry_price: +158
implied_probability: 38.8
estimated_true_probability_at_entry: 52_to_56
edge_range: +13.2_to_17.2_percentage_points
final_total: 161
ticket_line: 168.5
cover_margin: 7.5
grade: A
```

## Final Assessment

The market overpaid for a noisy 45-point first quarter. Portland’s Q1 points were built on free throws and second chances while its shooting efficiency was deeply unstable. Once the free throw and second-chance dependency cooled, the live total was exposed.

This belongs beside `LIVE_TOTAL_COLLAPSE_MISPRICE`, but it should stay separate as `LIVE_TOTAL_INFLATION_FADE` because the trigger happens earlier and does not require a halftime blowout state.