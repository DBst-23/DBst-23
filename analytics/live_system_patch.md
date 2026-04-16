# Live System Patch Activation

## Status
ACTIVE

## Activated On
2026-04-16

## Purpose
Apply immediate operating rules to SharpEdge LiveFlow based on early MPZ frequency results and current ROI / hit-rate diagnostics.

## Active Patch Rules

### 1. Rebounds Freeze Rule
Temporarily de-emphasize the following until the ledger proves recovery:
- forward rebound overs
- wing rebound unders

Allowed only when the setup is exceptionally clean and not flagged by existing MPZ failure patterns.

### 2. Structure Enforcement Rule
Prioritize:
- single-fire
- straight bets

Avoid routine 3-leg exposure unless each leg independently qualifies as a stand-alone edge.

### 3. Edge Qualification Filter
Do not fire a play when a known MPZ red flag is active, including:
- CENTER_SHARE_SUPPRESSION
- WING_REBOUND_SPIKE
- REBOUND_CONCENTRATION_FAIL
- CARD_STRUCTURE_DRAG

### 4. Preferred Attack Zones
Current green-light preference:
- 3PM markets
- isolated live milestones
- single-fire exchange contracts

### 5. Monitoring Requirement
Every future NBA postmortem should update:
- edge ledger
- ROI + hit rate module
- MPZ frequency tracker

## Trigger Source
Patch activated from the first NBA analytics stack after:
- Maxey 3PM validation
- Kalshi single-fire success
- Paolo rebound miss
- Edgecombe rebound under failure

## Operational Summary
This patch shifts SharpEdge away from weak rebound-distribution assumptions and toward isolated, structure-efficient edge conversion.
