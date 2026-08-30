# WNBA LIVE-FLOW Market-Blind Halftime Projection — Toronto Tempo at Phoenix Mercury

- Date: 2026-08-29
- Checkpoint: Halftime
- Venue: Mortgage Matchup Center, Phoenix, AZ
- Halftime score: Phoenix 58, Toronto 35
- Halftime total: 93
- Market status: NOT YET REVEALED
- Projection status: FROZEN BEFORE MARKET

## SharpEdge Market-Blind Projection

### Full game
- Phoenix Mercury: 101
- Toronto Tempo: 75
- Projected final total: 176
- Projected final margin: Phoenix -26

### Second half
- Phoenix Mercury: 43
- Toronto Tempo: 40
- Projected second-half total: 83
- Projected second-half spread: Phoenix -3

## Distribution Bands

### Full-game total
- Fair center: 176
- Working fair range: 169 to 183

### Team totals
- Phoenix fair center: 101
- Toronto fair center: 75

## Halftime Diagnosis

Phoenix's 58 first-half points were materially inflated by 58.8% three-point shooting, 52.5% overall shooting, 20 fast-break points, and Toronto's 10 turnovers. Those drivers are not projected to repeat at first-half intensity.

Toronto's 35-point half was dragged down by 22.2% three-point shooting and 10 turnovers. Some scoring recovery is projected, but roster absences and the current offensive structure cap the ceiling.

The strongest expectation is therefore asymmetric regression: Phoenix down from an extreme offensive first half, Toronto modestly up, with the combined second half remaining in the low-80s rather than repeating the 93-point first half.

## Key LIVE-FLOW Tags
- MARKET_BLIND_PROJECTION_FROZEN
- LIVEFLOW_HALFTIME_REGIME_CONFIRMATION_v1
- ASYMMETRIC_REGRESSION_DISTRIBUTION_v1
- TEAM_ALLOCATION_ERROR_TRACKING_v1
- PHX_3P_REGRESSION_DOWN_STRONG
- PHX_TRANSITION_SCORING_REGRESSION_DOWN
- TOR_TURNOVER_REGRESSION_UP
- TOR_3P_REGRESSION_UP_MODEST
- BLOWOUT_GAME_STATE_VOLATILITY
- GARBAGE_TIME_SCORING_RISK

```yaml
game_id: WNBA_2026-08-29_TOR_PHO
checkpoint: halftime
score_at_checkpoint:
  TOR: 35
  PHO: 58
halftime_total: 93
market_revealed: false
frozen_projection:
  TOR_final: 75
  PHO_final: 101
  full_game_total: 176
  PHO_margin: 26
second_half_projection:
  TOR: 40
  PHO: 43
  total: 83
  PHO_margin: 3
working_total_range:
  low: 169
  high: 183
status: FROZEN
```
