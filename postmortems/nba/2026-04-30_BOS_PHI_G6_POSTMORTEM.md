# NBA Playoff Postmortem — BOS @ PHI — Game 6 — 2026-04-30

## Game ID / Date

- Game ID: `NBA_2026_PLAYOFFS_R1_BOS_PHI_G6_0430`
- Matchup: Boston Celtics @ Philadelphia 76ers
- Round: East First Round, Game 6
- Final: 76ers 106, Celtics 93
- Venue: Xfinity Mobile Arena, Philadelphia, PA
- Officials: Marc Davis, Nick Buchert, Ray Acosta
- Attendance: 19,746 sellout
- Series state: tied 3-3
- Next game: Game 7 at Boston, May 2, 2026
- Investment: `Over 209.5 total points` — LOSS
- Actual total: 199
- Delta vs investment line: -10.5 points

## Source Files Consulted

- `20260430_BOSPHI_book.pdf`
- User-provided series screenshot
- User-provided bet slip screenshot
- User-provided AP recap in current session
- GitHub search for prior sim output: no retrievable pregame simulation output found for this matchup

## Projection Availability

Pregame model projection was requested from chat history/repo history, but no retrievable simulation output was found for BOS@PHI 2026-04-30. Therefore this file grades the known investment, actual game environment, and playoff profile signals.

```yaml
projection_status:
  model_projection_found: false
  investment_logged: true
  investment_market: full_game_total
  line: 209.5
  result_total: 199
  result: loss
```

## Series Score Map

| Game | Result | Series State |
|---|---:|---|
| Game 1 | BOS 123, PHI 91 | BOS 1-0 |
| Game 2 | PHI 111, BOS 97 | 1-1 |
| Game 3 | BOS 108, PHI 100 | BOS 2-1 |
| Game 4 | BOS 128, PHI 96 | BOS 3-1 |
| Game 5 | PHI 113, BOS 97 | BOS 3-2 |
| Game 6 | PHI 106, BOS 93 | 3-3 |

## Rolling-Form Update

### Full Series Scoring

| Team | Series PTS | Series Avg | Game 6 Delta vs Series Avg |
|---|---:|---:|---:|
| BOS | 646 | 107.7 | -14.7 |
| PHI | 617 | 102.8 | +3.2 |
| Combined | 1263 | 210.5 | -11.5 |

### Last 3 Games

| Team | G4 | G5 | G6 | Avg |
|---|---:|---:|---:|---:|
| BOS | 128 | 97 | 93 | 106.0 |
| PHI | 96 | 113 | 106 | 105.0 |
| Combined | 224 | 210 | 199 | 211.0 |

## Pregame / Investment vs Actual

| Item | Expected / Position | Actual | Result |
|---|---:|---:|---|
| Full game total | Over 209.5 | 199 | Miss by 10.5 |
| BOS scoring | Needed pace/shot-making support | 93 | Failed |
| PHI scoring | Needed enough push pace to carry total | 106 | Solid but not explosive |
| 3Q flow | Needed stable scoring | BOS 14, PHI 24 | Total broke in 3Q |

## Game Flow Breakdown

| Quarter | BOS | PHI | Total | Read |
|---|---:|---:|---:|---|
| 1Q | 23 | 20 | 43 | Under pace, not fatal |
| 2Q | 26 | 38 | 64 | Over stabilized temporarily |
| 3Q | 14 | 24 | 38 | Decisive total-kill quarter |
| 4Q | 30 | 24 | 54 | Too late, some bench/late scoring |
| Final | 93 | 106 | 199 | Under by 10.5 |

## Team Box Score Summary

| Team | FG | FG% | 3P | 3P% | FT | REB | AST | TO | PTS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BOS | 36/86 | 41.9% | 12/41 | 29.3% | 9/16 | 46 | 18 | 13 | 93 |
| PHI | 39/89 | 43.8% | 11/33 | 33.3% | 17/19 | 48 | 22 | 12 | 106 |

## Player Notes

### Boston

| Player | MIN | PTS | REB | AST | FG | 3P | +/- | Read |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Jaylen Brown | 28:29 | 18 | 1 | 2 | 7/17 | 2/6 | -24 | Foul/turnover drag; 5 TO |
| Jayson Tatum | 28:48 | 17 | 11 | 3 | 6/13 | 2/6 | -11 | Strong 1H, no 4Q run; left for treatment per recap |
| Payton Pritchard | 36:09 | 14 | 3 | 5 | 6/16 | 1/8 | -6 | Volume inefficient from 3 |
| Derrick White | 31:31 | 11 | 1 | 1 | 3/8 | 3/6 | -25 | Low creation impact |
| Neemias Queta | 20:18 | 4 | 11 | 0 | 2/5 | 0/0 | -14 | Rebound positive, offensive low impact |

### Philadelphia

| Player | MIN | PTS | REB | AST | FG | 3P | +/- | Read |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Tyrese Maxey | 39:49 | 30 | 2 | 5 | 11/22 | 3/5 | +15 | Primary offensive engine |
| Paul George | 39:37 | 23 | 4 | 3 | 8/17 | 5/9 | +11 | Resurgence / spacing unlock |
| Joel Embiid | 34:11 | 19 | 10 | 8 | 6/18 | 1/5 | +7 | Playmaking hub + interior anchor |
| VJ Edgecombe | 38:00 | 14 | 8 | 3 | 5/11 | 1/6 | +18 | Energy wing, transition/defense pop |
| Kelly Oubre Jr. | 38:44 | 14 | 9 | 1 | 6/11 | 1/3 | +23 | Defensive event impact; key block sequence |

## Pivotal Profile Tagging Roll

### 1. Boston Total Collapse Profile

```yaml
profile_tag: BOS_TOTAL_COLLAPSE_3Q
trigger:
  - Celtics scored 14 in 3Q
  - Celtics shot 6/23 FG and 2/13 from 3 in 3Q
  - Celtics had only 2 assists in 3Q
  - Tatum limited to 7:57 in 3Q and did not play 4Q
impact:
  - full_game_over_failure
  - live_total_under_validation_after_3Q_stall
```

### 2. Brown Foul / Turnover Drag

```yaml
profile_tag: BROWN_FOUL_TURNOVER_DRAG
trigger:
  - Brown 4 PF
  - Brown 5 TO
  - Brown -24 plus/minus
  - first-half foul pressure disrupted normal aggression
model_note:
  - downgrade BOS total ceiling when Brown foul trouble appears before halftime
```

### 3. Philadelphia Survival-Offense Profile

```yaml
profile_tag: PHI_SURVIVAL_CORE_CONFIRMED
players:
  - Maxey
  - George
  - Embiid
  - Oubre
  - Edgecombe
signal:
  - Maxey 30 points
  - George 5 made threes
  - Embiid 19/10/8
  - Oubre +23
  - Edgecombe +18
model_note:
  - PHI can win without elite Embiid scoring if George spacing and Maxey creation hit
```

### 4. Game 7 Risk Profile

```yaml
profile_tag: GAME7_VOLATILITY_ELEVATED
conditions:
  - series tied 3-3
  - PHI won two straight after trailing 3-1
  - BOS offense posted 93 and 97 in consecutive losses
  - Tatum apparent calf treatment noted in recap
  - Brown foul volatility elevated
```

## Rebound Environment

| Team | OREB | DREB | Total REB | 2nd Chance PTS |
|---|---:|---:|---:|---:|
| BOS | 8 | 38 | 46 | 10 |
| PHI | 8 | 40 | 48 | 9 |

Rebounding was not the main reason the total failed. Both teams were nearly even on the glass. The total failed because Boston's shot-making and creation collapsed, especially in the third quarter.

## Total Market Failure Diagnosis

The over missed because the game had one strong over quarter but two total-suppressing stretches:

1. The first quarter produced only 43 points.
2. The third quarter produced only 38 points and effectively killed the total.
3. Boston ended with only 93 despite 86 FGA because they shot 29.3% from three and only 56.2% from the line.
4. Philadelphia played well enough to win but not fast or hot enough to solo-carry the total.

## Signal vs Noise

| Signal | Classification | Reason |
|---|---|---|
| PHI Maxey/George offensive core | Confirmed | Maxey 30, George 23, George 5/9 from 3 |
| BOS offensive ceiling | Weakened | Back-to-back losses at 97 and 93 |
| Over 209.5 | Broken for Game 6 | BOS 3Q collapse and poor 3PT/FT efficiency |
| Rebound edge | Neutral | PHI +2 boards, equal OREB |
| Game 7 volatility | Elevated | Series pressure + Tatum treatment + Brown foul risk |

## Patch Evaluation

### Keep

- `PLAYOFF_SERIES_ROLLING_FORM`
- `QUARTER_COLLAPSE_DETECTION`
- `FOUL_TROUBLE_USAGE_DRAG`
- `INJURY_TREATMENT_VOLATILITY_TAG`

### Modify

- Add `BOS_3Q_CREATION_COLLAPSE_FLAG`.
- Add `OVER_EXPOSURE_WARNING_WHEN_TOTAL_DEPENDS_ON_BOS_SHOOTING`.
- Add `BROWN_FOUL_DRAG_GATE` for live totals and Boston team totals.
- Add `GAME7_ELEVATED_VARIANCE_PROFILE` for series tied 3-3.

### Revert

- None.

## Retraining Flags

```yaml
retraining_flags:
  - TOTAL_OVER_MISS_REGISTERED
  - BOS_3Q_CREATION_COLLAPSE
  - BROWN_FOUL_TURNOVER_DRAG
  - TATUM_TREATMENT_VOLATILITY
  - PHI_SURVIVAL_CORE_CONFIRMED
  - GEORGE_SPACING_RESURGENCE
  - GAME7_VOLATILITY_ELEVATED
```

## Final Status

- Postmortem status: complete
- Investment result: loss
- Model action: modify
- Confidence: medium-high
- Reason: official box score fully supports total-failure diagnosis, but missing pregame sim output limits direct model-vs-actual grading.
