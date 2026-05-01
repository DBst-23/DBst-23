# NBA LiveFlow Position Management — DEN @ MIN — 4Q 04:12

## Metadata

- Game: Denver Nuggets @ Minnesota Timberwolves
- Date: 2026-04-30
- Mode: LIVEFLOW_STRIPPED_MODE_ACTIVE
- Snapshot: 4Q 04:12 remaining
- Score: DEN 95, MIN 98
- Current total: 193
- Active position: Minnesota team total over 109.5
- Entry: Yes, MIN over 109.5
- Entry stake: $7.50
- Entry odds: +123
- Market: Kalshi

## Live State

- Minnesota current points: 98
- Target to cash: 110+
- Points needed: 12
- Time remaining: 4:12
- Required scoring pace: about 2.86 points per minute
- Current game margin: MIN +3

## Updated Market Board

### Spread / Full Game Total

- Minnesota wins by over 3.5
  - Yes +145
  - No -176
- Full-game total 216.5
  - Over +113
  - Under -143

### Team Totals

- Minnesota over 109.5
  - Yes +123
  - No -168
- Denver over 106.5
  - Yes -137
  - No +105

## Q4 Flow Notes

Minnesota has scored 16 points in the 4Q through 4:12 remaining. Since the position-confirmation point around MIN 91 at 7:46, Minnesota has scored 7 points in about 3:34. This is below the needed pace for the ticket, but the live game remains close, which preserves late-game foul/clock-extension paths.

Key recent Q4 events:

- Gobert tip layup and offensive rebound at 6:38
- McDaniels floater at 5:26
- Shannon made three at 5:53
- Minnesota missed/empty trips are creating tension around the team-total line
- Denver has closed the margin to three, keeping endgame extension possible

## Current Model Read

- Mean from state: 107.5 to 111.0
- Median from state: 109
- Estimated hit probability from state: 43% to 49%
- Position status: live but degraded
- Cashout logic: do not auto-cash unless cashout approaches strong value or the game state shifts to clock bleed with Minnesota no longer attacking

## Active Tags

- POSITION_OPEN
- MIN_TT_109_5_OVER_ACTIVE
- SCORE_PACE_DEGRADED
- CLOSE_GAME_FOUL_EXTENSION_PATH_ACTIVE
- MIN_NEEDS_12_IN_4_12
- NO_ADDING_TO_POSITION
- RISK_CLUSTER_LOCK_ACTIVE

## Management Decision

Default: HOLD.

Reason:

- The ticket is behind the ideal pace but still has a live path because the game is close.
- Minnesota only needs 3 to 4 scoring possessions plus possible late free throws.
- Market has repriced to +123, meaning adding is not allowed under single-fire mode and there is no reason to double exposure.

Do not add. Do not hedge yet unless Denver creates a multi-possession lead or Minnesota enters a hard scoring drought under 2:30.
