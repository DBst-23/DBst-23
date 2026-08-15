# WNBA LIVE-FLOW Checkpoint — New York Liberty at Connecticut Sun

## Market-Blind Freeze
- Date: 2026-08-15
- Checkpoint: Halftime
- Score: New York 46, Connecticut 37
- Market viewed before projection: NO

## Halftime Read
New York: 46 points, 17/38 FG (44.7%), 7/13 3PT (53.8%), 5/5 FT, 2 ORB, 16 REB, 10 AST, 5 turnovers.

Connecticut: 37 points, 13/36 FG (36.1%), 2/14 3PT (14.3%), 9/10 FT, 4 ORB, 20 REB, 7 AST, 8 turnovers.

Estimated first-half possession environment: roughly 39-40 possessions per team. The 83-point halftime total is not especially suppressed on pace, but the scoring split is highly distorted by opposite perimeter variance: New York is 53.8% from three while Connecticut is 14.3%.

Key structural notes:
- New York's 7/13 three-point shooting is the largest obvious negative-regression candidate in the game. A repeat of 53.8% from three is not a neutral baseline.
- Connecticut's 2/14 three-point shooting is the strongest positive-regression candidate. The Sun are not generating a dead offense overall: they have 20 paint points on 10/17 paint attempts, 9/10 FT, and a 20-16 rebounding edge.
- Connecticut's second quarter collapse to 10 points came with 3/17 FG and 0/10 from three. That quarter was extreme enough that the model should not anchor too heavily to the 37-point halftime output.
- New York's second quarter surge to 27 points came with 9/18 FG, 5/8 from three, zero turnovers and 9 assists. The no-turnover ball security is strong, but the 62.5% three-point rate is unlikely to carry unchanged.
- Jonquel Jones is the strongest sustainable New York offensive driver: 19 points on 7/11 FG, 3/5 from three, 6 rebounds and 2 assists. Her interior/scoring role is real, but her own three-point shooting is also running hot.
- Breanna Stewart is only 1/8 from the field with 4 points. New York has an internal positive-regression source even if team-level three-point shooting cools.
- Connecticut has multiple player-level shooting regression candidates: Diamond Miller 1/7, Kennedy Burke 1/5, and the team 2/14 from three. Olivia Nelson-Ododa is already converting efficiently inside with 13 points on 4/5 FG and 5/5 FT.
- Connecticut has 8 turnovers versus New York's 5. That is a real possession drag, but it is not severe enough by itself to justify treating the Sun's 10-point second quarter as a stable scoring regime.
- The nine-point margin keeps normal competitive rotations live. There is no blowout-state reason to suppress Connecticut's second-half scoring distribution.

## Regression Translation
### New York
Negative adjustments:
- Team 3PT: 53.8% on 13 attempts -> meaningful cooling risk.
- Q2 62.5% from three -> unsustainable continuation risk.

Positive offsets:
- Stewart 1/8 FG -> strong individual positive-regression candidate.
- Only 5 turnovers -> possession quality is stable.
- Jonquel Jones is creating sustainable interior/inside-out offense.

Net effect: New York should remain productive, but not at a 27-point-per-quarter continuation baseline.

### Connecticut
Positive adjustments:
- Team 3PT: 14.3% on 14 attempts -> major positive-regression candidate.
- Q2: 0/10 from three -> extreme low-tail quarter.
- Miller/Burke individual shooting suppression.
- Paint scoring, free throws and rebounding remain structurally healthy.

Negative offsets:
- 8 turnovers create some possession loss.
- Perimeter creation has not been clean enough to assume full normalization.

Net effect: Connecticut's second-half scoring expectation should rise materially above the first-half 37-point baseline.

## Frozen SharpEdge Projection
### Second Half
- New York: 40
- Connecticut: 42
- 2H total: 82
- 2H margin: Connecticut +2

### Full Game
- New York: 86
- Connecticut: 79
- Full-game total: 165
- Full-game margin: New York +7

## SharpEdge Fair Lines
- Spread: New York -7
- Total: 165
- New York team total: 86
- Connecticut team total: 79

## Distribution / Tail View
- New York central range: 82-90
- Connecticut central range: 74-84
- Full-game total central range: 158-172

Tail notes:
- New York upper tail remains live because Stewart is due for some field-goal regression upward even if team three-point shooting cools.
- Connecticut upper tail must be widened because 2/14 from three plus 3/17 FG in Q2 represents a strong positive-regression setup, especially with paint/FT production already present.
- Connecticut team-total Unders require extra caution under LIVEFLOW_REGRESSION_TRANSLATION_GATE_v1.

## Initial Classification
- Full-game total: FAIR around 165. Do not auto-under from New York's hot three-point shooting because Connecticut owns equally strong positive-regression pressure.
- New York team total: slight UNDER lean only if market is materially above 86; Stewart's 1/8 first half creates upside that offsets team-level 3PT cooling.
- Connecticut team total: directional OVER interest if market is materially below 79 because the first-half scoring suppression is driven by extreme perimeter failure rather than dead paint/FT opportunity.
- Spread: New York fair around -7; do not chase a large live favorite number if the market prices the second-quarter 27-10 run as permanent.

## Volatility / State Tags
- NYL_HOT_3P_REGRESSION_DOWN
- CON_EXTREME_3P_REGRESSION_UP
- CON_Q2_LOW_TAIL_MIRAGE
- NYL_STEWART_SHOOTING_REGRESSION_UP
- JONQUEL_JONES_SUSTAINABLE_USAGE
- CON_PAINT_FT_STRUCTURE_STABLE
- CON_TURNOVER_DRAG
- COMPETITIVE_ROTATION_SECURITY
- REGRESSION_TRANSLATION_ACTIVE
- SECOND_QUARTER_REGIME_REVERSAL_RISK

```yaml
game_id: WNBA_2026-08-15_NYL_CON
checkpoint: halftime
score_at_checkpoint:
  NYL: 46
  CON: 37
market_seen: false
estimated_first_half_possessions_per_team: 39.5
model:
  second_half:
    NYL: 40
    CON: 42
    total: 82
    margin: CON_2
  final:
    NYL: 86
    CON: 79
    total: 165
    margin: NYL_7
fair_lines:
  spread: NYL_-7
  total: 165
  nyl_tt: 86
  con_tt: 79
central_ranges:
  NYL: 82-90
  CON: 74-84
  total: 158-172
volatility_tags:
  - NYL_HOT_3P_REGRESSION_DOWN
  - CON_EXTREME_3P_REGRESSION_UP
  - CON_Q2_LOW_TAIL_MIRAGE
  - NYL_STEWART_SHOOTING_REGRESSION_UP
  - JONQUEL_JONES_SUSTAINABLE_USAGE
  - CON_PAINT_FT_STRUCTURE_STABLE
  - CON_TURNOVER_DRAG
  - COMPETITIVE_ROTATION_SECURITY
  - REGRESSION_TRANSLATION_ACTIVE
  - SECOND_QUARTER_REGIME_REVERSAL_RISK
status: MARKET_BLIND_PROJECTION_FROZEN
```
