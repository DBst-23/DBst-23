# NBA LIVE-FLOW Registry Coverage and Source Integrity — Preliminary Audit

Audit date: 2026-10-28. Canonical repository: `DBst-23/DBst-23`.

## Scope and limitations

This is an **inventory and internal-consistency audit**, not a completed historical backtest, source-by-source semantic verification, or proof of profitable wagering. The source manifest is a broad discovery inventory; its entries are not all eligible NBA halftime forecasts.

## Verified structural checks

- Registry: `analytics/liveflow_master/nba_halftime_game_accuracy_v2.json`.
- Registry game rows: **12**; unique game IDs: **12**.
- Source manifest discovery entries: **302** (includes unrelated markets, duplicates, and records awaiting extraction; do not interpret as 302 games).
- Source-path references: **21**; non-string or unresolved references: **1**.
- Numeric halftime full-game forecasts with regulation outcomes: **9**.
- Independently recomputed regulation total MAE: **5.73** points; registry reports **5.73**.
- Records with explicit non-null forecast wall-clock freeze timestamps: **0** of 12.
- Records flagged as overtime: **2**.

## Exceptions requiring attention

- `NBA_20260503_ORL_AT_DET_G7`: source_paths contains null; fix only after confirming intended source provenance.
- **Historical coverage incomplete**: the 302-entry discovery manifest has not been systematically classified, deduplicated, and reconciled against the 12-game registry. The ratio is not a coverage percentage because entries differ in scope and granularity.
- **Timestamp integrity incomplete**: missing exact freeze times prevent independently proving every forecast preceded the compared market quote. File presence is not a substitute for pre-market timing evidence.
- **Market timing/score integrity**: POR@LAL 2026-10-27 has official halftime 68–73 versus William Hill screenshot 68–75. Keep HOLD / paper-only and do not use for verified market-edge attribution.
- **Overtime integrity**: BKN@BOS 2026-10-27 regulation 234 vs full final 249; regulation-only forecast 236 must be evaluated against 234 for model accuracy. Separate final-score market settlement.
- **Nonrandom sampling and market-only entries**: reported 5.73 MAE describes only 9 eligible numeric forecasts in this selected sample. No inference of calibrated edge, ROI, or hit rate is warranted.

## Release gate for betting calibration

**NOT READY**. Before calibration, (1) classify historical discovery entries by NBA/halftime/forecast availability, (2) resolve null source references, (3) verify original freeze-versus-market chronology and preserve missing timestamps as unknown, (4) check independent final scores and OT/regulation semantics, (5) deduplicate game/checkpoint observations, (6) evaluate a chronological out-of-sample sample with explicit inclusion criteria. Never backfill or alter original frozen projections.

## Preservation policy

This audit creates a new document only. Existing registry rows, source files, timestamps, quotes, warnings, and postmortems remain unchanged.
