# WNBA LIVE-FLOW Postmortem — Minnesota Lynx at Golden State Valkyries

## Game Identity
- Date: 2026-08-19
- Venue: Chase Center, San Francisco, CA
- Final: Minnesota 77, Golden State 66
- Final total: **143**
- Halftime: Minnesota 41, Golden State 26
- Halftime total: **67**
- Game ID: `WNBA_2026-08-19_MIN_GSV`

## Pre-Market SharpEdge Freeze — Halftime
SharpEdge projected the game **before viewing the sportsbook market**.

### Frozen SharpEdge projection
#### Second half
- Minnesota: **38**
- Golden State: **35**
- 2H total: **73**
- 2H margin: Minnesota -3

#### Full game
- Minnesota: **79**
- Golden State: **61**
- Full-game total: **140**
- Full-game margin: Minnesota -18

### Fair lines
- Spread: **Minnesota -18**
- Full-game total: **140**
- Minnesota team total: **79**
- Golden State team total: **61**

### Central ranges
- Minnesota final: **75-83**
- Golden State final: **57-66**
- Full-game total: **134-147**
- Final margin: Minnesota by **11-24**

## Halftime State
Minnesota led 41-26.

### Minnesota
- 15/28 FG — 53.6%
- 4/10 3PT — 40.0%
- 7/8 FT — 87.5%
- 22 rebounds
- 11 assists
- 9 turnovers

### Golden State
- 9/37 FG — 24.3%
- 2/14 3PT — 14.3%
- 6/6 FT — 100%
- 15 rebounds
- 6 assists
- 4 turnovers

## Core Halftime Thesis
Golden State had the strongest positive-regression signal in the game. The Valkyries had generated **37 first-half FGA** with only four turnovers, but converted just 24.3% overall and 14.3% from three. Their possession process was substantially healthier than their 26-point scoring output.

Minnesota had the opposite efficiency profile. The Lynx were converting 53.6% from the field, 40% from three and 87.5% from the line, but had only 28 FGA because nine turnovers suppressed shot volume. The expected second-half tradeoff was therefore:

- Golden State scoring improves materially through shooting regression.
- Minnesota shooting efficiency cools.
- Minnesota turnover rate improves enough to preserve scoring opportunity.
- Minnesota's defensive quality and 15-point lead suppress the ceiling of Golden State's comeback scoring.
- Blowout/rotation risk increases uncertainty on both side and team-total markets.

That produced a 73-point second-half projection and **140 fair full-game total**.

## Market Reveal
William Hill posted:

- Minnesota -12.5 (-110)
- Golden State +12.5 (-120)
- Full-game total: **144.5**
  - Over -120
  - Under -110
- Minnesota team total: **78.5**
  - Over -120
  - Under -110
- Golden State team total: **65.5**
  - Over -105
  - Under -125

### Model vs market
| Market | SharpEdge | Book | Difference | Read |
|---|---:|---:|---:|---|
| Full-game total | 140 | 144.5 | **4.5 pts** | Under value |
| Minnesota TT | 79 | 78.5 | +0.5 | Essentially fair |
| Golden State TT | 61 | 65.5 | **4.5 pts** | Under pressure |
| Spread | MIN -18 | MIN -12.5 | **5.5 pts** | Model showed MIN side value, but high game-state risk |

## Wager Logged
| Checkpoint | Market | Line | Odds | Stake | Result | Final Total | Net |
|---|---|---:|---:|---:|---|---:|---:|
| Halftime | Full-game total | **Under 144.5** | -110 | **$15.00** | **WIN** | **143** | **+$13.64** |

- Total risk: **$15.00**
- Paid: **$28.64**
- Profit: **+$13.64**
- Closing margin to bet line: **1.5 points**

## Final Result vs Projection
### Team scores
| Team | SharpEdge | Actual | Error |
|---|---:|---:|---:|
| Minnesota | 79 | 77 | **-2** |
| Golden State | 61 | 66 | **+5** |

### Game-level results
| Metric | SharpEdge | Actual | Error |
|---|---:|---:|---:|
| Full-game total | 140 | 143 | **+3** |
| 2H total | 73 | 76 | **+3** |
| Final margin | MIN -18 | MIN -11 | **7 pts toward GSV** |

The final total landed **inside the frozen 134-147 central range** and only three points above the 140 fair center.

## What Happened in the Second Half
The second half finished:

- Minnesota 36
- Golden State 40
- Combined: **76**

SharpEdge had projected Minnesota 38, Golden State 35.

### Minnesota
Minnesota finished almost exactly where expected. The Lynx scored 36 second-half points versus a 38-point projection.

Their first-half efficiency did cool, but their offense remained stable enough to keep the total from collapsing. Minnesota finished the game at 50% FG and 36.8% from three, while converting 14-of-16 free throws.

### Golden State
Golden State's positive regression was real and stronger than the midpoint projection.

After scoring only 26 in the first half, the Valkyries scored **40 in the second half** despite still finishing at only 32.5% from the field and 18.9% from three for the game.

The second-half improvement came from a combination of:
- Better two-point conversion.
- More offensive-rebound activity.
- Reduced turnover damage.
- Sustained shot volume.
- A strong fourth quarter despite poor three-point shooting.

Golden State scored 25 in Q4 and finished with 77 field-goal attempts compared with Minnesota's 56.

This confirms that the first-half shot-volume signal was legitimate. The model correctly identified the Valkyries as a positive-regression offense, but the central estimate of 35 second-half points was about five points too low.

## Quarter Path
| Quarter | Minnesota | Golden State | Total |
|---|---:|---:|---:|
| Q1 | 21 | 13 | 34 |
| Q2 | 20 | 13 | 33 |
| Q3 | 13 | 15 | 28 |
| Q4 | 23 | 25 | 48 |

The Under was not a smooth coast.

The key pattern was:
- Q3 strongly supported the Under with only **28 combined points**.
- Q4 then jumped to **48 combined points**.
- The final landed at 143, just 1.5 below the wagered 144.5.

## Q4 Risk Audit
The fourth quarter is the most important learning component of this win.

The 48-point quarter was driven by more than simple shooting variance:
- Golden State continued attacking while trailing double digits.
- Minnesota's primary players remained active deep into the quarter.
- The game tightened enough to preserve competitive rotations rather than triggering a full bench-emptying blowout state.
- Golden State generated repeated offensive-rebound possessions.
- Late-game fouling added Minnesota free throws.

Minnesota shot 7/14 FG and 7/8 FT in Q4. Golden State took **25 field-goal attempts** in the quarter and added seven offensive rebounds.

The Under won, but late-game possession volume materially narrowed the cushion.

## Model Evaluation
### What SharpEdge got right
1. **The total direction was correct.**
   - Fair total: 140
   - Market: 144.5
   - Final: 143

2. **Minnesota scoring projection was excellent.**
   - Projected 79
   - Actual 77

3. **Golden State positive regression was correctly identified.**
   - The Valkyries improved from 26 first-half points to 40 second-half points.

4. **The frozen distribution captured the outcome.**
   - Central total range: 134-147
   - Actual: 143

5. **The market-blind sequencing worked.**
   - Projection was established before sportsbook exposure, preserving independence from market anchoring.

### What SharpEdge underestimated
1. **Golden State's second-half scoring ceiling.**
   - Projected 35
   - Actual 40

2. **Fourth-quarter possession volume.**
   - Golden State's 25 Q4 FGA plus seven offensive rebounds created far more scoring opportunity than a simple game-clock/blowout read would imply.

3. **Competitive persistence in a double-digit game.**
   - A 15-point halftime deficit did not produce passive late-game offense or early bench surrender.

4. **Side uncertainty.**
   - Model spread: MIN -18
   - Actual margin: MIN -11
   - The market's MIN -12.5 was closer than our side projection.

## Important Distinction: Correct Bet vs Comfortable Bet
This was a **correct process win**, but not a high-margin result.

SharpEdge had a 4.5-point modeled edge against 144.5, yet the ticket cleared by only 1.5 points. That does not invalidate the projection; a single result is one draw from the distribution. However, the postmortem shows why LIVE-FLOW totals need explicit late-game volatility treatment even when the core regression thesis is correct.

The game finished three points above the model center but still inside the central range.

## LIVE-FLOW Learning Rules Added
### Rule 1 — Shot-volume health is a real regression signal
When a team is shooting extremely poorly but still generating high FGA volume with low turnovers, do not project the raw scoring rate forward. Golden State's 37 first-half FGA was a major clue that 26 points understated its offensive opportunity quality.

### Rule 2 — Blowout does not automatically mean Under protection
A double-digit lead can reduce pace, but the trailing team's urgency can also create:
- faster possessions,
- more three-point attempts,
- offensive-rebound volume,
- and late fouling.

Treat blowout state as a **volatility modifier**, not an automatic Under modifier.

### Rule 3 — Separate efficiency regression from possession regression
Minnesota was due for shooting regression downward but turnover regression upward. These forces offset. Future LIVE-FLOW projections should keep these two mechanisms distinct rather than applying one generic regression adjustment.

### Rule 4 — Add a Q4 possession-floor check before Under entries
For halftime Unders, estimate whether the trailing team is still likely to generate normal-to-high fourth-quarter shot volume. If the trailing team has healthy shot generation and competitive starters are likely to remain on the floor, reduce the Under edge or widen the uncertainty band.

### Rule 5 — Strong model edge can coexist with narrow realized margin
Do not downgrade a valid projection solely because a winning bet clears narrowly. Grade the process using:
- pre-market independence,
- projection error,
- distribution containment,
- and whether the modeled mechanism actually occurred.

## Postmortem Grade
### Projection
**A-**

Reason:
- Full-game total error only +3.
- Minnesota team total error only -2.
- Actual total remained inside the frozen range.
- Golden State regression direction was correct, though magnitude was underestimated.

### Wager selection
**A**

The Under 144.5 provided 4.5 points above the 140 fair total and won.

### Risk calibration
**B+**

The bet was valid, but the 48-point Q4 shows that late-game possession/foul volatility needed more explicit weighting.

## Final Classification
- Result: **WIN**
- Market: **Full-game Under**
- Checkpoint: **Halftime**
- Model fair total: **140**
- Bet line: **Under 144.5 -110**
- Final total: **143**
- Modeled edge at entry: **4.5 points**
- Closing cushion: **1.5 points**
- Stake: **$15.00**
- Profit: **+$13.64**
- Process tag: **VALID_EDGE / CORRECT_DIRECTION / NARROW_FINISH**

## Tags
- MARKET_BLIND_PROJECTION_FROZEN_HALFTIME
- TOTAL_EDGE_UNDER
- GSV_POSITIVE_SHOOTING_REGRESSION_CONFIRMED
- GSV_SHOT_VOLUME_SIGNAL_CONFIRMED
- MIN_EFFICIENCY_REGRESSION_CONFIRMED
- MIN_TURNOVER_REGRESSION_OFFSET
- Q4_POSSESSION_VOLATILITY
- LATE_GAME_FOUL_RISK
- BLOWOUT_NOT_AUTOMATIC_UNDER
- CENTRAL_RANGE_HIT
- FULL_GAME_TOTAL_ERROR_PLUS_3
- VALID_EDGE_WIN

```yaml
game_id: WNBA_2026-08-19_MIN_GSV
checkpoint: halftime
market_seen_before_projection: false
score_at_checkpoint:
  MIN: 41
  GSV: 26
sharpedge:
  second_half:
    MIN: 38
    GSV: 35
    total: 73
  final:
    MIN: 79
    GSV: 61
    total: 140
    margin: MIN_18
  central_total_range: 134-147
market:
  spread: MIN_-12.5
  total: 144.5
  min_tt: 78.5
  gsv_tt: 65.5
wager:
  market: full_game_total
  side: under
  line: 144.5
  odds: -110
  stake: 15.00
  payout: 28.64
  profit: 13.64
result:
  MIN: 77
  GSV: 66
  total: 143
  margin: MIN_11
  wager_result: WIN
errors:
  MIN: -2
  GSV: +5
  total: +3
  margin: 7_points_toward_GSV
classification: VALID_EDGE_CORRECT_DIRECTION_NARROW_FINISH
```
