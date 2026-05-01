# NBA Playoff Postmortem — NYK @ ATL — Game 6 — 2026-04-30

## Game ID / Date

- Game ID: `NBA_2026_PLAYOFFS_R1_NYK_ATL_G6_0430`
- Matchup: New York Knicks @ Atlanta Hawks
- Round: East First Round, Game 6
- Final: Knicks 140, Hawks 89
- Series result: Knicks win series 4-2
- Investments: none
- Pregame model projections: none
- Betting grade: no-action postmortem only

## Source Files Consulted

- `Player box-outs.text`
- `Lineup scoring.text`
- `Lineup shot distribution.text`
- `Player scoring.text`
- `Lineup Rebound stats.text`
- `Player rebounds.text`
- User-provided AP recap in current session
- User-provided series screenshot

## Series Score Map

| Game | Result | Series State |
|---|---:|---|
| Game 1 | NYK 113, ATL 102 | NYK 1-0 |
| Game 2 | ATL 107, NYK 106 | 1-1 |
| Game 3 | ATL 109, NYK 108 | ATL 2-1 |
| Game 4 | NYK 114, ATL 98 | 2-2 |
| Game 5 | NYK 126, ATL 97 | NYK 3-2 |
| Game 6 | NYK 140, ATL 89 | NYK 4-2 |

## Rolling-Form Update

### Series Averages

| Team | Series PTS | Series Avg | Game 6 Delta vs Series Avg |
|---|---:|---:|---:|
| NYK | 707 | 117.8 | +22.2 |
| ATL | 602 | 100.3 | -11.3 |

### Last 3 Games

| Team | G4 | G5 | G6 | Avg |
|---|---:|---:|---:|---:|
| NYK | 114 | 126 | 140 | 126.7 |
| ATL | 98 | 97 | 89 | 94.7 |

### Signal Classification

- Knicks offense: signal confirmed and strengthened.
- Hawks offense: signal broken / collapse confirmed.
- Rebound environment: mixed — Atlanta generated offensive boards, but New York controlled defensive glass and converted better quality.
- Blowout distortion: major. Game 6 should be marked as high-garbage-time distortion after first-half separation.

## Pregame Assumption vs Actual Outcome

No formal pregame projection was logged for this matchup. This postmortem is therefore a pure outcome-ingestion and series-pattern file.

| Category | Pre-Game Assumption | Actual Outcome | Model Lesson |
|---|---|---|---|
| Game script | unavailable | NYK historic blowout, 140-89 | Add playoff closeout blowout environment tag |
| Pace | unavailable | NYK 98 possessions, ATL 100 possessions | Pace alone did not explain margin |
| Shot profile | unavailable | NYK 75.5% on 2PT, ATL 46.8% on 2PT | Shot-quality conversion gap was decisive |
| Rebounds | unavailable | NYK 52 REB, ATL 41 REB | Knicks defensive glass stabilized blowout |
| Discipline | unavailable | Robinson/Daniels ejected after fight | Add frustration/ejection blowout distortion note |

## Team Efficiency Profile

| Team | Poss | PTS | 2PT | 3PT | FT PTS | eFG% | TS% | Shot Quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| NYK | 98 | 140 | 37/49, 75.5% | 13/36, 36.1% | 27 | 66.5% | 69.0% | 0.60 |
| ATL | 100 | 89 | 22/47, 46.8% | 9/36, 25.0% | 18 | 42.8% | 47.3% | 0.51 |

## Shot Profile / Shot Distribution

| Team | Rim or 3 Freq | Rim FGM/FGA | Rim FG% | Above-Break 3 FGM/FGA | AB3 FG% |
|---|---:|---:|---:|---:|---:|
| NYK | 80.0% | 26/32 | 81.3% | 12/29 | 41.4% |
| ATL | 69.9% | 14/22 | 63.6% | 7/25 | 28.0% |

### Shot Profile Read

New York won the game through both shot quality and conversion. The Knicks created a rim-or-3-heavy profile and converted at elite levels at the rim and above the break. Atlanta had a workable rim-or-3 frequency but failed to convert perimeter attempts and generated much lower total efficiency.

### Key Tag

`NYK_RIM_AND_AB3_CONVERSION_SPIKE`

## Lineup Scoring Notes

| Lineup | Min | +/- | Poss | PTS | eFG% | TS% | Read |
|---|---:|---:|---:|---:|---:|---:|---|
| Towns / Anunoby / Hart / Bridges / Brunson | 17:53 | +11 | 36 | 52 | 70.0% | 72.9% | Primary dominance unit |
| Anunoby / Hart / Bridges / Brunson / Robinson | 2:52 | +11 | 7 | 14 | 110.0% | 116.7% | Short-sample explosion before Robinson ejection |
| Anunoby / Brunson / Robinson / McBride / Clarkson | 2:21 | +9 | 6 | 11 | 68.8% | 68.8% | Bench-stagger scoring held |

## Player Scoring / Usage Notes

### Knicks

| Player | MIN | PTS | eFG% | TS% | Usage | Note |
|---|---:|---:|---:|---:|---:|---|
| OG Anunoby | 27:14 | 29 | 92.9% | 90.6% | 25.4 | Primary closeout scoring pop |
| Mikal Bridges | 26:40 | 24 | 91.7% | 92.3% | 21.3 | Elite efficiency wing scoring |
| Jalen Brunson | 28:46 | 17 | 54.2% | 60.7% | 20.9 | Controlled, not overextended |
| Josh Hart | 27:15 | 14 | 70.0% | 70.0% | 19.1 | Connector + rim pressure |
| Karl-Anthony Towns | 27:32 | 12 | 25.0% | 62.5% | 17.5 | FT-driven scoring, rebound anchor |

### Hawks

| Player | MIN | PTS | eFG% | TS% | Usage | Note |
|---|---:|---:|---:|---:|---:|---|
| Jalen Johnson | 32:02 | 21 | 53.3% | 61.8% | 26.0 | Only stable offensive source |
| CJ McCollum | 23:36 | 11 | 34.6% | 39.3% | 27.1 | High usage, low return |
| Nickeil Alexander-Walker | 29:05 | 11 | 43.8% | 50.0% | 20.8 | Inefficient support offense |
| Jonathan Kuminga | 22:48 | 11 | 50.0% | 55.0% | 20.4 | Moderate efficiency, not enough |
| Onyeka Okongwu | 31:46 | 4 | 33.3% | 33.3% | 10.5 | Low offensive impact |

## Rebound Environment Analysis

| Team | REB | DREB | OREB | FG DREB% | FG OREB% | Rim DREB% | AB3 DREB% |
|---|---:|---:|---:|---:|---:|---:|---:|
| NYK | 52 | 40 | 12 | 71.2% | 34.3% | 87.5% | 72.2% |
| ATL | 41 | 26 | 15 | 65.7% | 28.9% | 50.0% | 76.5% |

### Rebound Signal

New York won the total glass 52-41 and owned the defensive glass enough to prevent Atlanta from turning misses into meaningful pressure. Atlanta did record 15 offensive rebounds, but the second-chance environment did not translate into efficient scoring because the Hawks shot only 42.8% eFG and 47.3% TS overall.

### Key Rebound Tags

- `NYK_DEFENSIVE_GLASS_STABLE`
- `ATL_OREB_EMPTY_CALORIES`
- `BLOWOUT_REBOUND_DISTORTION_ACTIVE`
- `KAT_REBOUND_ANCHOR_CONFIRMED`
- `ATL_EFFICIENCY_COLLAPSE_OVERRIDES_OREB`

## Physicality / Box-Out / Hustle Notes

| Team | Screen Ast | Screen Ast PTS | Deflections | Loose Balls Recovered | Contested Shots |
|---|---:|---:|---:|---:|---:|
| NYK | 7 | 16 | 19 | 6 | 46 |
| ATL | 7 | 16 | 14 | 3 | 37 |

New York generated more deflections, more loose-ball recoveries, and more total contested shots. This supports the read that the blowout was not only shot-making variance; it also came from engagement, physical pressure, and defensive activity.

## Ejection / Game-State Distortion

User-provided AP recap notes that Dyson Daniels and Mitchell Robinson were ejected after a fight in the second quarter, and that New York led 83-36 at halftime, described as the largest halftime deficit in NBA playoff history.

### Model Handling

This game should carry a high distortion flag for:

- blowout rotation distortion,
- emotional/frustration event,
- early competitive collapse,
- garbage-time lineup contamination.

Do not use late-game bench minutes as stable player baseline without filtering.

## Patch Evaluation

### Keep

- `REBOUND_ENVIRONMENT_PRIORITY`
- `RIM_OR_3_SHOT_PROFILE_TRACKING`
- `LINEUP_SIZE_AND_GLASS_TAGS`
- `PLAYOFF_SERIES_ROLLING_FORM`

### Modify

- Add `PLAYOFF_CLOSEOUT_COLLAPSE_FLAG`.
- Add `FRUSTRATION_EJECTION_DISTORTION_FLAG`.
- Add `EMPTY_OREB_FLAG` for games where a team wins/competes on OREB but fails to convert due to extreme shooting inefficiency.
- Add first-half blowout detector: if margin >= 25 before halftime, downstream prop and team-total reads should enter distortion mode.

### Revert

- None.

## Retraining Flags

```yaml
retraining_flags:
  - PLAYOFF_CLOSEOUT_COLLAPSE_FLAG
  - FIRST_HALF_BLOWOUT_DISTORTION
  - EMPTY_OREB_FLAG
  - NYK_RIM_AND_AB3_CONVERSION_SPIKE
  - ATL_HALFCOURT_EFFICIENCY_BREAKDOWN
  - FRUSTRATION_EJECTION_DISTORTION
  - GARBAGE_TIME_FILTER_REQUIRED
```

## Confidence Level

- Confidence: High for team-level shot profile and rebound environment.
- Confidence: Medium for player-level carryover because blowout and ejection distort rotations.
- Betting-model applicability: High for future series/team-level Knicks environment; lower for Hawks player props due to eliminated-series context.

## Final Status

- Final model action: `MODIFY`
- Reason: signal is strong, but it requires new distortion guards rather than raw projection updates.
- Next file to update: rolling-form summary for Knicks and Hawks playoff series.
