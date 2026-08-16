# WNBA LIVE-FLOW Postmortem — Minnesota Lynx at Las Vegas Aces

**Date:** 2026-08-15  
**Venue:** Michelob ULTRA Arena, Las Vegas, NV  
**Halftime:** Minnesota 48 — Las Vegas 48  
**End 3Q:** Minnesota 74 — Las Vegas 64  
**Final:** Minnesota 92 — Las Vegas 87  
**Final total:** 179  
**Status:** FINAL — 1 loss, 1 win

This game contained two separate LIVE-FLOW strikes at two different checkpoints. They must be graded independently because the model state materially changed between halftime and the end of the third quarter.

---

# 1. Halftime checkpoint

## Frozen SharpEdge projection — before sportsbook comparison

The existing checkpoint file confirms the market-blind halftime projection was frozen before William Hill prices were viewed.

| Market | SharpEdge halftime fair | Actual final | Error |
|---|---:|---:|---:|
| Minnesota team total | 91 | 92 | -1 |
| Las Vegas team total | 93 | 87 | +6 |
| Full-game total | 184 | 179 | +5 |
| Final margin | LVA by 2 | MIN by 5 | 7-point side miss |

Projected second half: **Las Vegas 45 — Minnesota 43**  
Actual second half: **Minnesota 44 — Las Vegas 39**

### Halftime fair lines

- Spread: **Las Vegas -2**
- Total: **184**
- Minnesota TT: **91**
- Las Vegas TT: **93**

### Halftime sportsbook reveal

William Hill showed:

- Minnesota -2.5 (-105)
- Las Vegas +2.5 (-125) initially
- Full-game total 184.5
- Minnesota TT 92.5
- Las Vegas TT 91.5

The executable Aces spread later moved to **Las Vegas +1.5 (-115)**.

## Halftime strike

- **Wager:** Las Vegas Aces +1.5
- **Odds:** -115
- **Stake:** $10.00
- **Potential profit:** $8.70
- **Sportsbook:** William Hill Nevada
- **Ticket time:** AUG 15 2026, 05:55 PM NV
- **Ticket ID:** `3dbb0f90-990d-11f1-9a9f-8df2172ebdb4`
- **Result:** **LOSS**
- **Final:** Minnesota 92 — Las Vegas 87
- **Net:** **-$10.00**

At entry, the gap was substantial on paper:

- SharpEdge fair: **LVA -2**
- Bet: **LVA +1.5**
- Model-to-market cushion: **3.5 points toward Las Vegas**

Yet Minnesota won by five.

## Why the halftime spread thesis failed

### 1. We overtrusted Las Vegas' first-half turnover advantage

At halftime:

- Las Vegas turnovers: **3**
- Minnesota turnovers: **8**

This was one of the main reasons Las Vegas graded as the stronger side despite the tied score.

The third quarter completely reversed that assumption.

Las Vegas committed **7 turnovers in Q3 alone**.

Jackie Young committed **4 third-quarter turnovers**, while Kayla McBride generated repeated live-ball disruption. Las Vegas' clean first-half ball security was not a stable game-state feature.

The side model treated the halftime turnover differential too much like a sustainable team-quality signal and not enough like a volatile state variable.

### 2. Minnesota's defensive disruption was underweighted

By the end of three quarters:

- McBride had **5 steals**
- Minnesota had **7 steals**
- Las Vegas had **10 turnovers**

The third quarter produced a direct defense-to-offense cascade:

- Minnesota scored **26**
- Las Vegas scored **16**
- Minnesota generated **8 points from Las Vegas turnovers** in Q3

The halftime side projection did not sufficiently price Minnesota's capacity to turn ball pressure into separation.

### 3. The Aces' offensive process was more fragile than the assist count suggested

At halftime Las Vegas owned a **15-8 assist edge**, which looked like evidence of superior half-court organization.

But Q3 exposed a different pathway:

- 3/13 FG
- 1/5 from three
- 7 turnovers
- only 1 assist

The assist edge was real, but it did not protect the Aces from a high-pressure turnover regime.

### 4. Minnesota's shooting regression did occur — just not enough to save the spread

Minnesota entered halftime at:

- **55.6% FG**
- **50.0% from three**

Second half Minnesota fell to:

- **42.9% FG**
- **35.7% from three**

So the expected efficiency cooling was directionally correct.

But spread outcomes are not determined by shooting regression alone. Las Vegas simultaneously suffered a turnover shock and shot only **35.5% in the second half**.

The model correctly identified Minnesota's regression risk but failed to account for the possibility that Las Vegas' own offensive state could deteriorate even more sharply.

### 5. A'ja Wilson's sustainable scoring was not enough to stabilize the team

Wilson was excellent:

- 32 points
- 11/12 FT
- 7 rebounds

She remained the exact sustainable offensive anchor identified at halftime.

But Jackie Young scored only **8**, Chelsea Gray was inefficient, and the team could not convert enough possessions around Wilson.

This is a useful reminder: a superstar scoring floor does not guarantee a team spread floor when the surrounding possession economy deteriorates.

---

# 2. End-of-third-quarter checkpoint

The most important positive from this game is that LIVE-FLOW **did not stay anchored to the halftime opinion**.

At the end of Q3, SharpEdge fully re-ran the game state market-blind.

Score: **Minnesota 74 — Las Vegas 64**.

## Frozen SharpEdge projection — End Q3

### Fourth quarter

- Minnesota: **20**
- Las Vegas: **22**
- Q4 total: **42**
- Q4 margin: **Las Vegas +2**

### Full game

- Minnesota: **94**
- Las Vegas: **86**
- Full-game total: **180**
- Final margin: **Minnesota +8**

### Fair lines

- Spread: **Minnesota -8 / Las Vegas +8**
- Total: **180**
- Minnesota TT: **94**
- Las Vegas TT: **86**

## Market reveal — End Q3

William Hill showed:

- Minnesota -8.5 (-115)
- Las Vegas +8.5 (-115)
- Full-game total 182.5
- Minnesota TT 95.5
- Las Vegas TT 85.5

The full-game total subsequently moved down to **181.5**, consistent with the model's lower-scoring reprice.

## End-Q3 strike

- **Wager:** Minnesota Lynx team total UNDER 95.5
- **Odds:** -110
- **Stake:** $10.00
- **Profit:** $9.09
- **Payout:** $19.09
- **Sportsbook:** William Hill Nevada
- **Ticket time:** AUG 15 2026, 06:39 PM NV
- **Ticket ID:** `50ee2a10-9913-11f1-a63d-2dc035288a17`
- **Result:** **WIN**
- **Minnesota final:** **92**
- **Winning cushion:** **3.5 points**

---

# End-Q3 model accuracy

This checkpoint was exceptionally well calibrated.

| Market | Q3 projection | Actual | Error |
|---|---:|---:|---:|
| Minnesota final | 94 | 92 | +2 |
| Las Vegas final | 86 | 87 | -1 |
| Full-game total | 180 | 179 | +1 |
| Final margin | MIN by 8 | MIN by 5 | +3 margin pts |
| Minnesota Q4 | 20 | 18 | +2 |
| Las Vegas Q4 | 22 | 23 | -1 |
| Q4 total | 42 | 41 | +1 |

That is the strongest signal from the entire game.

The end-Q3 model essentially nailed the remaining scoring environment.

## Why Minnesota TT Under 95.5 worked

Minnesota had 74 entering Q4 and needed **22+ fourth-quarter points** to clear 95.5.

SharpEdge projected only **20**.

The bearish Minnesota scoring signals were clear:

- 47.4% team 3P through three quarters
- Nia Coffey at 4/5 from three
- 9/9 FT in the third quarter
- ten-point lead reducing urgency
- late-game clock management risk

Minnesota scored **18** in Q4.

Their fourth-quarter shooting cooled to:

- 41.7% FG
- 28.6% from three

The exact regression thesis translated into the derivative we chose.

## Late foul risk was correctly recognized but did not break the Under

The end-Q3 projection explicitly acknowledged that a competitive Aces comeback could create late free throws.

That happened:

Minnesota made six fourth-quarter free throws, including four in the final 27 seconds.

Yet because the core half-court scoring slowed enough, Minnesota still finished at 92.

This was a good example of a team-total Under surviving a known upper-tail mechanism because the model had already priced the foul-scoring risk into a 94-point fair center.

---

# The biggest process lesson

This game is a textbook example of why LIVE-FLOW must be **checkpoint-adaptive rather than thesis-loyal**.

At halftime:

> SharpEdge had Las Vegas -2.

After Q3:

> SharpEdge had Minnesota -8.

That is a **10-point directional reprice** in the fair spread.

The system did not defend the original Aces opinion after the evidence changed.

The third-quarter turnover shock, McBride's pressure, Jackie Young's ball-security breakdown, and Minnesota's game control forced a complete re-evaluation.

That is exactly what a live model should do.

The halftime ticket lost. The updated model state was substantially better than the original state and produced a winning Minnesota team-total Under.

---

# Model patches / validations

## `LIVEFLOW_TURNOVER_STATE_PERSISTENCE_GATE_v1`

A halftime turnover advantage should not automatically be treated as sustainable.

Before using turnover differential to support a side, classify the source:

1. random dead-ball mistakes,
2. offensive sloppiness,
3. opponent pressure / active hands,
4. primary-handler vulnerability,
5. scheme-driven trapping or denial.

If the opponent has credible pressure personnel or the primary ballhandler is showing instability, widen the turnover tail instead of extrapolating first-half ball security.

## `LIVEFLOW_CHECKPOINT_REANCHOR_v1`

Validated strongly here.

At every major checkpoint, the prior projection becomes a reference — **not an anchor**.

If new evidence materially changes possession quality, turnover regime, foul state, rotations, or shot-generation quality, the fair spread and team totals must be rebuilt from the current state.

The halftime LVA -2 fair became MIN -8 after Q3. That reanchor was correct.

## `LIVEFLOW_HOT_TEAM_TT_COMPRESSION_GATE_v1`

Validated at end Q3.

When a leading team has accumulated scoring through elevated three-point shooting and perfect/near-perfect free-throw conversion, while game script favors clock management, compress the upper tail of its remaining team-total distribution.

Minnesota's 74 through three quarters looked dangerous for an Under, but the process underneath the number supported a lower Q4 scoring expectation.

---

# New / validated tags

- `HALFTIME_SPREAD_MISS`
- `TURNOVER_STATE_REVERSAL`
- `LVA_Q3_TURNOVER_SHOCK`
- `JACKIE_YOUNG_BALL_SECURITY_FAILURE`
- `MCBRIDE_DEFENSIVE_DISRUPTION`
- `DEFENSE_TO_OFFENSE_CASCADE`
- `MIN_HOT_3P_REGRESSION_DOWN`
- `COFFEY_HOT_3P_REGRESSION_DOWN`
- `AJA_WILSON_SUSTAINABLE_USAGE`
- `CHECKPOINT_RECALIBRATION_SUCCESS`
- `MARKET_BLIND_PROJECTION_FROZEN_Q3`
- `TEAM_TOTAL_DERIVATIVE_ALIGNMENT`
- `LATE_GAME_FOUL_SCORING_TAIL`
- `LIVEFLOW_CHECKPOINT_REANCHOR_v1`

---

# Final grades

### Halftime

**MARKET-BLIND TOTAL READ: B**  
**TEAM-TOTAL ALLOCATION: C+**  
**SPREAD / SIDE READ: D+**  
**TURNOVER-STATE MODELING: D**  
**HALFTIME WAGER: LOSS**

### End Q3

**MARKET-BLIND TOTAL READ: A+**  
**TEAM-TOTAL ALLOCATION: A**  
**SPREAD REPRICE: A-**  
**MINNESOTA TT UNDER READ: A**  
**CHECKPOINT ADAPTATION: A+**  
**END-Q3 WAGER: WIN**

## Financial result

- Aces +1.5: **-$10.00**
- Minnesota TT Under 95.5: **+$9.09**
- Combined game result: **-$0.91**

The financial result was essentially flat, but the modeling lesson was highly valuable.

### Bottom line

The halftime Aces spread failed because SharpEdge overestimated the persistence of Las Vegas' clean ball-security state and underestimated Minnesota's ability to create a pressure-driven turnover cascade.

But the system corrected aggressively at the next checkpoint.

At end Q3, SharpEdge moved from **LVA -2** to **MIN -8**, projected **Minnesota 94 — Las Vegas 86**, and projected a **42-point fourth quarter**. The game finished **Minnesota 92 — Las Vegas 87**, with **41 points in Q4**.

That is a major validation of the checkpoint-reprojection architecture:

> **A LIVE-FLOW model should be rewarded for changing its mind when the game changes.**
