# WNBA LIVE-FLOW Checkpoint — Toronto Tempo at Washington Mystics

## Market-Blind Freeze — End of 3rd Quarter
- Date: 2026-08-19
- Checkpoint: End 3rd quarter
- Score: Washington 69, Toronto 56
- Combined score: 125
- Market viewed before projection: NO

## Through-3Q Read
Toronto: 56 points, 21/51 FG (41.2%), 9/22 3PT (40.9%), 5/8 FT (62.5%), 6 ORB, 20 REB, 13 AST, 7 turnovers.

Washington: 69 points, 21/46 FG (45.7%), 8/19 3PT (42.1%), 19/23 FT (82.6%), 11 ORB, 34 REB, 16 AST, 14 turnovers.

Key structural notes:
- Washington leads by 13 despite committing 14 turnovers because it owns a major rebounding advantage (34-20), a strong offensive-rebounding edge (11-6), and a 17-3 second-chance scoring advantage.
- Toronto's Q3 scoring rebound came with 50% three-point shooting and zero turnovers in the quarter, a cleaner offensive period than its disastrous 9-point second quarter.
- Washington scored 22 in Q3 despite shooting only 29.4% from the field and 20% from three, with free throws and second-chance creation supporting the quarter.
- Toronto scored 23 in Q3 on 45% FG and 50% 3PT, meaning its third-quarter recovery carried substantial perimeter support.
- Washington remains structurally advantaged on the glass and in paint/second-chance opportunity creation, while Toronto's late-game scoring path depends more heavily on perimeter conversion.
- Game state is no longer neutral: Washington has led by as many as 18 and enters Q4 up 13, creating possible clock-management and reduced-possession pressure if the Mystics protect the lead.

## Frozen SharpEdge Projection — End 3Q
### Fourth Quarter
- Projected Q4 combined range: 35-41
- Central Q4 expectation: ~38 points

### Full Game
- Frozen SharpEdge fair total: 162.5
- Frozen SharpEdge fair spread: Washington -14.0
- Central projected finish: ~163 total points

## Market Reveal
William Hill live market after projection freeze:
- Full-game total: 166.5
- Over 166.5: -122 at initial reveal
- Under 166.5: -110 at initial reveal
- Spread: Washington -14.5 / Toronto +14.5

SharpEdge comparison:
- Fair total 162.5 vs book 166.5 = 4.0-point edge toward UNDER.
- Fair spread Washington -14.0 vs book Washington -14.5 = essentially fair / no spread strike.

## Executed Strike
- Bet: UNDER 166.5
- Odds actually locked: -113
- Wager: $10.00
- To win: $8.85
- Total payout: $18.85
- Sportsbook: William Hill
- Ticket timestamp shown: 2026-08-19 06:03 PM NV
- Status: OPEN / AWAITING FINAL

## LIVE-FLOW Classification
- Primary edge: Full-game UNDER
- Edge size at strike: +4.0 points versus frozen fair total
- Break-even at -113: ~53.1%
- Model confidence at market reveal: approximately 62-65% Under 166.5
- Spread: PASS

## Volatility / State Tags
- TOR_Q3_3P_ELEVATED
- TOR_Q3_ZERO_TURNOVERS
- WAS_Q3_FG_REGRESSION_UP
- WAS_OFFENSIVE_REBOUND_EDGE
- WAS_SECOND_CHANCE_EDGE
- WAS_REBOUND_CONTROL
- LEAD_STATE_WAS_PLUS_13
- CLOCK_COMPRESSION_RISK
- END3Q_UNDER_EDGE
- MARKET_BLIND_PROJECTION_FROZEN_END3Q
- LIVEFLOW_STRIKE_LOCKED

```yaml
game_id: WNBA_2026-08-19_TOR_WAS
checkpoint: end_3q
score_at_checkpoint:
  TOR: 56
  WAS: 69
combined_score: 125
market_seen_before_projection: false
model:
  q4_total_range: 35-41
  q4_total_center: 38
  final_total: 162.5
  spread: WAS_-14.0
market_reveal:
  total: 166.5
  spread: WAS_-14.5
  over_price_initial: -122
  under_price_initial: -110
edge:
  side: UNDER
  points: 4.0
strike:
  market: UNDER_166.5
  odds: -113
  wager_usd: 10.00
  to_win_usd: 8.85
  payout_usd: 18.85
  sportsbook: William_Hill
status: LIVEFLOW_STRIKE_LOCKED_AWAITING_FINAL
```
