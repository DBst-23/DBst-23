# WNBA LIVE-FLOW Checkpoint — Washington Mystics at Las Vegas Aces

## Market-Blind Freeze
- Date: 2026-08-13
- Checkpoint: Halftime
- Score: Las Vegas 38, Washington 32
- Market viewed before projection: NO

## Halftime Read
Washington: 32 points, 14/31 FG (45.2%), 3/8 3PT (37.5%), 1/5 FT, 4 ORB, 20 REB, 5 AST, 11 turnovers.

Las Vegas: 38 points, 12/31 FG (38.7%), 4/15 3PT (26.7%), 10/11 FT, 1 ORB, 14 REB, 9 AST, 6 turnovers.

Estimated first-half possession environment: roughly 40-41 possessions per team. The 70-point halftime total is genuinely suppressed, but the suppression is not entirely pace-driven; Las Vegas shot poorly from the field while Washington lost 11 possessions to turnovers and shot only 1/5 at the line.

Key structural notes:
- Las Vegas has a strong positive-regression setup: A'ja Wilson is 1/5, Chelsea Gray 1/5, and Jewell Loyd 0/4, while the team is only 38.7% FG and 26.7% from three.
- Jackie Young is carrying the offense with 18 points on 6/9 FG, 3/6 from three and 3/3 FT. Her first-half scoring is hot, so the Las Vegas projection should not simply double her production.
- Washington's 11 turnovers are the largest drag on its offense. Some turnover regression is reasonable, and 1/5 FT is also unlikely to persist.
- Washington has generated 22 paint points on 11/20 paint attempts and owns a 20-14 rebounding edge, so its offense is not purely fluky despite only 32 points.
- Las Vegas has only one offensive rebound and zero fast-break points, leaving room for additional possession and transition production if execution improves.
- Chelsea Gray has 3 fouls in 12:39 and NaLyssa Smith has 3 fouls in 12:53. Rotation/foul-management risk is material but not yet severe enough to override the positive-regression case.
- The game is only six points apart, so unlike recent blowout halftime states, full competitive rotations should remain active unless the third quarter separates quickly.

## Frozen SharpEdge Projection
### Second Half
- Washington: 38
- Las Vegas: 44
- 2H total: 82
- 2H margin: Las Vegas +6

### Full Game
- Washington: 70
- Las Vegas: 82
- Full-game total: 152
- Full-game margin: Las Vegas +12

## SharpEdge Fair Lines
- Spread: Las Vegas -12
- Total: 152
- Las Vegas team total: 82
- Washington team total: 70

## Projection Logic
### Las Vegas
The first-half 38 is below the quality of opportunities implied by the personnel distribution. Wilson, Gray and Loyd combined to shoot 2/14 from the field while Young carried the scoring load. The model expects some redistribution and positive shooting regression in the second half. A close score also keeps primary rotation minutes live. The main brake is Gray's foul situation plus weak first-half offensive rebounding.

### Washington
Washington's 32-point half is suppressed primarily by 11 turnovers and 1/5 free-throw shooting rather than disastrous field-goal efficiency. The Mystics have been productive in the paint and on the glass, so a modest second-half scoring lift is warranted. However, the 11 turnovers and only five assists indicate real ball-security/creation issues, so the projection does not fully normalize them to an average offensive half.

## Initial Classification
- Las Vegas side: lean Las Vegas only if the live spread is materially shorter than -12.
- Full-game total: compare market to 152 after reveal; do not auto-under solely because the first half produced 70 points.
- Las Vegas team total: directional interest is OVER if the market is materially below 82 because of star shooting regression and competitive-minute security.
- Washington team total: fair around 70; only attack if the market creates a meaningful cushion away from that number.

## Volatility / State Tags
- LV_STAR_SHOOTING_REGRESSION_UP
- JACKIE_YOUNG_FIRST_HALF_SCORING_CONCENTRATION
- WAS_TURNOVER_REGRESSION_UP
- WAS_FT_REGRESSION_UP
- WAS_PAINT_PRODUCTION_STABLE
- LV_LOW_ORB_EXTENSION
- CLOSE_GAME_ROTATION_SECURITY
- GRAY_FOUL_TROUBLE
- SMITH_FOUL_TROUBLE
- FIRST_HALF_TOTAL_SUPPRESSED_NOT_PURE_PACE

```yaml
game_id: WNBA_2026-08-13_WAS_LVA
checkpoint: halftime
score_at_checkpoint:
  WAS: 32
  LVA: 38
market_seen: false
estimated_first_half_possessions_per_team: 40.5
model:
  second_half:
    WAS: 38
    LVA: 44
    total: 82
    margin: LVA_6
  final:
    WAS: 70
    LVA: 82
    total: 152
    margin: LVA_12
fair_lines:
  spread: LVA_-12
  total: 152
  lva_tt: 82
  was_tt: 70
volatility_tags:
  - LV_STAR_SHOOTING_REGRESSION_UP
  - JACKIE_YOUNG_FIRST_HALF_SCORING_CONCENTRATION
  - WAS_TURNOVER_REGRESSION_UP
  - WAS_FT_REGRESSION_UP
  - WAS_PAINT_PRODUCTION_STABLE
  - LV_LOW_ORB_EXTENSION
  - CLOSE_GAME_ROTATION_SECURITY
  - GRAY_FOUL_TROUBLE
  - SMITH_FOUL_TROUBLE
  - FIRST_HALF_TOTAL_SUPPRESSED_NOT_PURE_PACE
status: MARKET_BLIND_PROJECTION_FROZEN
```
