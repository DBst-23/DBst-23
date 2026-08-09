# WNBA LIVE-FLOW Halftime Scan — Seattle Storm at Portland Fire

## Game State

- Date: 2026-08-08
- Venue: Moda Center, Portland, OR
- Halftime Score: Portland 56, Seattle 47
- First-Half Total: 103

## SharpEdge Market-Blind Halftime Projection

- Projected 2H Score: Seattle 45, Portland 43
- Fair 2H Total: 88.0
- Fair 2H Spread: Seattle -2 (low confidence)
- Projected Final Score: Portland 99, Seattle 92
- Fair Full-Game Total: 191.0
- Fair Full-Game Spread: Portland -7
- Fair Seattle Team Total: 92
- Fair Portland Team Total: 99

### Core Regression Read

Portland first-half scoring was materially inflated by extreme efficiency:
- 59.4% FG
- 44.4% 3PT
- 90.9% FT
- approximately 71.9% eFG
- approximately 78.6% shooting on two-point attempts

Seattle had mixed regression signals:
- positive: Flau'jae Johnson 3/10, Dominique Malonga 2/7, Ezi Magbegor 1/4
- negative: team 8/18 from three was already elevated

The model therefore projected second-half scoring regression without assuming an offensive collapse.

## William Hill Halftime Market

- Full-Game Spread: Portland -4.5 (-105) / Seattle +4.5 (-125)
- Full-Game Total: 191.5 (-115 both sides)
- Portland Team Total: 98.5 (Over -120 / Under -110)
- Seattle Team Total: 94.5 (Over -115 / Under -115)

## Edge Comparison

| Market | Book | SharpEdge Fair | Difference | Grade |
|---|---:|---:|---:|---|
| Full-game total | 191.5 | 191.0 | 0.5 toward Under | PASS |
| Full-game spread | POR -4.5 | POR -7 | 2.5 toward Portland | PASS — below threshold / low side confidence |
| Portland team total | 98.5 | 99 | 0.5 toward Over | PASS |
| Seattle team total | 94.5 | 92 | 2.5 toward Under | PASS |

## LIVE-FLOW Decision

**NO BET / DISCIPLINED PASS.**

The sportsbook market was tightly aligned with the model. No total or team-total discrepancy met the active LIVE-FLOW threshold of at least 4.0 points, with 5+ preferred under elevated uncertainty. The side showed only 2.5 points of model separation and the current framework explicitly treats team-score allocation and halftime spread projections as lower confidence than combined-total forecasting.

This scan is intentionally retained in the research library even though no wager was placed. A pass is a model decision and must be graded just like a strike. The purpose is to determine whether the model correctly recognized a low-edge market rather than judging the decision only by whether a hypothetical wager would later have won or lost.

## Process Classification

- Market-blind projection completed before viewing sportsbook prices: YES
- 4+ point total threshold met: NO
- 5+ point preferred separation met: NO
- Forced action avoided: YES
- Decision: PASS / NO STRIKE
- Capital exposed: $0
- Status: Pending final outcome for postgame validation

## Required Postgame Postmortem

When the game is final, complete the following regardless of outcome:

1. Record the final score, final total, and actual second-half score by team.
2. Compare actual second-half total against the 88.0 model center.
3. Compare actual final total against the 191.0 fair total.
4. Compare actual team finals against SEA 92 / POR 99.
5. Compare actual final margin against POR -7, while retaining the pregame note that the side carried low confidence.
6. Grade the Portland shooting-regression thesis separately from the Seattle positive-regression thesis.
7. Determine whether the sportsbook's 191.5 total was correctly classified as efficient relative to our model.
8. Evaluate all passed markets as hypothetical outcomes without retroactively converting a pass into a win or loss.
9. Record whether staying out protected capital from a bad edge, or simply avoided a result that happened to cash despite insufficient pre-bet separation.
10. Use this game as a discipline sample in the LIVE-FLOW database.

## Pass Evaluation Standard

The postgame grade will use two separate questions:

### Model accuracy
- How close were our fair lines to the actual outcome?
- Which regression reads were confirmed or broken?

### Decision quality
- Was the edge available at halftime large enough to justify risking capital under the active rules?

A hypothetical winning result does **not** make a pass incorrect if the edge failed the entry threshold. Likewise, a hypothetical losing result does not by itself prove the pass was sharp. The decision is graded on information available at halftime; the outcome is used to calibrate the model.

## Clean Machine-Readable Pending Record

```yaml
game_id: WNBA_2026-08-08_SEA_POR
halftime:
  score:
    SEA: 47
    POR: 56
  total: 103
model:
  second_half_score:
    SEA: 45
    POR: 43
  second_half_total: 88.0
  final_score:
    SEA: 92
    POR: 99
  full_game_total: 191.0
  full_game_spread: POR_-7
market:
  full_game_total: 191.5
  full_game_spread: POR_-4.5
  SEA_team_total: 94.5
  POR_team_total: 98.5
decision:
  action: pass
  wager_placed: false
  capital_exposed: 0
  reason: insufficient_model_market_separation
thresholds:
  minimum_total_edge: 4.0
  preferred_edge_high_uncertainty: 5.0
status: pending_postgame_validation
```
