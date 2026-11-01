# SharpEdge NBA Probability Calibration Protocol — v1.0
Effective: 2026-10-31 | Status: SPECIFICATION ONLY — NOT YET VALIDATED
Owner: SharpEdge OS / NBA LIVE-FLOW
Related: `analytics/liveflow_master/nba_halftime_game_accuracy_v2.json`; `liveflow/nba/ghost/GHOST_PICK_SOP_v1.md`

## Objective and non-negotiable rule
Demonstrate, using chronological out-of-sample evidence, that NBA halftime market probabilities are reliable **before** declaring positive expected value. An accurate point forecast, small MAE, a large Monte Carlo simulation count, or a favorable paper result does not establish probability calibration or profitability. If a market-specific probability is not supported, set `p_model=null`, `EV=null`, and `GHOST PASS`. No automatic authorization of real-money bets.

## Baseline and provenance
The current NBA halftime registry contains 16 games and 9 authenticated numeric forecasts with reported full-total MAE 5.73. This is an incomplete convenience sample, not a calibrated probability model. Preserve `uncalibrated_heuristic` for OKC @ HOU; do not silently promote it to a probabilistic forecast. Keep reconstructed/unverified freezes and post-outcome analyses out of prospective calibration metrics. Never overwrite original frozen predictions.

## 1. Data contract: one observation per game/checkpoint
Capture: `game_id`, UTC timestamp, venue-local timestamp, quarter/clock, away/home IDs, halftime official score, period scores, pace/possessions estimate and method, FGA/FGM/3PA/3PM/FTA/FTM, ORB/DRB, turnovers, fouls, confirmed lineups/injuries, rest, model feature cutoff, source URLs and provenance. Store market snapshot time, sportsbook, exact market/selection/line/American price, and market rules (OT included, push/void). Preserve final official score and settlement in separate postmortem records. Use null for unknown inputs; never infer missing odds or timestamps. Multiple market rows from one game share the same `game_id` for clustered evaluation.

## 2. Forecast model and distribution
Fit a documented, versioned predictive model using historical data available strictly before each forecast cutoff. Produce a **joint distribution** of away and home final scores or second-half scores so totals, spreads, team totals and ML can be evaluated consistently. Account for correlated outcomes and uncertainty from pace, scoring efficiency, shooting, fouls, injuries, and overtime according to the offered market rules. Specify model family, training window, features, hyperparameters, seed, simulation count, and version hash. Publish predictive mean, median, standard deviation, quantiles, and market event probability from the distribution. Simulations are draws from an estimated model, not independent evidence of model correctness; 50,000 draws cannot compensate for 20 historical games.

## 3. Chronological evaluation with no leakage
Split by game date, never random rows: (a) historical training, (b) later calibration/validation, (c) untouched later test; then use walk-forward re-fits and a prospective locked paper period. All rows from the same game remain in one split. Fit preprocessing, hyperparameters and probability recalibration **only** within the relevant past training/calibration window. No future injury status, closing lines, final scores or post-game statistics in prediction features. If historical snapshots cannot establish what was known at halftime, mark `retrospective_unverified` and exclude from authenticated prospective evidence. Version and timestamp every prediction before settlement.

## 4. Probability calibration methods and metrics
For each market type separately (full-game totals, spreads, team totals, moneyline; props separately), score probability forecasts against binary settled outcomes. Handle pushes as void/excluded from binary win/loss scoring and report push count; ensure odds settlement conventions match. Report:
- Reliability diagram by predeclared probability bins, with bin counts, observed frequencies and uncertainty intervals; avoid claims from sparse bins.
- Brier score and log loss (clip numerical probabilities for log loss), plus comparison to simple benchmark(s), including market-implied no-vig probabilities where a paired market is available.
- Calibration intercept and slope, expected calibration error (ECE; bin-dependent) and sample size; also sharpness and coverage of prediction intervals for points totals.
- Overall and segmented results by market, season, home/away, line range, time/score state and volatility regime; show clustered uncertainty by game.
- Distributional accuracy: MAE and median absolute error for points, interval coverage, and quantile/pinball scores; distinguish forecast accuracy from betting returns.
Use calibration mapping (e.g. isotonic or logistic/Platt) only on prior held-out calibration data, not on the untouched test set. Freeze mapping/version before prospective deployment.

## 5. Price and uncertainty-aware qualification
Convert American odds to decimal odds: negative `d=1+100/abs(A)`; positive `d=1+A/100`. `p_break_even=1/d`. For a settled binary event:
`EV_per_unit=p_model*(d-1)-(1-p_model)`; `edge_pp=100*(p_model-p_break_even)`.
Define an **ex ante** uncertainty method (e.g. game-cluster bootstrap of out-of-sample calibration errors, with a conservative lower bound on the event probability) and a documented additional safety buffer before evaluation. Require `lower_confidence_bound(p_model)>p_break_even+safety_buffer` to mark `PRICE_QUALIFIED_GHOST`. Do not use Monte Carlo sampling error alone as the uncertainty bound; include parameter, calibration, distribution and regime uncertainty. Until sufficient evidence exists, status remains `NOT_ESTABLISHED` and `GHOST PASS`. A qualifying ghost signal is not a real-money recommendation.

## 6. Market benchmarking and economic validation
Compare model vs same-time offered sportsbook price, account for vig and differing market rules, track later closing line when available, and calculate hypothetical returns at **recorded executable prices** with pushes/voids handled correctly. Track candidate-selection coverage, number of independent games, ROI/yield, CLV, drawdown, and confidence intervals; avoid cherry-picking market types, thresholds or dates after seeing results. Evaluate on untouched periods and report uncertainty around net ROI; paper performance is not realized profit. No stake sizing justified by unvalidated EV.

## 7. Release gates
- **G0 — Heuristic / no distribution:** mean-point forecasts only; probability and EV null; `GHOST PASS`.
- **G1 — Research:** reproducible distribution and leakage-safe historical walk-forward predictions; still no edge claim.
- **G2 — Calibrated candidate:** independent out-of-sample reliability, baseline comparisons, confidence intervals and predeclared thresholds documented; prospective ghost-only testing.
- **G3 — Prospective evidence:** sustained, independently logged prospective calibration, positive after-vig edge evidence with uncertainty, and risk review. Any real-money decision is separate and never automatic.
Sample-size planning: target hundreds of independent games for preliminary diagnostics, more for narrow market/regime slices; no fixed sample count alone proves calibration.

## 8. Required prediction record
```json
{
  "game_id": null,
  "forecast_timestamp_utc": null,
  "feature_cutoff_utc": null,
  "market_snapshot_timestamp_utc": null,
  "model_version": null,
  "calibration_version": null,
  "training_end_date": null,
  "evaluation_split": "prospective",
  "market_type": null,
  "selection": null,
  "line": null,
  "american_odds": null,
  "simulation_count": 0,
  "predictive_mean": null,
  "predictive_median": null,
  "predictive_quantiles": null,
  "p_model_raw": null,
  "p_model_calibrated": null,
  "p_model_lower_bound": null,
  "p_break_even": null,
  "safety_buffer": null,
  "edge_pp": null,
  "EV_per_unit": null,
  "qualification": "NOT_ESTABLISHED",
  "real_money_staked": 0,
  "source_paths": [],
  "data_quality_flags": []
}
```
The postmortem must independently append actual outcome, settlement, error metrics, market comparison, and calibration cohort without altering this frozen record.

## 9. Immediate implementation sequence
1. Audit existing registry for immutable freeze provenance and missing fields; tag each record `authenticated_prospective`, `authenticated_historical`, `retrospective_unverified`, or `uncalibrated_heuristic`.
2. Build a clean historical halftime feature/odds/outcome dataset with time-aware validation.
3. Implement a reproducible joint-score predictive distribution and walk-forward forecast exporter.
4. Fit calibration on prior validation windows and generate reliability/Brier/log-loss reports with game-cluster uncertainty.
5. Run prospective GHOST PASS/PICK evaluation using the SOP; review results before considering any financial risk.

**Current release state: G0. Calibrated betting probabilities and positive EV have not been demonstrated.**
