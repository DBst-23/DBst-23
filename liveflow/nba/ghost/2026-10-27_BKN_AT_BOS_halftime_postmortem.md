# SharpEdge NBA LIVE-FLOW postmortem | BKN @ BOS | 2026-10-27

**Classification:** PAPER / no confirmed wager. **Venue:** TD Garden. Source: user-provided official NBA final/regulation/OT gamebook. Independent pre-price forecast frozen at commit `9e454a2`; William Hill halftime screen archived at commit `d6e603e`. No projections changed after the outcome.

## Score chronology
| Stage | BKN | BOS | Total |
|---|---:|---:|---:|
| Q1 | 31 | 26 | 57 |
| Q2 | 30 | 30 | 60 |
| Halftime | 61 | 56 | 117 |
| Q3 | 21 | 30 | 51 |
| Q4 | 35 | 31 | 66 |
| 2H regulation | 56 | 61 | 117 |
| End regulation | 117 | 117 | 234 |
| OT1 | 7 | 8 | 15 |
| **Final** | **124** | **125** | **249** |

## Frozen model vs William Hill vs actual
| Target | Model | WH line | Regulation | Final | Model absolute error at final | WH absolute error at final |
|---|---:|---:|---:|---:|---:|---:|
| Full game total | 236 | 227.5 | 234 | 249 | 13 | 21.5 |
| BKN TT | 117 | 111.5 | 117 | 124 | 7 | 12.5 |
| BOS TT | 119 | 116.5 | 117 | 125 | 6 | 8.5 |
| BOS margin | +2 | +5.5 | 0 | +1 | 1 | 4.5 |

**Regulation comparison:** total projection error 2 vs book 6.5; BKN projection exact (117) vs book 5.5 low; BOS projection 2 high vs book 0.5 low; predicted BOS +2 vs regulation tie. Model projected regulation second-half BKN 56/BOS 63 (119 total), actual 56/61 (117 total), so second-half model total high by 2.

**OT impact:** 15 total points added. Model was closer than book to 249 total by 8.5, although full-game market includes overtime. Do not confuse regulation forecast accuracy with an accurate probability for overtime-inclusive totals.

## William Hill halftime odds and market grading
| Market | Quoted price | Outcome |
|---|---:|---|
| Full-game Over 227.5 | -115 | WIN (249 total, 234 regulation) |
| Full-game Under 227.5 | -115 | LOSS |
| BKN Over 111.5 | -125 | WIN (124 total, 117 regulation) |
| BKN Under 111.5 | -105 | LOSS |
| BOS Over 116.5 | -105 | WIN (125 total, 117 regulation) |
| BOS Under 116.5 | -125 | LOSS |
| BKN +5.5 | -110 | WIN (lost by 1) |
| BOS -5.5 | -120 | LOSS |
| BOS ML | -240 | WIN |
| BKN ML | +185 | LOSS |

Prior research flagged Over 227.5 and BKN Over 111.5 as largest raw discrepancies, also BKN +5.5 and BOS Over 116.5. **Actual decision: MONITOR / PAPER ONLY, with no confirmed ticket or realized P&L.** These are correlated same-game sides, not independently selected live bets.

## Explanatory observations
- BOS shot 2/16 from three in H1 (12.5%), then 9/22 in regulation H2 (40.9%). The anticipated three-point improvement did occur; it was not guaranteed at halftime.
- BKN shot 6/17 (35.3%) from three in H1, then 10/27 (37.0%) in regulation H2. Brooklyn's stable perimeter shooting supported scoring continuation.
- Brooklyn was uneven across Q3 (21) and Q4 (35), even while hitting exactly the projected 56 regulation second-half points.
- Tatum finished 40 points, after 16 at halftime. The final 15-point OT added additional uncertainty not modeled explicitly.
- The forecast was an uncalibrated heuristic, not an independently reproducible simulation. Price-conditioned EV and real market advantage remain unproven.

## Provenance
- Frozen: `liveflow/nba/ghost/2026-10-27_BKN_AT_BOS_halftime_freeze.md`
- Book: `liveflow/nba/ghost/2026-10-27_BKN_AT_BOS_halftime_market_snapshot_01.md`
- Final: user-supplied October 27 NBA official scorer report in this conversation.

**Research status:** postmortem complete; no real wager verified; preserve all original files unchanged.