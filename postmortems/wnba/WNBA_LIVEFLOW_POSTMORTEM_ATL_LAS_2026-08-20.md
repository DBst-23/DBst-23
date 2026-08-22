# WNBA LIVE-FLOW Postmortem — Atlanta Dream at Los Angeles Sparks

## Game Identity
- Date: 2026-08-20
- Venue: Crypto.com Arena, Los Angeles, CA
- Final: Atlanta 124, Los Angeles 88
- Final total: **212**
- End 3Q: Atlanta 94, Los Angeles 62
- End-3Q total: **156**
- Game ID: `WNBA_2026-08-20_ATL_LAS`

## Wager Logged
William Hill ticket:

| Checkpoint | Market | Line | Odds | Stake | Result | Final Total | Net |
|---|---|---:|---:|---:|---|---:|---:|
| End 3Q | Full-game total | **Under 200.5** | -125 | **$15.00** | **LOSS** | **212** | **-$15.00** |

- Total risk: **$15.00**
- Paid: **$0.00**
- Net: **-$15.00**
- End-3Q score: Atlanta 94, Los Angeles 62
- Book line at entry: 200.5
- Book-implied remaining scoring: **44.5 points**
- Actual Q4 scoring: **56 points**
- Miss versus wager line: **11.5 points Over**

## Projection-Persistence Note
The exact market-blind SharpEdge fair total that preceded the wager is not currently recoverable from the repository or the preserved checkpoint files available to this postmortem. The directional call is preserved by the wager itself: SharpEdge struck **Under 200.5** at the end of the third quarter.

This postmortem therefore does **not** invent a frozen fair number. It grades the process using the known end-3Q state, the actual wager, and the final-quarter path.

## End-3Q State
Atlanta led **94-62** after three quarters.

### Atlanta through 3Q
- 34/53 FG — **64.2%**
- 11/17 3PT — **64.7%**
- 15/20 FT — 75.0%
- 29 rebounds
- 25 assists
- 11 turnovers
- 46 points in the paint
- 13 second-chance points
- 15 fast-break points

### Los Angeles through 3Q
- 22/49 FG — 44.9%
- 8/20 3PT — 40.0%
- 10/13 FT — 76.9%
- 16 rebounds
- 15 assists
- 14 turnovers
- 24 points in the paint

### Score path
- Q1: Atlanta 34, Los Angeles 12 — 46 total
- Q2: Atlanta 28, Los Angeles 29 — 57 total
- Q3: Atlanta 32, Los Angeles 21 — 53 total
- Through 3Q: **156 total**

## Likely Under Thesis at the Strike
The Under case was understandable from the end-3Q profile:

1. Atlanta was shooting at an obviously extreme rate: **64.2% FG and 64.7% from three**.
2. Atlanta led by 32, creating a major blowout/rotation signal.
3. A 200.5 total required another **44.5 points** in the final quarter.
4. With the game effectively decided, normal intuition would expect:
   - reduced starter minutes,
   - lower urgency,
   - less intentional fouling,
   - some efficiency regression,
   - and a slower late-game environment.

The critical mistake was treating those forces as sufficient protection without properly pricing the scoring ability of the replacement rotations and the possibility that both benches would continue converting efficiently.

## What Actually Happened in Q4
The fourth quarter finished:

- Atlanta: **30**
- Los Angeles: **26**
- Combined: **56**

That was **11.5 points more** than the 44.5 points needed to beat the Under 200.5.

### Atlanta Q4
- 12/19 FG — **63.2%**
- 5/9 3PT — **55.6%**
- 1/2 FT
- 30 points

### Los Angeles Q4
- 7/12 FG — **58.3%**
- 2/7 3PT — 28.6%
- 10/13 FT — 76.9%
- 26 points

### Combined Q4
- 19/31 FG — **61.3%**
- 7/16 3PT — 43.8%
- 11/15 FT — 73.3%
- 56 points

## The Central Failure
The model's most important wrong assumption was that the blowout would force scoring efficiency down enough to protect the Under.

Instead, the opposite happened:

- Atlanta's shooting **did not regress materially at all**.
- The Dream scored 30 even after the game was long decided.
- Los Angeles' offense improved, helped by frequent free throws and cleaner bench scoring opportunities.
- The game entered a low-defensive-pressure environment rather than a low-scoring environment.

That distinction matters.

### Blowout ≠ low scoring
A blowout can produce two very different fourth-quarter states:

**State A — pace suppression**
- long possessions
- passive offense
- benches struggling to score
- fewer fouls

**State B — defensive relaxation / bench freedom**
- weak point-of-attack defense
- transition leaks
- low-pressure shot-making
- reserves playing aggressively
- free-flowing possessions

This game was decisively **State B**.

## Rotation Audit
Atlanta's primary starters began leaving early in Q4, but the bench did not reduce the offensive floor.

Key reserve production in Q4:
- Madina Okot: 6 points
- Te-Hina Paopao: 3 points
- Sika Kone: 6 points
- Aaliyah Nye: 3 points
- Shatori Walker-Kimbrough: 5 points

Atlanta's non-core rotation collectively maintained high shooting efficiency.

For Los Angeles, Cameron Brink played the entire fourth quarter and scored 8 points, while the Sparks repeatedly reached the free-throw line.

The substitution pattern therefore reduced star exposure, but **did not reduce scoring enough**.

## Free-Throw / Foul Environment
Los Angeles attempted **13 free throws in Q4**, making 10.

This is a major Under-killer in a blowout because the clock stops while points continue accumulating.

The Sparks' fourth-quarter free-throw volume came from:
- repeated attacking possessions,
- Atlanta reserves committing fouls,
- bonus situations,
- and continued rim pressure despite the game being out of reach.

The Under thesis did not sufficiently account for the possibility that bench-heavy defense would increase foul rate.

## Why Atlanta's Regression Signal Failed to Materialize
Atlanta had every textbook signal for negative shooting regression:
- 64.2% FG through 3Q
- 64.7% 3PT through 3Q
- 94 points through 30 minutes

Yet Q4 Atlanta shot:
- 63.2% FG
- 55.6% from three

This does **not** mean regression analysis is useless. It means that regression must be conditioned on lineup quality and defensive context.

The bench environment can create easier looks than the starter environment, especially in a 30+ point game where defensive intensity collapses.

A raw team-level regression model would incorrectly assume that the fourth-quarter shot quality distribution remains comparable to the first three quarters.

## Model / Process Audit
### What was reasonable
1. **Recognizing Atlanta's shooting as unsustainably hot.**
2. **Recognizing a 32-point lead as a blowout state.**
3. **Expecting starter minutes to fall.**
4. **Expecting a lower-intensity fourth quarter.**

### What was wrong
1. **Equating lower intensity with lower scoring.**
2. **Failing to model bench offensive competence.**
3. **Failing to price defensive degradation from reserve lineups.**
4. **Failing to price Q4 foul/free-throw volume.**
5. **Overweighting shooting regression without conditioning on shot quality.**
6. **Underestimating the probability of a 50+ point garbage-time quarter.**

## New LIVE-FLOW Rules From This Loss

### Rule 1 — `BLOWOUT_STATE_SPLIT`
Do not treat a blowout as one generic Under signal.

Classify the fourth quarter into:
- `PACE_SUPPRESSION_BLOWOUT`
- `DEFENSIVE_RELAXATION_BLOWOUT`

The second state can be neutral or even positive for scoring.

### Rule 2 — `BENCH_SCORING_COMPETENCE_GATE`
Before attacking a blowout Under, estimate whether the incoming second units can still score efficiently.

Key checks:
- bench shot creation
- bench 3-point quality
- offensive role continuity
- reserve ball-handling
- reserve transition ability

### Rule 3 — `BENCH_DEFENSE_DEGRADATION_GATE`
A reserve-heavy fourth quarter can weaken defense faster than it weakens offense.

If both teams downgrade defensively more than offensively, the Under should be downgraded.

### Rule 4 — `Q4_FOUL_FLOOR`
Project fourth-quarter free throws explicitly, even in blowouts.

Garbage time can create:
- poor closeouts,
- late rotations,
- reach fouls,
- transition fouls,
- inexperienced reserve defense.

### Rule 5 — `REGRESSION_REQUIRES_CONTEXT`
Extreme shooting percentages alone are not enough for an Under strike.

Regression must be conditioned on:
- expected lineups,
- expected shot quality,
- opponent defensive personnel,
- game-state intensity.

### Rule 6 — `END3Q_50PLUS_Q4_TAIL`
Every end-3Q total model must explicitly estimate the probability of **50+ remaining points**.

If a 50+ point fourth quarter is meaningfully live, the model cannot rely on a narrow central estimate.

## Comparison to the Aug. 19 MIN-GSV Lesson
The previous Aug. 19 Minnesota-Golden State postmortem already warned:

> Blowout does not automatically mean Under protection.

This game reinforces that lesson much more strongly.

MIN-GSV produced a 48-point Q4 and still barely stayed Under.
ATL-LAS produced **56 Q4 points** and destroyed the Under.

The pattern is now repeated enough to formalize:

**Do not assign a negative scoring adjustment to blowout state without separately modeling trailing-team urgency, reserve efficiency, defensive degradation, and free-throw risk.**

## Postmortem Grade
### Directional read
**D**

The Under lost by 11.5 points and the expected scoring suppression never materialized.

### Regression logic
**C-**

The theoretical regression signal was strong, but the model treated raw shooting percentages as more predictive than lineup/shot-quality context.

### Game-state calibration
**D**

The blowout state was misclassified as scoring-suppressive.

### Wager selection
**D+**

Under 200.5 was not reckless given the 156 end-3Q total and extreme Atlanta shooting, but the edge was not structurally protected once bench scoring and foul volatility are included.

## Final Classification
- Result: **LOSS**
- Market: **Full-game Under**
- Checkpoint: **End 3Q**
- Score at checkpoint: Atlanta 94, Los Angeles 62
- End-3Q total: **156**
- Bet: **Under 200.5 -125**
- Required Q4 to beat bet: **44.5 or fewer**
- Actual Q4: **56**
- Final total: **212**
- Miss to line: **11.5 points**
- Stake: **$15.00**
- Net: **-$15.00**
- Process tag: **BLOWOUT_STATE_MISCLASSIFIED / REGRESSION_CONTEXT_MISS / Q4_VOLATILITY_FAIL**

## Tags
- END3Q_LIVEFLOW
- UNDER_LOSS
- ATL_EXTREME_SHOOTING
- ATL_REGRESSION_FAILED_TO_MATERIALIZE
- BLOWOUT_STATE_MISCLASSIFIED
- DEFENSIVE_RELAXATION_BLOWOUT
- BENCH_SCORING_COMPETENCE
- BENCH_DEFENSE_DEGRADATION
- Q4_FOUL_VOLUME
- Q4_56_POINTS
- REGRESSION_REQUIRES_CONTEXT
- END3Q_50PLUS_Q4_TAIL
- MODEL_CALIBRATION_MISS

```yaml
game_id: WNBA_2026-08-20_ATL_LAS
checkpoint: end_3q
score_at_checkpoint:
  ATL: 94
  LAS: 62
  total: 156
wager:
  market: full_game_total
  selection: under
  line: 200.5
  odds_american: -125
  stake_usd: 15.00
  result: loss
  net_usd: -15.00
book_implied_remaining_points: 44.5
actual_q4:
  ATL: 30
  LAS: 26
  total: 56
  combined_fg: 19
  combined_fga: 31
  combined_fg_pct: 61.3
  combined_3p: 7
  combined_3pa: 16
  combined_ftm: 11
  combined_fta: 15
final:
  ATL: 124
  LAS: 88
  total: 212
wager_margin_points: -11.5
projection_persistence:
  exact_frozen_fair_total_available: false
  directional_call_preserved: under_200.5
process:
  blowout_state_classification: fail
  regression_context: fail
  q4_foul_modeling: fail
  bench_scoring_modeling: fail
new_rules:
  - BLOWOUT_STATE_SPLIT
  - BENCH_SCORING_COMPETENCE_GATE
  - BENCH_DEFENSE_DEGRADATION_GATE
  - Q4_FOUL_FLOOR
  - REGRESSION_REQUIRES_CONTEXT
  - END3Q_50PLUS_Q4_TAIL
status: POSTMORTEM_COMPLETE
```
