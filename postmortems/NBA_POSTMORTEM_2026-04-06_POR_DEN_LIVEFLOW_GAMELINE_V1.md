# NBA Postmortem — LIVE-FLOW Gameline — POR @ DEN — 2026-04-06

## Final Score
- Portland Trail Blazers 132
- Denver Nuggets 137 (OT)

## Logged Live-Flow Bet
- ✅ Denver Nuggets +9.5 — **WIN**
- Stake: $4.96
- Payout: $8.00

## Market Context at Entry
- Live spread played: **DEN +9.5**
- Snapshot context at entry:
  - Portland led early
  - Denver was shooting poorly from three
  - Denver was still generating paint pressure, second-chance volume, and star-led halfcourt creation
- Core live read: the score gap overstated true game state because Denver still had multiple possession-winning drivers intact.

## Why the Live Bet Won
### 1. Denver’s interior offense was real even while trailing
- Denver finished with:
  - **66 points in the paint**
  - **17 offensive rebounds**
  - **30 second-chance points**
- That is exactly the profile of a team that can erase a live spread deficit even if perimeter variance is shaky.

### 2. Jokic stabilized the game state
- Nikola Jokic:
  - 35 points
  - 14 rebounds
  - 13 assists
- Denver had the best late-game organizer and possession stabilizer on the floor.
- Live spread value came from trusting Denver’s control variables, not just the current score.

### 3. Portland’s shooting spike was vulnerable
- Portland made **25 threes on 52 attempts (48.1%)**.
- Toumani Camara alone hit **8 threes**.
- That kind of extreme shotmaking is difficult to maintain for a full game, especially once the opponent begins winning interior possessions.
- The ticket did not require Denver to dominate immediately; it only required them to remain within an inflated number.

### 4. Rebound and possession edge favored the comeback path
- Denver won rebounds **45-39**.
- Offensive boards: **17-11 Denver**.
- Assists: **37-29 Denver**.
- Portland turnovers: **15**.
- Denver turnovers: **12**.
- Even while behind, Denver carried the sturdier possession profile.

## Key Game Phase Notes
### Early live environment
- Portland was fueled by outsized perimeter efficiency and positive pace.
- Denver’s scoreboard position looked worse than its underlying control of paint and offensive rebounding.

### Middle game
- Denver kept manufacturing extra chances through Jokic, Gordon, and Valanciunas.
- Portland still scored, but the margin stopped reflecting true control.

### Closing stretch + OT
- Denver’s experience, interior scoring, and star orchestration tightened the game.
- The +9.5 became high-value because the game never separated decisively once Denver reestablished halfcourt leverage.

## Hidden Drivers Confirmed by Outcome
1. **Paint dominance travels better than hot threes**
   - Denver’s 66 paint points gave them a durable scoring floor.
2. **Second-chance pressure is a live spread weapon**
   - 30 second-chance points kept the comeback path alive all game.
3. **OT is not needed for the edge to be correct**
   - Even before overtime, the live thesis was already validated by Denver’s possession profile.

## Model Relevance Summary
### What the model/read got right
- Correctly identified a **scoreboard inflation spot**.
- Properly trusted the team with the stronger **interior + rebound + creator** framework.
- Correct live decision under pressure.

### What to preserve in LIVE-FLOW
- Upgrade confidence on underdog live spreads when:
  - the trailing team owns the paint,
  - offensive rebounds are favorable,
  - turnover margin is stable,
  - and the opponent is being propped up by unusually hot three-point variance.

### Tags to preserve
- LIVEFLOW_STRIPPED_MODE_ACTIVE
- LIVE_EDGE_HIT
- SCOREBOARD_INFLATION_SPOT
- INTERIOR_EDGE_CONFIRMED
- SECOND_CHANCE_PRESSURE
- THREE_POINT_VARIANCE_REGRESSION

## Final Verdict
This was a **sharp live spread capture**.

Denver +9.5 was supported by:
- elite star control,
- rebound leverage,
- paint pressure,
- and a likely unsustainable Portland shooting heater.

The final OT win makes it look comfortable in hindsight, but the real edge was that Denver’s underlying possession profile never matched the size of the live spread.
