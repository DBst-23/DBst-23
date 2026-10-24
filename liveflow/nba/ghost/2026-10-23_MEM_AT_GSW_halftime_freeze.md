# SharpEdge NBA LiveFlow Ghost #003 — MEM @ GSW — independent halftime freeze
**2026-10-23 | PAPER ONLY | PRE-BOOK PRICE | NOT A CALIBRATED FORECAST**
This forecast is independent of any sportsbook odds and must never be rewritten after the first book snapshot.

## Source / clock / context
User-submitted NBA Official Scorer's Report FIRST HALF and Q1/Q2 play-by-play only. Chase Center; officials Mark Lindsay, Che Flores, Brett Nansel.
Halftime MEM 60, GSW 56 (combined 116). Q1 MEM 33 GSW 34; Q2 MEM 27 GSW 22. No sportsbook price inspected for this entry.

## Halftime signals
MEM: 23/45 FG (51.1%), 8/18 three (44.4%), 6/9 FT; 8 OREB, 15 team TO (21 opponent points scored off TO), 26 paint, 13 transition, 12 second chance. Cameron Boozer 14 (4/5 three), GG Jackson 4 personal fouls in 10:12; Jaylen Wells 4 personal fouls; Isaiah Stewart 4 fouls; Ty Jerome 4 turnovers. Estimate MEM possessions ~45-8+15+0.44*9 =55.96 (warning: gross rebound/turnover data timing and formula sensitive).
GSW: 17/42 FG (40.5%), 7/20 three (35%), 15/17 FT; 9 OREB, 11 TO, 16 paint, 0 fastbreak, 7 second chance; 2Q 4/21 FG (19.0%), 1/10 three (10%). Curry 10 pts in 14:08, 3 PF; Podziemski 11, Lendeborg 8, 5 REB; Draymond technical in Q2. Estimate GSW possessions ~42-9+11+0.44*17=51.48. This nonmatching simple estimator is unreliable at this small sample: do not mistake as calibrated pace.
Qualitative: Warriors Q2 shooting slump likely to normalize partly, while Memphis first-half three-point efficiency (particularly Boozer 4/5) may regress. Defensive/rebounding and foul-dependent minutes introduce wide uncertainty; high turnover frequency may persist, raising transition/tail risk. Neither inference is guaranteed.

## Exploratory scenario model (not trained)
100,000 Monte Carlo draws using numpy default_rng(20261023), bivariate Gaussian z with correlation rho=.12, mean 0, unit SD; NYK/BOS prior Ghost #002 NOT used to fit outcome. Round modeled MEM 2H = max(0, round(54 + 9.7*z1)), GSW 2H = max(0, round(59 + 10.3*z2)). Judgmental means/SD; NO historical calibration. No overtime; score regulation only. Points modeled independently of player-level fouls/rotation after subjective aggregation.
- MEM second half mean 54.03, median 54.
- GSW second half mean 58.95, median 59.
- Combined second half mean 112.98, median 113.
- Projected MEM FINAL ~114.03 (60+54.03).
- Projected GSW FINAL ~114.95 (56+58.95).
- Final combined mean ~228.98, median 229.
- Final GSW margin mean ~+0.92.
- GSW regulation win 51.206%, tie 3.007%, MEM regulation win ~45.787%; NOT full-game moneyline odds because overtime omitted.
- Final total empirical percentiles: P10 210, P25 219, P50 229, P75 239, P90 248.
- Total over thresholds: O218.5 75.80%; O222.5 66.79%; O226.5 56.59%; O228.5 51.31%; O230.5 46.12%; O232.5 40.73%; O236.5 30.80%; O240.5 22.18%.
- GSW final TT overs 110.5 66.7%, 114.5 51.8%, 118.5 36.6%.
- MEM final TT overs 109.5 68.0%, 113.5 52.1%, 117.5 36.1%.
All model probability figures are exploratory not validated pricing, and cannot justify real-money strike.

## Status
PRE-MARKET FROZEN | GHOST WATCH ONLY. Next: screenshot William Hill (full-game vs half, score/quarter/clock, price) and compare without changing this file. Exact same-time alignment essential. Benchmark against other liquid markets if accessible; don't retroactively tune the distribution.
