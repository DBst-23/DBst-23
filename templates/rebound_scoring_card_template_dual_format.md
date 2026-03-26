# SharpEdge Rebound Scoring Card Template — Dual Format

This file contains:
1. A reusable markdown scoring-card template for manual use
2. A reusable JSON template for logging, automation, and GitHub postmortem workflows

---

## Markdown Template

```markdown
# SHARPEDGE REBOUND SCORING CARD — V1

## 1) Bet Info
- Player:
- Team:
- Opponent:
- Line:
- Direction: Higher / Lower
- Book / Multiplier:
- Game Time:

## 2) Core Projection Block
- Projected Minutes:
- Model Mean Rebounds:
- Model Median Rebounds:
- Floor (25th pct):
- Ceiling (75th pct):
- Hit Probability:
- Fair Price:
- Edge vs Line:

## 3) Tracking Rebound Profile
- Recent REB per game:
- Recent rebound chances:
- Recent rebound chance %:
- Adjusted rebound chance %:
- Contested rebounds:
- Contested rebound %:
- Avg rebound distance:
- Deferred rebound chances:

## 4) Role + Minutes Stability
- Expected starter? Yes / No
- Minutes stability: Strong / Medium / Fragile
- Rotation risk: Low / Medium / High
- Blowout risk: Low / Medium / High
- Foul risk: Low / Medium / High
- Usage/role notes:

## 5) Environment Score
- Opponent rebound environment: Strong / Neutral / Weak
- Teammate competition for boards: Low / Medium / High
- Center/big availability impact:
- Injury boost / suppression:
- Pace impact:
- Shot profile environment: More misses / Neutral / Efficient shooting risk
- Box-out environment: Favorable / Neutral / Unfavorable

## 6) Matchup Logic
- Why this line is attackable:
- Primary path to win:
- Primary failure condition:
- Does line align with tracking data? Yes / No
- Does line align with projected minutes? Yes / No
- Does line align with role? Yes / No

## 7) Final Score
- Minutes security: /5
- Tracking support: /5
- Matchup environment: /5
- Injury/rotation edge: /5
- Line value: /5
- Volatility control: /5

**Total Score:** /30

## 8) Decision Tier
- 26–30: 🔒 Strong play
- 21–25: ✅ Playable edge
- 16–20: ⚠️ Thin / only if needed
- 15 or less: ❌ Pass

## 9) Final Card Output
- Official read:
- Confidence tier:
- Best supporting stat:
- Biggest concern:
- Postmortem tag placeholder:
```

---

## JSON Template

```json
{
  "template_version": "SharpEdge_Rebound_Scoring_Card_v1",
  "bet_info": {
    "player": "",
    "team": "",
    "opponent": "",
    "line": 0,
    "direction": "Higher",
    "book_multiplier": "",
    "game_time": ""
  },
  "core_projection_block": {
    "projected_minutes": 0,
    "model_mean_rebounds": 0,
    "model_median_rebounds": 0,
    "floor_25_pct": 0,
    "ceiling_75_pct": 0,
    "hit_probability": 0,
    "fair_price": "",
    "edge_vs_line": 0
  },
  "tracking_rebound_profile": {
    "recent_reb_per_game": 0,
    "recent_rebound_chances": 0,
    "recent_rebound_chance_pct": 0,
    "adjusted_rebound_chance_pct": 0,
    "contested_rebounds": 0,
    "contested_rebound_pct": 0,
    "avg_rebound_distance": 0,
    "deferred_rebound_chances": 0
  },
  "role_minutes_stability": {
    "expected_starter": false,
    "minutes_stability": "",
    "rotation_risk": "",
    "blowout_risk": "",
    "foul_risk": "",
    "usage_role_notes": ""
  },
  "environment_score": {
    "opponent_rebound_environment": "",
    "teammate_competition_for_boards": "",
    "center_big_availability_impact": "",
    "injury_boost_or_suppression": "",
    "pace_impact": "",
    "shot_profile_environment": "",
    "box_out_environment": ""
  },
  "matchup_logic": {
    "why_line_is_attackable": "",
    "primary_path_to_win": "",
    "primary_failure_condition": "",
    "line_aligns_with_tracking_data": false,
    "line_aligns_with_projected_minutes": false,
    "line_aligns_with_role": false
  },
  "final_score": {
    "minutes_security": 0,
    "tracking_support": 0,
    "matchup_environment": 0,
    "injury_rotation_edge": 0,
    "line_value": 0,
    "volatility_control": 0,
    "total_score": 0
  },
  "decision_tier": "",
  "final_card_output": {
    "official_read": "",
    "confidence_tier": "",
    "best_supporting_stat": "",
    "biggest_concern": "",
    "postmortem_tag_placeholder": ""
  }
}
```

---

## Fast-Use Compact Template

```markdown
Player:
Line:
Direction:
Projected Minutes:
Mean:
Median:
Recent REB:
REB Chances:
Adj REB Chance%:
Contested REB:
Environment:
Rotation Risk:
Main Edge:
Main Risk:
Score: /30
Tier:
Official Read:
```
