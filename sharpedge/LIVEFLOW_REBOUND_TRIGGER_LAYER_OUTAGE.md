# LIVEFLOW REBOUND TRIGGER LAYER — OUTAGE VERSION

## Purpose

This module defines the SharpEdge in-game rebound execution framework to use when NBA tracking data is unavailable. It is designed to replace missing pregame tracking confidence with real-time confirmation from box score participation, rotation behavior, and game-state rebound opportunity signals.

This layer is only used when:

- `TRACKING_OUTAGE_MODE_ACTIVE`
- `REBOUND_PROTOCOL_FALLBACK`
- `MINUTES_FIRST_MODE`

are active.

---

## Core Principle

### During tracking outages, LiveFlow becomes the confirmation layer.

Pregame rebound bets may be passed due to incomplete confidence, but in-game rebound positions may become playable once:

1. minutes are confirmed,
2. role is behaving as expected,
3. rebound participation is visible,
4. rotation risk is reduced,
5. live price remains favorable.

---

## LiveFlow Trigger Rule

A rebound LiveFlow position may only be considered when **all 5** of the following conditions are checked:

### 1. Minutes Confirmation
- Player is on normal rotation pace
- No visible minutes cap
- No injury suppression behavior
- Player is not losing run unexpectedly

### 2. Rebound Participation Confirmation
At least one of the following must be true:
- Player is already on pace for the target
- Player has visible involvement in rebound zones
- Team rebound distribution supports their role
- Player is not being boxed out of the game flow by lineup changes

### 3. Role Stability Confirmation
- Player is still operating in expected role
- Backup big has not stolen the rebound environment
- Foul trouble is not suppressing opportunity
- Script has not moved away from the archetype

### 4. Game Environment Confirmation
At least one favorable environmental condition must be present:
- Miss volume is healthy
- Pace is healthy enough
- Opponent shot quality is creating reboundable possessions
- Team is not in an abnormal foul/travel/turnover environment that distorts rebound flow

### 5. Price Confirmation
- Live number must still show value relative to updated in-game expectation
- No forcing at dead prices
- No chasing after obvious correction

---

## Green-Light Trigger Matrix

### A. Center Over Trigger
Fire only if all are true:
- On pace for at least 85% of target by halftime or late 2Q
- Minutes pace is normal or above expectation
- No foul trouble
- Backup center not absorbing meaningful rebound share
- Live line still below updated median or fair threshold

### B. Forward Over Trigger
Fire only if all are true:
- Minutes are secure
- Team rebound split is not center-dominated
- Player is actively crashing from weak side or transition
- Target is still reachable without outlier variance
- Price remains favorable

### C. Guard / Wing Ladder Trigger
Fire only if all are true:
- Threshold is low
- Minutes are stable
- Role is rebound-adjacent in current game script
- Team is creating long-board environment or transition rebound volume
- Price has not fully corrected

---

## Auto-Pass Conditions

Immediately pass live rebound entries if any of the following are true:

- Player picks up 3+ fouls too early
- Visible limp / injury suppression / trainer attention
- Minutes pace falls below expectation
- Backup big is stealing rotation or closing minutes
- Team rebound share is being dominated by another frontcourt player
- Live line has already corrected beyond fair value
- Game script becomes blowout-sensitive and role retention is uncertain

---

## Halftime Evaluation Template

For each rebound candidate, update:

- Current rebounds
- Current minutes
- Rebound pace vs target
- Foul count
- Rotation stability
- Team rebound split
- Opposing shot volume / miss volume
- Updated fair probability
- Current live price

Only green-light if the updated in-game read is stronger than the pregame read.

---

## LiveFlow Confidence Grades

### A-Grade Live Rebound Trigger
- Minutes confirmed
- Role confirmed
- Rebound pace confirmed
- Price still favorable
- No major suppression flags

### B-Grade Live Rebound Trigger
- Most conditions positive
- One mild risk present
- Price still acceptable

### C-Grade or Lower
- Pass
- No forced action

---

## Execution Rule

### Single-fire only.

During outage mode:
- no stacking live rebound positions in same game state
- no parlay conversion
- one rebound position at a time
- must pass cleanly through trigger matrix

---

## Logging Tags

Use the following tags when a LiveFlow rebound bet is made under outage mode:

- `LIVEFLOW_REBOUND_TRIGGER_ACTIVE`
- `OUTAGE_CONFIRMATION_LAYER`
- `MINUTES_CONFIRMED_IN_GAME`
- `ROLE_CONFIRMED_IN_GAME`

If passed due to failed confirmation:

- `LIVEFLOW_REBOUND_PASS`
- `FAILED_TRIGGER_LAYER`
- `ROLE_INSTABILITY`
- `MINUTES_SUPPRESSION`
- `PRICE_DEAD_ZONE`

---

## Summary Principle

### In outage mode, pregame may be unclear — live can become clear.

Do not guess early.
Do not chase dead numbers.
Use live minutes + live role + live pace + live price to confirm whether a rebound angle is real enough to attack.

This module exists to turn missing tracking data from a handicap into a delayed-confirmation edge.
