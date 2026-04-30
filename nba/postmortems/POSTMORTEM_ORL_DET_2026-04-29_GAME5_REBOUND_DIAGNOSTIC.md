# POSTMORTEM_ORL_DET_2026-04-29_GAME5_REBOUND_DIAGNOSTIC

## Game Context
- Matchup: Orlando Magic @ Detroit Pistons
- Date: 2026-04-29
- Final: DET 116, ORL 109
- Series Context: ORL entered with 3-1 lead; DET survival spot
- Workflow: Postmortem GitHub workflow
- Model Focus: Rebounds, matchup adjustment validation, single-fire deployment logic

---

## Final Team Box

| Team | PTS | REB | OREB | DREB | AST | STL | BLK | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| ORL | 109 | 33 | 8 | 25 | 21 | 12 | 5 | 16 | 38-80 | 17-38 | 16-30 | 58.5 |
| DET | 116 | 49 | 16 | 33 | 20 | 10 | 5 | 17 | 39-80 | 10-28 | 28-35 | 60.8 |

### Key Team Splits
- DET won total rebounds by +16.
- DET won offensive rebounds 16-8.
- DET won points in paint 48-36.
- DET won second-chance points 22-21.
- ORL shot 44.7% from three but only 53.3% from the FT line.
- DET generated 35 free throws and made 28.

---

# Player Results vs Model

## Pre-Game / Workflow Projection Board

### Jalen Duren O10.5 REB — Downgraded to NO PLAY / Trap Zone

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Jalen Duren | O10.5 | 9.4 | 9.0 | 43-46% | 9 | Correct Avoid |

### Paolo Banchero O7.5 REB — Best Single

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Paolo Banchero | O7.5 | 8.5 | 8.1 | 59-61% | 9 | HIT |

### Cade Cunningham O6.5 REB — Secondary Leg

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Cade Cunningham | O6.5 | 7.1 | 6.8 | 54-56% | 4 | MISS |

### Anthony Black O2.5 REB — Conditional Wagner-Sit Boost

| Player | Line | Model Mean | Model Median | Model Prob | Actual | Result |
|---|---:|---:|---:|---:|---:|---|
| Anthony Black | O2.5 | 3.3 | 3.0 | 57-59% | 5 | HIT |

---

# Player Box Score Highlights

## Orlando

| Player | MIN | PTS | REB | OREB | AST | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| Paolo Banchero | 41 | 45 | 9 | 2 | 7 | 6 | 17-31 | 6-11 | 5-12 | 62.0 |
| Anthony Black | 39 | 19 | 5 | 0 | 3 | 3 | 7-12 | 4-6 | 1-2 | 73.8 |
| Wendell Carter Jr. | 34 | 9 | 4 | 2 | 4 | 1 | 2-4 | 1-3 | 4-4 | 78.1 |
| Desmond Bane | 34 | 18 | 5 | 1 | 1 | 2 | 6-15 | 4-10 | 2-2 | 56.7 |
| Jalen Suggs | 37 | 10 | 2 | 0 | 5 | 1 | 4-9 | 2-5 | 0-1 | 53.0 |

## Detroit

| Player | MIN | PTS | REB | OREB | AST | TOV | FG | 3P | FT | TS% |
|---|---:|---:|---:|---:|---:|---:|---|---|---|---:|
| Cade Cunningham | 44 | 45 | 4 | 3 | 5 | 6 | 13-23 | 5-8 | 14-14 | 77.2 |
| Ausar Thompson | 36 | 6 | 15 | 4 | 6 | 5 | 3-5 | 0-0 | 0-2 | 51.0 |
| Tobias Harris | 31 | 23 | 8 | 1 | 1 | 1 | 9-18 | 1-3 | 4-7 | 54.6 |
| Jalen Duren | 28 | 12 | 9 | 5 | 2 | 3 | 4-6 | 0-0 | 4-4 | 77.3 |
| Isaiah Stewart | 20 | 5 | 5 | 1 | 0 | 0 | 1-3 | 0-1 | 3-4 | 52.5 |

---

# Phase 1 — Game Phase Analysis

## Early Environment
Detroit established physicality through rim pressure and offensive rebounding. ORL shot well enough from three to stay within range, but DET owned the glass and free-throw volume.

## Middle Game
Banchero carried Orlando usage with 45 points, 31 FGA, and 41 minutes. His rebound line remained live because Franz Wagner was unavailable and Orlando needed Banchero's size on the floor for extended stretches.

## Closing Phase
Detroit's survival spot materialized through Cade Cunningham usage, free throws, and team rebounding. Cade's scoring workload increased, but his rebound distribution missed the modeled long-miss leakage path. Ausar and Tobias absorbed the wing/forward rebounding instead.

---

# Phase 2 — Pivotal Moments

## 1. Banchero Usage Spike
Banchero posted 45/9/7 on 41 minutes. He cleared the O7.5 rebound line despite massive scoring responsibility.

### Model Note
High-usage rebound suppressor should not automatically downgrade primary forwards when frontcourt role expands due to injury absence. Wagner out/questionable context created a role-stability boost.

## 2. Duren Trap Validation
Duren finished with 9 rebounds, under the 10.5 line. He had 5 offensive rebounds, but only 4 defensive rebounds and only 28 minutes due to foul/rotation constraints.

### Model Note
Duren downgrade was correct. Orlando's center/wing box-out scheme continued suppressing his ceiling.

## 3. Cade Rebound Miss
Cade finished with 4 rebounds despite 44 minutes. His scoring/usage load was extreme: 45 points, 23 FGA, 14 FTA.

### Model Note
High usage above 30% should apply stronger rebound suppression when the player is also primary on-ball initiator in a playoff elimination/survival script.

## 4. Ausar Rebound Spike
Ausar Thompson grabbed 15 rebounds, including 4 offensive boards.

### Model Note
Wing crash role should be upgraded when Duren is boxed out and Detroit plays with survival-level physicality. Add `DET_WING_CRASH_REDISTRIBUTION` tag.

---

# Phase 3 — Defensive / Psychological Variables

## Orlando Defensive Scheme
- Continued box-out pressure on Duren.
- Carter/Bitadze did not win the raw board count but contributed to Duren ceiling suppression.
- Orlando allowed DET wing/forward rebound redistribution.

## Detroit Psychological Variable
- Survival game intensity increased offensive rebounding and FT aggression.
- Cade entered alpha usage mode, which raised scoring efficiency but lowered rebound participation.

---

# Phase 4 — Model Relevance Summary

## Hits
- Banchero O7.5 rebound single was the best board call and hit.
- Duren O10.5 downgrade to NO PLAY / trap zone was correct.
- Anthony Black conditional rebound boost was valid and hit.

## Misses
- Cade Cunningham O6.5 missed due to extreme scoring usage and wing rebound redistribution to Ausar/Tobias.

## Patch Recommendations

### 1. Strengthen High-Usage Rebound Suppressor
```python
if usage_rate > 30 and player_role in ["primary_ball_handler", "primary_scorer"]:
    rebound_prob -= 0.04
```

### 2. Add Wing Redistribution Tag
```python
if primary_center_boxed_out and team_survival_spot:
    boost_wing_rebounders += 0.05
```

### 3. Preserve Primary Forward Role Boost
```python
if frontcourt_teammate_out and player_role == "primary_forward":
    rebound_prob += 0.03
```

### 4. Keep Duren Trap Tag Active
```python
DUREN_ORL_BOXOUT_SUPPRESSION = True
```

---

# B.004 Execution Notes

## Single-Fire Result
- Banchero O7.5 as single: HIT
- Duren avoid: correct
- Anthony Black as conditional single: HIT

## 2-Leg Result
- Banchero + Cade would have failed due to Cade miss.

## B.004 Confirmation
This game reinforces the Method-A diagnostic: best edges should be deployed as single-fire. The strongest model read was Banchero. Packaging it with a secondary leg created unnecessary fragility.

---

# Final Tags
- `POSTMORTEM_ORL_DET_2026-04-29_GAME5`
- `B004_SINGLE_FIRE_VALIDATION`
- `DUREN_TRAP_CONFIRMED`
- `BANCHERO_PRIMARY_FORWARD_EDGE_CONFIRMED`
- `CADE_HIGH_USAGE_REBOUND_SUPPRESSION`
- `DET_WING_CRASH_REDISTRIBUTION`
- `ANTHONY_BLACK_CONDITIONAL_BOOST_HIT`

## Status
Finalized and logged for Backtest_Logbook registry.
