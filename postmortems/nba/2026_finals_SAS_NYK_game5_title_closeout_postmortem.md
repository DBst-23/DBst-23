# SAS @ NYK - 2026 NBA Finals Game 5 Title Closeout Postmortem

## Game ID / Date
- game_id: `2026_NBA_FINALS_G5_NYK_AT_SAS`
- date: `2026-06-13`
- venue: Frost Bank Center, San Antonio, TX
- final: NYK 94, SAS 90
- series_result: Knicks win series 4-1
- title_result: New York Knicks NBA Champions

## Source files consulted
- `20260613_NYKSAS_book.pdf` official NBA scorer report
- User-provided AP recap text
- Prior SAS-NYK Game 4 rolling baseline
- LiveFlow halftime simulation notes from current workspace

## Final box anchors
- Knicks: 31/87 FG, 12/37 3PT, 20/28 FT, 48 REB, 13 OREB, 35 DREB, 14 AST, 10 TO, 94 PTS.
- Spurs: 33/86 FG, 12/37 3PT, 12/19 FT, 47 REB, 14 OREB, 33 DREB, 18 AST, 12 TO, 90 PTS.
- Jalen Brunson: 45 PTS, 14/27 FG, 4/7 3PT, 13/15 FT, +10.
- Victor Wembanyama: 19 PTS, 14 REB, 5 BLK.
- Josh Hart: 13 PTS, 11 REB.
- Mitchell Robinson: 10 REB, 6 OREB in 19:59.
- De'Aaron Fox: 7 PTS, 0 REB, 5 AST.

## Rolling-form update
Known full team-stat Finals rebound window, Games 2-5:
- G2 total team rebounds: 107
- G3 total team rebounds: 104
- G4 total team rebounds: 103
- G5 total team rebounds: 95
- mean: 102.25
- median: 103.5
- trend: opportunity fell in Game 5 despite high miss count.

Game 5 player-summed rebound total:
- Knicks 48, Spurs 47, total 95
- Game 5 official team rebounds including team rebounds: Knicks 66 gross accounting if player + team, Spurs 59 gross accounting if player + team. For prop logic, use player-summed only.

## Pregame assumption vs actual outcome
Pregame baseline:
- NYK +5.5 as main spread edge.
- NYK ML small plus-money edge.
- Fox 4+ REB as best prop edge.
- Live halftime strike: Over 184.5 at +101 after projected regression.

Actual:
- NYK +5.5 cashed.
- NYK ML cashed.
- Fox 4+ REB failed with 0 rebounds.
- Over 184.5 failed by 0.5 point; final total was 184.

## Rebound environment analysis
- Rebound environment remained strong but became player-specific rather than guard-distributed.
- Knicks and Spurs combined for 95 player rebounds.
- Mitchell Robinson and Josh Hart were the best Knicks rebound validators.
- Wembanyama validated elite big baseline with 14 rebounds.
- Fox remained at 0 rebounds despite 36:46 minutes, invalidating the long-rebound guard carryover for him.

## Rotation and fatigue notes
- Towns fouled out and played only 22:44, scoring 2 points but grabbing 10 rebounds.
- Robinson's 19:59 minutes with 10 rebounds and 6 OREB confirmed per-minute offensive glass value.
- Brunson played 41:07 and fully centralized the fourth-quarter offense.
- Wembanyama played 37:52; Kornet played 10:15 despite illness tag.

## Patch evaluation
| Patch | Status | Reason |
|---|---|---|
| NYK comeback/clutch resilience | KEEP | Knicks won after trailing by 16 and outscored SAS 29-18 in Q4. |
| NYK +5.5 spread resilience | KEEP | Closing margin NYK +4 outright; spread thesis fully validated. |
| NYK ML plus-money sprinkle | KEEP | Small plus-money position cashed. |
| Long-rebound guard boost - Fox | REVERT | Fox had 0 rebounds in 36:46 despite high 3PA environment. |
| Long-rebound environment - team level | MODIFY | Valid for Hart/wing/big crashers, not automatically guards. |
| Knicks weakside/physical rebound crash | KEEP | Hart 11 REB, Robinson 10 REB, OG 8 REB. |
| Knicks center blanket over | MODIFY | Towns foul risk remains severe; Robinson per-minute glass deserves separate boost. |
| Spurs late-game execution decay | KEEP | SAS scored only 18 in Q4 and lost another double-digit lead. |
| Live halftime total regression over | MODIFY | Direction was close but line lost by 0.5; add late-game suppression/foul-miss gate. |
| Team rebound accounting split | KEEP | Official team rebound accounting continues to differ from prop-relevant player rebounds. |

## Retraining flags
- Add `brunson_clutch_takeover_usage_gate`.
- Add `spurs_fourth_quarter_execution_decay`.
- Add `fox_rebound_role_zero_floor_flag`.
- Add `live_total_late_game_suppression_gate` for low-scoring elimination games.
- Split `long_rebound_guard_boost` into player-specific role/rim-run/boxout availability.
- Upgrade `mitchell_robinson_oreb_per_minute_gate`.

## Confidence level
- Confidence: 0.91
- Reason: Full official scorer report available with final, quarter, half, and play-by-play detail.

## Final status
MODIFY overall.

The macro model was right on Knicks resilience and spread/ML value. The prop model needs a Fox-specific rebound role downgrade, and LiveFlow totals need an added late-game suppression gate when elimination-game pace is low and the leading team enters clock-control mode.
