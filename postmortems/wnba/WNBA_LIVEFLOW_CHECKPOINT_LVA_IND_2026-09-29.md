# WNBA LIVE-FLOW Checkpoint — Las Vegas Aces at Indiana Fever

## Status
**OPEN — MARKET-BLIND FREEZE**

## Market-Blind Freeze
- Date: 2026-09-29
- Checkpoint: Halftime
- Score: Indiana 48, Las Vegas 43
- Halftime total: 91
- Market viewed before projection: NO

## First-Half Read
Indiana: 48 points. Quarter scoring: 18, 30.

Las Vegas: 43 points. Quarter scoring: 26, 17.

Structural notes:
- Competitive game state: Indiana +5 at halftime after four lead changes and four ties.
- Indiana's Q2 surge was driven by 13/20 FG (65%) and 22 paint points; that level of conversion is unlikely to fully persist.
- Las Vegas committed 9 first-half turnovers, including 8 in Q2, producing 14 Indiana points. That turnover rate is a major positive-regression candidate for the Aces.
- Both teams shot roughly 51-52% overall in the first half, but neither side relied on unsustainably hot three-point shooting: both were 4/12 from three.
- Indiana's half-court creation was strong: 30 paint points and Caitlin Clark generated 11 assists in 18:44.
- Las Vegas still produced 43 despite turnover drag; A'ja Wilson, Chelsea Gray and Jackie Young combined for 27 points.
- No current blowout-decay flag. This remains a competitive second-half environment.

## Frozen SharpEdge Projection
### Second Half
- Las Vegas: 45
- Indiana: 46
- Second-half total: 91

### Full Game
- Las Vegas: 88
- Indiana: 94
- Full-game total: 182
- Full-game margin: Indiana +6

## SharpEdge Fair Lines
- Spread: **Indiana -5.5**
- Full-game total: **181.5**
- Indiana team total: **93.5**
- Las Vegas team total: **88.0**

## Projection Range
Central 80% working band:
- Full-game total: approximately **175-189**
- Indiana: approximately **88-100**
- Las Vegas: approximately **82-95**

## LIVE-FLOW Interpretation
The first-half 91-point total is not being extrapolated mechanically. SharpEdge expects:
- Indiana Q2 shooting to cool,
- Las Vegas turnover rate to normalize,
- continued competitive starter minutes,
- enough offensive creation on both sides to keep the total environment near the low 180s.

The key tension is **Indiana efficiency regression vs. Las Vegas turnover regression**. Those forces partially offset, which is why the frozen total stays close to the first-half scoring pace rather than sharply moving in either direction.

## Market Comparison
**PENDING.** Do not overwrite the frozen projection after sportsbook/Kalshi prices are shown.

```yaml
game_id: WNBA_2026-09-29_LVA_IND
checkpoint: halftime
score_at_checkpoint:
  LVA: 43
  IND: 48
  total: 91
  margin: IND_5
market_seen_before_projection: false
first_half:
  LVA:
    fg: 15_29
    three: 4_12
    ft: 9_11
    turnovers: 9
    paint_points: 16
  IND:
    fg: 19_37
    three: 4_12
    ft: 6_8
    turnovers: 7
    paint_points: 30
model:
  second_half:
    LVA: 45
    IND: 46
    total: 91
  final:
    LVA: 88
    IND: 94
    total: 182
    margin: IND_6
fair_lines:
  spread: IND_-5.5
  total: 181.5
  IND_TT: 93.5
  LVA_TT: 88.0
status: OPEN_MARKET_BLIND_FREEZE
```
