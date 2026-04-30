# SharpEdge NBA B.003 — Rolling / Expanding Window Model Validation Protocol

## Objective
Build a strict out-of-sample NBA model validation workflow that trains on prior seasons or partial seasons, predicts only future games, evaluates betting performance, and slices results by situational context.

This protocol is designed to prevent overfitting and convert postmortems, market snapshots, and model predictions into a repeatable betting research pipeline.

---

## Core Principle
No game may be used for training if it occurs on or after the prediction date.

Every prediction must be generated as if the game has not happened yet.

---

## Data Sources

### Internal SharpEdge Inputs
- Pregame simulation logs
- LiveFlow logs
- Final card market locks
- MPZ tracker entries
- Postmortems
- Player rebound tracking
- Lineup rotation data
- Team shot distribution datasets
- Series matchup notes
- Market snapshots and closing line records

### External / Enrichment Inputs
- Injuries and expected lineups
- Projected minutes
- Market odds and line movement
- Team and player historical stats
- H2H regular-season matchups
- Playoff series splits

---

## Validation Modes

### 1. Expanding Window
Train on all data before a cutoff date, then predict the next game or next slate.

Example:
- Train: 2024-25 full season + 2025-26 games through 2026-03-31
- Test: 2026-04-01 through 2026-04-07
- Then expand training through 2026-04-07 and repeat

Use when the model benefits from long-term role baselines.

### 2. Rolling Window
Train only on the most recent N games, then predict future games.

Recommended windows:
- 10-game rolling player window
- 20-game rolling player window
- 30-game rolling team/context window
- Series-only playoff micro-window

Use when recent form, rotation change, injury impact, or playoff adjustment is more important than season average.

### 3. Hybrid Weighted Window
Blend long-term baseline with short-term recent form.

Recommended default weighting:
- 45% season baseline
- 30% last 10 games
- 15% H2H matchup data
- 10% current series/postmortem adjustment

For playoff games:
- 35% season baseline
- 25% H2H regular season
- 25% current series
- 15% postmortem tactical adjustment

---

## Required Prediction Record
Every predicted edge should be stored with this schema:

```json
{
  "prediction_id": "B003_YYYYMMDD_GAME_PLAYER_MARKET",
  "prediction_date": "YYYY-MM-DD",
  "game_id": "TEAM_TEAM_YYYYMMDD",
  "player": "Player Name",
  "team": "TEAM",
  "opponent": "OPP",
  "market": "rebounds",
  "line": 8.5,
  "side": "over",
  "market_price": -120,
  "model_mean": 9.6,
  "model_median": 9.2,
  "model_probability": 0.602,
  "market_implied_probability": 0.545,
  "edge_pct": 0.057,
  "confidence_tier": "Tier 2",
  "window_type": "hybrid_weighted",
  "training_cutoff": "YYYY-MM-DD",
  "features_used": [],
  "postmortem_tags_used": [],
  "result": null,
  "actual_value": null,
  "hit": null,
  "closing_line": null,
  "clv": null,
  "mpz_tags": []
}
```

---

## Evaluation Metrics

### Prediction Accuracy
- Hit rate
- Mean absolute error
- Median absolute error
- Calibration by probability bucket
- Brier score

### Betting Performance
- ROI
- Units won/lost
- Expected value vs realized value
- CLV by market
- Edge bucket performance
- Single vs 2-leg card performance

### Distribution Quality
- Mean vs actual
- Median vs actual
- Tail miss frequency
- Under/over directional bias
- Blowout sensitivity miss rate

---

## Situational Subsets
Evaluate each model window by these subsets:

### Game Context
- Home / away
- Favorite / underdog
- Spread buckets: 0-3, 3.5-6.5, 7-10.5, 11+
- Total buckets: low, mid, high
- Blowout vs competitive outcome
- Rest advantage / disadvantage

### Season Context
- Early season
- Midseason
- Post All-Star
- Play-in / playoffs
- Game 1 of series
- Games 2-4 adjustment window
- Elimination games

### Opponent Quality
- Strong rebounding team
- Weak rebounding team
- Strong defense
- Weak defense
- Size advantage / disadvantage
- Switch-heavy defense
- Paint-collapse defense

### Player Role Context
- Stable starter minutes
- Foul-risk big
- Rebound-owner profile
- Wing rebound spike
- Guard long-board profile
- Minutes cap risk
- Blowout-safe role
- Bench volatility

---

## Postmortem Integration Rules
Postmortems should not directly overwrite model outputs. They should create structured adjustment tags.

Examples:
- STRUCTURAL_GLASS_EDGE
- CENTER_DISPLACEMENT_RISK_ON
- BENCH_BIG_MINUTES_SPIKE
- PAINT_COLLAPSE_SUPPRESSION
- SERIES_ADJUSTMENT_NEGATIVE
- SERIES_ADJUSTMENT_POSITIVE
- BLOWOUT_MINUTES_RISK
- REBOUND_OWNER_PROFILE
- FAKE_VOLUME_WARNING

Each tag must have:
- source game
- evidence
- affected player/team
- adjustment direction
- expiration rule

---

## Anti-Overfitting Rules
1. No future data leakage.
2. No same-game result data in feature generation.
3. Postmortem tags only apply after the game has been logged.
4. Series data must be timestamped by game number.
5. Do not tune thresholds on the same sample used for final scoring.
6. Track no-call zones separately from active edge calls.
7. Grade only EDGE_CALL_ACTIVE predictions in betting ROI.

---

## First Implementation Target
Build a runner that can:
1. Load historical predictions and outcomes.
2. Split by rolling or expanding date windows.
3. Train a simple baseline model.
4. Predict next slate/player props.
5. Evaluate out-of-sample results.
6. Output subset diagnostics.

Suggested file:
`nba/model_validation/rolling_window_runner.py`

---

## Immediate Next Step
Create `rolling_window_runner.py` with baseline functionality for:
- CSV/JSON input
- date-based expanding-window split
- player-market prediction rows
- evaluation report
- subset grouping

