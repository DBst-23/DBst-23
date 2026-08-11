# WNBA LIVE-FLOW Checkpoint — Chicago Sky at Seattle Storm

## Market-Blind Freeze
- Date: 2026-08-10
- Checkpoint: Halftime
- Score: Seattle 47, Chicago 33
- Market viewed before projection: NO

## Halftime Read
Chicago: 33 points, 11/33 FG (33.3%), 2/7 3PT (28.6%), 9/12 FT, 6 ORB, 19 REB, 7 AST, 9 TO.

Seattle: 47 points, 15/38 FG (39.5%), 4/13 3PT (30.8%), 13/15 FT, 7 ORB, 22 REB, 11 AST, 7 TO, 7 STL, 3 BLK.

Key structural notes:
- Seattle leads by 14 despite shooting only 39.5% from the field and 30.8% from three, so the lead is not primarily built on unsustainable perimeter shooting.
- Chicago's offense has been damaged by 9 turnovers and poor half-court efficiency.
- Seattle has created 7 steals and 3 blocks, indicating genuine defensive disruption rather than simple Chicago shooting variance.
- Chicago frontcourt foul pressure is material: Kamilla Cardoso has 3 fouls and Azura Stevens has 3 fouls at halftime.
- Seattle has already generated 15 free-throw attempts; continued rim pressure can keep Chicago's frontcourt constrained.
- Chicago has some positive-regression room from 33.3% FG, so the second-half projection allows a scoring rebound rather than extending the first-half efficiency mechanically.

## Frozen SharpEdge Projection
### Second Half
- Seattle: 44
- Chicago: 40
- 2H total: 84
- 2H margin: Seattle +4

### Full Game
- Seattle: 91
- Chicago: 73
- Full-game total: 164
- Full-game margin: Seattle +18

## SharpEdge Fair Lines
- Spread: Seattle -18
- Total: 164
- Seattle team total: 91
- Chicago team total: 73

## Initial Classification
- Seattle side: LEAN, pending market comparison
- Full-game total: NEUTRAL until market comparison
- Seattle team total: LEAN OVER only if market materially below 91
- Chicago team total: LEAN UNDER only if market materially above 73

## Calibration Notes
This projection does not apply automatic late-game scoring compression merely because Seattle owns a double-digit lead. The model preserves a normal-to-moderate 84-point second half because Chicago has shooting-regression room and can increase urgency, while Seattle's first-half scoring was achieved without extreme field-goal or three-point shooting.

```yaml
game_id: WNBA_2026-08-10_CHI_SEA
checkpoint: halftime
score_at_checkpoint:
  CHI: 33
  SEA: 47
market_seen: false
model:
  second_half:
    CHI: 40
    SEA: 44
    total: 84
    margin: SEA_4
  final:
    CHI: 73
    SEA: 91
    total: 164
    margin: SEA_18
fair_lines:
  spread: SEA_-18
  total: 164
  sea_tt: 91
  chi_tt: 73
status: FROZEN_AWAITING_MARKET
```
