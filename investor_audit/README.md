# SharpEdge Investor Audit Archive

This folder is the append-only audit layer for SharpEdge.

## Purpose
Airtable is the dashboard and analysis layer.
This archive is the timestamped proof layer for:
- placed bets
- settled bets
- finalized postmortems

## File structure
- `placed_bets_YYYY_MM.jsonl`
- `settled_bets_YYYY_MM.jsonl`
- `postmortems_YYYY_MM.jsonl`
- `SCHEMA.md`

## Entry ID format
`SE_YYYY_MM_DD_SPORT_MATCHUP_SEQ`

Example:
`SE_2026_03_17_NBA_MIA_CHA_001`

## Screenshot naming format
`YYYY-MM-DD_sport_matchup_seq_status.png`

Examples:
- `2026-03-17_nba_mia_cha_001_placed.png`
- `2026-03-17_nba_mia_cha_001_settled.png`

## Audit rule
New records should be appended, not rewritten.
Each record should carry the same `entry_id` across:
- placement
- settlement
- postmortem

## Hash input recipe
Build the audit hash from:
`ENTRY_ID|TIMESTAMP_PLACED|SPORT|MATCHUP|STAKE|PLATFORM|LEGS_RAW`
