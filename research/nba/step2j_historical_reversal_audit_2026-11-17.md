# Step 2J — Historical Second-Half Reversal Audit (Exploratory)

Date: 2026-11-17

## Question
Does SharpEdge's historical halftime **point-estimate margin model** underrepresent lead reversals, motivated by MEM @ WAS 2026-11-16 (projected WAS +8.5, actual MEM +16; 24.5-point error)?

## Sources and reproducibility
- Historical predictions: existing local Step 2F artifact `holdout_enriched.csv` derived from the 2024 season holdout (1,170 regulation games); baseline source `scripts/liveflow_halftime_baseline.py`.
- Single-game motivation: `postmortems/nba/2026-11-16_MEM_WAS.md`.
- **The 2026 game is not in the 2024 historical sample.**
- No retraining, no sportsbook odds, no market edge estimate.
- 2024 holdout has been repeatedly inspected; **exploratory, not pristine validation**.
- Dataset excludes games that eventually went to overtime, a postgame selection criterion causing potential halftime lookahead bias.

## Definitions
- Halftime margin: home points minus away points at halftime.
- Actual final margin: halftime margin + actual second-half margin.
- Predicted final margin: halftime margin + predicted second-half margin.
- Lead reversal: halftime leader **loses in regulation**; operationally `halftime_margin * final_margin < 0`.
- Predicted reversal: predicted final margin point estimate changes sign relative to halftime margin. **Not a calibrated reversal probability.**
- Absolute error: `abs(actual second-half margin - predicted second-half margin)`, identical to absolute final margin error.

## Results
| Halftime lead | Games | Actual reversals | Actual rate | Predicted reversals (point estimates) | Mean absolute margin error | Errors >= 24.5 pts |
|---|---:|---:|---:|---:|---:|---:|
| All | 1,170 | 270 | 23.08% | 45 | 9.361 | 48 (4.10%) |
| 1–9 | 613 | 213 | 34.75% | 45 | 9.318 | 21 (3.43%) |
| 10+ | 507 | 57 | 11.24% | **0** | 9.363 | 25 (4.93%) |
| 10–14 | 255 | 43 | 16.86% | **0** | 9.161 | 13 (5.10%) |
| 15+ | 252 | 14 | 5.56% | **0** | 9.567 | 12 (4.76%) |

Note: the 1–9 and 10+ groups exclude 50 tied-at-half games; all-game counts include them, and ties are not classified as lead reversals.

## Interpretation
- **Confirmed descriptive blind spot:** for all 507 games with halftime lead >=10, the regression's **single point estimate** predicted the halftime leader would remain ahead, yet 57 leaders lost.
- **Do not interpret 0 point-estimate reversals as model probability 0%.** A mean/median forecast can correctly remain on the favorite side even when the calibrated probability of reversal is nonzero. The next test must calculate each game's *ex ante* reversal probability from the 2023 residual distribution and compare expected to observed reversals, with reliability bins and Brier/log loss versus a simple baseline.
- The 24.5-point MEM/WAS miss is a material tail error: 48/1170 (4.10%) of holdout margin errors were >=24.5, and 25/507 (4.93%) for leads >=10. This does not imply a specific 2026-game ex ante probability.
- These results alone **do not prove systematic probability underestimation**, because point forecasts are not probability forecasts.

## Example historical reversal
2025-02-08 Golden State Warriors @ Chicago Bulls: Chicago led by 14 at halftime, model predicted Chicago +11.91 final, actual Chicago -21; margin error -32.91.

## Next checkpoint
Evaluate *probabilistic* lead-reversal calibration using **2023-only validation residuals** for each 2024 holdout game; compare observed vs expected rates by halftime-lead band, and a simple halftime-lead baseline. Report confidence intervals and limitations. Do not modify coefficients or declare a profitable edge from these exploratory results.

**Real-money deployment remains LOCKED.**
