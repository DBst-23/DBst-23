# SharpEdge LIVE-FLOW Master Historical Dataset — v1

## Status (2026-10-26)
**Discovery inventory COMPLETE for candidate paths in the repository's default-branch tree; record normalization PARTIAL.**

- `source_manifest_v1.json`: **302** discovered candidate JSON/JSONL/CSV/MD source files (including potentially unrelated prop files, duplicates, reports and qualitative documents). Their source paths/blob hashes are preserved. No assertion is made that all 302 contain unique eligible halftime opportunities.
- `standardized_records_v1.json`: **26** normalized **position-level** records from **8** files actually read: **12** historical May NBA audit tickets, **3** Oct 21 NBA ghost selections, **2** Oct 23 NYK-BOS ghost watches, **1** Oct 23 MEM-GSW ghost selection, **3** Oct 26 GSW-DEN Under signals, **2** Oct 26 MIN-CLE flagged *opportunities* (not confirmed selections), **2** WNBA Aug 29 investment-ledger entries, **1** WNBA Aug 24 postmortem investment claim.
- This is a **source-backed starter consolidation**, NOT complete records, NOT a clean chronological backtest, and NOT a certified ROI data feed.
- Entirely unknown freeze timestamps, quote times, or model outputs are **null**; original documents remain authoritative; never backfill based on actual final scores.
- Market prices, real-money execution and profit reported in postmortems/ledgers are not independent account confirmation. `actual_profit=0` on paper means no realized money, not hypothetical ROI.

## Standardized record semantics
One row per proposed market side, paper signal, or ticket. Key fields: `record_id, date, league, matchup, market_type, selection, entry_phase, entry_score, model_freeze_time, model_projection, model_win_probability, bookmaker, market_snapshot_time, market_line, american_odds, price_verified, selection_class, execution_class, stake, actual_profit, model_error, final_score, final_total, overtime, settlement, record_quality, eligibility, source_path, notes`.

These fields intentionally separate:
- `selected_ghost` and `selected_watch` from `model_flagged_not_confirmed_selected`.
- `paper_only` vs `claimed_real_wager_unverified_ticket` vs historical audit claims.
- Regulation forecasts vs OT-included market settlement (add further explicit target fields before any wager-grade ROI analysis).
- Bookmaker from screenshot/exchange and any unresolved score-state discrepancy.

## Research blockers before ROI or wager readiness
1. Read all sources in manifest, classify genre and source duplication, and extract genuine market-level records from each. Do not convert a report with no timestamp/price into a fabricated bet.
2. Match each forecast with *earlier* immutable lock/commit (use Git history if needed), and appropriately time-align sportsbook snapshot to score/time.
3. Resolve duplicate same-game/ticket records across folders and historical audits. Preserve all citations to distinct source files.
4. Verify each payout and bet ticket if actual investment; independent account transaction missing => mark unverified.
5. Distinguish preseason, regular, playoff, WNBA/NBA, half/Q3/Q4, model versions, lines and prices. Avoid cross-league pooling without stratified report.
6. Record PASS/NO BET opportunity denominator, including losses and missing quotes.
7. Calculate ROI only on a defensible well-defined selection universe, with per-game clustering and forward holdout. Do not conflate positive hindsight outcomes with a positive-EV edge.

## Known integrity caveats
- Oct 23 MEM@GSW official halftime score conflicts by two points with market screenshot.
- Oct 23 NYK@BOS market screen observed ~21 seconds into Q3.
- Oct 26 MIN@CLE two exchange-style screenshot flags are not verified placed wagers or selected William Hill tickets.
- Oct 26 GSW@DEN normal simulation summary lacked independently reproducible saved run, and team-score projection disagreed with claimed fair spread.
- May NBA model audit includes pregame entries; not all 12 are halftime.
- Historical WNBA evidence lives outside the two-line JSONL ledger; more sources must be ingested and deduplicated.

## Next ingestion checkpoint
Extend standardized records to the remaining **294 unread source files** in the manifest, including historical NBA playoffs and WNBA postmortems, with exclusion classifications for documents that are not betting opportunities. Re-run manual source audits before statistics.

## Game-level accuracy registry (2026-10-27)
New: `nba_halftime_game_accuracy_v1.json` contains **5 unique NBA halftime games** reconstructed from October 2026 postmortems, with one frozen checkpoint per game and separately nested markets.

**Current convenience-sample diagnostics:** Regulation-total model MAE **7.414 points** across 5 games; official-final-total (including OT) MAE **12.614 points**. **Only 4 of 5 games have a documented full-game book total line**. The fifth (MIN @ CLE) had 26 overtime points and a regulation-only model. Thus these are descriptive diagnostics **not** a validated market-beating record; some sportsbook screenshots were at a different score/clock from freeze.

The source position ledger `standardized_records_v1.json` is preserved unchanged as an event/selection-level subsidiary. This new registry is **one row per game/checkpoint**, with nested market comparisons and source paths, preventing each correlated position from masquerading as another independent game. Dates, regulation-only/OT settlement, missing odds, and discrepancies preserved. Other older NBA and WNBA source files await review.
