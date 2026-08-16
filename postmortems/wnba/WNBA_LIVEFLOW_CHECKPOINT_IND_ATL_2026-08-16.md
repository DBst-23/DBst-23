# WNBA LIVE-FLOW Checkpoint — Indiana Fever at Atlanta Dream

## Market-Blind Freeze — Halftime
- Date: 2026-08-16
- Checkpoint: Halftime
- Score: Atlanta 44, Indiana 40
- Market viewed before projection: NO

## Halftime Read
Indiana: 40 points, 17/39 FG (43.6%), 3/13 3PT (23.1%), 3/8 FT (37.5%), 5 ORB, 20 REB, 10 AST, 5 turnovers.

Atlanta: 44 points, 14/39 FG (35.9%), 4/15 3PT (26.7%), 12/13 FT (92.3%), 5 ORB, 24 REB, 11 AST, 5 turnovers.

Key structural notes:
- Possession volume is nearly identical: both teams attempted 39 field goals and committed five turnovers.
- Indiana has generated the cleaner interior scoring profile, leading points in the paint 26-18.
- Indiana's perimeter shooting is depressed at 23.1% from three and free-throw conversion is extremely depressed at 37.5%, creating positive scoring-regression pressure.
- Kelsey Mitchell is 2/10 from the field and is a major individual positive-regression candidate if shot quality remains intact.
- Caitlin Clark has 10 points and five assists but four turnovers, so Indiana's second-half upside depends partly on ball-security stabilization.
- Makayla Timpson (12 points on 5/6 FG) and Aliyah Boston (8 points on 4/7 FG) have supported Indiana's interior efficiency.
- Atlanta's 35.9% overall FG rate is also depressed, but 12/13 FT shooting has materially supported the 44-point half and is unlikely to repeat at the same conversion rate.
- Allisha Gray has 17 points on 6/10 FG and 3/3 FT and is Atlanta's strongest sustainable scoring driver so far.
- Angel Reese is 3/10 from the field with three fouls; her foul state introduces rotation and interior-possession uncertainty.
- Atlanta owns a 24-20 rebounding edge and a 12-2 fast-break scoring edge, both meaningful support for its four-point halftime lead.
- Competitive state remains high: seven lead changes and eight ties.

## Regression Translation — Halftime
### Indiana
Positive pressure:
- 23.1% team 3PT is below a neutral continuation baseline.
- 37.5% FT is unsustainably low.
- Mitchell's 2/10 shooting is a clear positive-regression candidate.
- Interior scoring process has been strong: 26 paint points.

Negative / structural risk:
- Clark has four turnovers.
- Atlanta has controlled transition scoring 12-2.
- Indiana is -4 on the glass.

### Atlanta
Positive pressure:
- 35.9% FG and 26.7% 3PT leave room for shooting improvement.
- Rebounding and transition creation have been favorable.

Negative pressure:
- 12/13 FT conversion is unlikely to persist.
- Reese has three fouls and is 3/10 FG.
- Much of the first-half scoring burden has concentrated in Allisha Gray.

Net: both teams have positive field-goal regression paths, but Indiana has the stronger pure efficiency-regression case because both its three-point and free-throw rates are depressed while its paint offense is already functioning. Atlanta's rebounding/transition edge keeps the home side narrowly favored from the current state.

## Frozen SharpEdge Projection — Halftime
### Second Half
- Indiana: 42
- Atlanta: 42
- 2H total: 84
- 2H margin: Pick'em

### Full Game
- Indiana: 82
- Atlanta: 86
- Full-game total: 168
- Full-game margin: Atlanta +4

## SharpEdge Fair Lines — Halftime
- Spread: Atlanta -4
- Total: 168
- Indiana team total: 82
- Atlanta team total: 86

## Central Ranges — Halftime
- Indiana final: 78-86
- Atlanta final: 82-90
- Full-game total: 161-175
- Final margin: Atlanta by 0 to 8

## Initial Classification — Before Market Reveal
- Spread: Atlanta -4 is the fair center. Meaningful Indiana value would require a live number materially above +4; Atlanta value would require a number shorter than roughly -2.5 to -3.
- Total: 168 is fair. A live total materially above 171 would create Under pressure; materially below 165 would create Over pressure.
- Indiana TT: fair 82. The preferred derivative becomes Indiana Over only if the book remains below roughly 80.5-81, because the 3PT/FT/Mitchell regression profile is favorable.
- Atlanta TT: fair 86. No automatic Over despite low FG%, because the first-half 12/13 FT rate is carrying negative regression and Reese's foul state adds uncertainty.

## Volatility / State Tags
- IND_3P_REGRESSION_UP
- IND_FT_REGRESSION_UP
- KELSEY_MITCHELL_SHOOTING_REGRESSION_UP
- CAITLIN_CLARK_TURNOVER_RISK
- IND_PAINT_PROCESS_STRONG
- ATL_FG_REGRESSION_UP
- ATL_FT_REGRESSION_DOWN
- ATL_TRANSITION_EDGE
- ATL_REBOUND_EDGE
- ALLISHA_GRAY_SUSTAINABLE_USAGE
- ANGEL_REESE_FOUL_RISK_3
- COMPETITIVE_ROTATIONS_SECURE
- MARKET_BLIND_PROJECTION_FROZEN_HALFTIME

```yaml
game_id: WNBA_2026-08-16_IND_ATL
checkpoint: halftime
score_at_checkpoint:
  IND: 40
  ATL: 44
market_seen_before_projection: false
model:
  second_half:
    IND: 42
    ATL: 42
    total: 84
    margin: PK
  final:
    IND: 82
    ATL: 86
    total: 168
    margin: ATL_4
fair_lines:
  spread: ATL_-4
  total: 168
  ind_tt: 82
  atl_tt: 86
central_ranges:
  IND: 78-86
  ATL: 82-90
  total: 161-175
  margin: ATL_by_0_to_8
status: HALFTIME_MARKET_BLIND_PROJECTION_FROZEN_AWAITING_MARKET
```
