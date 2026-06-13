# SAS @ NYK — 2026 NBA Finals Game 4 Postmortem

## Game ID / Date
- game_id: `2026_NBA_FINALS_G4_SAS_AT_NYK`
- date: `2026-06-10`
- venue: Madison Square Garden, New York, NY
- final: NYK 107, SAS 106
- series_after: NYK leads 3-1
- market_close_observed: NYK -2.5 spread equivalent from FOX note; total 216.5; final total 213, under cashed.

## Source files consulted
- `Charlotte_updated_prompt_4-30-2026.text`
- `NBA_playoff_team_rebound_system_summary.txt`
- CBS Sports GameTracker, SAS @ NYK Game 4
- NBA.com Game 4 live recap
- FOX Sports Game 4 market/result page
- Bleacher Report Game 5 odds preview

## Rolling-form update
Rolling-window rules applied:
- recent_form: last 5 games when available
- secondary_validation: last 10 games when available
- series_window: current Finals series, Games 1-4
- Game 1 team rebound table unavailable in fetched sources; do not backfill invented values.

Series known full team-stat rebound window, Games 2-4:
- G2: NYK 55, SAS 52, total 107; OREB NYK 10, SAS 5
- G3: SAS 48, NYK 56, total 104; OREB SAS 6, NYK 12
- G4: SAS 50, NYK 53, total 103; OREB SAS 12, NYK 8
- team-stat total rebounds mean: 104.67
- team-stat total rebounds median: 104
- total offensive rebounds mean: 17.67
- total offensive rebounds median: 18

Player-summed rebound window, Games 2-4:
- G2: NYK 44, SAS 42
- G3: NYK 46, SAS 37
- G4: NYK 39, SAS 42
- player-summed total rebounds mean: 83.33
- player-summed total rebounds median: 83

## Pregame assumption vs actual outcome
Pregame baseline assumptions:
- Knicks: DOUBLE_BIG_ACTIVE, CRASH_HEAVY_OFFENSIVE, PUTBACK_RATE_BOOST_ON, CONDENSED_REBOUND_TREE, WEAKSIDE_CRASH_ELITE.
- Spurs: ELITE_DEF_REBOUND_TEAM, DOUBLE_BIG_ACTIVE, RIM_PROTECTION_TO_REBOUND_PIPELINE, LOW_VARIANCE_REBOUND_TEAM.

Actual Game 4:
- Spurs led 41-22 after Q1 and 76-49 at halftime.
- Knicks won Q4 32-16 and completed a 29-point comeback.
- Knicks won final score but did not dominate player-summed boards: SAS 42, NYK 39.
- Team-stat rebounds favored NYK 53-50 due to team rebound accounting.
- Offensive rebounds favored SAS 12-8, but NYK produced the decisive offensive rebound: OG Anunoby putback with 0:02/1.2 seconds left.

Classification:
- Knicks weakside crash: SIGNAL CONFIRMED.
- Knicks generic center rebound over bias: SIGNAL WEAKENED.
- Spurs defensive suppression: SIGNAL WEAKENED late, but not fully broken by total board count.
- Late-game fatigue/lineup decay: SIGNAL CONFIRMED.

## Rebound environment analysis
Key environment finding:
- Miss creation remained stable across Games 2-4, but capture location shifted late.
- G4 three-point volume: SAS 17/43, NYK 15/32; combined 75 3PA.
- G4 total FG misses: SAS 50, NYK 42; combined 92 FG misses.
- G4 was not a low-opportunity rebound game; it was a capture-quality and late-clock decision game.

Rebound tags activated:
- LONG_REBOUND_GENERATOR: active, combined 75 3PA.
- WEAKSIDE_CRASH_ELITE: confirmed by Anunoby game-winning putback.
- CENTER_DISPLACEMENT_RISK_ON: modified upward for Wembanyama when pulled into contest/block/transition sequences.
- FATIGUE_DECAY_BIG_CLOSE: added from Wembanyama 43-minute load and late FT misses/closing possessions.
- TEAM_REBOUND_ACCOUNTING_SPLIT: added to separate sportsbook/player-prop rebounds from official team rebounds.

## Rotation and fatigue notes
- Wembanyama: 43 minutes, 24 PTS, 13 REB, 5 OREB, 8 DREB, 9/25 FG, 2/8 3PT, 4/7 FT, +1.
- Towns: 25 minutes, 13 PTS, 10 REB, 2 OREB, 8 DREB, +17; foul/minute cap remains active.
- Mitchell Robinson: 12 minutes, 5 REB, 3 OREB, -14; high OREB/min but volatile minute floor.
- Hart: 32 minutes, 8 REB, 2 OREB, 6 DREB, +11.
- Anunoby: 41 minutes, 4 REB, 1 OREB, 3 DREB; final OREB was maximum leverage.
- Kornet: only 4 minutes; Game 5 illness/questionable status increases Wembanyama load risk.

## Patch evaluation
| Patch | Status | Reason |
|---|---|---|
| Knicks CRASH_HEAVY_OFFENSIVE | KEEP | Decisive weakside putback; recurring late rebound pressure. |
| Knicks CONDENSED_REBOUND_TREE | MODIFY | NYK top-heavy boards softened; Brunson/OG scoring load widened role distribution. |
| Knicks CENTER_REB_OVER boost | MODIFY | Towns minutes/fouls and Robinson volatility make center-only overs unstable. |
| Spurs ELITE_DEF_REBOUND_TEAM | MODIFY | Team still competitive on glass, but late weakside leaks appeared. |
| Spurs LOW_VARIANCE_REBOUND_TEAM | REVERT | Series has become volatility/fatigue-dependent; G4 collapse invalidates low-variance assumption. |
| LONG_REBOUND_GENERATOR | KEEP | 75 combined 3PA, 92 combined FG misses, wing/guard rebounds remain live. |
| EFFICIENCY_SUPPRESS_REBOUNDS | MODIFY | Efficiency was high enough to threaten unders, but miss count stayed stable. Use only after live efficiency gate >54% eFG through 2Q. |
| LATE_GAME_EXECUTION_DECAY | KEEP | Spurs have repeatedly lost late leads/late possessions. |
| FATIGUE_DECAY_BIG_CLOSE | KEEP | Wembanyama 43 minutes plus Game 5 backup-big uncertainty. |
| TEAM_REBOUND_ACCOUNTING_SPLIT | KEEP | Official team rebounds and player-summed rebounds diverged materially. |

## Retraining flags
- Add feature: `late_game_weakside_oreb_probability`
- Add feature: `center_fatigue_decay_by_minutes_36plus`
- Add feature: `team_rebound_vs_player_prop_rebound_split`
- Modify feature: `spurs_low_variance_rebound_team` -> `spurs_structural_rebound_strength_with_fatigue_decay`
- Modify feature: `knicks_center_rebound_boost` -> split into `towns_minutes_gate`, `robinson_oreb_per_min_gate`, `hart_weakside_guard_rebound_gate`, `anunoby_high_leverage_crash_gate`

## Confidence level
- Confidence: 0.76
- Reason: Game 4 box and Game 2-4 trend data are strong; Game 1 full team-stat rebound table unavailable in fetched sources.

## Final status
MODIFY overall.

Keep LiveFlow active, but update the baseline from static team DNA to rolling, game-state-aware rebound capture.
