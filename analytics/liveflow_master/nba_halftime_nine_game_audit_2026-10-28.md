# SharpEdge NBA LIVE-FLOW — Nine-game timestamp and market benchmark audit

**Status:** research-only; 2026-10-28. Based on registry and linked GitHub artifacts. No reconstructed timestamps. No new bet claims.

## Coverage
- scored_games: **9**
- paired_total_lines: **7**
- missing_total_lines: **2**
- strictly_comparable_candidates: **1**
- exact_wall_clock_verified: **0**

## Paired regulation-total comparison
| Game | Frozen model | Regulation actual | Model AE | Book total | Book AE | Timestamp / alignment gate |
|---|---:|---:|---:|---:|---:|---|
| NBA_20261021_GSW_AT_LAL | 232.5 | 232 | 0.5 | 236.5 | 4.5 | PREMARKET_CLAIM_ONLY |
| NBA_20261023_NYK_AT_BOS | 207.46 | 210 | 2.54 | 205.5 | 4.5 | ASYNCHRONOUS_Q3_21_SECONDS |
| NBA_20261023_MEM_AT_GSW | 229 | 219 | 10 | 231.5 | 12.5 | SCORE_STATE_MISMATCH |
| NBA_20261026_GSW_AT_DEN | 230 | 248 | 18 | 237.5 | 10.5 | RETROSPECTIVE_NO_SEPARATE_FREEZE |
| NBA_20261026_MIN_AT_CLE | 219.97 | 226 | 6.03 | N/A | N/A | PREMARKET_CLAIM_ONLY |
| NBA_20260510_SAS_AT_MIN_G4 | 221.5 | 223 | 1.5 | N/A | N/A | POSTMORTEM_ONLY_NO_FREEZE |
| NBA_20260503_ORL_AT_DET_G7 | 208 | 210 | 2 | 206.5 | 3.5 | MARKET_AND_MODEL_SAME_SNAPSHOT_NO_PREMARKET_PROOF |
| NBA_20261027_POR_AT_LAL | 256 | 265 | 9 | 254.5 | 10.5 | SCORE_STATE_MISMATCH |
| NBA_20261027_BKN_AT_BOS | 236 | 234 | 2 | 227.5 | 6.5 | PREMARKET_CLAIM_ONLY |

**All-nine model regulation MAE:** 5.73. **Paired model MAE:** 6.291; **paired book-line MAE:** 7.5; **model minus book:** -1.209 points (negative favors model). These are not apples-to-apples executable-market comparisons because of asynchronous/score-mismatched quotes and OT.

## Evidence and limitations
- Pairwise benchmark is descriptive only, not validated fair synchronized comparison; several screenshots have score mismatches or Q3 delays.
- Full-game sportsbook totals usually include overtime while forecast is regulation-only; BKN-BOS OT game market regulation comparison is not settlement-equivalent.
- No game has verified exact wall-clock premarket model freeze and matched sportsbook screenshot capture times in registry.
- Do not infer model superiority, betting edge, or ROI from these figures.
- GSW-LAL is only provisional same-score premarket claim; no exact capture timestamps.
- ORL-DET combined market/model snapshot cannot establish forecast before odds; SAS-MIN postmortem cannot establish original premarket freeze.

## Next control
Store UTC freeze_created_at, screenshot_captured_at, first_visible_at, screenshot score, official score, market operator, market type, and immutable artifact SHA for every new game. Require matching game clock/score state and pre-market ordering before promoting to strict comparison cohort. Keep raw audit JSON separate from immutable forecasts.
