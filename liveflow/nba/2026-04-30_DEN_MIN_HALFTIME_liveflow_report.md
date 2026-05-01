# NBA LiveFlow Halftime Report — DEN @ MIN

## Metadata

- Game: Denver Nuggets @ Minnesota Timberwolves
- Date: 2026-04-30
- Mode: LIVEFLOW_STRIPPED_MODE_ACTIVE
- Snapshot: Halftime
- Score: DEN 50, MIN 57
- Halftime total: 107
- Q1: DEN 30, MIN 29
- Q2: DEN 20, MIN 28
- Purpose: halftime market, rebound board, possession environment, and single-fire decision

## Halftime Market Snapshot

### Full Game / Spread

- Full-game total: 219.5
  - Over -117
  - Under -104
- Spread: Denver by over 3.5
  - Yes +123
  - No -149

### Team Totals

- Minnesota over 109.5
  - Yes -132
  - No +109
- Denver over 112.5
  - Yes +158
  - No -200

### Player Rebounds

- Nikola Jokic current rebounds: 3
  - 12+ +198
  - 14+ +279
- Rudy Gobert current rebounds: 5
  - 12+ +118
  - 14+ +489
- Julius Randle current rebounds: 3
  - 8+ -191
  - 10+ +279
  - 12+ +573
- Cameron Johnson current rebounds: 7
  - 8+ -661
  - 10+ +165
- Jaden McDaniels current rebounds: 5
  - 6+ -870
  - 8+ -112

## Halftime Team Stats

### Denver

- Points: 50
- FG: 19/41, 46.3%
- 3PT: 6/14, 42.9%
- FT: 6/8, 75.0%
- Rebounds: 18 total, 3 offensive
- Assists: 14
- Steals: 3
- Blocks: 7
- Turnovers: 9
- Points off turnovers: 7
- Fastbreak points: 5
- Paint points: 20
- Second-chance points: 0
- Fouls: 11

### Minnesota

- Points: 57
- FG: 22/49, 44.9%
- 3PT: 4/15, 26.7%
- FT: 9/11, 81.8%
- Rebounds: 25 total, 8 offensive
- Assists: 13
- Steals: 6
- Blocks: 2
- Turnovers: 4
- Points off turnovers: 9
- Fastbreak points: 10
- Paint points: 32
- Second-chance points: 8
- Fouls: 10

## Player Notes

### Denver

- Cameron Johnson: 17 min, 15 pts, 7 reb, 5/5 FG, 2/2 3PT, 3/5 FT
- Nikola Jokic: 19 min, 9 pts, 3 reb, 6 ast, 3 tov, 2 pf
- Jamal Murray: 22 min, 6 pts, 3 reb, 3 ast, 3/11 FG
- Tim Hardaway Jr.: 9 min, 10 pts, 0 reb, 3/4 FG
- Jonas Valanciunas: 4 min, 2 pts, 2 reb, 1 OREB

### Minnesota

- Jaden McDaniels: 22 min, 13 pts, 5 reb, 2 ast
- Julius Randle: 21 min, 12 pts, 3 reb, 3 ast
- Rudy Gobert: 20 min, 4 pts, 5 reb, 3 ast
- Terrence Shannon Jr.: 18 min, 12 pts, 4 reb
- Naz Reid: 15 min, 8 pts, 4 reb, 3 ast

## LiveFlow Tags

- HALFTIME_TOTAL_107
- MIN_POSSESSION_EDGE_ACTIVE
- MIN_OREB_EDGE_ACTIVE
- DEN_TURNOVER_DRAG_ACTIVE
- DEN_SECOND_CHANCE_ZERO
- MIN_PAINT_PRESSURE_ACTIVE
- DEN_PERIMETER_EFFICIENCY_REGRESSION_WATCH
- CAM_JOHNSON_REBOUND_SPIKE_ACTIVE
- GOBERT_REBOUND_LADDER_THIN_EDGE
- JOKIC_REBOUND_FADE_CONTEXT
- MIN_TEAM_TOTAL_OVER_ACTIVE_BUT_PRICEY
- DEN_TEAM_TOTAL_NO_CORRELATED_UNDER_WATCH
- FULL_GAME_TOTAL_NO_CLEAR_EDGE
- RISK_CLUSTER_LOCK_ACTIVE

## Read

Minnesota leads 57-50 at halftime behind possession quality rather than hot shooting. The Wolves have 8 offensive rebounds, 32 paint points, 10 fastbreak points, 8 second-chance points, and only 4 turnovers. Denver has 9 turnovers, only 3 offensive rebounds, and 0 second-chance points.

The full-game total sits at 219.5 with 107 points already scored. That requires 113+ second-half points to go over. The number is fair to slightly high, but Minnesota's possession engine and Denver's need to chase prevent a clean under fire.

Minnesota team total over 109.5 requires 53 second-half points. Given Minnesota's possession edge, this is live, but -132 is not a bargain. Denver team total over 112.5 requires 63 second-half points and is not supported by the current possession/turnover profile.

Rebound environment is interior-heavy with Minnesota controlling the offensive glass. Wing rebound ladders are not clean except Cameron Johnson, who already has 7 rebounds but whose price has mostly adjusted. Gobert 12+ remains the best plus-money big rebound ladder, but it is still thin because he needs 7 second-half rebounds.

## Decision

Status: HOLD / NO SINGLE-FIRE AT HALFTIME.

### Best Watch List

1. Minnesota team total over 109.5 if price improves to plus money or line drops back live.
2. Cameron Johnson 10+ rebounds +165 as a volatile continuation ladder if second-half minutes stay high.
3. Rudy Gobert 12+ rebounds +118 only if he opens Q3 with early rebound activity.
4. Denver team total no 112.5 if the price improves from -200 and Denver starts Q3 cold/turnover-heavy.

### Pass List

- Full-game over 219.5 at -117: not enough edge after halftime line reset.
- Full-game under 219.5 at -104: state conflict because Minnesota has persistent extra possessions.
- Denver team total over 112.5 +158: needs 63 second-half points with weak OREB and turnover drag.
- Jokic rebound ladders: underpaced with only 3 rebounds and name-tax pricing.
- Jaden McDaniels 8+ -112: not enough price edge.

## Trigger Map

- If full-game total jumps to 222.5+ early Q3 without a true pace spike: under watch reopens.
- If MIN team total remains 109.5 and price moves to -110 or better: MIN TT over becomes single-fire candidate.
- If Cameron Johnson gets his 8th rebound early Q3 and 10+ remains plus money: 10+ ladder becomes live candidate.
- If Gobert reaches 7 rebounds before Q3 8:00 and 12+ stays plus money: Gobert ladder becomes live candidate.

## Risk Rule

LIVEFLOW_STRIPPED_MODE_ACTIVE: one open bet only. Avoid stacking correlated Minnesota team-total over with full-game over. Avoid stacking full-game under with Denver team-total no unless one is explicitly marked as a hedge/post-entry adjustment.
