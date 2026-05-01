# NBA Rolling Form — NYK vs ATL — East First Round — Updated 2026-04-30

## Series Result

- Knicks win series 4-2
- Final game logged: Game 6, NYK 140, ATL 89
- Current status: Series closed

## Game Results

| Game | NYK | ATL | Margin | Winner |
|---|---:|---:|---:|---|
| 1 | 113 | 102 | NYK +11 | NYK |
| 2 | 106 | 107 | ATL +1 | ATL |
| 3 | 108 | 109 | ATL +1 | ATL |
| 4 | 114 | 98 | NYK +16 | NYK |
| 5 | 126 | 97 | NYK +29 | NYK |
| 6 | 140 | 89 | NYK +51 | NYK |

## Rolling Windows

### Last 5 Games — Games 2-6

| Team | Points | Avg | Trend |
|---|---:|---:|---|
| NYK | 594 | 118.8 | Strong upward acceleration |
| ATL | 500 | 100.0 | Downward collapse |

### Last 3 Games — Games 4-6

| Team | Points | Avg | Trend |
|---|---:|---:|---|
| NYK | 380 | 126.7 | Blowout dominance |
| ATL | 284 | 94.7 | Offensive collapse |

### Full Series

| Team | Points | Avg | High | Low |
|---|---:|---:|---:|---:|
| NYK | 707 | 117.8 | 140 | 106 |
| ATL | 602 | 100.3 | 109 | 89 |

## Game 6 Environment Snapshot

| Metric | NYK | ATL |
|---|---:|---:|
| Possessions | 98 | 100 |
| Points | 140 | 89 |
| 2PT FG% | 75.5% | 46.8% |
| 3PT FG% | 36.1% | 25.0% |
| eFG% | 66.5% | 42.8% |
| TS% | 69.0% | 47.3% |
| Rebounds | 52 | 41 |
| Offensive Rebounds | 12 | 15 |
| Defensive Rebounds | 40 | 26 |
| Shot Quality | 0.60 | 0.51 |

## Rolling Rebound Read

- Knicks finished Game 6 +11 on total rebounds.
- Knicks defensive rebound share was stable enough to erase Atlanta's offensive rebound count.
- Atlanta offensive rebounds were not predictive of scoring efficiency in Game 6.
- Treat Atlanta's 15 OREB as empty-calorie rebounds due to 42.8% eFG and 47.3% TS.

## Active Series Tags

```yaml
series_tags:
  - NYK_OFFENSIVE_SPIKE_CONFIRMED
  - NYK_DEFENSIVE_GLASS_STABLE
  - NYK_RIM_CONVERSION_SPIKE
  - NYK_AB3_CONVERSION_SPIKE
  - ATL_EFFICIENCY_COLLAPSE
  - ATL_EMPTY_OREB_FLAG
  - FIRST_HALF_BLOWOUT_DISTORTION
  - PLAYOFF_CLOSEOUT_COLLAPSE_FLAG
  - FRUSTRATION_EJECTION_DISTORTION
```

## Patch Status

- Keep: rebound environment tracking, rim-or-3 tracking, lineup size/glass tags.
- Modify: add closeout collapse and empty offensive rebound flags.
- Revert: none.

## Next-Series Carryover For Knicks

- Knicks primary lineup can generate extreme rim pressure and above-break three efficiency when starters are intact.
- Rebound model should trust Knicks defensive glass stability more than raw opponent OREB count.
- Blowout-adjusted filter required for bench-heavy samples from Game 6.

## Final Status

- Rolling update status: complete
- Series status: closed
- Model action: modify with distortion guards
