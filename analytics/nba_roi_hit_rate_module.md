# NBA ROI + Hit Rate Module

## Purpose
This module converts logged NBA edge entries into a running performance dashboard focused on ROI, hit rate, and structure efficiency.

## Core Metrics

### 1. ROI Formula
- ROI % = ((Total Returned - Total Staked) / Total Staked) * 100

### 2. Hit Rate Formula
- Hit Rate % = Wins / Total Tracked Bets

### 3. Structure Comparison
Track separately by:
- Single-fire
- Straight bet
- 2-pick card
- 3-pick card
- Ladder / alt-line

### 4. Market Comparison
Track separately by:
- Rebounds
- 3PM
- Points
- Assists
- PRA
- Game lines

## Initial Snapshot From Current NBA Ledger

### Overall
- Total Tracked Entries: 6
- Total Staked: 54.39
- Total Returned: 7.00
- Net: -47.39
- ROI: -87.13%

### By Core Hit/Miss Count
- Winning entries: 2
- Losing entries: 4
- Raw hit rate: 33.3%

### By Market
#### 3PM
- Entries: 2
- Wins: 2
- Hit Rate: 100%
- Stake: 14.39
- Return: 7.00
- Net: -7.39
- ROI: -51.36%
- Note: One winning leg existed inside a losing card, so market accuracy outperformed realized profit.

#### Rebounds
- Entries: 3 core rebound entries
- Wins: 0
- Hit Rate: 0%
- Stake allocation in logged cards: 30.00
- Return: 0.00
- Net: -30.00
- ROI: -100%

### By Structure
#### Kalshi Single-Fire
- Entries: 1
- Wins: 1
- Hit Rate: 100%
- Stake: 4.39
- Return: 7.00
- Net: +2.61
- ROI: +59.45%

#### Multi-Leg Card Structures
- Entries: 5 tracked legs inside bundled cards
- Result: negative realized ROI despite one true edge cashing
- Key takeaway: card structure is currently suppressing realized edge conversion

## Dashboard Guidance
### Green-Light Zone
- Single-fire bets showing positive ROI
- Markets with >55% hit rate and positive realized profit

### Yellow Zone
- Markets with positive directional accuracy but negative profit due to structure drag

### Red Zone
- Markets showing sub-45% hit rate and negative ROI
- Current example: rebounds

## Actionable Read
1. Prioritize single-fire structure whenever a leg is materially stronger than accompanying plays.
2. Continue tracking 3PM markets closely because current accuracy signal is materially stronger than rebound markets.
3. De-emphasize fragile rebound unders and forward rebound overs until enough positive evidence reappears in the ledger.

## Next Build Step
- Append every new NBA postmortem into this module
- Add rolling 7-entry and 20-entry snapshots
- Add MPZ failure frequency table under the ROI module
