# SharpEdge LIVE-FLOW — GHOST #004 | PRE-MARKET FROZEN HALFTIME PROJECTION
Game: Minnesota Timberwolves at Cleveland Cavaliers
Date: 2026-10-26 | Venue: Rocket Arena
Status: PAPER ONLY / PRE-MARKET MODEL FROZEN
**No sportsbook odds, spread, market totals or prices consulted for this projection.** Input is the user-supplied official first-half report. Forecast is exploratory, not historical-fit/calibrated.

## Locked halftime score and first-half facts
MIN 60 CLE 50; Q1 MIN 31 CLE 24, Q2 MIN 29 CLE 26.
MIN FGM/FGA 25/48, 3PM/3PA 3/15, FTM/FTA 7/12, turnovers 8, offensive rebounds 6, paint 38, Edwards 20 on 8/14, McDaniels 11 on 5/6, Gobert 3 on 0/6 and 3/6 FT.
CLE 20/47 FG, 6/17 threes, 4/8 FT, turnovers 7, offensive rebounds 4, paint 24, Mitchell 9 on 3/10, Harden 2 on 1/6, Mobley 4 on 1/4 and 3 PF.
Minnesota excellent interior efficiency (19/28 2PA) not assumed fully persistent. MIN 3P 20% can improve, but 2PT 57.6% and opponent starter cold shooting counterweight. Cleveland offense rebounds modestly without presuming full jump to baseline. No historical current-season priors or market data ingested.

## Exploratory simulation parameters — hand-set, NOT trained
200,000 Monte Carlo draws, numpy PCG64 seed 20261026, rounded nonnegative integer points for Q3/Q4.
Quarter means and SD:
- MIN Q3 27, sd 7.5; MIN Q4 26, sd 8
- CLE Q3 29, sd 8; CLE Q4 28, sd 8.5
- For each quarter, each team shock = sd * (sqrt(.15)* shared-quarter-standard-normal + sqrt(.85)* independent-standard-normal), giving same-quarter opponent shock correlation .15; other quarters independently drawn.
- These assumptions encode mean-reversion, late-quarter dispersion, and scoring covariance, but are not empirically calibrated, account for overtime, or explicitly fit team/lineup-specific distributions. The resulting probabilities are only scenario illustration. If tied at 48 minutes, ML probability is unmodeled.

## Forecast outputs / frozen
| Statistic | Mean | Median | 5th-95th percentiles |
|---|---:|---:|---:|
| MIN second half | 52.98 | 53 | 35-71 |
| CLE second half | 56.99 | 57 | 38-76 |
| Second-half combined | 109.97 | 110 | 82-138 |
| MIN final | 112.98 | 113 | 95-131 |
| CLE final | 106.99 | 107 | 88-126 |
| Final combined | 219.97 | 220 | 192-248 |
| MIN final margin | +5.99 | +6 | -18 to +30 |

Regulation: MIN wins 64.5055%, tie 2.45%, CLE wins 33.0445%. No ML overtime resolution.
Model fair line, as shorthand: MIN -6 spread (note 6 point integer margins cause pushes on -6); model final total 220; MIN team total 113; CLE team total 107.
Quarter forecast MIN Q3 27 Q4 26; CLE Q3 29 Q4 28.

### Full-game total threshold probabilities
| Threshold | Over | Under |
|---|---:|---:|
| 209.5 | 72.87% | 27.13% |
| 214.5 | 62.41% | 37.59% |
| 219.5 | 51.03% | 48.97% |
| 224.5 | 39.48% | 60.52% |
| 229.5 | 28.83% | 71.17% |
| 234.5 | 19.90% | 80.10% |
| 239.5 | 12.84% | 87.16% |

### MIN full-game handicap cover, no push on half-points
| MIN handicap | P(cover) |
|---|---:|
| -3.5 | 56.75% |
| -6.5 | 48.65% |
| -9.5 | 40.59% |
| -12.5 | 32.98% |
| -15.5 | 26.03% |

### Team totals P(over)
MIN 109.5=62.45%, 114.5=44.39%, 119.5=27.60%.
CLE 99.5=73.91%, 104.5=58.51%, 109.5=41.45%.

## Data-quality / interpretation gates
- Projection frozen before any market comparison. Later screenshot may have score or clock discrepancy, and must be reconciled without rewriting this file.
- Histories and model backtest calibration absent. Do not label simulation-based probabilities as validated betting edge or recommend staking on them alone.
- Oddsmaker price and vig absent, so market edge and EV genuinely **NOT COMPUTABLE** yet. Require market lines, exact odds, score/clock alignment before comparison.
- At roughly 48 MIN FGA and 47 CLE FGA in first half, observed play is relatively high shot volume. Minnesota's 38 paint points, Cleveland's 24 paint points; Cleveland's Mobley 3 PF. Important live risks: MIN's 20% three-point accuracy, CLE Harden/Mitchell 4/16 FG combined, Edwards' usage and defensive adjustments.
- Q3/Q4 separated per prior GHOST #003 postmortem; the quarterwise random variables remain simplistic and intentionally uncalibrated.

## Audit
Reproduce with Python numpy default_rng(20261026), 200000 rows, common size (n,2), independent size(n,4), loop team indices 0 MIN Q3,1 MIN Q4,2 CLE Q3,3 CLE Q4, each q index = k%2. Draw = mean + SD*(sqrt(.15)*common[:,q]+sqrt(.85)*independent[:,k]); clip at zero and np.rint; sum halftime.
