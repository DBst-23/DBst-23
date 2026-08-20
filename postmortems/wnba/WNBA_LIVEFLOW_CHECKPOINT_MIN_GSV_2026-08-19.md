# WNBA LIVE-FLOW Checkpoint — Minnesota Lynx at Golden State Valkyries

## Market-Blind Freeze — Halftime
- Date: 2026-08-19
- Checkpoint: Halftime
- Score: Minnesota 41, Golden State 26
- Market viewed before projection: NO

## Halftime Read
Minnesota: 41 points, 15/28 FG (53.6%), 4/10 3PT (40.0%), 7/8 FT (87.5%), 4 ORB, 22 REB, 11 AST, 9 turnovers.

Golden State: 26 points, 9/37 FG (24.3%), 2/14 3PT (14.3%), 6/6 FT (100%), 5 ORB, 15 REB, 6 AST, 4 turnovers.

Key structural notes:
- Golden State has generated substantially more shot volume (37 FGA to 28) because Minnesota has committed nine turnovers, yet the Valkyries have converted only 24.3% from the field and 14.3% from three.
- Golden State's first-half shooting is the dominant regression signal. The offense has been poor, but a 24.3% FG / 14.3% 3PT continuation is too extreme to treat as a stable second-half baseline.
- The Valkyries also own a slight offensive-rebounding edge (5-4) and only four turnovers, so their possession process is healthier than the 26-point output suggests.
- Minnesota's 53.6% FG, 40.0% 3PT and 87.5% FT profile carries some negative efficiency-regression pressure.
- Minnesota's counterweight is ball security: nine first-half turnovers suppressed its shot volume. Even modest turnover normalization can preserve scoring despite shooting regression.
- Napheesa Collier has 12 points on 4/7 FG with seven rebounds; her production is efficient but not abnormally hot.
- Olivia Miles has 9 points and five assists on 3/5 FG and 2/4 from three, giving Minnesota another sustainable creation source.
- Golden State's primary scorers are broadly cold: Gabby Williams 1/8, Kayla Thornton 2/7, Cecilia Zandalasini 1/7. This creates a strong team-level positive-regression case, although Minnesota's defense remains a real ceiling suppressor.
- Minnesota has controlled the glass 22-15 overall and leads paint scoring 18-12.
- Game state is one-sided: Minnesota has led by as many as 18 and Golden State has never led. Blowout/rotation risk is therefore elevated and reduces confidence in aggressive side or team-total projections.

## Regression Translation — Halftime
### Golden State
Positive pressure:
- 24.3% FG is extremely depressed.
- 14.3% 3PT is extremely depressed.
- 37 field-goal attempts show that shot-generation volume has not collapsed.
- Only four turnovers support continued opportunity volume.
- Multiple core shooters are simultaneously below normal conversion ranges.

Negative / structural risk:
- Minnesota has a strong defensive environment and a 22-15 rebounding advantage.
- Golden State is only 6/17 in the paint, so the inefficiency is not purely a three-point variance story.
- A 15-point deficit introduces rotation and late-game game-state uncertainty.

### Minnesota
Positive pressure:
- Nine turnovers create clear room for second-half ball-security improvement and additional shot volume.
- Collier/Miles production is not dependent on unsustainably extreme individual shooting.

Negative pressure:
- 53.6% FG, 40.0% 3PT and 87.5% FT are collectively above a neutral continuation baseline.
- Minnesota has only 28 FGA despite scoring 41, so first-half scoring efficiency has been doing substantial work.

Net: Golden State owns the stronger pure shooting-regression case, while Minnesota owns the stronger turnover-regression case. Those forces partially offset. Expect Golden State to score materially better than 26 in the second half, but Minnesota's defense and likely turnover normalization prevent a full pace-adjusted offensive explosion.

## Frozen SharpEdge Projection — Halftime
### Second Half
- Minnesota: 38
- Golden State: 35
- 2H total: 73
- 2H margin: Minnesota -3

### Full Game
- Minnesota: 79
- Golden State: 61
- Full-game total: 140
- Full-game margin: Minnesota -18

## SharpEdge Fair Lines — Halftime
- Spread: Minnesota -18
- Total: 140
- Minnesota team total: 79
- Golden State team total: 61

## Central Ranges — Halftime
- Minnesota final: 75-83
- Golden State final: 57-66
- Full-game total: 134-147
- Final margin: Minnesota by 11-24

## Initial Classification — Before Market Reveal
- Spread: Minnesota -18 is the fair center. Golden State becomes interesting only if the market materially stretches beyond roughly +20.5 to +21 because its shooting-regression profile is real; Minnesota value would require a number meaningfully shorter than roughly -15.5.
- Total: 140 is fair. A live total above roughly 144 creates Under pressure; below roughly 136 creates Over pressure.
- Minnesota TT: fair 79. Do not chase an Over unless the book is materially below 77 because shooting regression down offsets turnover regression up.
- Golden State TT: fair 61. The strongest derivative case is Golden State Over only if the market remains suppressed near 57.5-58.5; the 24.3% FG and 14.3% 3PT rates are too low to project straight forward.

## Volatility / State Tags
- GSV_FG_REGRESSION_UP_STRONG
- GSV_3P_REGRESSION_UP_STRONG
- GSV_SHOT_VOLUME_HEALTHY
- GSV_LOW_TURNOVER_PROCESS
- GABBY_WILLIAMS_SHOOTING_REGRESSION_UP
- KAYLA_THORNTON_SHOOTING_REGRESSION_UP
- ZANDALASINI_SHOOTING_REGRESSION_UP
- MIN_FG_REGRESSION_DOWN
- MIN_3P_REGRESSION_DOWN
- MIN_TURNOVER_REGRESSION_UP
- MIN_REBOUND_EDGE
- MIN_DEFENSIVE_CEILING_PRESSURE
- BLOWOUT_ROTATION_RISK
- MARKET_BLIND_PROJECTION_FROZEN_HALFTIME

```yaml
game_id: WNBA_2026-08-19_MIN_GSV
checkpoint: halftime
score_at_checkpoint:
  MIN: 41
  GSV: 26
market_seen_before_projection: false
model:
  second_half:
    MIN: 38
    GSV: 35
    total: 73
    margin: MIN_3
  final:
    MIN: 79
    GSV: 61
    total: 140
    margin: MIN_18
fair_lines:
  spread: MIN_-18
  total: 140
  min_tt: 79
  gsv_tt: 61
central_ranges:
  MIN: 75-83
  GSV: 57-66
  total: 134-147
  margin: MIN_by_11_to_24
status: HALFTIME_MARKET_BLIND_PROJECTION_FROZEN_AWAITING_MARKET
```
