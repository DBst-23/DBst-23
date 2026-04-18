# TRACKING OUTAGE REBOUND PROTOCOL

## Purpose

This protocol defines the SharpEdge fallback workflow for NBA rebound analysis when NBA tracking data is unavailable. It is specifically designed to keep rebound edge-hunting operational during outages affecting player rebound tracking, rebound chances, contested rebound data, and team box-out metrics.

This protocol does **not** attempt to recreate missing tracking metrics one-for-one. Instead, it reweights the workflow toward structural proxy signals that preserve discipline, edge quality, and execution standards.

---

## Trigger Condition

Activate this protocol when one or more of the following are unavailable:

- Player rebound tracking
- Rebound chances
- Contested rebounds
- Adjusted rebound chance percentage
- Team box-outs
- Other NBA Stats tracking-derived rebound data

When active, the rebound workflow shifts from **tracking-first** to **minutes-and-structure-first**.

---

## Core Rule

### Rebounds are estimated through:

`Rebounds ≈ Minutes × Rebound Rate × Opportunity Environment`

When tracking is unavailable:

- **Minutes** become the primary input
- **Role stability** becomes the secondary input
- **Opportunity environment** is inferred through proxy team and lineup data

---

## Priority Signal Stack

### Tier 1 — Mandatory Inputs

These are required before any pregame rebound investment is considered:

1. **Projected Minutes**
   - Primary opportunity driver
   - Prefer multiple-source validation when possible
   - Minutes uncertainty is treated as a major downgrade

2. **Confirmed / Expected Lineup**
   - Identify rebound-share competition
   - Flag shared frontcourt ecology
   - Track starter vs bench impact on rebound distribution

3. **Role Stability**
   - Stable starter
   - Volatile starter
   - Bench big threat
   - Fragile rotation role

4. **Injury Context**
   - Questionable bigs
   - Soft minute caps
   - Return-from-injury suppression risk

---

### Tier 2 — Preferred Proxy Inputs

These replace lost tracking-derived rebound signals as best as possible:

1. **Recent Rebound Outcomes**
   - L5
   - L10
   - Similar-minute games
   - Starter-only or role-specific samples

2. **Per-36 / Per-100 Rebound Rates**
   - Use to estimate sustainable rebound ceiling and baseline
   - Treat small-sample spikes with caution

3. **Team Rebound Environment**
   - Team rebound differential
   - Opponent rebounds allowed
   - Opponent rebounds allowed by position if available
   - Offensive rebound percentage allowed
   - Defensive rebound percentage allowed

4. **Frontcourt Concentration**
   - Estimate how rebounds are split across center / PF / wing
   - Downgrade overs when rebound share is diluted

5. **Second-Chance Profile**
   - Second-chance points for / against as a supporting proxy
   - Offensive rebounding style inference

---

### Tier 3 — Market Inputs

Use only after structural inputs are evaluated:

1. **Kalshi implied probability**
2. **Book odds / alt ladder pricing**
3. **Line movement**
4. **Third-party model outputs (support only, not authority)**

Market price can strengthen a read, but cannot rescue weak structure.

---

## Data Source Hierarchy During Outage

### Primary Fallback Sources

1. **Projected Minutes Providers**
   - Linestar
   - Other trusted DFS projection sources

2. **StatMuse**
   - Recent rebounds
   - Similar-game trends
   - Team rebound allowance queries
   - Role-based snapshots

3. **Basketball Reference / Game Logs**
   - Minutes trends
   - Game-by-game rebound outcomes
   - Starter and bench role validation

4. **Cleaning the Glass / Team Context Sources**
   - Team rebound profile
   - Offensive / defensive rebound tendencies
   - Team ecology support

5. **Rotowire / Injury and Depth Chart Feeds**
   - Status changes
   - Starter confirmation
   - Minute cap signals

6. **SharpEdge GitHub Logbook**
   - Postmortems
   - Archetype tags
   - Historical hit/miss patterns
   - Prior structural failures and validations

---

## Archetype Rules During Tracking Outage

### Green Zone

1. **Center Overs**
   - Only if projected minutes are stable
   - Only if rebound-share competition is manageable
   - Only if injury suppression is low

### Yellow Zone

2. **Forward Overs**
   - Require clear reason
   - Require stable minutes
   - Must not be heavily center-share dependent

3. **Low-Threshold Guard / Wing Ladders**
   - Only when minutes are stable and price is clearly favorable
   - Never force at inflated prices

### Red Zone

4. **Wing Unders / Volatile Shared Rebound Roles**
   - Avoid during outage unless overwhelming structural support exists

5. **Injury-Compromised Center Overs**
   - Avoid unless official confirmation removes restriction concerns and price remains favorable

---

## Pregame Checklist

Before any rebound bet is approved during outage mode, confirm:

- [ ] Projected minutes are stable
- [ ] Lineup is confirmed or strongly projected
- [ ] Rebound share competition is understood
- [ ] Injury suppression risk is acceptable
- [ ] Recent role-consistent outcomes are supportive
- [ ] Market price is favorable relative to estimated probability
- [ ] Bet is not relying on missing tracking data to justify itself

If any of the above are unclear, the default action is:

### PASS

---

## Execution Rule

### No clean structure = no pregame rebound investment.

If the outage removes too much confidence and the remaining proxy stack does not produce a clear edge, no bet is made.

Preserving bankroll and edge quality takes priority over forcing action.

---

## Live-Flow Adjustment

When pregame rebound structure is not clean due to outage conditions:

- prefer **no pregame rebound exposure**
- re-evaluate live only if:
  - minutes are normal
  - role is confirmed in-game
  - rebound participation is visible through box score and rotation behavior

Live opportunities may be cleaner than pregame during tracking outages.

---

## Logging Requirement

When this protocol is used, log the slate or decision under a label such as:

- `TRACKING_OUTAGE_MODE_ACTIVE`
- `REBOUND_PROTOCOL_FALLBACK`
- `MINUTES_FIRST_MODE`

This ensures future postmortems can separate outage-mode decisions from full-data decisions.

---

## Summary Principle

### Do not replace missing tracking data with false confidence.

Instead:

- tighten thresholds
- trust minutes and structure more heavily
- downgrade fragile archetypes
- demand better prices
- pass more often when the board is unclear

This protocol keeps SharpEdge operational without pretending the environment is unchanged.
