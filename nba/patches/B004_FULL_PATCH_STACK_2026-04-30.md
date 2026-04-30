# SharpEdge B.004 — Full Patch Stack Upgrade

## Patch Label
`B004_FULL_PATCH_STACK_2026-04-30`

## Activation Context
This patch stack is derived from the completed postmortem workflow covering:

- ORL @ DET Game 5
- TOR @ CLE Game 5
- HOU @ LAL Game 5
- Method-A single-fire diagnostic
- Rebound-only and full-NBA execution diagnostics

## Core Finding
The model edge is real, but deployment structure must protect it.

| Diagnostic | Result |
|---|---:|
| Rebounds-only Method-A hit rate | 53.40% |
| Rebounds-only Method-A ROI | +5.29% |
| Full NBA Method-A hit rate | 54.14% |
| Full NBA Method-A ROI | +5.74% |

Primary system leak:

> Multi-leg/parlay construction, shared rebound pools, and thin secondary legs are suppressing profitable single-leg edge.

---

# Patch Stack Overview

## 1. B.004 Single-Fire Default

### Rule
All qualified edges default to single-fire execution.

```python
if edge_pct >= 0.03:
    execution_type = "single_fire"
    allow_bet = True
```

### Purpose
Preserve true leg edge and avoid parlay wipeout risk.

---

## 2. Multi-Leg Restriction Gate

### Rule
2-leg cards are restricted. 3+ leg cards are boost-only.

```python
if number_of_legs == 2:
    allow_card = (
        all(leg.edge_pct >= 0.04 for leg in legs)
        and correlation_risk == "LOW"
        and shared_rebound_pool is False
        and no_thin_leg is True
    )

if number_of_legs >= 3:
    allow_card = (
        payout_boost is True
        and boost_adjusted_ev >= 0.05
        and correlation_risk != "HIGH"
        and no_thin_leg is True
    )
```

### Purpose
Stop profitable legs from being destroyed by fragile card construction.

---

## 3. Shared Rebound Pool Guard

### Trigger
Multiple rebound legs from the same game or same frontcourt ecosystem.

```python
if market == "rebounds" and same_game_card and same_game_rebound_legs >= 2:
    if shared_rebound_pool:
        card_allowed = False
        tag = "SHARED_REBOUND_POOL_BLOCK"
```

### Purpose
Prevent same-game rebound legs from competing for the same missed-shot supply.

---

## 4. Secondary Rebounder Downgrade

### Rule
```python
if player_role == "secondary_rebounder" and rebound_chances_shared:
    downgrade_prob -= 0.04
```

### Purpose
Reduce overconfidence on players who need leftovers from the same rebound ecosystem.

---

## 5. Low-Minute Cap

### Rule
```python
if projected_minutes < 20:
    pred_prob = min(pred_prob, 0.55)
```

### Purpose
Protect against high rate / low minute volatility.

---

## 6. High-Usage Rebound Suppressor

### Rule
```python
if usage_rate > 30 and player_role in ["primary_ball_handler", "primary_scorer"]:
    rebound_prob -= 0.04
```

### Origin
Cade Cunningham missed O6.5 rebounds while scoring 45 points with extreme usage.

### Purpose
Primary scorers can lose rebounding path when shot creation load spikes.

---

## 7. Wing Rebound Redistribution Boost

### Rule
```python
if primary_center_boxed_out and team_survival_spot:
    if player_role in ["high_minute_wing", "athletic_forward"]:
        rebound_prob += 0.05
```

### Origin
Ausar Thompson 15 rebounds vs ORL after Duren box-out suppression.

### Purpose
Capture redistribution when centers are boxed out and wings crash hard.

---

## 8. Primary Forward Role Expansion Boost

### Rule
```python
if frontcourt_teammate_out and player_role == "primary_forward":
    rebound_prob += 0.03
```

### Origin
Paolo Banchero hit O7.5 rebounds with Franz Wagner unavailable/questionable.

### Purpose
Avoid over-downgrading primary forwards in expanded role environments.

---

## 9. Trap Tiering System

### Rule
Trap tags must be tiered as hard traps or soft traps.

```python
if trap_detected:
    if rebound_line <= 4.5 and player_rebound_rate_strong:
        trap_type = "SOFT_TRAP"
        pred_prob = min(pred_prob, 0.56)
    else:
        trap_type = "HARD_TRAP"
        skip_bet = True
```

### Origin
Duren hard trap was correct. Poeltl low-line trap failed.

### Purpose
Low lines should not be full fades when player per-minute rebound rate remains strong.

---

## 10. Two-Big Split Volatility Penalty

### Rule
```python
if team_has_two_primary_bigs and player_minutes < 30:
    rebound_prob -= 0.04
```

### Origin
Mobley hit while Jarrett Allen collapsed to 3 rebounds.

### Purpose
Avoid duplicating confidence across two frontcourt rebounders.

---

## 11. Long-Rebound Guard Trap Override

### Rule
```python
if opponent_three_point_attempt_rate_high and player_minutes >= 35:
    guard_rebound_trap = False
```

### Origin
Harden and Mitchell cleared rebound lines despite trap tags.

### Purpose
High 3PA environments generate long-board paths for guards.

---

## 12. Total Under Kill Switch

### Rule
```python
if both_teams_projected_3pa_high and transition_points_profile_active:
    under_confidence -= 0.05
```

### Origin
TOR/CLE under failed as game reached 245 points.

### Purpose
Prevent under bets when pace/transition/3PA profile is live.

---

## 13. Hook-Zone Center Volatility Penalty

### Rule
```python
if market == "rebounds" and player_position == "C" and line_delta <= 1.5:
    if opponent_center_oreb_dominance_active:
        rebound_prob -= 0.04
```

### Origin
Sengun missed O9.5 by hook with 9 rebounds.

### Purpose
Protect against center props that need one extra bounce in hostile board environments.

---

## 14. Opponent Big Dominance Suppressor

### Rule
```python
if opponent_big_oreb >= 6 or opponent_big_reb_share_spike:
    center_rebound_prob -= 0.04
```

### Origin
Ayton produced 17 rebounds and 10 offensive rebounds, suppressing HOU frontcourt overs.

### Purpose
Live or projected opposing-big dominance reduces center rebound ceiling.

---

## 15. Perimeter Volume Center OREB Suppressor

### Rule
```python
if team_3pa_rate_high and center_oreb_path_required:
    center_rebound_prob -= 0.03
```

### Origin
Houston attempted 40 threes, reducing Sengun's interior OREB path.

### Purpose
Heavy 3PA teams create long rebounds that centers do not reliably collect.

---

## 16. LeBron / Secondary Star Role Suppressor

### Rule
```python
if dominant_big_glass_role_active and player_role == "primary_creator_forward":
    rebound_prob -= 0.05
```

### Origin
LeBron finished with only 3 rebounds while Ayton grabbed 17.

### Purpose
When a dominant big owns the glass, high-usage creators can lose rebound involvement.

---

## 17. Edge Threshold Skip Rule

### Rule
```python
if edge_pct < 0.03:
    skip_bet = True
```

### Purpose
No thin-edge entries. Protect bankroll and reduce noise.

---

# Final B.004 Bet Qualification Flow

```python
def qualify_bet(edge):
    if edge.edge_pct < 0.03:
        return "SKIP_THIN_EDGE"

    if edge.projected_minutes < 20:
        edge.pred_prob = min(edge.pred_prob, 0.55)

    if edge.market == "rebounds":
        apply_rebound_patch_stack(edge)

    if edge.pred_prob < edge.market_implied_prob + 0.03:
        return "SKIP_NO_REAL_EDGE"

    return "SINGLE_FIRE_APPROVED"
```

---

# Final B.004 Card Qualification Flow

```python
def qualify_card(legs, payout_boost=False):
    if len(legs) == 1:
        return qualify_bet(legs[0]) == "SINGLE_FIRE_APPROVED"

    if len(legs) == 2:
        return (
            all(leg.edge_pct >= 0.04 for leg in legs)
            and not has_shared_rebound_pool(legs)
            and correlation_risk(legs) == "LOW"
            and not has_thin_leg(legs)
        )

    if len(legs) >= 3:
        return (
            payout_boost
            and boost_adjusted_ev(legs) >= 0.05
            and correlation_risk(legs) != "HIGH"
            and not has_thin_leg(legs)
        )
```

---

# Deployment Notes

## Primary Execution Identity
`B004_SINGLE_FIRE_DEFAULT`

## Restricted Modes
- `B004_TWO_LEG_RESTRICTED`
- `B004_THREE_PLUS_BOOST_ONLY`

## New Diagnostic Tags
- `SHARED_REBOUND_POOL_BLOCK`
- `HIGH_USAGE_REBOUND_SUPPRESSION`
- `WING_REBOUND_REDISTRIBUTION`
- `PRIMARY_FORWARD_ROLE_EXPANSION`
- `SOFT_TRAP_LOW_LINE`
- `HARD_TRAP_CONFIRMED`
- `TWO_BIG_SPLIT_VOLATILITY`
- `LONG_REBOUND_GUARD_OVERRIDE`
- `TOTAL_UNDER_KILL_SWITCH`
- `HOOK_ZONE_CENTER_VOLATILITY`
- `OPPONENT_BIG_DOMINANCE_SUPPRESSOR`
- `PERIMETER_VOLUME_CENTER_SUPPRESSOR`

---

# Status
Patch stack logged. B.004 is now the active SharpEdge execution framework for NBA rebound and mixed-market deployment.
