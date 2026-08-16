# WNBA LIVE-FLOW Checkpoint — Minnesota Lynx at Las Vegas Aces

## Market-Blind Freeze
- Date: 2026-08-15
- Checkpoint: Halftime
- Score: Minnesota 48, Las Vegas 48
- Market viewed before projection: NO

## Halftime Read
Minnesota: 48 points, 20/36 FG (55.6%), 6/12 3PT (50.0%), 2/3 FT, 4 ORB, 17 REB, 8 AST, 8 turnovers.

Las Vegas: 48 points, 20/38 FG (52.6%), 5/13 3PT (38.5%), 3/5 FT, 5 ORB, 13 REB, 15 AST, 3 turnovers.

Key structural notes:
- Minnesota's first-half efficiency was elevated: 55.6% from the field and 50.0% from three.
- Las Vegas matched the score despite lower three-point efficiency and only three turnovers.
- Las Vegas created 15 assists against Minnesota's 8, indicating cleaner half-court creation and ball movement.
- A'ja Wilson was the strongest sustainable Las Vegas offensive driver with 19 points on 9/12 FG.
- Jackie Young added 8 points and 6 assists, while Chelsea Gray had 7 assists and zero turnovers.
- Minnesota committed 8 turnovers, including 5 by Olivia Miles, creating meaningful possession leakage.
- Minnesota's 12 second-chance points helped support the 48-point half; that contribution is less certain to repeat at the same rate.
- The game was tied with 10 total ties and 7 lead changes, so full competitive rotations remained secure.

## Frozen SharpEdge Projection
### Second Half
- Minnesota: 43
- Las Vegas: 45
- 2H total: 88
- 2H margin: Las Vegas +2

### Full Game
- Minnesota: 91
- Las Vegas: 93
- Full-game total: 184
- Full-game margin: Las Vegas +2

## SharpEdge Fair Lines
- Spread: Las Vegas -2
- Total: 184
- Minnesota team total: 91
- Las Vegas team total: 93

## Initial Classification
- Spread: Las Vegas -2 fair. Any plus-money/plus-point live Aces spread creates a model-side cushion.
- Total: roughly fair around 184; no automatic totals strike from the halftime scoring alone.
- Minnesota team total: mild UNDER pressure from first-half shooting efficiency and turnover leakage.
- Las Vegas team total: modest OVER pressure if market remains below the low 90s, supported by assist quality and turnover control.

## Market Reveal
William Hill halftime/live market after the model freeze:
- Minnesota -2.5 (-105)
- Las Vegas +2.5 (-125) initially shown
- Full-game total 184.5 (-115 both sides)
- Minnesota TT 92.5: Over -125 / Under -105
- Las Vegas TT 91.5: Over -120 / Under -110

The actionable spread later moved to Las Vegas +1.5 (-115).

## Strike Decision
### BET LOCKED
- Market: Live full-game spread
- Selection: Las Vegas Aces +1.5
- Odds: -115
- Stake: $10.00
- To win: $8.70
- Total payout: $18.70
- Sportsbook: William Hill Nevada
- Ticket time: 2026-08-15 5:55 PM PT
- Score at entry: 48-48 halftime

### Edge at Entry
- SharpEdge fair spread: Las Vegas -2
- Bet line: Las Vegas +1.5
- Model-to-market gap: 3.5 points toward Las Vegas
- Classification: PLAYABLE EDGE

## Why the Strike Qualified
1. The model projected Las Vegas to win the second half by approximately two points before seeing the market.
2. The sportsbook was still giving Las Vegas +1.5 despite a tied halftime score.
3. Minnesota's 55.6% FG and 50.0% 3PT shooting carried meaningful cooling risk.
4. Las Vegas had superior ball security: 3 turnovers versus Minnesota's 8.
5. Las Vegas had a major assist edge, 15-8, supporting the quality of its offensive process.
6. Competitive game state reduced blowout/rotation uncertainty.

## Risk Flags
- SharpEdge's spread/allocation layer remains less validated than the combined-total layer.
- Minnesota's offensive rebounding and second-chance production could offset shooting regression.
- A one-possession spread outcome remains inherently high variance.

## Volatility / State Tags
- MIN_HOT_FG_REGRESSION_DOWN
- MIN_HOT_3P_REGRESSION_DOWN
- MIN_TURNOVER_LEAKAGE
- MIN_SECOND_CHANCE_DEPENDENCE
- LVA_BALL_SECURITY_EDGE
- LVA_ASSIST_CREATION_EDGE
- AJA_WILSON_SUSTAINABLE_USAGE
- COMPETITIVE_ROTATION_SECURITY
- SPREAD_LAYER_EDGE
- MARKET_BLIND_PROJECTION_FROZEN

```yaml
game_id: WNBA_2026-08-15_MIN_LVA
checkpoint: halftime
score_at_checkpoint:
  MIN: 48
  LVA: 48
market_seen_before_projection: false
model:
  second_half:
    MIN: 43
    LVA: 45
    total: 88
    margin: LVA_2
  final:
    MIN: 91
    LVA: 93
    total: 184
    margin: LVA_2
fair_lines:
  spread: LVA_-2
  total: 184
  min_tt: 91
  lva_tt: 93
market_reveal:
  initial_spread:
    MIN: -2.5_-105
    LVA: +2.5_-125
  total: 184.5
  min_tt: 92.5
  lva_tt: 91.5
bet:
  selection: LVA_+1.5
  odds: -115
  stake: 10.00
  to_win: 8.70
  payout: 18.70
  sportsbook: William_Hill_Nevada
  ticket_time_local: 2026-08-15T17:55:00-07:00
  model_market_gap_points: 3.5
  classification: PLAYABLE_EDGE
status: BET_LOCKED_AWAITING_RESULT
```
