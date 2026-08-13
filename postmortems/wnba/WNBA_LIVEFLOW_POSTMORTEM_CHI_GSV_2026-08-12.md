# WNBA LIVE-FLOW Postmortem — Chicago Sky at Golden State Valkyries

**Date:** 2026-08-12  
**Venue:** Chase Center, San Francisco, CA  
**Checkpoint:** Halftime  
**Halftime score:** Golden State 43 — Chicago 40  
**Final score:** Golden State 91 — Chicago 71  
**Final total:** 162  
**Status:** FINAL — Golden State team-total Under loss

## SharpEdge frozen projection — before sportsbook comparison

Initial market-blind projection:

| Market | SharpEdge projection | Actual | Error |
|---|---:|---:|---:|
| Full-game total | 163.0 | 162 | +1.0 |
| Golden State team total | 83.0 | 91 | -8.0 |
| Chicago team total | 80.0 | 71 | +9.0 |

Projected second half: **Golden State 40 — Chicago 40**  
Actual second half: **Golden State 48 — Chicago 31**

The working Golden State team-total fair referenced immediately before the wager was approximately **84.5**. William Hill offered **88.5**, creating a roughly **4-point working gap toward the Under**.

## LIVE-FLOW strike

- **Wager:** Golden State Valkyries team total UNDER 88.5
- **Odds:** -125
- **Stake:** $10.00
- **Potential profit:** $8.00
- **Sportsbook:** William Hill
- **Ticket timestamp:** AUG 12 2026, 08:07 PM NV
- **Ticket ID:** `2ebe0ec0-96c4-11f1-b764-7b0a946ce410`
- **Result:** **LOSS**

Golden State finished with **91**, beating the team-total line by **2.5 points**.

# The most important lesson

This was **not primarily a full-game total failure**.

SharpEdge projected **163 total points**. The game finished at **162**.

We projected approximately **80 combined second-half points**. The second half produced **79**.

That part of LIVE-FLOW was almost exact.

The failure was **how we allocated those remaining points between the teams**.

We projected the second half around **40-40**. It finished **Golden State 48 — Chicago 31**.

So the core diagnosis is:

> **TEAM-TOTAL ALLOCATION FAILURE, not total-environment failure.**

## What we got right

### 1. The total scoring environment

At halftime the game had 83 points. Our final projection was 163, implying approximately 80 more points.

Actual second-half scoring: **79**.

That is excellent combined-total calibration.

### 2. Chicago shooting regression

Chicago entered halftime shooting:

- **58.6% FG**
- **50% from three**

That was highly vulnerable to regression.

Chicago's second half fell to:

- **29.4% FG**
- **23.1% from three**
- only **31 points**

The regression thesis itself was correct.

## Where the model broke

### 1. We treated Chicago regression as only a Chicago scoring reduction

That was incomplete.

At halftime Golden State already had:

- **8 steals**
- Chicago had **10 turnovers**
- Golden State had only **4 turnovers**

When Chicago's offense regressed, those possessions did not simply disappear from the game. Some became Golden State transition opportunities.

Golden State finished with:

- **16 steals — a franchise record**
- Chicago committed **18 turnovers**
- Chicago allowed **25 points off turnovers**
- Golden State scored **15 fast-break points**

That first-half defensive disruption was a forward-looking offensive signal for Golden State.

We underweighted it.

### 2. The Q2 regime shift was already visible

Golden State scored:

- Q1: **16**
- Q2: **27**

The halftime average of 21.5 points per quarter hid a very different most-recent state.

Golden State had already moved from a poor opening quarter into a much more productive offensive/defensive regime.

Then they scored **29 in Q3**.

Our projection effectively pulled them back toward the full-half average too aggressively.

### 3. Tiffany Hayes was not noise

At halftime Hayes had:

- **11 points**
- in only **8:54**
- **4-for-5 FG**
- **3 steals**
- **+11**

She was showing both offensive usage and defensive activity.

She finished with **22 points**, six rebounds, five assists and three steals.

Kaila Charles also had meaningful first-half shot volume despite poor efficiency, then scored **10 second-half points**.

Golden State's bench was carrying more live upside than the team-total Under projection priced.

### 4. The derivative selection was structurally misaligned

This is the biggest betting-process lesson.

Our total Under thesis was strongly tied to **Chicago's unsustainable first-half shooting**.

But we chose an Under on **Golden State's team total**.

Those are not equivalent positions.

Chicago could regress hard — which it did — while Golden State captured a larger share of the remaining scoring through steals, transition offense and bench production.

That is exactly what happened:

- Chicago second half: **31**
- Golden State second half: **48**
- Combined: **79**

The total stayed in our expected range while the team split moved dramatically.

## Why 88.5 was less insulated than it looked

Golden State had **43 at halftime**.

To beat 88.5, they needed **46 second-half points**.

Our initial second-half projection gave them only **40**.

The gap looked comfortable, but 46 points over 20 minutes was not an extreme outcome given:

- the Q2 27-point burst,
- 8 halftime steals,
- Chicago's turnover load,
- Golden State's 14 first-half free-throw attempts,
- Hayes' bench ignition,
- and the possibility that Chicago shooting regression would create transition opportunities.

Golden State scored **48** after halftime — only a few points above the threshold needed to break the Under.

## Model patch — `LIVEFLOW_TEAM_TOTAL_ALLOCATION_GATE_v1`

Going forward:

1. **Project combined remaining scoring first.** Then allocate those points between the teams through a separate scoring-share model.
2. Team scoring share must include **turnover differential, steals, transition opportunities, offensive rebounds, free-throw generation, and live rotation/usage**.
3. If a team has **7+ halftime steals** or the opponent has **9+ halftime turnovers**, trigger `DEFENSE_TO_OFFENSE_CASCADE` and widen that team's upper scoring tail before approving a team-total Under.
4. Add a **quarter-regime check**. When Q2 differs sharply from Q1 because of sustainable opportunity signals, weight the recent quarter more heavily than the simple first-half average.
5. Track **bench ignition** separately. High scoring/usage plus defensive activity in limited minutes is a rotation-upside signal.
6. Run a **derivative consistency check** before betting. If the total Under is mainly driven by expected regression from Team A, do not automatically bet Team B Under.
7. Team-total Unders need a **tail-risk gate**, not just a mean projection. A 3-5 point point-estimate gap is not automatically strong if the upper quartile can still clear the line.

## New volatility / failure tags

- `TEAM_TOTAL_ALLOCATION_MISS`
- `DEFENSE_TO_OFFENSE_CASCADE`
- `HALFTIME_STEAL_PRESSURE`
- `Q2_REGIME_SHIFT`
- `BENCH_IGNITION`
- `DERIVATIVE_MISALIGNMENT`
- `TEAM_TOTAL_UPPER_TAIL_RISK`

## Final grade

**FULL-GAME TOTAL READ: A**  
**SECOND-HALF COMBINED SCORING READ: A**  
**TEAM-TOTAL ALLOCATION: D**  
**DERIVATIVE SELECTION: D+**  
**PROCESS VALUE OF POSTMORTEM: HIGH**

### Bottom line

We were nearly dead-on about **how many total points remained in the game**. We were wrong about **who would score them**.

That distinction matters enormously for LIVE-FLOW.

This loss teaches SharpEdge not to treat a team total as a miniature full-game total. The combined environment and the allocation of that scoring are two separate modeling problems. In this game, Chicago's regression suppressed Chicago exactly as expected — but Golden State's defensive disruption, transition conversion, Q2 regime shift and bench production redirected the scoring share toward the Valkyries and broke the team-total Under.
