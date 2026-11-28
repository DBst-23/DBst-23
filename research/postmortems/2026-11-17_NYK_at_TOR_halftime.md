# SharpEdge B.003 — NYK @ TOR halftime postmortem

**Game:** 2026-11-17, New York Knicks at Toronto Raptors, Scotiabank Arena. **Status:** paper-only; user-supplied official scorer's report and halftime sportsbook screenshots. No paid API request or wager confirmed.

## Frozen halftime checkpoint
- Halftime: NYK 54, TOR 50 (104 combined; NYK +4).
- Captured screenshot (capture timestamp/book ID not verified): full game total 209.5 O/U -115/-115; NYK -5.5 -105, TOR +5.5 -125; NYK ML -210, TOR ML +165; NYK team total 107.5 O -105/U -125; TOR team total 102.5 O -105/U -125.
- Previously stated SharpEdge point forecasts (not a recorded executable simulation): full game 213; NYK 110; TOR 103; NYK margin +7; 2H total 109. Previous response assumed 2H SD=15 and quoted illustrative probabilities/EV; those were **not calibrated or validated**.

## Official outcome
| Period | NYK | TOR | Combined |
|---|---:|---:|---:|
| Q1 | 23 | 29 | 52 |
| Q2 | 31 | 21 | 52 |
| Q3 | 26 | 33 | 59 |
| Q4 | 31 | 19 | 50 |
| First half | 54 | 50 | 104 |
| Second half | 57 | 52 | 109 |
| Final | 111 | 102 | 213 |

Final NYK +9. Second-half NYK +5. NYK shot 19/35 (54.3%) FG, 6/14 (42.9%) 3P, 13/13 FT after halftime. TOR 18/36 (50%) FG, 9/18 (50%) 3P, 7/12 FT after halftime. TOR scored 33 in Q3 but 19 in Q4; NYK 26 and 31. Brunson scored 21 second-half points, 31 overall; Towns 16 rebounds, 8 assists overall; Walter 25 points with 7/12 3P overall.

## Forecast accuracy (point forecasts)
| Variable | Frozen forecast | Actual | Forecast minus actual | Absolute error |
|---|---:|---:|---:|---:|
| Full game total | 213 | 213 | 0 | 0 |
| NYK full game points | 110 | 111 | -1 | 1 |
| TOR full game points | 103 | 102 | +1 | 1 |
| NYK final margin | +7 | +9 | -2 | 2 |
| Second-half combined | 109 | 109 | 0 | 0 |

Across the five *correlated* forecast quantities: mean absolute error 0.8, median absolute error 1; not an independent-sample model accuracy metric. One-game sample is not evidence of predictive edge. The 213 total forecast equals the sum of 110+103, and second-half total is derived from 213-104.

## Halftime sportsbook outcomes (hypothetical only)
- Over 209.5 (-115): **WIN**, final 213, +3.5 vs line; net +0.8696 units per 1 unit risked.
- NYK over 107.5 (-105): **WIN**, 111, +3.5 vs line; net +0.9524 units.
- TOR over 102.5 (-105): **LOSS**, 102, -0.5 vs line; net -1 unit.
- NYK -5.5 (-105): **WIN**, margin +9, +3.5 vs line; net +0.9524 units.
- NYK moneyline (-210): **WIN**, +0.4762 units.
- TOR under 102.5 (-125): **WIN**, 102, +0.5 vs line; was not a recommended play.
- Under 209.5 (-115), TOR +5.5 (-125), TOR ML (+165), NYK under 107.5 (-125): losses.
- No tickets or stake evidence provided: **record hypothetical settlement only**, realized P&L = not available. Do not sum overlapping markets as independent bets.

## Diagnostic
- Forecast aligned exactly with final combined total and second-half combined points, but this is a single result with correlated targets; no validated probability calibration or positive expected value established.
- Q3 produced 59 points (TOR 33, NYK 26), Q4 50 (NYK 31, TOR 19). Quarter-level swings were large despite an accurate 2H aggregate forecast.
- At Q2 end, NYK led 54-50; Q3 TOR surged to 83-80; NYK recovered with 31-19 Q4. A full-game line may win while a halftime live-flow directional assumption experiences significant intra-half reversal.
- TOR 9/18 second-half threes (50%), NYK 6/14 (42.9%); efficiency variance remains important. Toronto's Q4 0 FTA and 19 points contrasted with Q3 12 FTA and 33 points.
- Official first-half scorer's report shows NYK 8 offensive rebounds and TOR 4, consistent with the original possession-advantage observation. Final NYK 12 offensive rebounds vs TOR 5.
- No verified licensed Q2-end/Q3-start timestamp, provider event ID, odds capture timestamp, bookmaker ID, or validated executable simulation. **training_eligible=false; tier_1_approved=false**.

## Next validation
Keep this record as an immutable manual halftime checkpoint. For future games persist licensed halftime clocks, timestamped odds, frozen model distribution, calibrated probability, and paper settlement before assessing CLV/ROI. No paid calls enabled.
