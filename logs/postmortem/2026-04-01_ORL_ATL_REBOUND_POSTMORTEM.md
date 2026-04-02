# ORL @ ATL Rebound Postmortem — 2026-04-01

## Final score
- Hawks 130
- Magic 101

## Invested plays from this matchup
1. Onyeka Okongwu UNDER 7.5 rebounds — **WIN**
   - Final: 7 rebounds
2. Paolo Banchero UNDER 8.5 rebounds — **WIN**
   - Final: 8 rebounds

## Model-flagged leans from this matchup
- Onyeka Okongwu UNDER 7.5 — **Hit**
- Paolo Banchero UNDER 8.5 — **Hit**
- Dyson Daniels UNDER 6.5 — **Miss**
  - Final: 13 rebounds
- Wendell Carter Jr. OVER 7.5 was avoided / not endorsed at the final line
  - Final: 6 rebounds
- Jalen Suggs UNDER 4.5 was a thinner under lean
  - Final: 5 rebounds
- Desmond Bane rebound exposure was avoided
  - Final: 2 rebounds

## Pre-game grading recap
- Okongwu U7.5
  - Projected mean: ~7.0
  - Median: 7
  - Grade: B
- Paolo U8.5
  - Projected mean: ~8.0
  - Median: 8
  - Grade: B
- Dyson U6.5
  - Projected mean: ~5.9
  - Median: 6
  - Grade: B

## Outcome assessment
### What the model got right
- Correctly identified **Paolo** and **Okongwu** as the best under candidates at their posted lines.
- Properly treated **Wendell Carter Jr. OVER 7.5** as too expensive.
- Correctly stayed away from forcing **Desmond Bane rebounds**.
- Correctly viewed **Suggs U4.5** as thin rather than elite; it missed by a single rebound.

### What failed
- **Dyson Daniels UNDER 6.5** failed badly.
- Daniels finished with **13 rebounds** and 6 offensive rebounds, indicating the game environment produced far more wing/chaos rebound opportunity than expected.

## Environment notes
- ATL won the rebound battle **51–37**.
- ORL shot just **39.8% FG** and **18.8% from three**.
- Massive Orlando inefficiency created elevated defensive rebound volume for Atlanta.
- ATL recorded **11 offensive rebounds** and controlled game flow early.
- Blowout script plus poor Orlando shotmaking boosted Atlanta board chances, especially for active wings.

## Key lesson
The two invested unders were correct because their lines were placed just above realistic median outcomes. But the matchup also showed that when Orlando's offense collapses, rebound distribution can spike toward aggressive wings rather than staying only with the center rotation.

## Patch note for future workflow
Add a rebound volatility tag for:
- Opponent low-efficiency risk
- Wide miss dispersion environments
- Active wing crashers (like Dyson Daniels / Jalen Johnson archetypes)

Suggested label:
- `WING_CRASH_OVERLAY_ON`
- `LOW_EFFICIENCY_REBOUND_SPIKE`

## Final grading
- Invested matchup plays: **2/2**
- Broader model leans from matchup: **Mixed, but strongest signals were correct**
- Matchup workflow grade: **A-**

## Status
- Logged before DEN @ UTA final.
- Jokic leg remains pending in separate card evaluation.
