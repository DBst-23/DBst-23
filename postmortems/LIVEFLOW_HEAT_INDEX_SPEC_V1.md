# LIVEFLOW_HEAT_INDEX_SPEC_V1

## Purpose
The **LiveFlow Heat Index** is a SharpEdge module designed to detect when a live total is being inflated by **temporary shooting heat** rather than a truly sustainable scoring environment.

Its job is to answer:

- Is this a **real continuation** game?
- Or is this a **fake-over / heat-fade under** spot?

This module is intended for halftime and in-game total reassessment, especially when books aggressively reprice a live total after an abnormally hot first half.

---

## Core Output
For every live checkpoint, the module should return:

- **Heat Index Score:** `0–100`
- **Classification**
  - `COOL`
  - `WARM`
  - `HOT`
  - `EXTREME_HEAT`
- **Action Tag**
  - `NO_EDGE`
  - `WATCH_UNDER`
  - `UNDER_TRIGGER`
  - `DO_NOT_FADE`

---

## High-Level Philosophy
The model should distinguish between:

### 1. **Cosmetic Inflation**
A live total rises because:
- both teams are shooting far above sustainable levels
- turnovers are low
- offensive rebound volume is modest
- foul pressure is not extreme
- pace is not truly chaotic

This is usually an **under-fade candidate**.

### 2. **Real Continuation**
A live total rises because:
- multiple scorers are stable
- assist structure is strong
- pace and transition volume are high
- free-throw ecology is active
- offensive rebound pressure is extending possessions

This is **not** an auto-under spot.

---

## Component Scores

### 1. Shooting Heat Score
Measures how far current efficiency is above sustainable expectation.

#### Inputs
- current FG%
- current 3P%
- current FT%
- expected FG%
- expected 3P%
- expected FT%

#### Suggested Formula
```python
fg_delta = current_fg - expected_fg
tp_delta = current_3p - expected_3p
ft_delta = current_ft - expected_ft

shooting_heat_score = (
    max(0, fg_delta) * 0.8 +
    max(0, tp_delta) * 1.4 +
    max(0, ft_delta) * 0.3
)
```

#### Notes
- 3P delta should carry the highest weight
- FT inflation matters, but should not dominate the signal

---

### 2. Pace Support Score
Measures whether the game environment actually supports a high total through volume.

#### Inputs
- possessions pace estimate
- offensive rebounds
- turnovers
- fastbreak points
- FTA rate

#### Suggested Formula
```python
pace_support_score = (
    pace_z * 1.2 +
    oreb_z * 0.8 +
    fta_rate_z * 0.7 +
    fastbreak_z * 0.6
)
```

#### Interpretation
High pace + high OREB + high FTA = total can sustain more easily.

If pace support is low, then elite scoring is more likely **heat-based**.

---

### 3. Clean Possession Penalty
If both teams are scoring efficiently with:
- low turnovers
- modest OREB
- no whistle chaos

then the total may be inflated by **accuracy**, not ecology.

#### Suggested Logic
```python
clean_possession_penalty = 0
if turnovers_total <= 10:
    clean_possession_penalty += 8
if oreb_total <= 10:
    clean_possession_penalty += 6
if fta_total <= 20:
    clean_possession_penalty += 5
```

---

### 4. Market Inflation Score
Measures how far the live total has moved beyond the pregame baseline.

#### Inputs
- closing total
- live total
- current score
- time remaining

#### Suggested Logic
```python
market_inflation = live_total - closing_total
market_inflation_score = max(0, market_inflation) * 2.0
```

Add a bonus if the live total implies an unrealistically high remaining scoring pace:

```python
required_remaining_points = live_total - current_total
required_ppm = required_remaining_points / minutes_remaining
```

```python
if required_ppm > baseline_ppm + 0.25:
    market_inflation_score += 10
```

---

### 5. Star Sustainability Offset
If stars are driving the game in a stable, scalable way, the model should avoid auto-fading a hot total.

#### Inputs
- top scorers count
- usage stability
- assist structure
- shot profile quality
- pace support context

#### Suggested Logic
```python
star_sustainability_offset = 0
if primary_scorers_count >= 3:
    star_sustainability_offset += 8
if assist_rate_delta >= 0:
    star_sustainability_offset += 5
if pace_support_score >= 12:
    star_sustainability_offset += 5
```

This protects the model from false under triggers in **real continuation** games.

---

## Final Formula
```python
heat_index = (
    shooting_heat_score +
    market_inflation_score +
    clean_possession_penalty -
    pace_support_score -
    star_sustainability_offset
)
```

Clamp the score:

```python
heat_index = max(0, min(100, round(heat_index)))
```

---

## Classification Thresholds
```python
if heat_index < 25:
    classification = "COOL"
    action_tag = "NO_EDGE"
elif heat_index < 45:
    classification = "WARM"
    action_tag = "WATCH_UNDER"
elif heat_index < 65:
    classification = "HOT"
    action_tag = "UNDER_TRIGGER"
else:
    classification = "EXTREME_HEAT"
    action_tag = "UNDER_TRIGGER"
```

### Override Rule
If the game has:
- elite pace support
- multiple stable scorers
- strong foul ecology

then override the under trigger:

```python
if pace_support_score >= 14 and primary_scorers_count >= 3 and free_throw_attempts_total >= 20:
    action_tag = "DO_NOT_FADE"
```

---

## Example Case: MIN @ DEN Halftime
### Observed Halftime Conditions
- both teams at **64**
- both teams at **50% from three**
- elite TS%
- low turnover chaos
- modest offensive rebound pressure
- live total jumped to **245.5**

### Expected Module Output
- **Heat Index:** ~61–68
- **Classification:** `HOT` or `EXTREME_HEAT`
- **Action Tag:** `UNDER_TRIGGER`

### Outcome Validation
- final total: **233**
- live under 245.5: ✅ WIN

This case should be retained as a benchmark example of **halftime heat-fade inflation**.

---

## Python Module Shell
Suggested file path:

`modules/liveflow_heat_index.py`

```python
from dataclasses import dataclass


@dataclass
class LiveFlowHeatInput:
    closing_total: float
    live_total: float
    current_total: int
    minutes_remaining: float

    current_fg_pct: float
    current_3p_pct: float
    current_ft_pct: float

    expected_fg_pct: float
    expected_3p_pct: float
    expected_ft_pct: float

    turnovers_total: int
    offensive_rebounds_total: int
    free_throw_attempts_total: int
    fastbreak_points_total: int

    pace_z: float = 0.0
    oreb_z: float = 0.0
    fta_rate_z: float = 0.0
    fastbreak_z: float = 0.0

    primary_scorers_count: int = 0
    assist_rate_delta: float = 0.0


def compute_liveflow_heat_index(inp: LiveFlowHeatInput) -> dict:
    fg_delta = max(0.0, inp.current_fg_pct - inp.expected_fg_pct)
    tp_delta = max(0.0, inp.current_3p_pct - inp.expected_3p_pct)
    ft_delta = max(0.0, inp.current_ft_pct - inp.expected_ft_pct)

    shooting_heat_score = (
        fg_delta * 0.8 +
        tp_delta * 1.4 +
        ft_delta * 0.3
    )

    pace_support_score = (
        inp.pace_z * 1.2 +
        inp.oreb_z * 0.8 +
        inp.fta_rate_z * 0.7 +
        inp.fastbreak_z * 0.6
    )

    clean_possession_penalty = 0
    if inp.turnovers_total <= 10:
        clean_possession_penalty += 8
    if inp.offensive_rebounds_total <= 10:
        clean_possession_penalty += 6
    if inp.free_throw_attempts_total <= 20:
        clean_possession_penalty += 5

    market_inflation = max(0.0, inp.live_total - inp.closing_total)
    market_inflation_score = market_inflation * 2.0

    required_remaining_points = inp.live_total - inp.current_total
    baseline_ppm = inp.closing_total / 48.0
    required_ppm = required_remaining_points / max(inp.minutes_remaining, 1.0)

    if required_ppm > baseline_ppm + 0.25:
        market_inflation_score += 10

    star_sustainability_offset = 0
    if inp.primary_scorers_count >= 3:
        star_sustainability_offset += 8
    if inp.assist_rate_delta >= 0:
        star_sustainability_offset += 5
    if pace_support_score >= 12:
        star_sustainability_offset += 5

    heat_index = (
        shooting_heat_score +
        market_inflation_score +
        clean_possession_penalty -
        pace_support_score -
        star_sustainability_offset
    )

    heat_index = max(0, min(100, round(heat_index)))

    if heat_index < 25:
        classification = "COOL"
        action_tag = "NO_EDGE"
    elif heat_index < 45:
        classification = "WARM"
        action_tag = "WATCH_UNDER"
    elif heat_index < 65:
        classification = "HOT"
        action_tag = "UNDER_TRIGGER"
    else:
        classification = "EXTREME_HEAT"
        action_tag = "UNDER_TRIGGER"

    if pace_support_score >= 14 and inp.primary_scorers_count >= 3 and inp.free_throw_attempts_total >= 20:
        action_tag = "DO_NOT_FADE"

    return {
        "heat_index": heat_index,
        "classification": classification,
        "action_tag": action_tag,
        "shooting_heat_score": round(shooting_heat_score, 2),
        "market_inflation_score": round(market_inflation_score, 2),
        "clean_possession_penalty": clean_possession_penalty,
        "pace_support_score": round(pace_support_score, 2),
        "star_sustainability_offset": star_sustainability_offset,
        "required_remaining_points": round(required_remaining_points, 2),
        "required_points_per_minute": round(required_ppm, 3),
    }
```

---

## SharpEdge Operational Rule
Use the LiveFlow Heat Index when:
- halftime totals jump sharply above close
- both teams are shooting unusually well
- the game does **not** clearly show possession chaos
- the market appears to be pricing in continued elite shotmaking

Primary use case:
- identify **halftime heat-fade under** spots before the board fully stabilizes

---

## Version Tag
- `LIVEFLOW_HEAT_INDEX_SPEC_V1`
- `SHARPEDGE_PROTOCOL_ACTIVE`
- `HALFTIME_HEAT_FADE_MODULE`
