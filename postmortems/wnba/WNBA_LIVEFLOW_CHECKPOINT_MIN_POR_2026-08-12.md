# WNBA LIVE-FLOW Checkpoint — Minnesota Lynx at Portland Fire

## Market-Blind Freeze
- Date: 2026-08-12
- Checkpoint: Halftime
- Score: Minnesota 57, Portland 33
- Market viewed before projection: NO

## Halftime Read
Minnesota: 57 points, 20/38 FG (52.6%), 6/11 3PT (54.5%), 11/13 FT, 5 ORB, 22 REB, 19 AST, 4 TO, 5 STL, 4 BLK.

Portland: 33 points, 13/35 FG (37.1%), 4/16 3PT (25.0%), 3/8 FT, 4 ORB, 17 REB, 10 AST, 8 TO, 3 STL, 1 BLK.

Estimated first-half possession environment: about 42.6 possessions per team, equivalent to roughly an 85-possession full-game pace if maintained. This is a high-opportunity environment; the 90-point halftime total is not evidence of a slow game.

Key structural notes:
- Minnesota's first-half offense is highly efficient but not purely random: 19 assists on 20 made field goals, only 4 turnovers, 22 paint points, and 11 fast-break points support real offensive control.
- Minnesota's 54.5% three-point shooting is above sustainable expectation and should regress downward.
- Portland's 21.4% shooting in Q2 and 37.5% first-half free-throw shooting are also unlikely to persist; the model expects meaningful positive scoring regression from Portland.
- Portland's 8 turnovers materially suppressed first-half scoring. Even modest turnover normalization raises second-half scoring potential.
- The 24-point margin creates blowout/rotation risk. Minnesota may reduce starter load and tempo, while Portland can accumulate late-game scoring against reserve units.
- Because the prior TOR-DAL miss exposed the danger of confusing low realized efficiency with low opportunity, this projection explicitly separates possession volume from current conversion.

## Frozen SharpEdge Projection
### Second Half
- Minnesota: 41
- Portland: 43
- 2H total: 84
- 2H margin: Portland +2

### Full Game
- Minnesota: 98
- Portland: 76
- Full-game total: 174
- Full-game margin: Minnesota +22

## SharpEdge Fair Lines
- Spread: Minnesota -22
- Total: 174
- Minnesota team total: 98
- Portland team total: 76

## Initial Classification
- Minnesota side: NEUTRAL pending market comparison because the 24-point halftime lead introduces strong garbage-time variance.
- Full-game total: FAIR 174; compare market only after this freeze.
- Minnesota team total: LEAN UNDER only if market is materially above 98.
- Portland team total: LEAN OVER only if market is materially below 76.

## Volatility / State Tags
- HIGH_PACE_EFFICIENCY_DIVERGENCE
- MINNESOTA_PERIMETER_REGRESSION_RISK
- PORTLAND_SHOOTING_REGRESSION_UP
- BLOWOUT_ROTATION_VARIANCE
- GARBAGE_TIME_SCORING_RISK

## Calibration Notes
This is not treated as a simple '57+33=180 pace' extrapolation. Minnesota should cool from extreme three-point efficiency, while Portland should rebound from a 10-point second quarter, 21.4% Q2 field-goal shooting, and 3/8 first-half free throws. High first-half possession volume keeps the upper tail alive despite the lopsided score. The most balanced market-blind center is 174, with a wider-than-normal variance band because the second half can be shaped heavily by rotations and garbage time.

```yaml
game_id: WNBA_2026-08-12_MIN_POR
checkpoint: halftime
score_at_checkpoint:
  MIN: 57
  POR: 33
market_seen: false
estimated_first_half_possessions_per_team: 42.6
model:
  second_half:
    MIN: 41
    POR: 43
    total: 84
    margin: POR_2
  final:
    MIN: 98
    POR: 76
    total: 174
    margin: MIN_22
fair_lines:
  spread: MIN_-22
  total: 174
  min_tt: 98
  por_tt: 76
volatility_tags:
  - HIGH_PACE_EFFICIENCY_DIVERGENCE
  - MINNESOTA_PERIMETER_REGRESSION_RISK
  - PORTLAND_SHOOTING_REGRESSION_UP
  - BLOWOUT_ROTATION_VARIANCE
  - GARBAGE_TIME_SCORING_RISK
status: FROZEN_AWAITING_MARKET
```
