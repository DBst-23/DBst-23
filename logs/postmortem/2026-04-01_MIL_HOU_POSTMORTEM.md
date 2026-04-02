# MIL @ HOU Postmortem — 2026-04-01

## Final score
- Bucks 113
- Rockets 119

## Invested plays tied to this game
1. Kevin Durant OVER 4.5 assists — **WIN**
   - Final: 9 assists

## Matchup-linked combo outcome
- Kevin Durant OVER 4.5 assists + Kyle Filipowski OVER 7.5 rebounds — **Won**
- Filipowski leg belongs to the separate UTA @ DEN postmortem, but this entry records that the Houston leg contributed a clean hit to the boosted card.

## Pre-game context
- Houston faced a severely undermanned Milwaukee roster.
- Ball-handling and playmaking burden remained heavily centered around Durant and Amen.
- The bet thesis was that Durant would function as a primary hub and clear a modest assist line if the offense maintained normal conversion.

## Final player result
### Kevin Durant
- 19 points
- 5 rebounds
- **9 assists**
- 39 minutes
- 7-of-16 FG

## Outcome assessment
### What the model got right
- Correctly identified Durant as a strong assist hub in this specific version of the Rockets lineup.
- Correctly expected enough halfcourt orchestration and shot conversion around him to clear **4.5 assists**.
- This was not a hook sweat; it cleared by a wide margin.

### Game environment notes
- Rockets recorded **30 team assists**.
- Houston scored **119 points** on solid efficiency.
- Milwaukee was severely depleted, allowing Houston to run through primary creators without much resistance.
- Durant finished with **9 assists**, nearly doubling the line.

## Structural validation
This was a good example of a line that stayed too low for role.
- Primary initiator equity remained intact.
- Team conversion was sufficient.
- No usage collapse or alternate creator siphon occurred.

## Key lesson
In injury-distorted games, assist props for elite secondary/primary creators can stay underpriced when the market focuses more on points and spread than direct playmaking burden.

## Patch note for future workflow
Reinforce:
- `INJURY_THINNED_OPPONENT_ASSIST_BOOST`
- `PRIMARY_HUB_AST_ROLE_LOCK`

## Final grading
- Invested play from matchup: **1/1**
- Process grade: **A**
- Result type: **Role-based smash hit**

## Tags
- `HIT_REGISTERED`
- `ASSIST_ROLE_VALIDATED`
- `CLEAR_MARGIN_WIN`
