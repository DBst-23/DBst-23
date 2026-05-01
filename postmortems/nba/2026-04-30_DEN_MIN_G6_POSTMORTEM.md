# NBA Playoff Postmortem — DEN @ MIN — Game 6 — 2026-04-30

## Game ID / Date

- Game ID: `NBA_2026_PLAYOFFS_R1_DEN_MIN_G6_0430`
- Matchup: Denver Nuggets @ Minnesota Timberwolves
- Round: West First Round, Game 6
- Final: Timberwolves 110, Nuggets 98
- Venue: Target Center, Minneapolis, MN
- Officials: Josh Tiven, Courtney Kirkland, JB DeRosa, Brian Forte
- Attendance: 18,978 sellout
- Series result: Minnesota wins 4-2
- Next opponent: Minnesota opens Round 2 at San Antonio

## Investment Ledger

| Market | Entry | Stake | Price / Chance | Result | Return |
|---|---:|---:|---:|---|---:|
| MIN Team Total | Minnesota over 109.5 points | $7.50 | 43% / +123-type payout | WIN | $16.77 paid out |
| Player Rebounds | Cameron Johnson 10+ rebounds | $2.50 | 35% chance | LOSS | $0 |

```yaml
investment_summary:
  total_risked: 10.00
  total_return: 16.77
  net_profit: 6.77
  roi: 67.7
  record: 1-1
```

## Source Files Consulted

- `20260430_DENMIN_book.pdf`
- User-provided series screenshot
- User-provided investment screenshots
- User-provided AP recap
- User-provided NBA Stats hustle/advanced/rebounding lineup extracts

## Final Box Summary

| Team | FG | FG% | 3P | 3P% | FT | REB | AST | TO | PTS |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DEN | 34/75 | 45.3% | 10/27 | 37.0% | 20/25 | 33 | 24 | 13 | 98 |
| MIN | 43/94 | 45.7% | 7/29 | 24.1% | 17/24 | 50 | 26 | 8 | 110 |

## Score Flow

| Quarter | DEN | MIN | Total | Read |
|---|---:|---:|---:|---|
| 1Q | 30 | 29 | 59 | Denver shot efficiency start, live over pace active |
| 2Q | 20 | 28 | 48 | Minnesota seized control with paint/rebound pressure |
| 3Q | 24 | 25 | 49 | Minnesota protected lead despite poor 3P shooting |
| 4Q | 24 | 28 | 52 | Minnesota closed with McDaniels/Shannon/Gobert actions |
| Final | 98 | 110 | 208 | MIN TT clears; full game total not logged as investment |

## Series Score Map

| Game | Result | Series State |
|---|---:|---|
| Game 1 | DEN 116, MIN 105 | DEN 1-0 |
| Game 2 | MIN 119, DEN 114 | 1-1 |
| Game 3 | MIN 113, DEN 96 | MIN 2-1 |
| Game 4 | MIN 112, DEN 96 | MIN 3-1 |
| Game 5 | DEN 125, MIN 113 | MIN 3-2 |
| Game 6 | MIN 110, DEN 98 | MIN wins 4-2 |

## Core Game Diagnosis

Minnesota won without Anthony Edwards, Donte DiVincenzo, and Ayo Dosunmu by going bigger, crashing the glass, and attacking the paint. The official box confirms Minnesota won points in the paint 64-40, second-chance points 20-4, and rebounds 50-33.

Denver hit 10 threes and got 28/10/9 from Jokic, but the Nuggets were overwhelmed on the interior and got only 12 points on 4/17 shooting from Jamal Murray.

## Investment 1 — MIN Team Total Over 109.5

### Result: WIN

| Metric | Number |
|---|---:|
| Entry line | 109.5 |
| Final MIN points | 110 |
| Margin | +0.5 |
| Stake | $7.50 |
| Paid out | $16.77 |

### Why it cashed

- Minnesota generated 94 field-goal attempts.
- Minnesota had 19 offensive rebounds.
- Minnesota scored 20 second-chance points.
- Minnesota scored 64 points in the paint.
- Late-game foul/free-throw sequence preserved the 110-point finish.

### Model Note

This was a thin-margin but valid LiveFlow win. The strongest support was not 3-point shooting; Minnesota shot only 7/29 from three. The cover came from possessions, offensive rebounding, interior volume, and foul-line closure.

```yaml
tag: MIN_TT_OVER_1095_HIT
edge_source:
  - offensive_rebound_volume
  - paint_pressure
  - Denver interior fatigue/foul pressure
  - late_game_free_throw_close
warning:
  - hook_sensitive_win
  - not_repeatable_without rebound/paint dominance
```

## Investment 2 — Cameron Johnson 10+ Rebounds

### Result: LOSS

| Metric | Number |
|---|---:|
| Entry target | 10+ rebounds |
| Final rebounds | 8 |
| Miss margin | -2 |
| Stake | $2.50 |
| Paid out | $0 |

### Why it missed

Cameron Johnson had 7 rebounds by halftime, but Minnesota's second-half possession/rebound pressure and Denver's smaller spacing environment reduced his late rebound access. He finished with 8 rebounds, all defensive, with 0 offensive rebounds.

### Model Note

This was a live ladder that looked strong early but stalled because Denver lost the rebounding environment. Minnesota grabbed 25 second-half rebounds to Denver's 15, including 11 offensive rebounds in the second half.

```yaml
tag: CAM_JOHNSON_REB_LADDER_STALL
trigger:
  - 7 rebounds at halftime
  - finished with 8 rebounds
  - Denver second-half rebound share collapsed
  - Minnesota +10 second-half rebound margin
correction:
  - downgrade wing rebound ladder when opponent OREB rate spikes
  - require live rebound-share confirmation after halftime before ladder extension
```

## Rebound Environment

| Team | OREB | DREB | Total REB | 2nd Chance PTS |
|---|---:|---:|---:|---:|
| DEN | 6 | 27 | 33 | 4 |
| MIN | 19 | 31 | 50 | 20 |

### Rebound-Lineup Signal

User-provided lineup rebound table showed Minnesota team total rebounds at 55 in the tracking dataset, with 21 offensive rebounds and a 37.25% FG OREB rate. Denver was listed at 42 team rebounds and only 8 offensive rebounds in that extract. This confirms the same directional signal as the official scorer box: Minnesota dominated extra possessions and glass control.

```yaml
rebound_profile:
  tag: MIN_REBOUND_ENVIRONMENT_DOMINANCE
  official_reb_margin: MIN +17
  official_oreb_margin: MIN +13
  official_second_chance_margin: MIN +16
  lineup_extract_direction: MIN +13 team rebounds
  model_impact:
    - boost MIN team total support when OREB dominance active
    - downgrade DEN wing rebound ladders once MIN OREB pressure is sustained
```

## Player Notes

### Minnesota

| Player | MIN | PTS | REB | AST | FG | 3P | +/- | Read |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Jaden McDaniels | 44:54 | 32 | 10 | 3 | 13/25 | 1/4 | +16 | Breakout two-way closer; primary Game 6 profile upgrade |
| Terrence Shannon Jr. | 34:42 | 24 | 6 | 1 | 9/20 | 1/7 | +7 | Surprise-start speed/pressure profile |
| Rudy Gobert | 41:46 | 10 | 13 | 8 | 4/6 | 0/0 | +11 | Interior hub, 7 OREB, 8 AST, paint/rebound engine |
| Julius Randle | 37:27 | 18 | 4 | 5 | 6/17 | 2/5 | +15 | Big lineup connector; inefficient but physical |
| Naz Reid | 33:47 | 15 | 7 | 4 | 7/13 | 1/3 | +11 | Bench big pressure, spacing enough, glass support |

### Denver

| Player | MIN | PTS | REB | AST | FG | 3P | +/- | Read |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Nikola Jokic | 43:24 | 28 | 9 | 10 | 11/19 | 1/5 | -9 | Near triple-double, but late turnover and interior stress |
| Cameron Johnson | 39:14 | 27 | 8 | 3 | 8/15 | 5/10 | -3 | Scoring carried Denver, rebound ladder stalled |
| Jamal Murray | 40:18 | 12 | 6 | 4 | 4/17 | 0/2 | -18 | Defensive pressure victim; McDaniels chase impact |
| Tim Hardaway Jr. | 20:59 | 13 | 4 | 2 | 4/7 | 1/2 | -5 | Efficient secondary scoring |
| Spencer Jones | 35:17 | 8 | 2 | 1 | 3/4 | 2/3 | -9 | Low-volume role, foul pressure |

## Injury / Rotation Context

### Denver Inactive

- Aaron Gordon — left calf tightness
- Peyton Watson — right hamstring strain

### Minnesota Inactive

- Kyle Anderson — illness
- Donte DiVincenzo — right Achilles tendon repair
- Anthony Edwards — left knee bone bruise
- Ayo Dosunmu — right calf soreness

### Model Interpretation

Minnesota missing three guards should normally reduce shot creation. In this game, it created a counterintuitive big-lineup edge: more size, more paint attempts, more offensive boards, more Gobert/Randle/Reid involvement, and more McDaniels/Shannon pressure usage.

```yaml
tag: MIN_INJURY_BIG_LINEUP_COUNTEREDGE
trigger:
  - Edwards inactive
  - DiVincenzo inactive
  - Dosunmu inactive
  - MIN starts Shannon Jr.
  - Gobert/Randle/Reid/McDaniels size profile expanded
impact:
  - lower 3P expectation
  - higher paint frequency
  - higher OREB probability
  - higher second-chance points
  - support MIN TT if line is low enough
```

## Advanced / Hustle Signals

### Hustle

| Team | Screen AST | Deflections | Contested Shots | Box Outs |
|---|---:|---:|---:|---:|
| DEN | 11 | 10 | 37 | 4 |
| MIN | 12 | 15 | 45 | 3 |

Minnesota won the hustle layer through deflections and contested shots. Gobert alone contested 21 shots, including 14 two-point attempts and 7 threes. This supports the Murray suppression and Denver interior resistance read.

### Advanced Team Profile

| Team | OFFRTG | DEFRTG | NETRTG | AST/TO | OREB% | DREB% | REB% | PACE | PIE |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| DEN | 105.4 | 118.3 | -12.9 | 1.9 | 19.0 | 61.8 | 43.3 | 93.00 | 43.1 |
| MIN | 118.3 | 105.4 | +12.9 | 3.3 | 38.2 | 81.0 | 56.7 | 93.00 | 56.9 |

Minnesota's 38.2 OREB% and 81.0 DREB% are the model-defining metrics for this postmortem.

## Pivotal Moments

1. **Second quarter pivot** — Minnesota won Q2 28-20 and turned a one-point deficit into a seven-point halftime lead.
2. **Third quarter survival** — Denver repeatedly got within one possession, but Minnesota kept answering through Gobert putbacks, McDaniels midrange, and Reid/Shannon pressure.
3. **4Q 7:46 Naz Reid three** — gave Minnesota breathing room after Denver cut it to one.
4. **4Q 6:38 Gobert tip layup** — reinforced the offensive-rebound edge.
5. **4Q 1:43 Shannon and-one** — pushed lead to six.
6. **4Q 1:07 McDaniels 19-foot pull-up** — dagger to make it 105-98.
7. **4Q 1:01 McDaniels steal on Jokic** — final closeout possession swing.

## Signal vs Noise

| Signal | Classification | Reason |
|---|---|---|
| MIN big lineup | Confirmed edge | 64 paint points, 19 OREB, +17 rebounds |
| McDaniels offensive ceiling | Confirmed upgrade | 32/10 on 44:54 minutes |
| Shannon Jr. speed pressure | Confirmed playoff utility | 24 points in surprise start |
| Gobert passing hub | Confirmed | 8 assists, 10 screen-assist points per user extract |
| Murray suppression | Confirmed | 12 points, 4/17 FG, -18 |
| Cam Johnson rebound ladder | Failed live extension | 8 final despite 7 at half |
| MIN TT Over 109.5 | Correct edge | Cashed by hook via paint/OREB/FT close |

## Patch Evaluation

### Keep

- `LIVEFLOW_REBOUND_ENVIRONMENT_TRACKER`
- `BIG_LINEUP_COUNTEREDGE`
- `OREB_SECOND_CHANCE_TT_BOOST`
- `MCDANIELS_DEFENSIVE_SUPPRESSION_PROFILE`
- `GOBERT_INTERIOR_HUB_PROFILE`

### Modify

- Add `WING_REBOUND_LADDER_STALL_AFTER_HALFTIME`.
- Add `MIN_BIG_LINEUP_WITHOUT_GUARDS_PROFILE`.
- Add `MURRAY_CHASE_DEFENDER_SUPPRESSION_GATE`.
- Add `TEAM_TOTAL_HOOK_SENSITIVITY_FLAG` for wins by 0.5 to 1.5 points.

### Revert

- None.

## Retraining Flags

```yaml
retraining_flags:
  - MIN_TT_OVER_1095_HIT
  - CAM_JOHNSON_REB_LADDER_STALL
  - MIN_REBOUND_ENVIRONMENT_DOMINANCE
  - MIN_BIG_LINEUP_COUNTEREDGE
  - MCDANIELS_TWO_WAY_BREAKOUT
  - SHANNON_SURPRISE_START_SPEED_PRESSURE
  - GOBERT_INTERIOR_HUB_8AST
  - MURRAY_SUPPRESSION_BY_LENGTH
  - DEN_SUPPORT_SCORING_FAILURE
  - SERIES_CLOSEOUT_ENERGY_SPIKE
```

## Final Status

- Postmortem status: complete
- Investment record: 1-1
- Net result: +$6.77
- Model action: modify
- Confidence: high
- Reason: official box, AP recap, investment screenshots, and NBA Stats extracts all converge on the same read: Minnesota's size, rebounding, paint pressure, and defensive length decided the game.
