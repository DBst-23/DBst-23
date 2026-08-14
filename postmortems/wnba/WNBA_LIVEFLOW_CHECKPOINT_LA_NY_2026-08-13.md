# WNBA LIVE-FLOW Checkpoint — Los Angeles Sparks at New York Liberty

## Market-Blind Freeze
- Date: 2026-08-13
- Checkpoint: Halftime
- Score: New York 49, Los Angeles 32
- Market viewed before projection: NO

## Halftime Read
Los Angeles: 32 points, 13/31 FG (41.9%), 4/16 3PT (25.0%), 2/4 FT, 3 ORB, 14 REB, 9 AST, 10 turnovers.

New York: 49 points, 20/44 FG (45.5%), 4/15 3PT (26.7%), 5/6 FT, 11 ORB, 25 REB, 16 AST, 5 turnovers.

Estimated first-half possession environment: roughly 42 possessions per team. The 81-point halftime total is not especially slow; New York generated 44 field-goal attempts plus 11 offensive rebounds, while Los Angeles lost 10 possessions to turnovers.

Key structural notes:
- New York's scoring is being driven by volume and interior control, not hot three-point shooting. The Liberty have 32 paint points, 13 second-chance points, 12 fast-break points, and 11 offensive rebounds despite shooting only 26.7% from three.
- Jonquel Jones has 12 rebounds in 17:04 with 5 offensive boards, signaling a major possession-extension edge.
- Los Angeles has 10 turnovers and only 32 points. That suppresses scoring now, but turnover regression can lift the Sparks' second-half offense.
- Los Angeles is also only 25% from three and 50% at the line, so some positive efficiency regression is reasonable.
- New York does have a 17-point halftime lead, so blowout/rotation risk must be included. However, unlike the prior Minnesota case, New York's first-half offense is not inflated by unsustainably hot perimeter shooting; its scoring base is more structurally supported.
- Sabrina Ionescu is 1/7 from the field and 1/5 from three. That creates an additional New York positive-regression tail if normal usage continues.
- Cameron Brink already has 3 fouls in 10:36, which can weaken Los Angeles rim protection and rebounding if her second-half minutes are constrained.

## Frozen SharpEdge Projection
### Second Half
- Los Angeles: 38
- New York: 45
- 2H total: 83
- 2H margin: New York +7

### Full Game
- Los Angeles: 70
- New York: 94
- Full-game total: 164
- Full-game margin: New York +24

## SharpEdge Fair Lines
- Spread: New York -24
- Total: 164
- New York team total: 94
- Los Angeles team total: 70

## Projection Logic
### New York
Expected second-half scoring remains healthy because the Liberty's first-half offense is supported by repeatable opportunity creation rather than unsustainable shotmaking:
- 11 offensive rebounds
- 32 paint points
- 16 assists
- only 5 turnovers
- 44 field-goal attempts
- only 26.7% from three

A modest drop from 49 first-half points is appropriate because of the 17-point lead and potential rotation effects, but a collapse similar to Minnesota's prior game is not the base case.

### Los Angeles
The Sparks project upward from 32 because 10 first-half turnovers, 25% three-point shooting, and 50% free-throw shooting leave room for positive regression. The offense still has structural issues, though: low shot volume, weak rebounding, and New York's defensive pressure have limited clean possession quality.

## Initial Classification
- New York side: LEAN NY if market is materially shorter than -24; otherwise pass due to blowout variance.
- Full-game total: compare to 164 only after market reveal.
- New York team total: strongest directional interest is OVER only if the market sits materially below 94; do not auto-fade the leading favorite simply because of the score.
- Los Angeles team total: lean OVER only if market is meaningfully below 70, because turnover and shooting regression support a better second half.

## Volatility / State Tags
- NY_INTERIOR_VOLUME_DOMINANCE
- OFFENSIVE_REBOUND_POSSESSION_EXTENSION
- LOW_3P_SCORING_BASE_NOT_INFLATED
- LA_TURNOVER_REGRESSION_UP
- LA_SHOOTING_REGRESSION_UP
- BRINK_FOUL_TROUBLE_FRONTCOURT_RISK
- BLOWOUT_ROTATION_VARIANCE
- FAVORITE_CONTINUATION_NOT_AUTOMATIC_FADE

## Calibration Note
This checkpoint is intentionally distinguished from the prior Minnesota-Portland halftime state. Minnesota's 57-point half was helped by 54.5% three-point shooting and a 24-point lead, creating a clear continuation-fade setup. New York has 49 despite poor three-point shooting, with scoring supported by paint production, offensive rebounding, transition, and shot volume. Therefore the favorite-team-total continuation fade is not automatically activated here.

```yaml
game_id: WNBA_2026-08-13_LA_NY
checkpoint: halftime
score_at_checkpoint:
  LA: 32
  NY: 49
market_seen: false
estimated_first_half_possessions_per_team: 42
model:
  second_half:
    LA: 38
    NY: 45
    total: 83
    margin: NY_7
  final:
    LA: 70
    NY: 94
    total: 164
    margin: NY_24
fair_lines:
  spread: NY_-24
  total: 164
  ny_tt: 94
  la_tt: 70
volatility_tags:
  - NY_INTERIOR_VOLUME_DOMINANCE
  - OFFENSIVE_REBOUND_POSSESSION_EXTENSION
  - LOW_3P_SCORING_BASE_NOT_INFLATED
  - LA_TURNOVER_REGRESSION_UP
  - LA_SHOOTING_REGRESSION_UP
  - BRINK_FOUL_TROUBLE_FRONTCOURT_RISK
  - BLOWOUT_ROTATION_VARIANCE
  - FAVORITE_CONTINUATION_NOT_AUTOMATIC_FADE
status: MARKET_BLIND_PROJECTION_FROZEN
```
