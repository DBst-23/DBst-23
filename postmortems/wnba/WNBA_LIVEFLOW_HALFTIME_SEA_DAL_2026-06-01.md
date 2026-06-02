# WNBA LiveFlow Halftime Postmortem/Decision Log

**Game:** Seattle Storm @ Dallas Wings  
**Date:** 2026-06-01  
**Venue:** College Park Center, Arlington, TX  
**Score at Halftime:** Dallas 36, Seattle 25  
**Live Market Snapshot:** Dallas -14.5 (-155), Seattle +14.5 (+123), Total 154.5; No/Under 154.5 -1430, Yes/Over +684  
**Mode:** LIVEFLOW_STRIPPED_MODE_ACTIVE

## Halftime State

Seattle scored 25 first-half points with poor perimeter efficiency and low shot creation:

- Seattle FG: 9/29, 31.0%
- Seattle 3PT: 0/10, 0.0%
- Seattle assists: 5
- Seattle turnovers: 7
- Seattle Q1/Q2 scoring: 10, 15

Dallas led 36-25 despite inefficient shooting because of possession and glass control:

- Dallas FG: 15/44, 34.1%
- Dallas 3PT: 3/14, 21.4%
- Dallas offensive rebounds: 9
- Dallas total rebounds: 25
- Dallas second-chance points: 16
- Dallas points in paint: 22

## Market Assessment

The live total at 154.5 was still anchored high relative to only 61 first-half points. Directionally, the under/no-over read is correct, but the displayed price already absorbed the edge.

## Engine Tags Triggered

```yaml
LIVE_TOTAL_COLLAPSE_MISPRICE:
  status: PARTIAL_TRIGGER
  halftime_lead: 11
  trailing_team_q2_points: 15
  trailing_team_fg_pct: 31.0
  trailing_team_3pt_pct: 0.0
  live_total: 154.5
  note: "Total was directionally high relative to first-half output, but halftime lead did not reach 15-point trigger and market price was too juiced."

PREGAME_TOTAL_ANCHOR_FAILURE:
  status: WATCHLIST_TRIGGER
  description: "Live total still inflated against a 61-point first half and Seattle offensive suppression."
```

## Decision

**No bet at displayed price.**  
The correct strategic read is under/no-over, but -1430 is beyond threshold and offers no practical bankroll edge.

## Live Projection

```yaml
projected_final_total:
  mean: 139.5
  median: 138
  range: 130-150

projected_margin:
  Dallas_by:
    mean: 10.5
    median: 11

market_edges:
  no_over_154_5:
    true_probability_estimate: 0.90
    playable_price_threshold: "Do not play above -250"
    displayed_price: -1430
    action: PASS
  seattle_team_total_under:
    status: preferred_if_available
  third_quarter_under:
    status: secondary_if_reasonable_price
```

## Workflow Note

This game is a restraint example: even when the model identifies the right direction, the bet is rejected if the market price is beyond threshold.
