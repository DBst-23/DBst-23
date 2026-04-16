# Rebound Refinement Backtest — 2026-04-16

## Status
COMPLETED

## Purpose
Use recent logged NBA rebound exposures to classify archetypes, evaluate failure shape, and refine the playoff rebound model before the 2026-04-17 slate.

## Review Set Used
1. MIA @ CHA postmortem sequence
2. ORL @ PHI postmortem sequence
3. NBA edge ledger / ROI / MPZ tracker context already logged in repo

## Archetype Classification Results

### 1. Wing Under Archetype
#### Cases reviewed
- Andrew Wiggins U4.5 REB — MISS (7)
- VJ Edgecombe U5.5 REB — MISS (11)

#### Common failure shape
- Stable or extended minutes
- Competitive game flow preserved closing run
- Opponent miss volume created extra cleanup chances
- Wing/guard rebound role was underestimated

#### Classification
**RED ZONE (temporary freeze)**

#### Tags repeatedly aligned
- WING_REBOUND_SPIKE
- MINUTES_EXTENSION_PENALTY
- ROLE_UNDERFAIL

---

### 2. Forward Over Archetype
#### Cases reviewed
- Paolo Banchero O8.5 REB — MISS (5)

#### Failure shape
- Same-team center maintained strong rebound share
- Team rebound ecology stayed flatter than required
- Forward scoring burden did not convert into board dominance

#### Classification
**YELLOW / HIGH SCRUTINY**
Allowed only when center share suppression is clearly present.

#### Tags aligned
- CENTER_SHARE_SUPPRESSION
- REBOUND_CONCENTRATION_FAIL

---

### 3. Center Over Archetype
#### Cases reviewed
- Moussa Diabate O8.5 REB — HIT (14)

#### Positive shape
- Clear glass role
- Strong offensive rebound path
- Interior board environment aligned with player profile

#### Classification
**GREEN ZONE**
Current strongest rebound subtype in recent logged sample.

#### Tags aligned
- CENTER_GLASS_EDGE_CORRECT

---

### 4. Lead Guard / Scoring Wing Unders
#### Cases reviewed
- LaMelo Ball U5.5 REB — HIT (5)
- Brandon Miller U5.5 REB — HIT (5)

#### Positive shape
- Under stayed live with cleaner rebound role assumptions
- Did not require suppression of an active crash wing role like Wiggins/Edgecombe

#### Classification
**YELLOW-GREEN**
Playable only when no wing spike warning is present.

#### Tags aligned
- LEAD_GUARD_REBOUND_UNDER_CORRECT
- WING_SCORER_REBOUND_UNDER_CORRECT

---

## Preliminary Archetype Ranking
1. **CENTER_OVER** — strongest current subtype
2. **LEAD_GUARD_UNDER / SCORING_WING_UNDER (clean role only)** — selectively playable
3. **FORWARD_OVER** — needs strong center-share suppression check
4. **WING_UNDER** — temporary freeze / red zone

## Playoff Rebound Filters

### Green-Light Rebound Attack Zones
- Elite or clear-role center overs
- Bigs with stable minutes and strong rebound chance share
- Unders on guards/wings only when rebound role is clearly passive and no wing spike risk is present

### Red-Zone Rebound Trap Profiles
- Wing unders with 36+ projected minutes
- Wings/guards in competitive games with high miss-volume environment
- Forward overs when same-team center remains a dominant rebound vacuum
- Any rebound play requiring three or more teammates to simultaneously underperform their natural board share

## Execution Refinement
### Single-Fire Rule
When a rebound edge is isolated and materially stronger than other available legs:
- prefer single-fire deployment
- avoid bundling with weaker rebound assumptions

### Card Restriction
Do not use 3-leg rebound cards unless each leg independently qualifies as a stand-alone play.

## Model Interpretation
The rebound venture remains active.
The issue is not the entire market — it is the fragility of specific playoff rebound archetypes.
Recent logs suggest the model should:
- trust center overs more
- treat forward overs with stricter ecology checks
- suppress wing unders unless the rebound role is clearly weak and minutes ceiling is modest

## Recommended Rule Set for 2026-04-17 Slate
1. Prioritize center rebound overs first.
2. Require explicit center-share suppression proof before taking forward rebound overs.
3. Freeze wing rebound unders unless matchup and role structure are exceptionally clean.
4. Default to single-fire deployment for rebound edges.
5. Continue logging every rebound outcome into ledger + MPZ tracker.

## Next Commands
- `rank rebound archetypes`
- `update rebound attack filters`
- `scan 2026-04-17 slate in patched rebound mode`
