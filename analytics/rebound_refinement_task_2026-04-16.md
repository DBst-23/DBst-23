# Rebound Refinement Task — 2026-04-16

## Status
ACTIVE

## Purpose
Use the 2026-04-16 off day to backtest recent rebound plays, classify rebound archetypes, and refine the SharpEdge playoff rebound model before the 2026-04-17 slate.

## Strategic Position
SharpEdge remains committed to the rebound market as a core venture.
This task does **not** represent a lane switch away from rebounds.
Instead, it records a temporary refinement pivot:
- preserve the rebound edge
- isolate weak rebound sub-archetypes
- improve deployment through single-fire execution
- prepare cleaner rebound attacks for the next playoff slate

## Refinement Goals
1. Separate rebound plays by archetype rather than treating all rebound props as one market bucket.
2. Identify which rebound subtypes remain profitable in playoff-style environments.
3. Detect which rebound failures are caused by share dilution, center suppression, wing spike risk, or structure drag.
4. Re-test whether single-fire deployment converts rebound edge more efficiently than bundled card structure.

## Archetype Buckets
- `CENTER_OVER`
- `FORWARD_OVER`
- `WING_UNDER`
- `GUARD_UNDER`
- `CLEAN_SHARE_ENV`
- `CROWDED_SHARE_ENV`
- `CENTER_SHARE_DOMINANT`
- `LONG_REBOUND_ENV`
- `TIGHT_ROTATION`
- `OT_RISK`

## Required Review Set
Backtest and classify recent logged rebound exposures, including:
- MIA @ CHA rebound postmortem sequence
- ORL @ PHI rebound postmortem sequence
- any other recent NBA rebound plays already preserved in GitHub postmortems or analytics logs

## Required Data Points Per Play
- player
- matchup
- line
- over/under
- projected minutes
- actual minutes
- result
- rebound chances if available
- adjusted rebound chance rate if available
- teammate center rebound share
- rebound environment classification
- execution structure (single-fire, straight, 2-pick, 3-pick)
- MPZ tags triggered

## Working Hypotheses
### Hypothesis 1
Elite center rebound overs may remain the strongest playoff rebound subtype due to condensed rotations and more stable board share.

### Hypothesis 2
Forward rebound overs become fragile when:
- same-team center rebound share remains dominant
- scoring burden pulls the forward away from the glass
- 3+ teammates maintain viable 5+ rebound paths

### Hypothesis 3
Wing rebound unders become dangerous when:
- projected minutes are 36+
- game spread implies full closing run
- opponent miss volume is elevated
- weak-side cleanup opportunities remain open

### Hypothesis 4
Single-fire deployment may be the best execution structure for rebound edges even if the rebound lane itself stays active.

## Deliverables Before 2026-04-17 Slate
1. Rebound archetype ranking
2. Temporary playoff rebound filters
3. List of safe rebound attack zones
4. List of red-zone rebound trap profiles
5. Updated execution rule for when a rebound edge must be deployed as single-fire only

## Current Operating Interpretation
The system is **not abandoning rebounds**.
The system is using the off day to refine and sharpen them so the rebound venture can continue with better precision in the playoffs.

## Follow-Up Commands
- `run rebound refinement backtest`
- `rank rebound archetypes`
- `update rebound attack filters`
- `scan 2026-04-17 slate in patched rebound mode`
