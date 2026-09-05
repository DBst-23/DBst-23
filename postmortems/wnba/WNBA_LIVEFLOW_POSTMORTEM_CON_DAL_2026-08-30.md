# WNBA LIVE-FLOW Postmortem — Connecticut Sun at Dallas Wings

## Game
- Date: 2026-08-30
- Venue: College Park Center, Arlington, TX
- Final: Dallas Wings 97, Connecticut Sun 71
- Final total: **168**
- Halftime: Dallas 60, Connecticut 47
- End 3Q: Dallas 83, Connecticut 59
- Second half: Dallas 37, Connecticut 24

## Executive Summary
This game produced two different failures that must be separated cleanly:

1. **Model/reading failure on the halftime Over 188.5.** The game had already produced 107 first-half points, but the remaining scoring environment was overestimated. The second half generated only 61 points.
2. **Execution/tilt failure after the game state changed.** By the end of the third quarter, SharpEdge's frozen projection had reset to approximately 179.0 and the live market was 180.5. The system explicitly classified the edge as too small and recommended **NO STRIKE / HOLD**. The subsequent Over 174.5 and Over 170.5 entries were discretionary chase bets, not model-approved positions.

The correct lesson is not to rewrite all three losses as one modeling miss. The first was a bad total read; the next two were a discipline breach after the model had already moved away from the Over.

## Wager Ledger

| Ticket | Market | Odds | Stake | Result | Final margin |
|---|---:|---:|---:|---|---:|
| 1 | Over 188.5 | -115 | $15.00 | LOSS | 20.5 points below line |
| 2 | Over 174.5 | -120 | $20.00 | LOSS | 6.5 points below line |
| 3 | Over 170.5 | -105 | $11.68 | LOSS | 2.5 points below line |

**Total risked:** $46.68  
**Total returned:** $0.00  
**Net:** **-$46.68**

## Halftime State
Dallas led 60-47 at halftime, with 107 combined points already scored.

### Dallas first half
- 21/35 FG — **60.0%**
- 4/9 3PT — **44.4%**
- 14/16 FT — **87.5%**
- 30 paint points
- 8 second-chance points
- 6 turnovers

### Connecticut first half
- 17/40 FG — **42.5%**
- 5/15 3PT — **33.3%**
- 8/10 FT — **80.0%**
- 20 paint points
- 3 turnovers

Aaliyah Edwards had 21 first-half points on 6/8 shooting, 2/2 from three and 7/7 from the line. Dallas was converting at an elite rate across multiple scoring channels.

The Over 188.5 required at least 82 second-half points.

## Why the Halftime Over Failed
The core halftime mistake was treating first-half scoring productivity as more sustainable than it actually was.

### 1. Dallas efficiency had substantial cooling risk
Dallas entered halftime shooting 60.0% from the field and 44.4% from three. The offense was excellent, but the projection did not sufficiently price the possibility that a double-digit lead would later reduce starter minutes and late-game urgency.

Dallas scored 60 in the first half but only 37 in the second half.

### 2. Connecticut's scoring concentration was fragile
Connecticut's 47 first-half points were heavily supported by Aaliyah Edwards, who scored 21 before halftime. The rest of the offense was much less dependable.

Edwards scored only five points after halftime. Connecticut as a team shot **7/33 (21.2%)** in the second half and produced only 24 points.

### 3. The model underestimated blowout-state suppression
Dallas led by 13 at halftime and pushed the lead to 24 by the end of the third quarter. Once the game entered a noncompetitive state, the scoring environment changed materially.

The fourth-quarter Dallas lineup was largely reserve-driven, while Connecticut remained unable to convert even against the lower-leverage game environment.

### 4. Regression was asymmetric, not balanced
The game reinforced the exact issue already identified in recent SharpEdge reviews: regression does not need to distribute evenly.

Dallas cooled, but Connecticut did not provide the compensating offensive rebound the Over needed. Instead, Connecticut deteriorated further:

- Q3: 12 points
- Q4: 12 points
- Second half: 24 points

The correct total model must allow one offense to remain broken while the other shifts into clock/bench management.

## End-3Q Recalibration — Model Recovered
At the end of the third quarter, Dallas led 83-59 and the game total stood at 142.

SharpEdge froze the following approximate market-blind projection before viewing the sportsbook line:

- Connecticut final: **76.5**
- Dallas final: **102.5**
- Full-game total: **179.0**
- Implied final margin: Dallas **-26.0**

William Hill then showed:

- Full-game total: **180.5**
- Dallas TT: **103.5**
- Connecticut TT: **77.5**
- Spread: Dallas **-25.5**

Every scoring market was slightly higher than the SharpEdge center, but the gaps were only 1.0-1.5 points. The system correctly labeled the full-game Under as only marginal and issued **NO STRIKE / HOLD FIRE**.

That was the proper process decision.

## Fourth-Quarter Audit
The fourth quarter finished:

- Dallas 14
- Connecticut 12
- Combined: **26**

Final total: **168**.

Relative to the frozen end-3Q projection:

- Projected total: 179.0
- Actual total: 168
- Total error: **-11.0**
- Projected Dallas: 102.5
- Actual Dallas: 97
- Dallas error: **-5.5**
- Projected Connecticut: 76.5
- Actual Connecticut: 71
- Connecticut error: **-5.5**

The striking feature is that the team-allocation error was symmetric in this particular checkpoint: both teams finished 5.5 below their frozen centers. The larger problem was not allocation but a shared fourth-quarter pace/efficiency collapse created by blowout game state and reserve usage.

## Tilt / Execution Postmortem
The two 7:11 PM Over bets are classified separately from the model.

The user explicitly identified the state afterward as tilt. That admission matters because the repository should preserve process truth rather than laundering discretionary action into model performance.

### Over 174.5 — $20 at -120
- Result: LOSS
- Final: 168
- Miss: 6.5 points
- Classification: **TILT CHASE / NON-MODEL**

### Over 170.5 — $11.68 at -105
- Result: LOSS
- Final: 168
- Miss: 2.5 points
- Classification: **TILT CHASE / NON-MODEL**

Both bets were directionally inconsistent with the end-3Q SharpEdge read, which had already shifted to a slight Under lean and a no-bet decision.

## Execution Patch — TILT_CHASE_LOCKOUT_v1
This game justifies a formal execution safeguard.

### Rule
Once a live-game position loses its original thesis or SharpEdge produces a later checkpoint projection in the opposite direction, **no same-game recovery wager may be placed unless a fresh market-blind projection independently clears the normal strike threshold**.

### Operational requirements
1. Every new live entry must have its own frozen projection.
2. A prior loss cannot be used as justification for another entry.
3. If the model flips direction, all earlier directional bias is considered dead.
4. Two or more same-game entries require explicit cumulative exposure review before another dollar is risked.
5. A wager placed without a fresh model-approved edge is logged as **NON_MODEL** and excluded from model hit-rate evaluation.

## Exposure Patch — ONE_GAME_EXPOSURE_CAP_v1
This game also shows why unit sizing must be evaluated at the game level, not ticket level.

Three individual wagers may each look modest, but together they created **$46.68** of exposure to one game and one correlated scoring thesis.

Future LIVE-FLOW review should display:

- current game exposure
- prior same-game wagers
- directional correlation
- remaining approved risk budget

before allowing any additional strike.

## Model-Learning Notes
### Negative
- Halftime scoring sustainability was overestimated.
- Blowout probability was not weighted aggressively enough.
- Connecticut's offense was assumed to retain more scoring floor than it actually had.
- The model did not sufficiently separate "positive regression is possible" from "positive regression is likely enough to support an Over."

### Positive
- End-3Q recalibration moved sharply downward and correctly rejected the live market as lacking sufficient edge.
- The final 168 validates the direction of the end-3Q downgrade, even though the 179.0 center remained 11 points too high.
- The model correctly recognized that 180.5 was not a buyable Over merely because the halftime Over thesis had existed earlier.
- Logging the two chase wagers as NON_MODEL protects future performance analysis from contaminated attribution.

## Highest-Priority Test After Break
When WNBA play resumes on **September 17, 2026**, the highest-priority LIVE-FLOW refinement from this game should be a **BLOWOUT_SCORING_DECAY + ROTATION_SUPPRESSION** test.

For historical halftime and end-3Q checkpoints, stratify games by lead size and estimate how remaining scoring changes when:

- lead is 12+
- lead is 18+
- lead is 24+
- starters begin losing projected minutes
- losing team has weak half-court efficiency
- leading team no longer needs transition pressure or aggressive shot creation

The test should compare remaining-total MAE with and without a blowout-decay term.

## Classification
- Primary halftime call: Over 188.5
- Halftime model result: LOSS
- Later model checkpoint: End 3Q
- End-3Q model direction: Slight Under / no bet
- End-3Q execution decision: CORRECT PASS
- Chase wagers: 2
- Chase wagers model-approved: NO
- Combined game result: 0-3
- Combined game net: -$46.68
- Primary failure: Scoring sustainability + blowout-state suppression
- Secondary failure: Tilt / same-game overexposure

## Frozen Tags
- LIVE_FLOW_POSTMORTEM
- WNBA_2026_08_30_CON_DAL
- HALFTIME_OVER_LOSS
- SCORING_SUSTAINABILITY_MISS
- BLOWOUT_SCORING_DECAY
- ROTATION_SUPPRESSION
- ASYMMETRIC_REGRESSION_DISTRIBUTION
- END3_MARKET_BLIND_PROJECTION_FROZEN
- END3_DIRECTIONAL_FLIP
- END3_NO_STRIKE_CORRECT
- TILT_CHASE_LOCKOUT_v1
- ONE_GAME_EXPOSURE_CAP_v1
- SAME_GAME_CORRELATION_RISK
- NON_MODEL_WAGER
- EXECUTION_DISCIPLINE_FAILURE
- MODEL_ATTRIBUTION_SEPARATION
- CLOSED_LOSS

```yaml
game_id: WNBA_2026-08-30_CON_DAL
halftime:
  CON: 47
  DAL: 60
  total: 107
halftime_entry:
  market: full_game_total
  side: OVER
  line: 188.5
  odds: -115
  stake: 15.00
  result: LOSS
end3:
  CON: 59
  DAL: 83
  total: 142
end3_frozen_projection:
  CON: 76.5
  DAL: 102.5
  total: 179.0
  spread: DAL_-26.0
end3_market:
  total: 180.5
  DAL_TT: 103.5
  CON_TT: 77.5
  spread: DAL_-25.5
end3_decision: NO_STRIKE
chase_entries:
  - side: OVER
    line: 174.5
    odds: -120
    stake: 20.00
    classification: NON_MODEL_TILT_CHASE
    result: LOSS
  - side: OVER
    line: 170.5
    odds: -105
    stake: 11.68
    classification: NON_MODEL_TILT_CHASE
    result: LOSS
final:
  CON: 71
  DAL: 97
  total: 168
q4:
  CON: 12
  DAL: 14
  total: 26
end3_projection_errors:
  CON: -5.5
  DAL: -5.5
  total: -11.0
combined_game_exposure: 46.68
combined_net: -46.68
status: CLOSED
```
