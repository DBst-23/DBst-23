# Postmortem — GSW @ DEN — 2026-03-29 — LiveFlow Rebound Card

## Final score
- Warriors 93
- Nuggets 116

## Card logged
- ❌ Nikola Jokic Higher 15.5 rebounds — finished with 15
- ❌ Brandin Podziemski Higher 7.5 rebounds — finished with 5

## Card result
- Record: 0-2
- Entry: $5.00
- Payout: $0.00
- Mode: LIVE-FLOW

## LiveFlow entry state
### At entry
- Score around early 3Q: Warriors 57, Nuggets 55
- Rebound live lines shown:
  - Jokic 15.5 with 9 rebounds already tracked on entry screenshot
  - Podziemski 7.5 with 5 rebounds already tracked on entry screenshot

## Final rebound results
### Warriors
- Gui Santos: 10
- Brandin Podziemski: 5
- Gary Payton II: 5
- Pat Spencer: 5
- Draymond Green: 4
- Kristaps Porzingis: 3

### Nuggets
- Nikola Jokic: 15
- Peyton Watson: 6
- Jamal Murray: 6
- Christian Braun: 3

## Team rebound result
- Golden State: 41
- Denver: 40
- Offensive rebounds: Golden State 9, Denver 6
- Defensive rebounds: Golden State 32, Denver 34

## Why the card lost
### 1. Jokic lost by the hook
- This was a ceiling chase at a very high live number.
- He landed exactly at 15, one short of 15.5.
- The read was not wildly wrong, but the number was already tax-heavy.

### 2. Podziemski board share got crowded
- Podziemski stayed at 5 despite enough game time to threaten the number.
- Warriors rebound distribution spread wider than expected:
  - Santos 10
  - GP2 5
  - Spencer 5
  - Draymond 4
- Too many secondary rebound collectors reduced his lane.

### 3. Blowout script changed the board environment
- Final margin expanded to 23.
- Denver controlled game flow late.
- Blowout conditions often distort live rebound pacing, minutes, and possession quality.

## What the model got wrong
- Overestimated Jokic’s remaining rebound runway relative to the posted live tax.
- Underestimated rebound spillover across Golden State’s wing/guard mix.
- Did not downgrade enough for late-game script risk after entry.

## What the model still saw correctly
- Jokic remained the central Denver rebound engine.
- Podziemski was active enough to stay relevant, but not enough to justify a 7.5 over once spillover was fully priced in.

## Confidence ladder grading
- Jokic O15.5 REB — Spillover / late tax chase ❌
- Podziemski O7.5 REB — Spillover / crowd-risk miss ❌

## Tags
- `LIVEFLOW_ACTIVE`
- `HOOK_BURN`
- `BLOWOUT_SCRIPT_RISK`
- `SPILLOVER_MISS`
- `LATE_TAX_EDGE_FALSE`
- `GSW_DEN_0329`

## Sharp takeaway
This was a classic LIVE-FLOW trap card:
- one side was priced at an inflated ceiling number
- the other side looked live but had hidden crowd-risk on the glass

## Correction rule going forward
Do not force live rebound overs when:
1. the line already requires near-ceiling output from current pace
2. rebound share is being split across 3+ active spillover players
3. blowout probability is rising entering 3Q

## Verdict
**Missed card.**
The workflow needs a stronger late-tax filter for elite rebounders and a stricter crowd-risk penalty for non-anchor guards/wings in LIVE-FLOW environments.
