# SharpEdge Platform Execution Note — California Singles Constraint

**Date logged:** 2026-04-28

## Key Constraint

Kalshi is currently the only platform identified in the user's California-accessible betting workflow that supports true single-position execution.

Underdog-style entries generally force multi-leg construction, which changes the execution profile from pure edge capture into structure-dependent payout hunting.

## Operational Impact

The 2026 YTD audit showed:

- Singles are profitable and structurally cleaner.
- Two-leg cards are the major EV leak.
- Boosted multi-leg cards can be profitable, but only when tightly filtered.
- Rebound-heavy multi-leg cards require stricter detector approval.

Because single-bet execution is limited mostly to Kalshi, SharpEdge needs two separate execution tracks:

## Track A — Kalshi Single-Fire Mode

Use Kalshi for:

- Single gameline edges
- Single team total edges
- Single spread/total exposures
- LiveFlow stripped entries
- Smaller, repeatable EV capture

Default rule:

```text
If a clean single exists on Kalshi and the model edge is valid, prioritize Kalshi over forced multi-leg construction.
```

## Track B — Underdog Forced-Card Mode

Use Underdog only when:

- A boost is active, or
- Two or more legs independently clear detector thresholds, or
- A gameline anchor plus one strong player prop creates a clean 2-leg build.

Default rule:

```text
Do not force a second leg just to access the market.
```

## Updated Execution Patch

1. Kalshi becomes the preferred platform for single-position edges in California.
2. Underdog two-leg cards require both legs to clear 58%+ projected probability or detector approval.
3. Rebound props cannot be used as filler legs.
4. If only one strong edge exists and no Kalshi equivalent is available, pass rather than force a parlay.
5. Boosts remain useful, but only when the underlying legs are model-valid.

## Model Tag

`CA_SINGLE_ACCESS_CONSTRAINT_V1`

## Summary

This constraint explains why some model-positive edges have been forced into two-leg or three-leg structures. Going forward, platform availability must be logged as part of edge evaluation so the system separates true model edge from execution friction.