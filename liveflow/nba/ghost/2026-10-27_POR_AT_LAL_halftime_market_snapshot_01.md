# SharpEdge LIVE-FLOW — POR @ LAL — William Hill halftime snapshot 01 (2026-10-27)

**Frozen independent model:** `liveflow/nba/ghost/2026-10-27_POR_AT_LAL_halftime_freeze.md`, commit `428176fb7f9ca0e684763d2fcc0816f4dff9ffcc`. **Original official first-half score:** POR 68–LAL 73, total 141.

**CRITICAL discrepancy:** William Hill screenshot displays **POR 68–LAL 75**, total **143**, while the official gamebook supplied for the freeze says POR 68–LAL 73, total **141**. Both UI and report label the moment 'halftime'. The +2 Lakers discrepancy is unresolved, possibly feed adjustment/timing. **Do not claim fully synchronized model-to-book comparison.** Preserve both values and do not silently rebase forecast.

## Screenshot market quotes
| Market | William Hill |
|---|---|
| POR +5.5 | -115 |
| LAL -5.5 | -115 |
| POR ML | +175 |
| LAL ML | -220 |
| Full game Over 254.5 | -115 |
| Full game Under 254.5 | -115 |
| LAL TT Over 128.5 | -120 |
| LAL TT Under 128.5 | -110 |
| POR TT Over 124.5 | -115 |
| POR TT Under 124.5 | -115 |

## Original frozen (at official 68–73) versus screenshot threshold (at 68–75)
| Target | Frozen model | Book | Raw difference (not synchronized) |
|---|---:|---:|---:|
| Total | 256 | 254.5 | +1.5 |
| LAL team | 133 | 128.5 | +4.5 |
| POR team | 123 | 124.5 | -1.5 |
| LAL winning margin | +10 | +5.5 | +4.5 |

Note snapshot market total 254.5 and team-total lines 128.5+124.5=253; lines can diverge because distinct market prices and thresholds. Break-even at -115=53.49%; -120=54.55%; -110=52.38%. These raw differences **are not valid priced edges** because inputs may be at differing score states, model is heuristic with no calibrated probabilities, and snapshot time unknown.

**Disposition: HOLD / PAPER ONLY / quote-score mismatch.** Next authoritative score verification or final postmortem may resolve which half score is correct, but it cannot alter frozen forecast.
