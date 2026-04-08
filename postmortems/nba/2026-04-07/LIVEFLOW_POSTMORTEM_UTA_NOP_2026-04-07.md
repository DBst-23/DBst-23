# LIVEFLOW POSTMORTEM — UTA @ NOP

- Date: 2026-04-07
- Mode: LIVE-FLOW Ghost Bet
- Market: Live Spread
- Pick: NOP +3.5
- Trigger: Halftime
- Score at Trigger: UTA 69 - NOP 61
- Final Score: NOP 156 - UTA 137
- Result: WIN
- Cover Margin vs Line: +22.5 points
- Tags: LIVEFLOW_GHOST_WIN, HALFTIME_OVERREACTION, PACE_FLIP, TRANSITION_EDGE, DEFENSIVE_MISMATCH

## Snapshot
Utah led by 8 at halftime, but the lead profile was fragile. The Jazz were benefiting from strong first-half shotmaking, while New Orleans remained within striking distance despite weaker perimeter efficiency. The live market offered NOP +3.5, creating a comeback spot based on likely shooting normalization and New Orleans' superior interior and transition pressure.

## Trigger Rationale
- Utah first-half three-point efficiency looked overheated relative to game control.
- New Orleans still had a viable paint and transition pathway despite trailing.
- The halftime line overstated Utah control and provided a cushion on the trailing side.
- Ghost bet was logged instead of executed for tracking under LIVE-FLOW protocol.

## Second-Half Outcome Drivers
### New Orleans
- 156 total points
- 57.5% FG
- 14-34 3PT (41.2%)
- 90 points in the paint
- 44 fastbreak points
- 28 points off 17 Utah turnovers
- 48 rebounds and 32 assists

### Utah
- 137 total points
- 51.0% FG
- 10-32 3PT (31.3%)
- 16 turnovers
- Allowed 156 points and 90 paint points
- Could not contain New Orleans once pace and pressure flipped in the second half

## Team Stat Comparison
- Rebounds: NOP 48, UTA 41
- Assists: UTA 38, NOP 32
- Steals: NOP 15, UTA 12
- Blocks: NOP 5, UTA 1
- Fastbreak Points: NOP 44, UTA 22
- Points in Paint: NOP 90, UTA 78
- Points Off Turnovers: NOP 28, UTA 23

## Core Interpretation
This was not strictly a Utah collapse. Utah still scored 137. The real story was that New Orleans possessed the more explosive second-half path through paint attacks, transition scoring, and defensive pressure. The halftime market over-weighted the current score and under-weighted the structural instability of Utah's lead.

## LiveFlow Evaluation
- Edge Quality: Strong
- Trigger Quality: Strong
- Execution Quality: Correct ghost classification
- Estimated Cover Probability at Trigger: 57-59%
- Fair Live Spread Range: NOP +1.5 to +2.0
- Live Number Taken: NOP +3.5
- Estimated Edge: 4-6% cover value
- Mean Projected Final Margin at Trigger: NOP +1.8
- Median Projected Final Margin at Trigger: NOP +2

## Registry Log
- Entry Type: LIVEFLOW
- Classification: LIVEFLOW_GHOST_WIN
- Game: UTA @ NOP
- Bet: NOP +3.5
- Trigger Window: Halftime
- Trigger State: UTA 69 - NOP 61
- Final State: NOP 156 - UTA 137
- Status: Logged for future LIVE-FLOW audit and pattern training

## Takeaway
This was a clean halftime overreaction capture. The trailing side had the more sustainable comeback profile, and the live spread offered enough margin to exploit it. This is the exact type of LIVE-FLOW ghost bet worth preserving in the logbook for future mid-game reversal pattern detection.
