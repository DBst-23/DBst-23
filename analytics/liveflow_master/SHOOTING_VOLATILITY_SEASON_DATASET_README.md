# NBA halftime shooting-volatility — season-scale expansion (v0.1)
Status: **INGESTION AND WALK-FORWARD CODE COMMITTED; SEASON DATA NOT YET INGESTED.** This is not a validated model or market-edge test.

## Scope and sources
Target: all regular-season NBA team-games in **2025–26** (historical completed season), one CSV row per team-game, with both teams sharing game_id. Source official period box scores / play-by-play for 1H and 2H shooting and scoring. The existing five-row convenience sample at `nba_halftime_shooting_volatility_pilot_2026-11-02.json` is not season-scale and must not be presented as representative.

Input header, in order:
`game_id,game_date,team,opponent,h1_3pm,h1_3pa,h2_3pm,h2_3pa,h1_points,h2_points,h1_fga,h1_fta,h1_orb,h1_tov,h2_fga,h2_fta,h2_orb,h2_tov,halftime_total,final_total,market_book,market_captured_utc,market_total_line,market_under_american,market_over_american,source_url`

Missing possession inputs or historical halftime prices **must be blank, not estimated or replaced with closing lines**. Possessions use the explicitly labeled approximation FGA + 0.44 FTA - ORB + TOV, not actual possession counts. Exclude OT from second-half regulation features; separately record OT final totals when applicable. Data ingestion must document whether period statistics include OT, and must reconcile both teams' period scores against official game summaries. Markets require actual halftime snapshot timestamp and sportsbook, both sides of the market, and correct OT settlement rule. Missing markets are not evidence of missing lines.

## Execute
```bash
python analytics/liveflow_master/shooting_volatility_walkforward.py --input path/to/2025_26_team_halves.csv --output path/to/walkforward_results.json --min-train-games 200
```
The script validates rows and runs an expanding-window **date-grouped** test (no same-day observations enter each other's training). Baseline: historical mean second-half points and historical second-half 3PT rate. Experimental 3PT estimator shrinks observed 1H accuracy toward the historical 2H rate using 50 pseudo-attempts. Experimental scoring estimator is a simple historical shooting-deviation slope. These are research benchmarks, not probabilistic market models.

## What is and is not tested
- Computes OOS MAE for 2H points and shooting percentage for both baselines and experimental estimators.
- Records missing/partial market snapshots as validation errors rather than filling odds.
- Does **not** yet compute market no-vig comparisons, game-level total probabilities, Brier/log loss, ROI, or edge; these require paired team forecasts, a validated predictive distribution and timestamped halftime prices. It is incorrect to compare a team 2H points forecast directly with a full-game market total.
- All test-game observations are scored retrospectively but predictions use only previous dates. Historical data alone cannot authenticate a real-time model freeze.
- All wagers remain G0 Ghost/PASS, $0, until probability calibration protocol gates are met.

## Required next ingestion task
Acquire a **complete 2025–26 regular-season period-box-score export** with stable NBA game IDs and authoritative source URLs, reconcile each half's score, count expected games and teams, and write the CSV to a versioned data location. Audit missingness and sampling bias before interpreting results. Then independently obtain timestamped halftime sportsbook archives; if unavailable, label the market-comparison subset separately and report coverage. Never imply that the current repository contains the season-scale rows until ingestion succeeds.
