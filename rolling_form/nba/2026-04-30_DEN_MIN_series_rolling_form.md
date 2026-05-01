# NBA Rolling Form — DEN vs MIN — West First Round — Updated 2026-04-30

## Series Result / Status

- Series: Denver Nuggets vs Minnesota Timberwolves
- Status: Minnesota wins 4-2
- Latest logged game: Game 6 — MIN 110, DEN 98
- Minnesota advances to Round 2 at San Antonio

## Game Results

| Game | DEN | MIN | Margin | Winner |
|---|---:|---:|---:|---|
| 1 | 116 | 105 | DEN +11 | DEN |
| 2 | 114 | 119 | MIN +5 | MIN |
| 3 | 96 | 113 | MIN +17 | MIN |
| 4 | 96 | 112 | MIN +16 | MIN |
| 5 | 125 | 113 | DEN +12 | DEN |
| 6 | 98 | 110 | MIN +12 | MIN |

## Rolling Windows

### Full Series

| Team | Points | Avg | High | Low |
|---|---:|---:|---:|---:|
| DEN | 645 | 107.5 | 125 | 96 |
| MIN | 672 | 112.0 | 119 | 105 |
| Combined | 1317 | 219.5 | 238 | 208 |

### Last 5 Games — Games 2-6

| Team | Points | Avg | Trend |
|---|---:|---:|---|
| DEN | 529 | 105.8 | Suppressed in 3 of final 4 losses |
| MIN | 567 | 113.4 | Stable 110+ floor across series close |
| Combined | 1096 | 219.2 | High total environment but MIN edge-driven |

### Last 3 Games — Games 4-6

| Team | Points | Avg | Trend |
|---|---:|---:|---|
| DEN | 319 | 106.3 | Game 5 spike, otherwise suppressed |
| MIN | 335 | 111.7 | Stable despite injuries |
| Combined | 654 | 218.0 | Total environment stayed playable |

## Series-Level Signal

Minnesota averaged 112.0 points in the series and scored at least 110 in five of six games. Denver averaged 107.5 but scored 98, 96, and 96 in three of its four losses.

## Game 6 Carryover Tags

```yaml
series_tags:
  - MIN_SERIES_CLOSEOUT_CONFIRMED
  - MIN_STABLE_TEAM_TOTAL_FLOOR
  - MIN_REBOUND_ENVIRONMENT_DOMINANCE
  - MIN_BIG_LINEUP_COUNTEREDGE
  - MCDANIELS_TWO_WAY_BREAKOUT
  - SHANNON_SURPRISE_START_SPEED_PRESSURE
  - GOBERT_INTERIOR_HUB_PROFILE
  - MURRAY_SUPPRESSION_BY_LENGTH
  - JOKIC_SUPPORT_GAP
  - DEN_REBOUND_ENVIRONMENT_FAILURE
```

## Round 2 Carryover vs San Antonio

- Minnesota's base offensive projection should not be downgraded solely for guard injuries if big-lineup rebounding/paint pressure remains active.
- McDaniels must receive expanded role/usage ceiling after 32/10 closeout.
- Gobert playmaking hub logic must be retained when opponents overload on paint help.
- Shannon Jr. can function as a speed-pressure substitute when guard creation is missing.
- Minnesota team total edges require explicit OREB/paint confirmation; 3P shooting was not the source of the Game 6 cover.

## Patch Status

- Keep: rebound-environment tracker, big-lineup counteredge, paint/OREB team-total support.
- Modify: wing rebound ladder stall after halftime, Murray chase-defender suppression, hook-sensitivity logging.
- Revert: none.

## Final Status

- Rolling update status: complete
- Series status: closed
- Model action: modify and carry forward to Round 2
