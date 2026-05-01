# NBA LiveFlow Log — BOS @ PHI Game 6

**Date:** 2026-04-30  
**Mode:** LIVEFLOW_STRIPPED_MODE_ACTIVE  
**Game:** Boston Celtics @ Philadelphia 76ers  
**Snapshot Score:** PHI 74 — BOS 59  
**Live Total:** 133  
**Market Snapshot:** Full Game Total 209.5, Over +113 / Under -137  
**Spread Snapshot:** PHI -8.5 -126 / BOS +8.5 +105  

---

## Team State

| Team | PTS | FG | 3PT | FT | REB | OREB | AST | STL | BLK | TOV | Fastbreak | Paint | 2nd Chance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| BOS | 59 | 21-47 / 44.7% | 8-20 / 40.0% | 7-13 / 53.8% | 27 | 1 | 11 | 3 | 3 | 12 | 10 | 22 | 0 |
| PHI | 74 | 27-60 / 45.0% | 10-23 / 43.5% | 10-11 / 90.9% | 29 | 7 | 14 | 6 | 3 | 5 | 15 | 28 | 6 |

---

## Possession / Script Drivers

- PHI leads by 15 with strong turnover edge: BOS 12 TOV, PHI 5 TOV.
- PHI has +6 OREB margin: PHI 7 OREB, BOS 1 OREB.
- Combined 25 fastbreak points indicates pace leakage and live-ball event creation.
- BOS still shooting efficiently enough from three: 8-20 / 40.0%.
- PHI efficiency is stable: 45.0% FG, 43.5% 3PT, 90.9% FT.
- Current total requires 77 more points to clear 209.5.

---

## Player State

### Boston

| Player | MIN | PTS | REB | AST | TOV | PF | FG | 3PT | FT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Jayson Tatum | 25 | 17 | 10 | 3 | 3 | 1 | 6-12 | 2-5 | 3-5 |
| Jaylen Brown | 19 | 16 | 1 | 2 | 4 | 4 | 6-11 | 2-3 | 2-6 |
| Derrick White | 24 | 11 | 1 | 1 | 2 | 2 | 3-6 | 3-4 | 2-2 |
| Neemias Queta | 16 | 2 | 8 | 0 | 1 | 3 | 1-4 | 0-0 | 0-0 |
| Sam Hauser | 16 | 5 | 2 | 1 | 0 | 0 | 2-4 | 1-3 | 0-0 |

### Philadelphia

| Player | MIN | PTS | REB | AST | TOV | PF | FG | 3PT | FT |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Tyrese Maxey | 26 | 21 | 2 | 3 | 0 | 1 | 8-15 | 3-3 | 2-2 |
| Paul George | 25 | 17 | 2 | 3 | 2 | 0 | 5-10 | 5-8 | 2-2 |
| Joel Embiid | 22 | 13 | 7 | 5 | 1 | 2 | 4-13 | 1-4 | 4-5 |
| Kelly Oubre Jr. | 27 | 11 | 8 | 1 | 2 | 2 | 5-9 | 1-3 | 0-0 |
| VJ Edgecombe | 23 | 8 | 3 | 2 | 0 | 2 | 3-7 | 0-3 | 2-2 |

---

## LiveFlow Decision

**Primary Single-Fire Candidate:** Over 209.5 +113  
**Model Mean Range:** 214.5–217.5  
**Model Median Range:** 212.5–215.0  
**Estimated Win Probability:** 59–62%  
**Edge vs Market:** +5 to +8 points from current line  
**Fair Price Band:** roughly -144 to -163  
**Risk Tags:** PHI_CLOCK_BLEED_RISK, BOS_TURNOVER_VOLATILITY, BLOWOUT_SUPPRESSION_RISK, LIVE_BALL_PACE_SUPPORT

**Decision:** Single-fire live edge. Do not pair with correlated over exposure unless line drops materially or pace re-confirms.

---

## Model Notes

- This is a live-flow snapshot, not a final postmortem.
- Requires later result grading under EDGE_CALL_ACTIVE if executed.
- Track whether PHI lead management suppresses late possessions or whether BOS comeback/foul script keeps total live.
