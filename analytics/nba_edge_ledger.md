# SharpEdge NBA Edge Ledger

## Purpose
This ledger is the running NBA performance table for tracked edges, outcomes, structure type, and MPZ tags.

## Ledger Columns
| Date | Matchup | Market | Pick | Line | Structure | Stake | Return | Net | Result | Core Edge | MPZ Tag |
|------|---------|--------|------|------|-----------|-------|--------|-----|--------|-----------|---------|

## Entries
| 2026-04-15 | ORL @ PHI | 3PM | Tyrese Maxey Over | 2.5 | Underdog 2-Pick | 10.00 | 0.00 | -10.00 | Hit leg / Lost card | Yes | EDGE_CALL_ACTIVE |
| 2026-04-15 | ORL @ PHI | Rebounds | Paolo Banchero Over | 8.5 | Underdog 2-Pick | 10.00 | 0.00 | -10.00 | Miss | Yes | REBOUND_CONCENTRATION_FAIL |
| 2026-04-15 | ORL @ PHI | Rebounds | Paolo Banchero Over | 8.5 | 3 Pick Max Cash | 10.00 | 0.00 | -10.00 | Miss | Yes | CENTER_SHARE_SUPPRESSION |
| 2026-04-15 | ORL @ PHI | Rebounds | VJ Edgecombe Under | 5.5 | 3 Pick Max Cash | 10.00 | 0.00 | -10.00 | Miss | Yes | WING_REBOUND_SPIKE |
| 2026-04-15 | ORL @ PHI | Points | Stephen Curry Over | 0.5 | 3 Pick Max Cash | 10.00 | 0.00 | -10.00 | Hit leg / Lost card | No | BOOSTER_LEG |
| 2026-04-15 | ORL @ PHI | 3PM | Tyrese Maxey 3+ | alt milestone | Kalshi Single-Fire | 4.39 | 7.00 | 2.61 | Win | Yes | SINGLE_FIRE_SUCCESS |

## Initial Read
- Single-fire structure produced cleaner edge conversion than bundled card formats.
- Rebound distribution props on wings/forwards showed higher failure volatility than shooting-threshold markets.
- Maxey 3PM angle is the first confirmed positive edge in the ledger.

## Next Build Targets
1. Add ROI by market section
2. Add hit rate by structure section
3. Add MPZ frequency table
4. Append future NBA entries automatically after each postmortem
