# NBA LiveFlow Attack Window — DEN @ MIN — 2Q 01:19

## Metadata

- Game: Denver Nuggets @ Minnesota Timberwolves
- Date: 2026-04-30
- Mode: LIVEFLOW_STRIPPED_MODE_ACTIVE
- Snapshot: 2Q 01:19 remaining
- Score: DEN 49, MIN 54
- Current total: 103
- Q1 score: DEN 30, MIN 29
- Q2 partial: DEN 19, MIN 25
- Purpose: updated market line evaluation, rebound board, and single-fire LiveFlow decision

## Market Snapshot

### Full Game / Spread

- Full-game total: 219.5
  - Over -168
  - Under +128
- Spread: Denver by over 3.5
  - Yes +113
  - No -143

### Team Totals

- Minnesota over 112.5
  - Yes +105
  - No -191
- Denver over 112.5
  - Yes +145
  - No -209

### Player Rebounds

- Nikola Jokic current rebounds: 3
  - 12+ -143
  - 14+ +265
- Rudy Gobert current rebounds: 5
  - 12+ +109
  - 14+ +207
- Julius Randle current rebounds: 3
  - 8+ -191
  - 10+ +252
  - 12+ +573
- Cameron Johnson current rebounds: 6
  - 8+ -183
  - 10+ +228
- Jaden McDaniels current rebounds: 4
  - 6+ -720
  - 8+ -137

## Box Snapshot

### Denver

- Score: 49
- FG: 17/36, 47.2%
- 3PT: 5/12, 41.7%
- FT: 5/6, 83.3%
- REB: 16 total, 3 offensive
- AST: 12
- STL: 3
- BLK: 5
- TOV: 9
- Fastbreak points: 5
- Paint points: 20
- Second-chance points: 0

### Minnesota

- Score: 54
- FG: 21/43, 48.8%
- 3PT: 4/13, 30.8%
- FT: 7/9, 77.8%
- REB: 21 total, 6 offensive
- AST: 13
- STL: 6
- BLK: 1
- TOV: 4
- Fastbreak points: 10
- Paint points: 30
- Second-chance points: 8

## Player Notes

### Denver

- Cameron Johnson: 13 min, 11 pts, 6 reb, 4/4 FG, 1/1 3PT, 2/3 FT
- Nikola Jokic: 16 min, 7 pts, 3 reb, 5 ast, 3 tov, 2 pf
- Jamal Murray: 19 min, 6 pts, 3 reb, 3 ast, 3/10 FG
- Tim Hardaway Jr.: 6 min, 8 pts, 0 reb

### Minnesota

- Rudy Gobert: 17 min, 4 pts, 5 reb, 3 ast
- Julius Randle: 18 min, 9 pts, 3 reb, 3 ast
- Jaden McDaniels: 19 min, 11 pts, 4 reb
- Naz Reid: 12 min, 8 pts, 4 reb, 3 ast
- Terrence Shannon Jr.: 15 min, 10 pts, 2 reb

## LiveFlow Tags

- TOTAL_MARKET_REPRICED_DOWN_TO_219_5
- OVER_PRICE_TOO_EXPENSIVE
- UNDER_PLUS_MONEY_BUT_STATE_CONFLICT
- MIN_POSSESSION_EDGE_PERSISTENT
- MIN_OREB_EDGE_ACTIVE
- DEN_TURNOVER_DRAG_ACTIVE
- DEN_SECOND_CHANCE_ZERO
- GOBERT_REBOUND_LADDER_REACTIVATED
- CAM_JOHNSON_REBOUND_VALUE_REDUCED
- JOKIC_REBOUND_MARKET_MISPRICED_TO_NAME
- RISK_CLUSTER_LOCK_ACTIVE

## Read

The total market dropped back to 219.5, but over is heavily juiced at -168. Under is plus-money at +128, but the current game state is not clean enough to fire under because Minnesota continues to win the extra-possession battle with 6 offensive rebounds, 6 steals, 10 fastbreak points, 30 paint points, and 8 second-chance points.

Denver is showing regression from the early efficiency spike, but Minnesota's possession engine is keeping scoring pressure alive. This creates a no-fire zone on the full-game total.

Rebound board: Jokic name tax is severe given only 3 rebounds and foul/TOV drag. Cameron Johnson is live but the 8+ price is now too expensive at -183. Gobert 12+ at +109 is the cleanest rebound watch because he is up to 5 rebounds, minutes are stable, and Minnesota's interior/OREB environment remains active.

## Decision

Status: HOLD / NO SINGLE-FIRE.

### Best Watch

- Rudy Gobert 12+ rebounds +109
  - Current: 5
  - Estimated mean: 10.0 to 11.2
  - Median: 10
  - Estimated hit probability: 48% to 52%
  - Edge: thin, needs plus-money and second-half minutes confirmation

### Pass

- Full-game over 219.5 at -168: price too expensive.
- Full-game under 219.5 +128: not enough state alignment due to Minnesota extra possessions.
- Denver team total over 112.5 +145: score path possible but turnover/OREB profile too weak.
- Denver team total no 112.5 -209: too expensive.
- Jokic rebounds: name-tax misprice.
- Cameron Johnson 8+ at -183: value mostly gone.
- McDaniels 8+ at -137: overpriced.

## Next Trigger

- If live total climbs to 222.5+ before halftime without another pace spike, under watch reactivates.
- If Gobert remains at 5+ rebounds and 12+ stays plus-money into halftime, evaluate as second-half rebound attack.
- If Minnesota team total drops back to 109.5, re-evaluate MIN TT over.
