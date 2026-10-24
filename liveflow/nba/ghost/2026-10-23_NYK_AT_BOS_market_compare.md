# NBA Ghost #002 — NYK @ BOS, October 23 2026 — first sportsbook comparison
## Audit
Pre-book frozen forecast: `liveflow/nba/ghost/2026-10-23_NYK_AT_BOS_halftime_freeze.md`, commit `2c4ea331c417903baa54e2e8867119d188157b9a`. Do NOT modify original forecast.
Snapshot from user-provided sportsbook screenshots: Q3 11:39, NYK 51, BOS 50; halftime baseline was NYK 49, BOS 50. **Market is live 21 seconds after halftime**, not exactly synchronized with frozen halftime timestamp. Two NYK points happened already; no new possessions/parameters assimilated. All prices are **full-game** outcomes, not 2H lines.
Snapshot: NYK +2.5 -125, BOS -2.5 -105; NYK ML +100, BOS ML -130; total Over205.5 -110 / Under205.5 -120; BOS full-game TT Over103.5 -110/Under103.5 -120; NYK TT Over101.5 -120/Under101.5 -110.
## Model
Preserve original 100k exploratory bivariate normal half scoring assumptions from frozen baseline. Replay seed 20261023, 100000 draws, mean NYK final ~102.5, BOS ~105.0, full ~207.5. No conditional in-game adjustment for 21 seconds, so all comparisons indicative and not strictly matched-time quotes. Full-game ML counts here are **regulation only**; ~3.06% modeled regulation draws, so DO NOT use to assign verified full-game moneyline EV without overtime adjustment. No betting recommendation.
| Book market | Price | Frozen-model indicative p | Implied p | Apparent pp diff | Apparent ROI at book | Classification |
|---|---:|---:|---:|---:|---:|---|
| BOS full-game over 103.5 | -110 | 56.235% | 52.381% | +3.854 | +7.36% | GHOST_WATCH_1 |
| Full game over 205.5 | -110 | 55.588% | 52.381% | +3.207 | +6.12% | GHOST_WATCH_2 |
| NYK full-game over 101.5 | -120 | 54.166% | 54.545% | -0.379 | -0.69% | PASS |
| BOS -2.5 full game | -105 | 50.175% | 51.220% | -1.045 | -2.04% | PASS |
| NYK +2.5 full game | -125 | 49.825% | 55.556% | -5.731 | -10.32% | PASS |
| NYK ML +100 | +100 | 40.477% regulation-only | 50.000% | N/A | N/A | PASS_UNADJUSTED_ML |
| BOS ML -130 | -130 | 56.462% regulation-only | 56.522% | N/A | N/A | PASS_UNADJUSTED_ML |
Notes: Boston TT over and full-game over are positively correlated. 1-2 apparent advantages are weak relative to uncalibrated model error. No independent confirmation, zero real money and zero stakes. Set `paper_only:true`.
## Further QC
- Explicit screenshot Q3 11:39, NYK 51/BOS 50; 2 points after halftime. Need market-timestamp adjustment to build a proper price-driven model in future.
- Next outcome grading ONLY after final report. Collect error by team/total/spread and grade ghost selections as baseline observations, not proof of long-run profitability.
