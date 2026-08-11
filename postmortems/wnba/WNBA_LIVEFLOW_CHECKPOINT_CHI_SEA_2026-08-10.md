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

## William Hill Halftime Market
- Spread: Chicago +9.5 (-115) / Seattle -9.5 (-115)
- Moneyline: Chicago +380 / Seattle -550
- Total: Over 171.5 (-115) / Under 171.5 (-115)
- Seattle team total: Over 90.5 (-125) / Under 90.5 (-105)
- Chicago team total: Over 81.5 (-105) / Under 81.5 (-125)

## Model vs Market
| Market | SharpEdge | William Hill | Separation | LIVE-FLOW Read |
|---|---:|---:|---:|---|
| Spread | SEA -18 | SEA -9.5 | 8.5 pts | Strong SEA value |
| Full total | 164 | 171.5 | 7.5 pts | Strong UNDER value |
| Seattle TT | 91 | 90.5 | 0.5 pt | PASS / market aligned |
| Chicago TT | 73 | 81.5 | 8.5 pts | Strong CHI UNDER value |

## Strike Hierarchy
### Primary strike candidate: Chicago Under 81.5 (-125)
Chicago has 33 at halftime and must score 49+ in the second half to beat 81.5. SharpEdge projects 40 second-half points. The 8.5-point model-market gap directly isolates the strongest first-half signal: Chicago's offensive inefficiency plus Seattle's defensive disruption, while already granting Chicago meaningful positive shooting regression.

### Secondary strike candidate: Seattle -9.5 (-115)
Seattle enters halftime +14 and can be outscored by four points in the second half and still cover -9.5. SharpEdge projects Seattle to win the second half by four and finish +18, creating an 8.5-point separation from market. This is a strong side read, but it is correlated with the Chicago team-total under thesis.

### Third: Full-game Under 171.5 (-115)
The first half produced 80 points. Under 171.5 permits as many as 91 second-half points, while SharpEdge projects 84. The 7.5-point cushion is substantial, but the full-game under carries more exposure to Seattle offensive acceleration and late-game foul/pace variance than the isolated Chicago TT under.

### Pass: Seattle TT 90.5
SharpEdge projects Seattle 91, only 0.5 above the market. No meaningful edge exists.

## LIVE-FLOW Decision Logic
Do not stack all three correlated positions. The cleanest single expression of the model discrepancy is Chicago TT Under 81.5. Seattle -9.5 is the next-best expression if prioritizing side over total. Full-game Under 171.5 is valid model value but ranks below the isolated Chicago under because a hot Seattle half could threaten the game total without invalidating the core Chicago-offense thesis.

## Calibration Notes
This projection does not apply automatic late-game scoring compression merely because Seattle owns a double-digit lead. The model preserves a normal-to-moderate 84-point second half because Chicago has shooting-regression room and can increase urgency, while Seattle's first-half scoring was achieved without extreme field-goal or three-point shooting.

```yaml
game_id: WNBA_2026-08-10_CHI_SEA
checkpoint: halftime
score_at_checkpoint:
  CHI: 33
  SEA: 47
market_seen_before_projection: false
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
market:
  spread: SEA_-9.5_-115
  total: 171.5_-115_both_sides
  sea_tt_over: 90.5_-125
  sea_tt_under: 90.5_-105
  chi_tt_over: 81.5_-105
  chi_tt_under: 81.5_-125
separation:
  spread_points: 8.5
  total_points: 7.5
  sea_tt_points: 0.5
  chi_tt_points: 8.5
strike_hierarchy:
  primary: CHI_TT_UNDER_81.5_-125
  secondary: SEA_-9.5_-115
  tertiary: FULL_GAME_UNDER_171.5_-115
  pass: SEA_TT_90.5
status: MARKET_COMPARED_STRIKE_READY
```
