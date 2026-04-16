# SharpEdge MPZ Frequency Tracker

## Purpose
Track recurring miss and hit patterns across logged NBA postmortems so the system can identify repeated failure clusters and prioritize model patches.

## MPZ Frequency Table

| Tag | Category | Count | Last Seen | Severity | Notes |
|-----|----------|-------|-----------|----------|-------|
| SINGLE_FIRE_SUCCESS | Hit Pattern | 1 | 2026-04-15 | High | Kalshi single-fire validated as cleanest structure |
| EDGE_CALL_ACTIVE | Hit Pattern | 1 | 2026-04-15 | High | Confirmed on Maxey 3PM read |
| CENTER_SHARE_SUPPRESSION | Miss Pattern | 1 | 2026-04-15 | High | Paolo rebound over failed due to center rebound share concentration |
| WING_REBOUND_SPIKE | Miss Pattern | 1 | 2026-04-15 | High | Edgecombe rebound under failed due to expanded rebound role |
| REBOUND_CONCENTRATION_FAIL | Miss Pattern | 1 | 2026-04-15 | Medium | Forward rebound over failed from diluted team board share |
| CARD_STRUCTURE_DRAG | Structural | 1 | 2026-04-15 | High | Correct edge buried inside card structure |
| MULTI_LEG_STRUCTURE_PUNISH | Structural | 1 | 2026-04-15 | High | Realized ROI suppressed by bundled-card format |

## Current Read

### Strongest Positive Pattern
- `SINGLE_FIRE_SUCCESS`
- `EDGE_CALL_ACTIVE`

These indicate the model can identify isolated edge correctly, especially in single-fire execution environments.

### Strongest Negative Pattern
- `CENTER_SHARE_SUPPRESSION`
- `WING_REBOUND_SPIKE`

These indicate current rebound modeling is most fragile in:
- forward rebound overs when center share remains dominant
- wing rebound unders when minutes are stable and game flow supports crash opportunities

## Patch Priority Queue

### Priority 1
- WING_REBOUND_SPIKE_GUARD
- REBOUND_CONCENTRATION_FILTER
- SINGLE_FIRE_PRIORITY

### Priority 2
- Structure drag suppression in multi-leg cards
- Market/structure split logging for all future 3PM wins inside losing cards

## Tracker Rules
1. Add every MPZ tag from each postmortem.
2. Increase count on recurring tags.
3. Update `Last Seen` with latest date.
4. Escalate severity when the same miss tag appears in back-to-back postmortems.
5. Promote high-frequency miss tags into live system patch queue.

## Next Build Step
- Link MPZ tag counts directly into ROI + hit rate module.
- Build sport-specific MPZ trackers after NBA template proves stable.
