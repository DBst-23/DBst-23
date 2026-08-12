# WNBA LIVE-FLOW Checkpoint — Washington Mystics at Las Vegas Aces

## Market-Blind Freeze
- Date: 2026-08-11
- Checkpoint: Halftime
- Score: Washington 41, Las Vegas 41
- Market viewed before projection: NO

## Halftime Read
Washington: 41 points, 17/34 FG (50.0%), 3/6 3PT (50.0%), 4/4 FT, 5 ORB, 23 REB, 11 AST, 9 TO, 2 STL, 2 BLK.

Las Vegas: 41 points, 15/36 FG (41.7%), 6/13 3PT (46.2%), 5/6 FT, 4 ORB, 13 REB, 11 AST, 5 TO, 5 STL, 4 BLK.

Key structural notes:
- The score is tied despite Washington holding a large 23-13 rebounding advantage and a 26-12 points-in-the-paint advantage.
- Washington has been highly efficient from both the field (50%) and three (50%), but the three-point volume is low at only six attempts, so the first-half offense is not solely driven by perimeter variance.
- Las Vegas is shooting 46.2% from three on 13 attempts while only 41.7% overall; some perimeter regression is expected, but the Aces have room to improve inside the arc.
- Las Vegas has produced 5 steals and 4 blocks and has committed only 5 turnovers, giving the Aces a cleaner possession profile than Washington's 9 turnovers.
- Washington's interior production is real and has been driven by Iriafen/Austin plus offensive rebounding, so the model does not assume an abrupt collapse in Mystics scoring.
- The strongest second-half correction candidate is Las Vegas' two-point offense and defensive rebounding rather than additional three-point expansion.

## Frozen SharpEdge Projection
### Second Half
- Las Vegas: 44
- Washington: 40
- 2H total: 84
- 2H margin: Las Vegas +4

### Full Game
- Las Vegas: 85
- Washington: 81
- Full-game total: 166
- Full-game margin: Las Vegas +4

## SharpEdge Fair Lines
- Spread: Las Vegas -4
- Total: 166
- Las Vegas team total: 85
- Washington team total: 81

## Initial Classification
- Las Vegas side: LEAN, pending market comparison
- Full-game total: NEUTRAL until market comparison
- Las Vegas team total: LEAN OVER only if market materially below 85
- Washington team total: LEAN UNDER only if market materially above 81

## Calibration Notes
The tied halftime score masks two opposing first-half edges: Washington controlled the paint and glass, while Las Vegas won the turnover/disruption battle and generated more three-point volume. The second-half projection gives Las Vegas a modest home-side correction through improved interior efficiency and defensive rebounding, but it does not erase Washington's legitimate interior success.

```yaml
game_id: WNBA_2026-08-11_WAS_LVA
checkpoint: halftime
score_at_checkpoint:
  WAS: 41
  LVA: 41
market_seen: false
model:
  second_half:
    WAS: 40
    LVA: 44
    total: 84
    margin: LVA_4
  final:
    WAS: 81
    LVA: 85
    total: 166
    margin: LVA_4
fair_lines:
  spread: LVA_-4
  total: 166
  lva_tt: 85
  was_tt: 81
status: FROZEN_AWAITING_MARKET
```
