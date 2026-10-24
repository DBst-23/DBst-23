# SharpEdge NBA LIVE-FLOW — Ghost #002 final postmortem
Date: 2026-10-23 | NYK @ BOS | TD Garden | **PAPER ONLY / NO WAGER**

## Provenance / strict chronological holdout
- Frozen independent halftime file: `liveflow/nba/ghost/2026-10-23_NYK_AT_BOS_halftime_freeze.md` (frozen commit 2c4ea331c417903baa54e2e8867119d188157b9a). Never rewrite it.
- First posted market snapshot: `liveflow/nba/ghost/2026-10-23_NYK_AT_BOS_market_compare.md` (Q3 11:39, NYK 51 BOS 50, 21 seconds after halftime). Screenshot operator/book branding NOT verified in data; user identifies William Hill. Prices are **full-game** lines.
- Settlement: user-provided NBA official final scorer's report and play by play (not independently verified). FINAL BOS 107 NYK 103. Full total 210; margin BOS +4.
- Timing warning: market quote was 21 seconds AFTER halftime, NYK already +2; comparing frozen halftime distribution to that market quote creates asynchronous comparison bias. Preserve snapshot, do not retroactively fit.
## Score audit
| | Q1 | Q2 | H1 | Q3 | Q4 | H2 | Final |
|---|---:|---:|---:|---:|---:|---:|---:|
| NYK |27|22|49|24|30|54|103|
| BOS |26|24|50|33|24|57|107|
| Combined |53|46|99|57|54|111|210|

## Prediction accuracy: no hindsight adjustment
| Measure | Frozen projection | Actual | Error actual-minus-model |
|---|---:|---:|---:|
| NYK second half | 53.483 | 54 | +0.517 |
| BOS second half | 54.977 | 57 | +2.023 |
| Second-half combined | 108.460 | 111 | +2.540 |
| NYK full-game | 102.483 | 103 | +0.517 |
| BOS full-game | 104.977 | 107 | +2.023 |
| Full-game total | 207.460 | 210 | +2.540 |
| BOS full-game margin | 2.494 | 4 | +1.506 |
Frozen simulated median: NYK 2H 54, BOS 2H 55, combined 2H 109, full-game total 208. All projected numbers from freeze, NOT trained estimates.

## Quote-time ghost outcome grading
| Market | Price as captured | Model P | Apparent edge (pp) | Actual settle | Paper outcome |
|---|---:|---:|---:|---|---|
| BOS team total OVER 103.5 | -110 | 56.235% | +3.854 | BOS 107 >103.5 | WIN (WATCH #1) |
| Combined OVER 205.5 | -110 | 55.588% | +3.207 | 210 >205.5 | WIN (WATCH #2) |
| NYK team total OVER 101.5 | -120 | 54.166% | -0.379 | NYK 103 >101.5 | WIN, but correctly classified PASS |
| BOS -2.5 | -105 | 50.175% | -1.045 | BOS wins by 4 | WIN, classified PASS |
| NYK +2.5 | -125 | 49.825% | -5.731 | loses by 4 | LOSS, classified PASS |
| NYK ML +100 | +100 | unadjusted regulation probability 40.477% | N/A | NYK lost | LOSS, classified PASS |
| BOS ML -130 | -130 | unadjusted regulation probability 56.462% | N/A | BOS won | WIN, classified PASS |
Ghost #002 **2/2 wins** under frozen watch criteria. Hypothetical one unit stakes: two -110 wins yield +1.818 units gross net profit before fees; **NO wagers made**, NOT actual profit, correlated wagers, NOT calibration proof. Unselected PASS results never enter selected-pick win rate.

## Diagnostic mechanisms supported by report
- NYK 2H 54 points, 19/41 FG (46.3%), 10/20 3PT (50%). NYK 3PT shooting H1 6/20 (30%) -> H2 10/20 (50%). Overall 3P spike contributed to second-half scoring.
- BOS 2H 57 points, 20/41 FG (48.8%), 8/19 3PT (42.1%). BOS H1 7/20 3PT (35%). Tatum 11 first-half points -> 25 second-half, 36 total; 9/15 2H FG with 5/5 FT. Boston 3rd quarter 33 decided cushion.
- Towns 3 fouls at half, 5 by final but 19:33 in second half; didn't foul out. NYK Bridges 0/8 overall in 21:53. NYK McBride 20 points with 6/8 from 3; volatile bench scoring rather than uniform starters regression.
- NYK TO 9 first half then 9 second half (18 total). Boston 7 H1 then 4 H2 (11 total). BOS 3Q 33-24, NYK 4Q 30-24. Near-game spread and margin divergence small, but direction correct.
- Evidence supports qualitative player-/quarter-level recalibration research, NOT attributing causality to isolated factors or changing tuned params after one game.
## Patch review
- KEEP: independent halftime-before-book freeze; full-game vs H2 market classification; exact price/time logging; no hindsight overwrite; inclusion of PASS selections and correlated market tags.
- MODIFY NEXT VERSION (not frozen): quote-time alignment to Q3 11:39; explicitly conditional update for elapsed possessions; foul-risk minutes model (Towns remained 19:33 H2); distribution for bench 3PT shocks/lineup concentration; overtime rules for ML; calibration backtest by market and spread environment.
- REVERT / DO NOT PROMOTE: labeling apparent +3pp edges as verified betting edges, declaring a 2/2 night statistical proof, equating ghost selection results with actual profits.
## Registry
Ghost #002 selected 2 wins / 0 losses; Ghost #001 reported previous 3 wins / 0 losses, not independently reaudited here. Cumulative provisional selected paper results 5/5, sample size tiny, correlated, **no evidence of sustainable positive EV**. Current bankroll stakes $0. Next candidate MEM @ GSW to be frozen BEFORE viewing lines, with no automatic strike.
