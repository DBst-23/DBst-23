# WNBA LIVE-FLOW Checkpoint — Seattle Storm at Golden State Valkyries

## Status
**CLOSED — graded WIN**

Final postmortem: `postmortems/wnba/WNBA_LIVEFLOW_POSTMORTEM_SEA_GS_2026-09-19.md`

## Market-Blind Freeze
- Date: 2026-09-19
- Checkpoint: End of 3rd Quarter
- Score: Golden State 64, Seattle 46
- Market viewed before projection: NO

## End-3Q Read
Golden State: 64 points through three quarters. Quarter scoring: 21, 28, 15.

Seattle: 46 points through three quarters. Quarter scoring: 19, 6, 21.

Structural notes:
- Golden State built a 24-point halftime lead, then cooled to 15 points in Q3.
- Seattle rebounded from a 6-point Q2 with 21 points in Q3, so the second-half environment was materially different from the first-half collapse.
- Golden State still led by 18 entering Q4, creating meaningful blowout/rotation suppression risk.
- The aggregate total had largely converged toward SharpEdge's fair number, while the team-allocation layer still showed separation.
- Because both team-total under angles were driven by the same low-Q4/blowout-decay thesis, stacking correlated exposures was not preferred.

## Frozen SharpEdge Projection
### Fourth Quarter
- Golden State: 23
- Seattle: 14
- Q4 total: 37

### Full Game
- Golden State: 87
- Seattle: 60
- Full-game total: 147
- Full-game margin: Golden State +27

## SharpEdge Fair Lines
- Spread: Golden State -27.5
- Full-game total: 146.5
- Golden State team total: 87.0
- Seattle team total: 59.5

## Market Snapshot
### Game Markets
- Golden State -18.5
- Seattle +18.5
- Full-game total: 145.5

### Team Totals
- Golden State 90.5
- Seattle 65.5

## Model vs Market
| Market | SharpEdge | Market | Separation | LIVE-FLOW Read |
|---|---:|---:|---:|---|
| Spread | GS -27.5 | GS -18.5 | 9.0 pts | GS side value, but not primary expression |
| Full total | 146.5 | 145.5 | 1.0 pt | PASS / market aligned |
| Golden State TT | 87.0 | 90.5 | 3.5 pts | UNDER lean |
| Seattle TT | 59.5 | 65.5 | 6.0 pts | UNDER lean, higher raw separation but more garbage-time variance |

## Strike Hierarchy
### Primary execution: Golden State TT Under 90.5
Golden State had 64 entering Q4 and needed 27+ fourth-quarter points to clear 90.5. SharpEdge projected approximately 23 fourth-quarter points and 87 final, creating a 3.5-point team-total cushion.

### Secondary read: Seattle TT Under 65.5
Seattle needed 20+ fourth-quarter points to clear 65.5. SharpEdge projected approximately 14, creating the larger raw model-market gap. It ranked behind the Golden State under because Seattle's Q3 rebound and garbage-time scoring variance increased uncertainty.

### Pass: Full-game total 145.5
SharpEdge's frozen total was approximately 146.5, too close to market for a clean strike.

## Locked Position
- Platform: Kalshi
- Contract: **No · Golden State over 90.5 points scored**
- Equivalent sports-betting expression: **Golden State Valkyries team total UNDER 90.5**
- Displayed market probability at entry: 99%
- Cost: $9.60
- Max payout shown at entry: $9.69
- Execution status: 🔒 LOCKED IN

## Final Grade
- Final score: Golden State 70, Seattle 57
- Golden State final points: 70
- Ticket: **WIN**
- Paid out: $9.69
- Profit: +$0.09
- ROI: +0.94%
- Under cushion: 20.5 points
- Frozen GS projection error: -17 points
- Frozen full-total projection error: -20 points
- Primary calibration lesson: blowout-scoring lower tail remained too weak.

## Risk / Correlation Note
Do not treat the Seattle TT under and Golden State TT under as independent edges. Both are materially driven by the same low-Q4 scoring / blowout-decay regime. One position is the preferred expression unless a separately validated, non-correlated signal appears.

```yaml
game_id: WNBA_2026-09-19_SEA_GS
checkpoint: end_3q
score_at_checkpoint:
  SEA: 46
  GS: 64
market_seen_before_projection: false
model:
  q4:
    SEA: 14
    GS: 23
    total: 37
  final:
    SEA: 60
    GS: 87
    total: 147
    margin: GS_27
fair_lines:
  spread: GS_-27.5
  total: 146.5
  gs_tt: 87.0
  sea_tt: 59.5
market:
  spread: GS_-18.5
  total: 145.5
  gs_tt: 90.5
  sea_tt: 65.5
execution:
  platform: Kalshi
  contract: NO_GS_OVER_90.5
  equivalent_market: GS_TT_UNDER_90.5
  displayed_market_probability_pct: 99
  cost_usd: 9.60
  payout_usd: 9.69
  profit_usd: 0.09
  roi_pct: 0.94
  result: WIN
final:
  SEA: 57
  GS: 70
  total: 127
status: CLOSED_WIN
```
