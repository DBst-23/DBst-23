# Postmortem — NOP @ SAC — 2026-04-03

## Final Score
- New Orleans Pelicans 113
- Sacramento Kings 117

## Tracked Ghost Bet Leg
- Maxime Raynaud — Higher 8.5 Rebounds ✅ (finished with 9)

## Game Script Summary
- Sacramento won a close game by 4.
- The environment stayed competitive enough for starters to retain meaningful minutes.
- Sacramento won the rebounding battle 46 to 36.
- New Orleans failed to control the defensive glass and allowed multiple Kings frontcourt pieces to contribute.

## Why Maxime Raynaud Over 8.5 Worked
- Raynaud played 29 minutes in a competitive script.
- He finished with 9 rebounds and cleared the line.
- Sacramento frontcourt support was real: Achiuwa had 7 and Cardwell added 8 off the bench.
- The Kings generated enough total rebound volume for Raynaud to remain live even without a massive ceiling game.

## Supporting Rebound Context
### Kings
- Maxime Raynaud: 9 rebounds
- Precious Achiuwa: 7 rebounds
- Devin Carter: 6 rebounds
- Nique Clifford: 5 rebounds
- Dylan Cardwell: 8 rebounds in 24 minutes

### Pelicans
- Jeremiah Fears: 8 rebounds
- Yves Missi: 7 rebounds
- Zion Williamson: 6 rebounds
- Derik Queen: 6 rebounds
- Trey Murphy III: 4 rebounds

## Structural Takeaways
### 1. Competitive script preserved the over
- This was not a blowout suppression environment.
- Raynaud retained enough minutes and rebound chances to stay on track.

### 2. Kings frontcourt rebound ecosystem remained favorable
- Sacramento’s rebound production was spread but still strong enough for the primary center over to cash.
- Secondary frontcourt rebounding did not kill the center over; instead it confirmed overall team control of the glass.

### 3. Trey Murphy over failed structurally
- Murphy finished with only 4 rebounds.
- Despite solid minutes (32), his board share did not climb enough.
- This supports caution on wing-over builds when multiple Pelicans frontcourt rebounders are active and shot distribution is balanced.

## Model Validation
### Hit
- Maxime Raynaud Over 8.5 rebounds — validated

### Miss / Warning
- Trey Murphy Over 5.5 rebounds — did not clear
- Indicates that wing rebound overs on this Pelicans configuration can be fragile if center/forward rebound share remains healthy.

## Tracking Tags
- COMPETITIVE_SCRIPT_REBOUND_OVER_VALIDATED
- TEAM_GLASS_CONTROL_SUPPORTS_CENTER_OVER
- WING_OVER_FRAGILITY_NOP
- FRONTCOURT_SUPPORT_DID_NOT_KILL_PRIMARY_CENTER_OVER

## Box Score Reference
### Pelicans Starters
- Saddiq Bey: 1 rebound
- Trey Murphy III: 4 rebounds
- Herbert Jones: 1 rebound
- Zion Williamson: 6 rebounds
- Yves Missi: 7 rebounds

### Pelicans Bench
- Jeremiah Fears: 8 rebounds
- Micah Peavy: 3 rebounds
- Derik Queen: 6 rebounds
- Jordan Hawkins: 0 rebounds

### Kings Starters
- DeMar DeRozan: 2 rebounds
- Precious Achiuwa: 7 rebounds
- Maxime Raynaud: 9 rebounds
- Nique Clifford: 5 rebounds
- Devin Carter: 6 rebounds

### Kings Bench
- Daeqwon Plowden: 3 rebounds
- Dylan Cardwell: 8 rebounds
- Killian Hayes: 3 rebounds
- Doug McDermott: 3 rebounds
