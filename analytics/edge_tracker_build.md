# SharpEdge Edge Tracker Build

## Purpose
Create a structured tracker framework to measure edge quality, hit rate, ROI, and failure patterns across logged postmortems.

## Core Tracking Categories

### 1. Bet Metadata
- sport
- date
- matchup
- market_type
- player
- line
- pick_direction
- sportsbook_or_platform
- stake
- payout
- result

### 2. Model Metrics
- projected_mean
- projected_median
- model_win_probability
- market_implied_probability
- edge_percent
- confidence_tier

### 3. Execution Structure
- execution_type (single-fire, straight, parlay, ladder, alt-line)
- card_name
- core_leg_flag
- non_core_leg_flag
- correlation_risk_flag

### 4. Outcome Tags
- HIT_REGISTERED
- MISS_REGISTERED
- EDGE_CALL_ACTIVE
- NO_CALL_ZONE
- DELTA_LOG
- MPZ failure tags

### 5. Session Metrics
- total_staked
- total_returned
- net_result
- roi_percent

## Initial Folder Targets
- `analytics/`
- `analytics/nba/`
- `analytics/mlb/`
- `analytics/wnba/`

## First Dashboard Goals
1. ROI by prop type
2. Hit rate by market
3. Single-fire vs parlay comparison
4. Rebound model hit rate
5. 3PM model hit rate
6. Top recurring MPZ miss tags

## Build Roadmap
### Phase 1
- Standardize postmortem file structure
- Ensure each postmortem captures stake, payout, tags, and result

### Phase 2
- Build a summary markdown ledger per sport
- Append each postmortem into edge tracker table format

### Phase 3
- Add structured JSON or CSV export for spreadsheet/dashboard ingestion

## Immediate Recommendation
Prioritize single-fire and straight-bet performance tracking first, since those are currently showing cleaner edge conversion than bundled card structure.
