# LIVE-FLOW Investment Log — Connecticut Sun @ Dallas Wings

**Date:** 2026-08-30  
**Sport:** WNBA  
**Checkpoint:** Halftime / early Q3 entry window  
**Score at model freeze:** Connecticut 47 — Dallas 60  
**Market:** Full Game Total  
**Position:** OVER 188.5  
**Odds:** -115  
**Sportsbook:** William Hill  
**Stake:** $15.00  
**Potential payout:** $28.04  
**Potential profit:** $13.04  
**Ticket timestamp:** 2026-08-30 6:28 PM NV  
**Status:** OPEN

## Market-blind SharpEdge read

Before sportsbook pricing was revealed, LIVE-FLOW froze an approximate **194.0 full-game total center**.

At halftime, Connecticut trailed Dallas 60-47 for 107 combined points. The model expected the remaining game to produce roughly **86.5 points**, supporting a final center near 194 rather than simply extrapolating the 107-point first half.

The first-half scoring profile contained competing forces: Dallas had shot an unsustainably hot 60.0% from the field, while Connecticut still had identifiable positive-regression paths through several inefficient individual shooting lines and a 31.2% team three-point rate. The aggregate read therefore favored continued scoring while allowing the allocation between teams to remain uncertain.

## Market comparison

- SharpEdge frozen center: 194.0
- William Hill live total at executed price: 188.5
- Market distance from center: **+5.5 points toward the OVER**
- Required remaining points from the 107-point halftime state: 82 to clear 188.5
- SharpEdge expected remaining points: ~86.5
- Side: OVER
- Price: -115

## Execution note

This was selected as the cleanest expression of the model edge because the aggregate total was considered more reliable than direct team allocation. The market offered a number materially beneath the frozen SharpEdge center while remaining inside the normal LIVE-FLOW price discipline.

The sportsbook had briefly shown 189.5 at -115 after the model freeze; the executed ticket captured **188.5 at the same -115 price**, improving the entry by one full point.

## Ticket evidence

William Hill ticket screenshot supplied in-chat:

- OVER 188.5
- -115
- Wager: $15.00
- To win: $13.04
- Pays: $28.04
- Ticket timestamp: AUG 30 2026 06:28 PM NV

## Model-state tags

- MARKET_BLIND_PROJECTION_FREEZE
- EDGE_BUFFER_VALUE_v1
- ASYMMETRIC_REGRESSION_DISTRIBUTION_v1
- TEAM_ALLOCATION_ERROR_TRACKING_v1
- FULL_GAME_VS_TEAM_TOTAL_DIVERGENCE_v1
- LIVEFLOW_HALFTIME_REGIME_CONFIRMATION_v1

## Postmortem fields

To be completed after final:

- Final score:
- Final total:
- Result:
- Closing/live line movement after entry:
- Second-half score:
- Projection error vs center:
- Why the bet won/lost:
- Tags/patches triggered:
