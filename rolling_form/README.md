# Rolling Form Registry

This folder stores rolling-form summaries for SharpEdge postgame analysis.

## Standard windows

- Last 5 games: immediate form and short-term regression detection.
- Last 10 games: stability context and trend confirmation.
- Series-level window: playoff-round matchup pattern detection.

## Required update rule

Every finalized postgame report should update the relevant rolling summary and remove stale games outside the active window.
