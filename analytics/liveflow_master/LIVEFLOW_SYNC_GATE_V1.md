# LIVE-FLOW strict premarket synchronization gate v1

Mandatory **for promotion into the strict accuracy cohort**, not a claim that all existing pipelines now invoke the gate. Invoke `python -m liveflow.nba.sync_gate freeze.json market.json --output gate.json` before adding any checkpoint to the strict model-vs-book accuracy registry. Exit 0 = PASS; exit 2 = REJECT. Rejects must be retained for diagnostics, never silently dropped.

## Required evidence
- Two separately captured immutable JSON artifacts, model forecast **before** sportsbook exposure, with source-generated UTC `captured_at_utc`, durable `ingested_at_utc`, SHA-256 of raw source bytes, independent source, game ID, period, game clock and both scores.
- Freeze also needs model version and **regulation** total prediction. Market needs sportsbook, market type, quoted full-game total, odds format, and whether overtime is included.
- `freeze.captured_at < freeze.ingested_at < market.captured_at <= market.ingested_at` (capture equal ingestion is also accepted for the individual artifact). Git commit time alone does not prove market visibility order.
- Score, game ID, period, clock must match exactly. No score correction or reconstructed timestamp after the fact.
- **Strict regulation comparator:** market must explicitly exclude overtime. Conventional NBA full-game sportsbook totals include overtime, so these will be rejected from the *strict regulation* cohort. Store those prices in a separate descriptive cohort, or build a separately calibrated OT-inclusive model and benchmark on the book's settlement basis.
- Any absent, contradictory, unverifiable, or asynchronous field => REJECT. Do not claim an edge or promote a forecast based on rejected pairs.

## Usage and integration
1. Save model-first freeze to an immutable JSON file, before opening sportsbook odds.
2. Capture sportsbook quote in its own JSON with exact clock/score and provenance; do not rewrite freeze.
3. Run gate and persist result. Only PASS pairs enter strict regulation model-versus-market statistics. Always retain failed cases for QC.
4. Before production activation, wire this function into the actual snapshot ingestion and registry writer, add authenticated capture provenance and run CI. This commit adds a reusable gate and unit tests, **not** a production-wide enforcement hook.

Audit background: `analytics/liveflow_master/nba_halftime_nine_game_audit_2026-10-28.md`.
