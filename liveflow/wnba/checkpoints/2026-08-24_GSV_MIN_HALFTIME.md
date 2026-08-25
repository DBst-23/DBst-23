# WNBA LIVE-FLOW Checkpoint — Golden State Valkyries at Minnesota Lynx

## Market-Blind Freeze — Halftime
- Date: 2026-08-24
- Checkpoint: Halftime
- Score: Golden State 34, Minnesota 32
- Combined: 66
- Market viewed before projection: NO

## Halftime Read
Golden State: 34 points, 15/38 FG (39.5%), 4/16 3PT (25.0%), 0 FT attempts, 6 ORB, 15 REB, 13 AST, 6 turnovers.

Minnesota: 32 points, 11/31 FG (35.5%), 6/17 3PT (35.3%), 4/6 FT, 5 ORB, 20 REB, 9 AST, 11 turnovers.

Key structural notes:
- Both offenses are underperforming in raw scoring, but the causes are different.
- Golden State has generated solid shot volume (38 FGA) and only six turnovers. Its 39.5% FG and 25.0% 3PT conversion create positive shooting-regression pressure.
- Minnesota has only 31 FGA because 11 first-half turnovers have suppressed opportunity volume. The Lynx's strongest positive-regression signal is ball security rather than shooting alone.
- Minnesota is shooting 35.5% overall despite making 35.3% from three, meaning the two-point offense has been especially poor.
- Golden State has attempted zero free throws. Even modest second-half foul-line access would raise its scoring floor.
- Minnesota owns the rebounding advantage 20-15 and has five offensive rebounds, but the turnover disadvantage has erased much of that possession value.
- Minnesota has produced only 8 paint points; Golden State has 14. Neither side is consistently generating high-efficiency rim pressure.
- Golden State has already forced 11 Minnesota turnovers and converted them into 13 points. That is meaningful, but it is risky to project Minnesota to continue turning the ball over at the same rate.
- Minnesota has no transition scoring in the first half. A small transition normalization is possible if ball security improves and defensive rebounds become runouts.
- Kayla McBride is 1/7 and 1/6 from three; that is a meaningful individual positive-regression signal.
- Napheesa Collier is 3/6 for 6 points and is not carrying abnormal efficiency. She has room for greater usage in the second half.
- Olivia Miles has four turnovers in 14 minutes. Her decision-making is a major variable for Minnesota's second-half offensive ceiling.
- Golden State's Gabby Williams is 2/8 and Cecilia Zandalasini 2/7, giving the Valkyries multiple positive-regression candidates.
- Game state is tight: Golden State leads by two, with five lead changes and only a six-point maximum Valkyries lead. Competitive-game rotation risk is low.

## Regression Translation — Halftime
### Golden State
Positive pressure:
- 39.5% FG is below a neutral offensive baseline.
- 25.0% 3PT leaves clear upward shooting room.
- 38 FGA with only six turnovers indicates healthy opportunity generation.
- Zero first-half FT attempts creates potential second-half scoring upside if whistle/foul pressure normalizes.
- Gabby Williams and Cecilia Zandalasini are both below efficient conversion levels.

Negative / structural risk:
- Minnesota has controlled the defensive glass and leads overall rebounding 20-15.
- Golden State has only 14 paint points and has not generated free throws, so rim pressure is modest.
- Tiffany Hayes has three fouls, which slightly increases rotation uncertainty.

### Minnesota
Positive pressure:
- Eleven first-half turnovers are the strongest normalization signal in the game.
- Only 31 FGA means Minnesota can materially raise second-half shot volume without needing a pace spike.
- Kayla McBride's 1/7 shooting, including 1/6 from three, should not be projected linearly.
- Collier has room for greater offensive involvement.
- Minnesota's rebounding edge gives it a stable possession base if turnover rate falls.

Negative pressure:
- Minnesota's half-court scoring has been weak: only 8 paint points.
- Olivia Miles has four turnovers and Minnesota's guard creation has been unstable.
- The Lynx have not reached the line consistently enough to create a strong foul-rate scoring floor.

Net: Both teams have upward scoring pressure, but Minnesota's is more opportunity-driven while Golden State's is more conversion-driven. The first-half total of 66 looks too low to extrapolate directly. Expect a materially higher-scoring second half, with Minnesota slightly favored to win the remaining 20 minutes if its turnover rate normalizes.

## Frozen SharpEdge Projection — Halftime
### Second Half
- Minnesota: 40
- Golden State: 36
- 2H total: 76
- 2H margin: Minnesota -4

### Full Game
- Minnesota: 72
- Golden State: 70
- Full-game total: 142
- Full-game margin: Minnesota -2

## SharpEdge Fair Lines — Halftime
- Spread: Minnesota -2
- Total: 142
- Minnesota team total: 72
- Golden State team total: 70

## Central Ranges — Halftime
- Minnesota final: 68-77
- Golden State final: 66-74
- Full-game total: 136-149
- Final margin: Minnesota by 7 to Golden State by 4

## Initial Classification — Before Market Reveal
- Spread: Minnesota -2 is the fair center. Minnesota becomes attractive only if the live market is around pick'em or plus money / +1.5 or better; Golden State value would require a materially stronger number than roughly +4.5.
- Total: 142 is fair. A live total at 146.5 or higher creates Under pressure; 138.5 or lower creates Over pressure.
- Minnesota TT: fair 72. Over becomes interesting if the book remains 68.5-69.5 or lower because turnover normalization can increase second-half attempts materially.
- Golden State TT: fair 70. Over becomes interesting at 67.5-68.5 or lower because first-half 25% 3PT and zero FT attempts create upside; Under pressure begins above roughly 72.5.

## Volatility / State Tags
- BOTH_TEAMS_SCORING_REGRESSION_UP
- GSV_3P_REGRESSION_UP
- GSV_ZERO_FTA_FIRST_HALF
- GSV_SHOT_VOLUME_HEALTHY
- GABBY_WILLIAMS_REGRESSION_UP
- ZANDALASINI_REGRESSION_UP
- MIN_TURNOVER_REGRESSION_UP_STRONG
- MIN_SHOT_VOLUME_SUPPRESSED
- MCBRIDE_SHOOTING_REGRESSION_UP_STRONG
- COLLIER_USAGE_UPSIDE
- MILES_TURNOVER_RISK
- MIN_REBOUND_EDGE
- COMPETITIVE_GAME_STATE
- MARKET_BLIND_PROJECTION_FROZEN_HALFTIME

```yaml
game_id: WNBA_2026-08-24_GSV_MIN
checkpoint: halftime
score_at_checkpoint:
  GSV: 34
  MIN: 32
market_seen_before_projection: false
model:
  second_half:
    MIN: 40
    GSV: 36
    total: 76
    margin: MIN_4
  final:
    MIN: 72
    GSV: 70
    total: 142
    margin: MIN_2
fair_lines:
  spread: MIN_-2
  total: 142
  min_tt: 72
  gsv_tt: 70
central_ranges:
  MIN: 68-77
  GSV: 66-74
  total: 136-149
  margin: MIN_by_7_to_GSV_by_4
status: HALFTIME_MARKET_BLIND_PROJECTION_FROZEN_AWAITING_MARKET
```
