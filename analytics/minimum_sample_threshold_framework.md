# Minimum Sample Threshold Framework

## Purpose
Define when a rebound archetype has enough logged evidence to be promoted, monitored, or frozen inside SharpEdge. This framework is designed to prevent overreaction to tiny samples while still allowing early-warning patches when failure shapes are strong.

## Core Principle
A market archetype can be:
- **EARLY WARNING** — useful for temporary caution, but not trustworthy enough for permanent conclusions
- **MONITORED** — enough evidence to guide deployment with caution
- **PROMOTED** — strong enough to treat as a preferred attack lane
- **FROZEN** — strong enough evidence of failure to temporarily block the archetype until refined

## Archetype Definitions
- `CENTER_OVER`
- `FORWARD_OVER`
- `WING_UNDER`
- `LEAD_GUARD_UNDER`
- `SCORING_WING_UNDER`
- `GUARD_OVER`
- `CLEAN_SHARE_ENV`
- `CROWDED_SHARE_ENV`
- `CENTER_SHARE_DOMINANT`
- `LONG_REBOUND_ENV`
- `TIGHT_ROTATION`
- `OT_RISK`

## Sample Threshold Tiers

### Tier 0 — Insufficient Sample
- Fewer than **4** logged plays in an archetype
- Action: no permanent judgment allowed
- Allowed output: descriptive notes only

### Tier 1 — Early Warning Sample
- **4 to 7** logged plays in an archetype
- Action: temporary patch allowed if failure shape is consistent
- Use case: cautionary downgrade, not full strategic abandonment

### Tier 2 — Monitoring Sample
- **8 to 14** logged plays in an archetype
- Action: eligible for provisional promotion or provisional freeze
- Must check both hit rate and MPZ pattern repetition

### Tier 3 — Actionable Sample
- **15 to 24** logged plays in an archetype
- Action: trustworthy enough for deployment rules and confidence tiers
- At this stage, ROI, hit rate, and structural conversion should all be tracked

### Tier 4 — Stable Sample
- **25+** logged plays in an archetype
- Action: full trust for model policy decisions unless playoff environment materially changes

## Decision Rules

### Promote an Archetype When
All of the following are true:
1. Sample is at least **Tier 2 (8+)**
2. Hit rate is **55%+** or ROI is positive under preferred structure
3. MPZ miss tags are not clustering in a repeat failure pattern
4. Wins are not being driven only by external-source picks or weak structure accounting

### Freeze an Archetype When
Any of the following are true:
1. Sample is at least **Tier 2 (8+)** and hit rate is **45% or lower**
2. Sample is **Tier 1 (4–7)** but the same high-severity MPZ miss tag repeats **2+ times** in similar environments
3. Losses are not hook losses but structural misses (role misclassification, rebound share collapse, wing spike, center suppression)
4. Realized ROI is materially negative even after accounting for structure type

### Temporary Patch Rule
If sample is only **Tier 1** but failure shape is highly consistent, the archetype may be patched as:
- `temporary freeze`
- `high scrutiny`
- `single-fire only`

This is a risk-control action, not a final verdict.

## Structure Weighting Rule
Not all logged entries should count equally.

### Full Weight
Count as **1.0 weight** when the play is:
- `MODEL_NATIVE`
- executed as single-fire or straight
- clearly logged with result and archetype tags

### Partial Weight
Count as **0.5 weight** when the play is:
- inside a bundled card but still a clearly model-native leg
- affected by card structure drag in realized ROI accounting

### Informational Only
Count as **0.25 weight** when the play is:
- `EXTERNAL_SOURCE`
- tailed but not model-generated
- used for market context but not internal model validation

## Environment Split Requirement
Before promoting or freezing an archetype, split the sample by:
- regular season vs playoff environment
- competitive game vs blowout environment
- stable minutes vs unstable minutes
- center share dominant vs clean-share environment

An archetype should not be fully promoted or frozen if its evidence comes from only one narrow environment unless that environment is the primary target context.

## Recommended Current Interpretation
Based on the recent rebound refinement batch:
- Current rebound archetype evidence is **Tier 1 / Early Warning** only
- This supports temporary caution and patching
- It does **not** yet justify permanent abandonment of the rebound lane

## Current Temporary Policy
- `CENTER_OVER` — promising, but still early sample
- `FORWARD_OVER` — high scrutiny
- `WING_UNDER` — temporary freeze based on repeated failure shape
- `LEAD_GUARD_UNDER / SCORING_WING_UNDER` — selectively playable with clean-role filters

## Tracker Fields to Add Going Forward
For every logged rebound play, include:
- archetype
- environment
- structure type
- source tag (`MODEL_NATIVE`, `HYBRID_CONFIRMED`, `EXTERNAL_SOURCE`)
- sample weight
- MPZ tags
- actual result
- realized ROI impact

## Promotion / Freeze Checklist
Before changing policy on any archetype, answer:
1. How many weighted samples exist?
2. Are they model-native or external?
3. Is the hit rate still strong after removing noisy structure effects?
4. Are misses hook losses or structural misses?
5. Is the environment consistent with upcoming slate conditions?

## Operational Summary
This framework exists to stop overreaction while still allowing fast adaptation. Small samples can justify a temporary patch, but larger weighted samples are required for permanent model policy changes.
