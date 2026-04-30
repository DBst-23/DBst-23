# POSTMORTEM_TOR_CLE_2026-04-29_GAME5_REBOUND_DIAGNOSTIC

## Game Context
- Matchup: Toronto Raptors @ Cleveland Cavaliers
- Date: 2026-04-29
- Final: CLE 125, TOR 120
- Workflow: Postmortem GitHub workflow
- Model Focus: Rebounds, gameline/total validation, frontcourt battle, single-fire deployment logic

---

## Final Team Box

| Team | PTS | REB | OREB | DREB | AST | STL | BLK | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| TOR | 120 | 48 | 15 | 33 | 32 | 8 | 8 | 14 | 44-95 | 15-38 | 17-25 | 56.6 |
| CLE | 125 | 35 | 4 | 31 | 20 | 8 | 8 | 14 | 43-81 | 18-36 | 21-28 | 67.0 |

### Key Team Splits
- TOR won total rebounds by +13.
- TOR won offensive rebounds 15-4.
- TOR generated 95 FGA to CLE's 81.
- CLE shot 53.1% FG and 50.0% from three.
- TOR had 32 assists, but CLE won efficiency and late-game shot quality.
- Fastbreak points strongly favored TOR, 26-6.

---

# Player Results vs Model

## Evan Mobley O8.5 REB — Primary Frontcourt Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Evan Mobley | O8.5 | 9.6 | 9.2 | 59-61% | 9 | HIT |

## Jarrett Allen O8.5 REB — Secondary / Thin Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Jarrett Allen | O8.5 | 8.9 | 8.5 | 53-55% | 3 | MISS |

## RJ Barrett O5.5 REB — Strong Wing Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| RJ Barrett | O5.5 | 6.6 | 6.3 | 58-60% | 12 | HIT |

## Scottie Barnes O7.5 REB — Thin Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Scottie Barnes | O7.5 | 7.8 | 7.4 | 52-54% | 8 | HIT |

## Collin Murray-Boyles O6.5 REB — Activity Edge

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Collin Murray-Boyles | O6.5 | 7.2 | 6.9 | 56-58% | 5 | MISS |

## Jakob Poeltl O4.5 REB — Trap Tag

| Player | Line | Model Mean | Model Trap Logic | Actual | Result |
|---|---:|---:|---|---:|---|
| Jakob Poeltl | O4.5 | 4.8 | Box-out / frontcourt suppression trap | 9 | Trap Miss |

## Guard Rebound Traps

| Player | Line | Model Read | Actual | Result |
|---|---:|---|---:|---|
| Donovan Mitchell | O4.5 | Trap / reduced share with Harden | 5 | Trap Miss |
| James Harden | O4.5 | Trap / long rebound dependent | 9 | Trap Miss |

---

# Player Box Score Highlights

## Toronto

| Player | MIN | PTS | REB | OREB | AST | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| RJ Barrett | 38 | 25 | 12 | 5 | 5 | 3 | 9-19 | 2-5 | 5-9 | 54.4 |
| Scottie Barnes | 39 | 17 | 8 | 2 | 11 | 4 | 6-16 | 0-3 | 5-6 | 45.6 |
| Jakob Poeltl | 21 | 14 | 9 | 0 | 3 | 0 | 5-6 | 0-0 | 4-6 | 81.0 |
| Ja'Kobe Walter | 35 | 20 | 3 | 1 | 2 | 1 | 7-16 | 6-14 | 0-0 | 62.5 |
| Collin Murray-Boyles | 26 | 8 | 5 | 2 | 2 | 1 | 4-5 | 0-0 | 0-0 | 80.0 |
| Jamal Shead | 34 | 18 | 1 | 1 | 7 | 3 | 7-15 | 4-10 | 0-0 | 60.0 |

## Cleveland

| Player | MIN | PTS | REB | OREB | AST | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| Evan Mobley | 33 | 23 | 9 | 2 | 1 | 0 | 8-13 | 3-3 | 4-8 | 69.6 |
| Jarrett Allen | 25 | 9 | 3 | 0 | 1 | 3 | 4-5 | 0-0 | 1-2 | 76.5 |
| James Harden | 40 | 23 | 9 | 1 | 5 | 6 | 7-13 | 4-8 | 5-6 | 73.5 |
| Donovan Mitchell | 31 | 19 | 5 | 0 | 3 | 2 | 7-17 | 3-5 | 2-2 | 53.1 |
| Max Strus | 27 | 8 | 4 | 0 | 2 | 0 | 2-4 | 0-2 | 4-4 | 69.4 |
| Dennis Schroder | 21 | 19 | 0 | 0 | 2 | 0 | 7-11 | 3-6 | 2-2 | 80.0 |

---

# Phase 1 — Game Phase Analysis

## Early Environment
Toronto created extra possessions through volume, offensive rebounding, and transition. Cleveland won the efficiency battle behind elite shooting and cleaner scoring pockets.

## Middle Game
Toronto's committee glass profile was strong. Barrett and Barnes carried wing rebounding while Poeltl outperformed the trap expectation in limited minutes. Cleveland's central rebound profile became split: Mobley cleared his number, while Allen was suppressed by minutes and role.

## Closing Phase
Cleveland's scoring efficiency, Harden/Mobley production, and three-point shotmaking carried the finish. The game exceeded the under lean because CLE shot 50% from three and TOR created 95 attempts plus 26 fastbreak points.

---

# Phase 2 — Pivotal Moments

## 1. Mobley Edge Validated
Mobley finished with 9 rebounds, clearing O8.5 by hook. His role remained stable enough even with Cleveland losing the team rebound battle.

### Model Note
Mobley remains a strong primary frontcourt rebound profile. However, when paired with Allen, projection should account for possible split frontcourt volatility and shot-quality impact.

## 2. Allen Role Suppression
Allen finished with only 3 rebounds in 25 minutes.

### Model Note
Allen's minutes and role were less stable than Mobley's. Add a center-minutes volatility penalty when paired with another elite big and when opponent plays high-volume wing/forward rebounders.

## 3. Barrett Wing Rebound Spike
Barrett delivered 12 rebounds with 5 offensive boards.

### Model Note
Barrett's rebound path was elite because Toronto created 95 FGA, attacked transition, and crashed by committee. Wing rebounders can spike when team shot volume and offensive rebounding identity are active.

## 4. Poeltl Trap Failed
Poeltl finished with 9 rebounds despite the model tagging him as a trap at O4.5.

### Model Note
Box-out trap was over-weighted. Poeltl's minutes were low, but his per-minute rebounding converted. Need a floor check: if line is low enough and player is an efficient rebounder, trap tags should cap probability instead of fully avoiding.

## 5. Guard Trap Failed
Harden and Mitchell both cleared 4.5 rebounds.

### Model Note
Guard rebound trap failed due to long rebound environment and Cleveland three-point volume. Harden's 40 minutes created enough collection opportunities despite long-board dependency.

---

# Phase 3 — Defensive / Psychological Variables

## Toronto Style
- Committee rebounding was active.
- Offensive glass aggression was real: 15 OREB.
- Barrett and Barnes operated as high-minute wing rebounders.
- Toronto pace/transition pressure was higher than under-game expectation.

## Cleveland Style
- Efficiency-first offense.
- 18 made threes on 36 attempts.
- Harden acted as both scorer and long-board collector.
- Mobley remained the most reliable big-man rebound profile.

---

# Phase 4 — Model Relevance Summary

## Hits
- Mobley O8.5 hit.
- RJ Barrett O5.5 hit strongly.
- Scottie Barnes O7.5 hit narrowly.

## Misses
- Allen O8.5 missed badly.
- Murray-Boyles O6.5 missed.
- Poeltl trap tag failed.
- Guard rebound trap tags failed.
- Under 216 lean failed due to 245 total points.
- CLE -8.5 lean failed; CLE won by 5.

---

# Patch Queue — Hold Until Postmortem Batch Ends

## 1. Low-Line Trap Override
```python
if rebound_line <= 4.5 and player_rebound_rate_strong:
    trap_tag = "cap_prob_only"
```

## 2. Two-Big Split Volatility Penalty
```python
if team_has_two_primary_bigs and player_minutes < 30:
    rebound_prob -= 0.04
```

## 3. Wing Crash Boost
```python
if team_oreb_rate_high and player_role == "high_minute_wing":
    rebound_prob += 0.04
```

## 4. Long-Rebound Guard Trap Override
```python
if opponent_three_point_attempt_rate_high and player_minutes >= 35:
    guard_rebound_trap = False
```

## 5. Total Under Kill Switch
```python
if both_teams_projected_3pa_high and transition_points_profile_active:
    under_confidence -= 0.05
```

---

# B.004 Execution Notes

## Single-Fire Review
- Mobley O8.5: HIT
- RJ Barrett O5.5: HIT
- Barnes O7.5: HIT
- Poeltl avoid: incorrect

## Card Construction Review
Best single-fire candidates were Mobley and Barrett. Allen and Murray-Boyles were weaker multi-leg inclusions due to role volatility.

## B.004 Confirmation
This game supports single-fire deployment while adding caution around overconfident trap tags. Trap tags should become probabilistic caps, not automatic full fades, especially on low lines.

---

# Final Tags
- `POSTMORTEM_TOR_CLE_2026-04-29_GAME5`
- `B004_SINGLE_FIRE_VALIDATION`
- `MOBLEY_PRIMARY_BIG_EDGE_CONFIRMED`
- `RJ_BARRETT_WING_CRASH_SPIKE`
- `POELTL_LOW_LINE_TRAP_FAILURE`
- `GUARD_REBOUND_TRAP_FAILURE`
- `TWO_BIG_SPLIT_VOLATILITY`
- `TOTAL_UNDER_KILL_SWITCH_REQUIRED`

## Status
Finalized and logged for Backtest_Logbook registry.
