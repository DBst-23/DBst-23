# NBA Postmortem + Patch Log
## MIA @ CHA — 2026-04-14

### Invested cards settled

#### Card A — Late boosted 3-leg under card
- Stake: $10.00
- To win: $64.70
- Boost: 40% Play-In Boost
- Legs:
  - LaMelo Ball under 5.5 rebounds ✅ (5)
  - Brandon Miller under 5.5 rebounds ✅ (5)
  - Andrew Wiggins under 4.5 rebounds ❌ (6)
- Result: Loss
- Failure type: one-leg miss / concentrated under exposure

#### Card B — 3-leg under card
- Stake: $5.50
- To win: $23.37
- Legs:
  - Brandon Miller under 5.5 rebounds ✅ (5)
  - LaMelo Ball under 5.5 rebounds ✅ (5)
  - Andrew Wiggins under 4.5 rebounds ❌ (7)
- Result: Loss
- Failure type: one-leg miss / repeated fragile leg

#### Card C — 3-leg mixed rebound card
- Stake: $10.00
- To win: $32.18
- Legs:
  - LaMelo Ball under 5.5 rebounds ✅ (5)
  - Andrew Wiggins under 4.5 rebounds ❌ (7)
  - Moussa Diabate over 8.5 rebounds ✅ (14)
- Result: Loss
- Failure type: one-leg miss / repeated fragile leg

### Final game result
- Final/OT: Hornets 127, Heat 126
- OT occurred: Yes
- Team rebounds:
  - Miami 48
  - Charlotte 54
- Offensive rebounds:
  - Miami 12
  - Charlotte 17
- Second chance points:
  - Miami 20
  - Charlotte 25

### Key player results tied to our positions
- Andrew Wiggins: 7 rebounds in 42 minutes ❌ vs under 4.5
- LaMelo Ball: 5 rebounds in 40 minutes ✅ vs under 5.5
- Brandon Miller: 5 rebounds in 37 minutes ✅ vs under 5.5
- Moussa Diabate: 14 rebounds in 36 minutes ✅ vs over 8.5

### MPZ tagging
- EDGE_CALL_ACTIVE
- MISS_REGISTERED: WING_UNDER_FRAGILITY_FAILURE
- MISS_REGISTERED: SINGLE_LEG_CONCENTRATION_BURN
- MISS_REGISTERED: OT_INFLATION_BURN
- MISS_REGISTERED: PORTFOLIO_CHOKE_LEG
- HIT_REGISTERED: LAMELO_REBOUND_UNDER_HIT
- HIT_REGISTERED: BRANDON_MILLER_REBOUND_UNDER_HIT
- HIT_REGISTERED: DIABATE_REBOUND_OVER_HIT

### Core postmortem read
The read on Charlotte primary wing rebound suppression was mostly right. Ball and Miller both stayed under. The portfolio failed because Andrew Wiggins under 4.5 rebounds was reused across multiple cards and the game environment turned hostile to fragile unders.

The main killers were:
1. Overtime extension added extra rebound volume.
2. Charlotte generated 17 offensive rebounds, increasing chaos and repeat rebound chances.
3. Wiggins played 42 minutes in a one-possession game and landed on 7 rebounds.
4. Exposure architecture was poor because the same fragile leg was repeated across the portfolio.

### Live system patch applied
This log corresponds to the following patch intent:
- Block repeated fragile rebound-under legs across multiple cards.
- Penalize wing rebound unders at 4.5 and 5.5 in close/high-volume environments.
- Add OT sensitivity penalty to under props.
- Enforce portfolio dependency checks before card approval.

### Patch summary
- WING_UNDER_FRAGILITY_GATE: ON
- CARD_CORRELATION_WARNING: ON
- OT_SENSITIVITY_OVERLAY: ON
- PORTFOLIO_DEPENDENCY_CHECK: ON

### Operational conclusion
The model found valid player-level reads on Ball and Miller. The portfolio construction failed by allowing repeated dependence on one fragile leg. Future cards should avoid duplicating the same wing rebound under across multiple slips, especially in close games with rebound-extended environments.
