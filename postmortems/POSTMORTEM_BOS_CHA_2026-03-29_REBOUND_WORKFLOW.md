# Postmortem — BOS @ CHA — 2026-03-29

## Final score
- Celtics 114
- Hornets 99

## Rebound plays logged
- ✅ Brandon Miller **Lower 6.5 rebounds** — finished with **6**
- ❌ Jayson Tatum **Higher 6.5 rebounds** — finished with **5**

## Result summary
- Card result: **1-1**
- Entry: **$2.50**
- Paid: **$0.00**
- Multiplier shown: **3.01x**

## Workflow context used
- ON/OFF rebound tool
- Confirmed lineup context
- Projected minutes input
- Charlotte-side shooting frequency context
- One pick from each team structure

## Pre-play rationale recap
### Hornets side — Brandon Miller lower 6.5
- Strong offensive spacing lineup but not a pure board-dominant role
- Rebound competition from Diabate, Bridges, Ball, and wing spillover
- Line likely a touch rich relative to role share
- Result: cleared, finished with 6

### Celtics side — Jayson Tatum higher 6.5
- Expanded usage environment with White/Brown/Vucevic out
- Heavy minutes projection and broad box-score role
- However, rebound distribution risk remained because Queta, Walsh, and Pritchard all had live glass roles
- Result: missed, finished with 5

## Actual rebound outcomes
### Celtics
- Neemias Queta: 8
- Jordan Walsh: 7
- Payton Pritchard: 6
- Jayson Tatum: 5
- Sam Hauser: 3

### Hornets
- Brandon Miller: 6
- Moussa Diabate: 6
- LaMelo Ball: 4
- Kon Knueppel: 4
- Coby White: 4
- Miles Bridges: 2

## Team rebound result
- Boston: 39
- Charlotte: 37
- Offensive rebounds: Boston 8, Charlotte 10
- Defensive rebounds: Boston 31, Charlotte 27

## What the model got right
1. **Correct under identification on Miller**
   - The workflow correctly treated Miller as a non-anchor board piece in this configuration.
2. **Good trap resistance on Charlotte side**
   - Miller did not spike into an outlier rebound ceiling.

## What the model got wrong
1. **Tatum rebound share was overestimated**
   - Extra usage did not translate to extra boards.
2. **Board distribution went elsewhere**
   - Queta and Walsh absorbed more of the available rebound volume than expected.
3. **Star-forward rebound tax warning**
   - Tatum’s all-around role looked attractive, but the actual rebound lane was less clean than the line implied.

## Sharp notes
- This is a clean example of why **usage expansion ≠ rebound expansion**.
- Rebound edges should stay tied to:
  - actual rebound lane clarity
  - center/wing competition
  - role-specific board share
- Tatum was probably a **Strong Secondary / Spillover** type look, not a true anchor.

## Confidence ladder grading
- Brandon Miller L6.5 REB — **Strong Secondary** ✅
- Jayson Tatum O6.5 REB — **Spillover / borderline Trap** ❌

## Tag summary
- `ON_OFF_TOOL_APPLIED`
- `PROJECTED_MINUTES_APPLIED`
- `CONFIRMED_LINEUP_APPLIED`
- `STRONG_SECONDARY_HIT`
- `SPILLOVER_MISS`
- `BOS_CHA_0329`

## Overall postmortem verdict
**Mixed result.**
The workflow properly identified the cleaner Charlotte under, but it over-credited Tatum’s rebound upside. Lesson: in rebound scans, role expansion must not be confused with true board control.
