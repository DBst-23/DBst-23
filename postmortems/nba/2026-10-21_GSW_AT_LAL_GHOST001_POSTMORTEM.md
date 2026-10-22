# NBA 2026-27 LIVE-FLOW GHOST #001 — GSW @ LAL Postmortem
**Game:** 2026-10-21 GSW @ LAL, Crypto.com Arena, Los Angeles.
**Mode:** PAPER ONLY — 0 dollars wagered.
**Sources:** User-supplied NBA official scorer's final/half/quarter box scores and play-by-play; frozen pre-market forecast `liveflow/nba/ghost/2026-10-21_GSW_AT_LAL_halftime_freeze.md` (commit `b0e6dac`); price snapshot `liveflow/nba/ghost/2026-10-21_GSW_AT_LAL_halftime_market_compare.md` (commit `fc779b1`). Data-quality note: some previously supplied halftime lines differed slightly in assists/turnover presentation, so final official first-half and final box are canonical. No final data was used to change the original forecast.

## Result and exact forecast errors
| Metric | Frozen mean | Actual | Actual minus projected |
|---|---:|---:|---:|
| GSW second-half points | 56.0 | 53 | -3.0 |
| LAL second-half points | 58.5 | 61 | +2.5 |
| Second-half combined | 114.5 | 114 | -0.5 |
| GSW final points | 108 | 105 | -3 |
| LAL final points | 124.5 | 127 | +2.5 |
| Final total | 232.5 | 232 | -0.5 |
| LAL final winning margin | 16.5 | 22 | +5.5 |
| LAL second-half winning margin | 2.5 | 8 | +5.5 |

Quarter scores: GSW 33,19,16,37; LAL 34,32,36,25. At 3Q LAL led 102-68 (34 points), making Q4 fundamentally garbage-time dominated. LAL largest lead 35. GSW made 3/18 threes in second half; Lakers 5/14. LAL second-half eFG = (22+0.5*5)/43=56.98%; GSW=(18+0.5*3)/44=44.32%.

## Frozen ghost picks: outcomes, pricing, calibration
| Market | Odds snapshot | Frozen model p | Implied p | Actual | Result |
|---|---:|---:|---:|---|---|
| GSW full-game TT UNDER 111.5 | -105 | 65.9% | 51.22% | GSW 105 | HIT (by 6.5 points) |
| Full-game UNDER 236.5 | -110 | 62.3% | 52.38% | Combined 232 | HIT (by 4.5 points) |
| LAL full-game -13.5 | -120 | 59.8% | 54.55% | LAL win by 22 | HIT (8.5-point clearance) |
Three out of three ghost outcomes won. Counterfactual flat $1 risk each: profits +0.95238, +0.90909, +0.83333 => +2.69481 units / 3 units risk = +89.83% *illustrative only, not actual realized ROI*. They are **correlated**, based on one game, and are no basis for promoting probability accuracy. Do not claim any bankroll gain.

## Core game script
- First half LAL 66-52: LAL 24/38 FG (63.2%) with Walker Kessler 7/7 and Luka 23, Curry 20; GSW Q2 19.
- Third quarter: LAL 36-16; GSW 5/17 FG, 0/8 3PT and 9 turnovers. 14-point halftime lead became 34.
- Fourth quarter: GSW 37-25, but lineups replaced major stars: Curry and Luka both 0 Q4 minutes, while GSW's Will Richard/Graham Ike/LJ Cryer/Malevy Leons played 12/12/8:57/8:57. High garbage-time points after game outcome was functionally secure.
- Lakers 46/81 FG 56.8%, Kessler 12/12 for 26; Luka 28 in 29:42, Reaves 23. Warriors 38/92 FG 41.3%, 8/36 3PT; Curry 23 in only 21:11, including 0 4Q.
- Foul/rim/rotation factors: Draymond 3 first-half fouls, finished 21:11; opening-night injuries from user data; Lakers 66 paint points v GSW 56.
- The halftime model predicted net total exceptionally well (-0.5 error), but missed the *composition*: underprojected LA by 2.5 while overprojecting GSW by 3.0. End-game points are heavily nonstationary from 34-point lead/bench rotations.

## Keep / Modify / Revert (evidence from ONE game: Tier 0, provisional ONLY)
| Component | Decision | Why |
|---|---|---|
| Timestamped pre-market frozen forecast + price compare | KEEP | Allows auditable no-lookahead grading |
| Full-game total central estimate | KEEP FOR TESTING | 232.5 vs 232, but accuracy can be luck in one game |
| GSW offensive suppression risk | KEEP AS HYPOTHESIS | GSW 16 Q3; 21:11 Curry minutes and 8/36 team 3PT |
| Lakers blanket hot-shooting fade | MODIFY | Lakers 51.2% second-half FG and Kessler 12/12 overall; paint quality supported shooting |
| 2H single normal scoring distribution | MODIFY | Q3 52 combined vs Q4 62, major structural rotation switch |
| GSW automatic positive 3PT regression | MODIFY | 27.8% 1H 3PT fell to 16.7% 2H; no auto-reversion |
| Competitive-game minutes based on halftime starters | MODIFY | Curry and Luka were shut down by Q4 |
| Independent tracking of 2 correlated unders | KEEP reporting, REVERT independent-signal assumption | Overlapping outcome drivers; never count as 2 independent validations |
| Immediate policy promotion from 3-for-3 | REVERT | 1 event; minimum_sample_threshold_framework Tier 0 (<4) |

## Data quality and analytical safeguards
- Pregame first-half included 118 points; final 232, second-half 114.
- The original ghosts are full-game bets, not second-half-only markets.
- Live-flow probability outputs came from manually chosen normal-means/SDs, not calibrated backtests. Grade observed forecasts, but do not label the model as proven.
- **Change proposals**: introduce score-margin-dependent substitution state, garbage-time probability (margin/time), star_minutes_gate, 3P uncertainty conditional on personnel, role-specific paint efficiency, third-quarter check/override, and overdispersion for garbage-time points.
- Future test: compare a basic halftime baseline, Vegas implied halftime live totals, and revised LiveFlow on out-of-sample games using MAE, RMSE, Brier score/log loss, and calibration by margin bands. No retroactive editing of frozen inputs.

## Final
**Ghost record:** 3-0 (0 real bets); correlation-adjusted independent count: not 3. **PATCH OVERALL: MODIFY.** Label as `SAMPLE_TIER_0`. Preserve frozen forecasts and quote timestamps; use next game as another out-of-sample paper observation.