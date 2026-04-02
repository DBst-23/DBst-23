# NYK @ MEM Rebound Postmortem — 2026-04-01

## Final score
- Knicks 130
- Grizzlies 119

## Invested play from this matchup
1. Mikal Bridges UNDER 3.5 rebounds — **WIN**
   - Final: 2 rebounds

## Other invested plays referenced but not part of this matchup file
- Nikola Jokic UNDER 13.5 rebounds — separate UTA @ DEN file
- Kevin Durant OVER 4.5 assists — separate MIL @ HOU file
- Kyle Filipowski OVER 7.5 rebounds — separate UTA @ DEN file

## Model-flagged rebound leans from NYK @ MEM
- Mikal Bridges UNDER 3.5 rebounds — **Hit**
- Josh Hart rebound under value disappeared after market move and was not captured on final card
- Karl-Anthony Towns rebound environment remained favorable but line was elevated and not selected as best final investment
- OG Anunoby rebound upside was present as a secondary volatility risk and became the main disruptor

## Pre-game grading recap
- Mikal Bridges U3.5
  - Projected mean: ~3.3-3.8
  - Median: 3
  - Edge profile: thin but playable because Memphis wing environment did not force him into primary glass role
  - Final grade pre-tip: B-

## Outcome assessment
### What the model got right
- Correctly isolated **Mikal Bridges UNDER 3.5** as the best available final line from the board.
- Correctly did not overexpose into broader Knicks rebound overs after market movement.
- Correctly recognized that the best direct value on the Knicks side had shifted away from Hart by the time the final board was posted.

### What changed the game
- New York completely crushed Memphis on the glass **49–20**.
- Knicks posted **20 offensive rebounds** and **27 second-chance points**.
- Even in an extreme rebound environment, Bridges still stayed below line with only **2 rebounds**, validating role-based suppression.

### Main variance event
- **OG Anunoby finished with 13 rebounds** and became the unexpected dominant wing rebound collector.
- Towns added **11** and Hukporti grabbed **6 in 12 minutes**.
- This shows that the rebound spike concentrated into other Knicks archetypes, not Bridges.

## Structural notes
- Memphis frontcourt was severely undermanned.
- Knicks won because of massive possession control and offensive glass domination.
- This was a perfect example of a good under surviving inside a huge team-rebound outlier because individual role mattered more than team environment.

## Key lesson
When team rebound environment spikes, the critical question is not just **how many rebounds will exist**, but **who is structurally first in line to absorb them**. In this matchup, Bridges remained behind Towns / Hart / OG / bench big spillover in rebound priority.

## Patch note for future workflow
Add reinforcement for:
- `ROLE_REBOUND_PRIORITY_FILTER`
- `TEAM_REBOUND_SPIKE_CAN_STILL_SUPPORT_GUARD_WING_UNDERS`

This game is a positive example that strong role suppression can survive even in extreme team rebound conditions.

## Final grading
- Invested play from matchup: **1/1**
- Process grade: **A-**
- Result type: **Clean role-based hit**

## Tags
- `HIT_REGISTERED`
- `ROLE_SUPPRESSION_VALIDATED`
- `TEAM_REBOUND_OUTLIER_SURVIVED`
