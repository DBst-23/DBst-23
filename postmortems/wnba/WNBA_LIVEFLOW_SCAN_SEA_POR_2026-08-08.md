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

**NO BET.**

The sportsbook market was tightly aligned with the model. No total or team-total discrepancy met the active LIVE-FLOW threshold of at least 4.0 points, with 5+ preferred under elevated uncertainty. The side showed only 2.5 points of model separation and the current framework explicitly treats team-score allocation and halftime spread projections as lower confidence than combined-total forecasting.

## Process Classification

- Market-blind projection completed before viewing sportsbook prices: YES
- 4+ point total threshold met: NO
- 5+ point preferred separation met: NO
- Forced action avoided: YES
- Decision: PASS / NO STRIKE
- Status: Pending final outcome for informational backtest only
