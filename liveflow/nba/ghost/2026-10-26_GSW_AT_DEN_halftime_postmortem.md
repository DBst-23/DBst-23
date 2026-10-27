# SharpEdge NBA LIVE-FLOW — GSW @ DEN halftime postmortem
**Date:** 2026-10-26 | **Venue:** Ball Arena, Denver | **Mode:** retrospective / paper-only; actual wager not documented.
**Source of truth:** user-provided official NBA first-half and final scorer's reports, Q1-Q4 reports/play-by-play; William Hill screenshot supplied in conversation. No external odds were fetched. Forecast and odds below preserve the *prior conversation* values rather than recalibrating after the result.

## Period reconstruction
| Period | GSW | DEN | Total |
|---|---:|---:|---:|
| Q1 | 28 | 32 | 60 |
| Q2 | 32 | 24 | 56 |
| Halftime | 60 | 56 | 116 |
| Q3 | 40 | 28 | 68 |
| Q4 | 34 | 30 | 64 |
| Second half | 74 | 58 | 132 |
| Final | **134** | **114** | **248** |

GSW won by 20. The halftime model predicted DEN winning; actual result and margin diverged substantially.

## Original halftime SharpEdge projection — unchanged, *heuristic and uncalibrated*
| Metric | Predicted | Actual | Actual minus prediction |
|---|---:|---:|---:|
| GSW full-game points | 114.0 | 134 | +20.0 |
| DEN full-game points | 116.0 | 114 | -2.0 |
| Full-game total | 230.0 | 248 | +18.0 |
| GSW second-half points | 54.0 | 74 | +20.0 |
| DEN second-half points | 60.0 | 58 | -2.0 |
| Second-half combined | 114.0 | 132 | +18.0 |
| DEN margin (from team totals) | +2.0 | -20 | -22.0 |

**Model inconsistencies in prior response:** It separately reported DEN -1.0 and DEN ML -127/+127, and 55.9% DEN win; the projected team totals (DEN 116, GSW 114) mathematically imply DEN -2, not -1. The original 100,000-simulation claim/interval was not backed by a preserved reproducible run, seed or file: treat listed probability/EV as **unverified illustrative outputs**, not an audited simulation. Do not retrofit a new model to claim predictive success.

## William Hill halftime market snapshot and settled outcomes
Original screenshot: GSW 60, DEN 56; full-game GSW +2.5 (-115), DEN -2.5 (-115), GSW ML +120, DEN ML -150, Over 237.5 (-125), Under 237.5 (-105); GSW TT 117.5 Over -125 / Under -105; DEN TT 119.5 Over -125 / Under -105.

| Market / side | Price | Settlement | Result | Net hypothetical $100 stake |
|---|---:|---|---|---:|
| Full-game UNDER 237.5 | -105 | 248 | LOSS | -$100.00 |
| Full-game OVER 237.5 | -125 | 248 | WIN | +$80.00 |
| GSW TT UNDER 117.5 | -105 | GSW 134 | LOSS | -$100.00 |
| GSW TT OVER 117.5 | -125 | GSW 134 | WIN | +$80.00 |
| DEN TT UNDER 119.5 | -105 | DEN 114 | WIN | +$95.24 |
| DEN TT OVER 119.5 | -125 | DEN 114 | LOSS | -$100.00 |
| GSW +2.5 | -115 | GSW wins by 20 | WIN | +$86.96 |
| DEN -2.5 | -115 | DEN loses by 20 | LOSS | -$100.00 |
| GSW moneyline | +120 | GSW wins | WIN | +$120.00 |
| DEN moneyline | -150 | DEN loses | LOSS | -$100.00 |

No bet slip or staking confirmation recorded, so **no actual P&L/ROI or bankroll change**. Do not aggregate hypothetical sides as independent bets.

**Market errors:** WH 237.5 understated final 248 by 10.5; SharpEdge 230 understated by 18 (market closer by 7.5). WH GSW 117.5 understated 134 by 16.5; SharpEdge GSW 114 understated by 20 (market closer by 3.5). WH DEN 119.5 overstated 114 by 5.5; SharpEdge DEN 116 overstated by 2 (model closer by 3.5). DEN -2.5 missed actual DEN margin -20 by 22.5.

## Why the primary signal failed
1. **GSW did not regress as expected.** GSW 1H 12/25 from three = 48%; 2H 10/19 = 52.6%; final 22/44 = 50%. Blanket shooting regression was erroneous for this game. GSW added 74 second-half points versus the forecast 54.
2. **Stephen Curry's low first-half shot volume was a major missed upside scenario.** At half Curry 3 points on 1/1 FG in 14:20; then 21 second-half points on 7/7 FG, 2/2 threes and 5/5 FT in 12:14. This changed both team projection and matchup trajectory.
3. **Third-quarter breakaway preceded late-game rotation effects.** GSW Q3 40 vs DEN 28, growing the lead to 16. Q4 34-30, final +20. Late benches entered at ~2:46 in Q4, so both starter-driven and reserve-driven scoring matter.
4. **Foul/rotation disruption:** Aaron Gordon received two technical fouls and was ejected with 8:34 remaining in Q4; do not use this *post-halftime unknown event* to rationalize the original forecast retroactively.
5. **DEN had no expected broad 3-point rebound:** Denver 1H 5/16 (31.2%) and 2H 5/13 (38.5%), but managed only 58 second-half points. DEN overall scoring prediction (60) was close while Golden State error drove the total miss.

## Signal accounting and corrective control
- Previous assistant classified UNDER 237.5 as its strongest provisional discrepancy and cited 68.8% win probability/+34.3% estimated EV at -105: **FAILED**. GSW UNDER 117.5 (claimed 63.6%/+24.2%) **FAILED**. DEN UNDER 119.5 (claimed 62.8%/+22.8%) **WON**. These probabilities were not independently verifiable/calibrated.
- **Primary ghost-card benchmark: 1/3 directional unders, correlated outcomes, zero documented real wagers**. This tally is illustrative only; avoid interpreting this as bankroll results or statistically meaningful hit rate.
- Formal patch candidates: model 3PT persistence alongside regression; create Curry / star usage and second-half minutes distribution; condition scoring variance on 3PA rate and trailing/leading scripts; timestamp exact books' odds; include ejection/injury contingency; store executable MC seed, assumptions and quantiles; audit model fair spread consistency against projected team scores.
- **Status:** POSTMORTEM COMPLETE / RESEARCH ONLY. No ex-post correction to halftime model. No model deployment promotion off one game.
