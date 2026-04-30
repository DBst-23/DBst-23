# POSTMORTEM_HOU_LAL_2026-04-29_GAME5_REBOUND_DIAGNOSTIC

## Game Context
- Matchup: Houston Rockets @ Los Angeles Lakers
- Date: 2026-04-29
- Final: HOU 99, LAL 93
- Workflow: Postmortem GitHub workflow
- User Tracking Slip: Mobley + Sengun 2-leg card lost, 1 hit / 1 miss
- Model Focus: Rebounds, endgame variance, slow-tempo playoff environment, single-fire validation

---

## Final Team Box

| Team | PTS | REB | OREB | DREB | AST | STL | BLK | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| HOU | 99 | 34 | 6 | 28 | 25 | 10 | 4 | 10 | 33-75 | 14-40 | 19-25 | 57.6 |
| LAL | 93 | 41 | 13 | 28 | 19 | 5 | 5 | 15 | 32-76 | 7-27 | 22-27 | 52.9 |

### Key Team Splits
- LAL won total rebounds by +7.
- LAL won offensive rebounds 13-6.
- Defensive rebounds were even, 28-28.
- HOU won turnovers, 10 to 15.
- HOU shot 14-40 from three; LAL shot 7-27.
- LAL won points in paint 44-36.
- LAL won second-chance points 13-6.
- Final total: 192 points.

---

# Player Results vs Model

## Alperen Sengun O9.5 REB — Primary Houston Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Alperen Sengun | O9.5 | 11.1 | 10.6 | 60-62% | 9 | MISS |

## Jabari Smith Jr. O7.5 REB — Secondary Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Jabari Smith Jr. | O7.5 | 8.2 | 7.9 | 54-56% | 7 | MISS |

## Tari Eason O6.5 REB — Secondary Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Tari Eason | O6.5 | 7.1 | 6.8 | 55-57% | 5 | MISS |

## Amen Thompson O7.5 REB — Avoid / Suppressed

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Amen Thompson | O7.5 | 6.9 | 6.5 | 48-50% | 7 | Correct Avoid |

## LeBron James O7.5 REB — Lakers Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| LeBron James | O7.5 | 8.6 | 8.2 | 58-60% | 3 | MISS |

## Deandre Ayton O7.5 REB — Secondary Lakers Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Deandre Ayton | O7.5 | 8.1 | 7.8 | 53-55% | 17 | HIT |

## Rui Hachimura O4.5 REB — Thin Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Rui Hachimura | O4.5 | 5.0 | 4.7 | 52-54% | 4 | MISS |

---

# Player Box Score Highlights

## Houston

| Player | MIN | PTS | REB | OREB | AST | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| Alperen Sengun | 43 | 14 | 9 | 1 | 8 | 5 | 5-9 | 0-0 | 4-4 | 65.1 |
| Amen Thompson | 46 | 15 | 7 | 2 | 4 | 3 | 4-14 | 2-5 | 5-8 | 42.8 |
| Jabari Smith Jr. | 42 | 22 | 7 | 2 | 3 | 0 | 6-13 | 4-9 | 6-8 | 66.6 |
| Tari Eason | 31 | 18 | 5 | 1 | 1 | 0 | 6-11 | 2-6 | 4-5 | 68.2 |
| Reed Sheppard | 35 | 12 | 0 | 0 | 6 | 1 | 5-12 | 2-7 | 0-0 | 50.0 |

## Lakers

| Player | MIN | PTS | REB | OREB | AST | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| Deandre Ayton | 38 | 18 | 17 | 10 | 0 | 1 | 9-14 | 0-0 | 0-0 | 64.3 |
| LeBron James | 39 | 25 | 3 | 0 | 7 | 2 | 9-20 | 0-6 | 7-10 | 51.2 |
| Austin Reaves | 34 | 22 | 4 | 0 | 6 | 3 | 4-16 | 2-8 | 12-13 | 50.6 |
| Marcus Smart | 37 | 11 | 5 | 0 | 2 | 6 | 3-7 | 3-7 | 2-2 | 69.8 |
| Rui Hachimura | 37 | 12 | 4 | 1 | 0 | 1 | 5-11 | 2-3 | 0-0 | 54.5 |

---

# Phase 1 — Game Phase Analysis

## Early Environment
The game opened as a slow, halfcourt playoff battle. Houston controlled turnover margin and spacing, while the Lakers created interior pressure through Ayton and free throws.

## Middle Game
Houston's offense became perimeter-heavy. The Rockets attempted 40 threes, which reduced traditional center offensive-board paths for Sengun. Meanwhile, Ayton dominated the interior glass and created a massive LAL offensive rebounding edge.

## Closing Phase
The game stayed tight and low scoring. Sengun remained on the floor for 43 minutes and reached 9 rebounds, but the final two-rebound path failed because Houston had limited offensive-board chances, LAL gathered 13 OREB, and late possessions created more free throws / long boards than clean center DREB chances.

---

# Phase 2 — Pivotal Moments

## 1. Sengun Hook Miss
Sengun missed O9.5 by one rebound despite 43 minutes. This was not a minutes failure. It was a rebound-environment failure.

### Model Note
Projection over-weighted Houston's series offensive glass edge and under-weighted Ayton's live dominance. Add hook-zone volatility penalty for centers facing an opponent big actively dominating OREB.

## 2. Ayton Interior Dominance
Ayton finished with 17 rebounds, including 10 offensive rebounds. This directly stole rebound share and disrupted Sengun's path.

### Model Note
Ayton should receive a major interior-possession-control tag when Lakers are using him as primary paint stabilizer.

## 3. LeBron Rebound Collapse
LeBron finished with only 3 rebounds despite 39 minutes. His role tilted toward scoring and ballhandling, while Ayton absorbed the rebounding workload.

### Model Note
When Ayton is controlling the glass, LeBron defensive-rebound boost should be downgraded. Add `AYTON_GLASS_DOMINANCE_SUPPRESSES_LEBRON_REB`.

## 4. Houston Frontcourt Shared Misses
Sengun 9, Jabari 7, Tari 5, Amen 7. Multiple Houston rebound overs came close but failed.

### Model Note
This validates the shared-rebound-pool risk. Houston had several plausible overs but not enough total available boards for all of them to clear.

---

# Phase 3 — Defensive / Psychological Variables

## Houston Style
- Slow pace.
- Strong turnover control.
- Heavy three-point volume.
- Sengun used as offensive hub, but not as dominant glass finisher.

## Lakers Style
- Ayton central rebounding role.
- Reaves and LeBron carried offensive creation.
- Lakers generated 13 OREB and 27 FTA.
- Halfcourt grind preserved under environment but created center/paint board concentration for Ayton.

---

# Phase 4 — Model Relevance Summary

## Hits
- Ayton O7.5 hit massively.
- Amen O7.5 avoid was correct.
- Game total under lean was directionally right relative to pregame 207.5 / 209.5 range, with final 192.

## Misses
- Sengun O9.5 missed by hook.
- LeBron O7.5 missed badly.
- Jabari O7.5 missed by hook.
- Tari O6.5 missed.
- Rui O4.5 missed by hook.

## Card Result
- Mobley + Sengun card: LOST
- Mobley leg: HIT
- Sengun leg: MISS

## B.004 Single-Fire Read
This is another clear single-fire validation. Mobley as a single would have cashed. Pairing with Sengun exposed the card to a hook-zone center rebound miss.

---

# Patch Queue — Hold Until Postmortem Batch Ends

## 1. Hook-Zone Center Volatility Penalty
```python
if market == "rebounds" and player_position == "C" and line_delta <= 1.5:
    if opponent_center_oreb_dominance_active:
        rebound_prob -= 0.04
```

## 2. Opponent Big Dominance Suppressor
```python
if opponent_big_oreb >= 6 or opponent_big_reb_share_spike:
    center_rebound_prob -= 0.04
```

## 3. Shared Rebound Pool Guard
```python
if same_game_rebound_legs >= 2 and shared_rebound_pool:
    card_allowed = False
```

## 4. LeBron Role Shift Suppressor
```python
if ayton_glass_dominance_active and lebron_primary_creation_role:
    lebron_rebound_prob -= 0.05
```

## 5. Perimeter Volume Center OREB Suppressor
```python
if team_3pa_rate_high and center_oreb_path_required:
    center_rebound_prob -= 0.03
```

---

# B.004 Execution Notes

## Stronger Single-Fire Candidates
- Mobley O8.5 from prior card: HIT
- Ayton O7.5: HIT

## Avoid Multi-Leg Pairing
- Mobley + Sengun failed despite both being individually plausible.
- Shared volatility plus hook-zone exposure killed the card.

---

# Final Tags
- `POSTMORTEM_HOU_LAL_2026-04-29_GAME5`
- `B004_SINGLE_FIRE_VALIDATION`
- `SENGUN_HOOK_ZONE_MISS`
- `AYTON_GLASS_DOMINANCE`
- `LEBRON_REB_SUPPRESSION_BY_AYTON`
- `HOU_SHARED_REBOUND_POOL_FAILURE`
- `CENTER_OREB_PATH_SUPPRESSED_BY_3PA_VOLUME`
- `UNDER_GAME_SCRIPT_CONFIRMED`

## Status
Finalized and logged for Backtest_Logbook registry.
