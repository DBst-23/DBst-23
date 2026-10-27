# SharpEdge LIVE-FLOW evidence audit — baseline v0
Date: 2026-10-26 | Scope: documented records inspected; **not a comprehensive historical backtest** | Decision: **NO LIVE WAGER DEPLOYMENT**.

## Dataset inventory / coverage
GitHub default branch tree has 1,140 entries. Evidence families inspected: `liveflow/nba/ghost/` October 2026; `Backtest_Logbook/NBA/Model_Audits/NBA_LIVEFLOW_MODEL_AUDIT_2026_05_10.json`; `Backtest_Logbook/WNBA/LIVE_FLOW_investments.jsonl`; selected WNBA postmortems. Additional NBA playoffs, WNBA postmortems and duplicate folders exist. This baseline does **not** ingest/grade every listed document or assess chronological eligibility for each.

## A. NBA October 2026 illustrative selected ghost observations (PAPER / no verified wagers)
- GSW @ LAL Oct 21: 3/3 selected markets won, from `liveflow/nba/ghost/2026-10-21_GSW_AT_LAL_GHOST001_RESULT.json`. Same-game correlated.
- NYK @ BOS Oct 23: 2/2 selected WATCH positions won, from `liveflow/nba/ghost/2026-10-23_NYK_AT_BOS_postmortem.md`. Quoted market 21 seconds into Q3, not exact halftime.
- MEM @ GSW Oct 23: 1/1 pre-registered principal market MEM +2 -115 won, from `liveflow/nba/ghost/2026-10-23_MEM_AT_GSW_GHOST003_final_postmortem.md`; sportsbook score at snapshot differs from official half by 2 points. Other market sides that happened to win were **NOT eligible selected picks**.
- GSW @ DEN Oct 26: 1/3 primary Under signals won (DEN team total Under; game Under and GSW team total Under lost), from `liveflow/nba/ghost/2026-10-26_GSW_AT_DEN_halftime_postmortem.md`; original claims of 100,000 simulations and model EV unverified.
**Illustrative subtotal: 7 wins / 2 losses on 9 selected/flagged paper markets in 4 games.** This is a biased convenience sample with inconsistent signal categories, highly correlated same-game exposures, stale/async quotes, no confirmed executable bet slips and nonreproducible models. **Do not publish a credible edge, standalone ROI, confidence interval or readiness conclusion from it**.
- MIN @ CLE Oct 26: halftime speculative TT Unders at unverified prediction-style screenshot (both lost in OT at full-game final 125-127 vs 117.5/111.5), distinct from later Q3 William Hill screens. File `liveflow/nba/ghost/2026-10-26_MIN_AT_CLE_GHOST004_market_snapshot_01.md`. Excluded from the selected-WH convenience subtotal; must be included in broader opportunity-level audit with source/platform label and overtime settlement.

## B. Prior-period adverse evidence
`Backtest_Logbook/NBA/Model_Audits/NBA_LIVEFLOW_MODEL_AUDIT_2026_05_10.json` reports a **12-ticket historical review, 1 win, 9 losses, 2 cashouts/partial losses**, along with zero-bankroll cooldown lock and diagnoses of bench garbage-time tail failures. This is **not necessarily the same market, season, or entry selection protocol** as Oct 2026; it must not be casually pooled into an aggregate 8/21 or historical ROI. It strongly disputes any blanket claim of demonstrated profitability.

## C. WNBA execution evidence, not all history
`Backtest_Logbook/WNBA/LIVE_FLOW_investments.jsonl` contains **2** parsed investment records: Aug 29 CHI@NYL halftime Under 161.5 -120 stake $10 profit +$8.33 WIN; Aug 29 TOR@PHO end-Q3/early-Q4 Under 176.5 -105 stake $9.33 profit +$8.89 WIN. These 2 are *not* a full WNBA investment ledger. The repository has many other WNBA postmortems (including Aug 24 ATL@LAS reported executed +$19.79 and July 20 NYL@DAL OT-rescued ticket) which must be deduplicated and categorized before any WNBA ROI claim. Some WNBA records are non-halftime and must not be pooled with halftime strike without stratification.

## D. Initial falsification checks
1. Timing: model freeze time before bookmaker observation required for fair blinded tests. For NYK@BOS market from after halftime, align score-state or exclude.
2. Price verification: capture venue, line, side, odds, timestamp, fees, settlement incl. overtime. Separate regulated sportsbook from prediction exchange.
3. Reproducibility: persist distributions/seed and code version; manual normal approximations and verbal `100k` trials are not verified simulations.
4. Predictive target: regulation and official including overtime separately; score/team total/spread arithmetic coherent.
5. Sampling: enumerate **all eligible games and all published pre-registered selections**, including PASS, not only wins, and keep correlated sides within game clusters.
6. Evaluation: base-rate sportsbook benchmark; scoring MAE / bias; Brier/log loss for ML; probabilistic calibration; realized paper P&L vs quoted executable prices and CLV where both snapshots exist; uncertainty by date/game block. Hold out later periods for out-of-sample.
7. Do not deploy funds on current evidence. Complete full inventory/chronological eligibility tagging and independent out-of-sample paper tracking first.

## Bottom line
Evidence is **mixed**: recent selected NBA ghost picks look encouraging but are too small/selected; historical NBA May audit is severely negative and confirms risk controls were necessary. Positive WNBA bets exist but no complete audited denominator or cleanly comparable halftime cohort. **Profitability and reliable positive EV are NOT established.**

## Next audit action
Create a row-level canonical opportunity register with identifiers: date, league, match, period, frozen_commit, freeze_time, market_time, score_state_at_both_times, bet_type, side, book, line, odds, published selection/pass, actual ticket or paper, stake, outcome, actual_score, OT_flag, verified_data, simulation_reproducible, exclusion_reason. Then enumerate all historical records; grade strictly chronologically before calculating statistics. Keep this baseline immutable; subsequent audits versioned.
