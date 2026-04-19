# HALFTIME_ENVIRONMENT_CLASSIFIER

## Purpose
Classify halftime NBA LiveFlow environments as either:
- `REAL_INFLATION`
- `FAKE_INFLATION`
- `REAL_SUPPRESSION`
- `FAKE_SUPPRESSION`
- `MIXED_NO_FIRE`

This module is designed to stop weak halftime fades and improve continuation detection for totals, spreads, and team totals.

---

## Core Definitions

### REAL_INFLATION
The halftime market is higher than pregame because the game environment is sustainably strong.

Typical traits:
- Multiple scorers active
- Ball movement supports scoring continuation
- Trailing side still has offensive viability
- Efficiency is elevated but not dependent on one fragile outlier
- Pace / possession ecology can support further scoring

### FAKE_INFLATION
The halftime market is higher than pregame, but the score is being held up by unstable inputs.

Typical traits:
- Extreme 3PT variance
- One-sided FT spike
- Unsustainably low turnover drag despite fragile creation
- Poor rebound/possession support
- One player carrying too much of the load

### REAL_SUPPRESSION
The halftime market is lower than pregame because the game is genuinely slow or structurally suppressed.

Typical traits:
- Half-court density
- Few transition chances
- Stable defensive control
- Rebound environment not creating extra possessions
- Low foul volume and weak rim pressure

### FAKE_SUPPRESSION
The halftime market is lower than pregame, but the score is artificially low due to unstable misses rather than a true slow environment.

Typical traits:
- Open looks missed
- Star players underperforming on makeable volume
- Pace remains viable
- Rebounding and extra possessions are present
- Shot profile suggests positive scoring regression

### MIXED_NO_FIRE
Signals conflict too heavily for a clean edge.

---

## Inputs Required
- Pregame closing spread
- Pregame closing total
- Halftime score
- Halftime live spread
- Halftime live total
- Team totals if available
- Team shooting splits
- Team rebound profile
- Offensive rebounds
- Assists / ball movement
- Foul / FT context
- Turnovers
- Leading scorers and distribution profile
- Optional: starter minutes, foul trouble, rebound trigger notes

---

## Classification Logic

### Step 1: Measure repricing
- `inflation_delta = halftime_live_total - closing_total`
- `spread_delta = halftime_live_spread - closing_spread`

### Step 2: Evaluate sustainability
Use the following lenses:

#### A. Scoring distribution
- 3+ players in double figures by half → supports continuation
- Single-player carry job → more fragile

#### B. Assist integrity
- High assist rate / connected offense → supports continuation
- Low assist rate + hot shooting → points to fake inflation

#### C. Free throw distortion
- One side living at the line can inflate scoring artificially
- If whistle dependence is extreme, downgrade continuation confidence

#### D. 3PT dependence
- Extreme first-half 3PT numbers without supporting shot quality can indicate fake inflation

#### E. Rebound / possession ecology
- Offensive rebounds, total rebound edge, second-chance points, turnovers forced
- Extra possession support makes continuation more believable

#### F. Trailing team viability
- If trailing team can still score, totals and continuation angles stay alive
- If trailing team is collapsing, inflation is less trustworthy

---

## Decision Output Schema
```json
{
  "halftime_environment": {
    "type": "REAL_INFLATION",
    "confidence": 0.74,
    "notes": [
      "multi-source offense confirmed",
      "trailing side still viable",
      "inflation supported by assist structure"
    ]
  }
}
```

---

## Action Rules

### If `REAL_INFLATION`
- Do **not** auto-fade the total
- Spread continuation remains eligible
- Team-total overs remain in play if lead/control is real

### If `FAKE_INFLATION`
- Totals under become more attractive
- Team-total overs should be treated with caution
- Spread continuation requires stronger possession proof

### If `REAL_SUPPRESSION`
- Avoid blind over buys
- Lean into unders / favorite control if supported

### If `FAKE_SUPPRESSION`
- Look for live over recovery
- Consider trailing-side buyback if offensive process is intact

### If `MIXED_NO_FIRE`
- No single-fire activation

---

## Calibration Anchors

### Example: TOR @ CLE — 2026-04-18
Classification:
- `REAL_INFLATION`

Why:
- Cleveland offensive structure was scalable
- Toronto kept enough scoring pressure alive
- Spread, team totals, and total all continued successfully

This is a benchmark case for continuation environments.

---

## Intended Integrations
- `summary_engine`
- `auto_adjuster`
- `LIVEFLOW_OUTAGE_SUMMARY.json`
- rebound gate decision context
- future halftime trigger classifier scripts
