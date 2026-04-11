# POSTMORTEM_CLE_ATL_REB_CARD_2026-04-10

## Game
- Matchup: Cleveland Cavaliers @ Atlanta Hawks
- Date: 2026-04-10
- Final Score: ATL 124 - CLE 102
- Market Context: Rebound-focused pregame card

## Card Summary
- Entry: $10.00
- Payout: $0.00
- Net: -$10.00
- Result: 1 hit / 2 misses
- Overall Grade: C+

## Card Legs
1. ✅ Dyson Daniels Over 6.5 Rebounds — FINISHED 10
2. ❌ Jalen Johnson Over 9.5 Rebounds — FINISHED 9
3. ❌ Evan Mobley Over 7.5 Rebounds — FINISHED 6

## Postmortem Read
This card was not a full model failure. The strongest read on the board was Dyson Daniels, who cleared comfortably and validated the wing-chaos rebound environment. Jalen Johnson missed by a hook, while Evan Mobley missed more cleanly as Cleveland’s game script collapsed.

## Leg-by-Leg Breakdown
### Dyson Daniels O6.5 REB — A
- Finished with 10 rebounds
- Collected 5 offensive rebounds
- Benefited from Atlanta’s activity edge and Cleveland’s poor shot quality
- Tracking profile supported the chaos-board environment

### Jalen Johnson O9.5 REB — B-
- Finished with 9 rebounds
- Lost by a single rebound / hook
- Blowout script likely capped his ceiling through reduced minutes
- Still produced an efficient 18-9-2 line in only 25 minutes

### Evan Mobley O7.5 REB — D+
- Finished with 6 rebounds in 22 minutes
- Cleveland’s game environment failed early
- Mobley did show some activity with 3 offensive rebounds
- Blowout compression and unstable game flow prevented volume from stabilizing

## Root Causes
### 1. Blowout Compression
Atlanta won by 22, suppressing full starter-minute access for key rebound legs.

### 2. Cleveland Environment Failure
- CLE turnovers: 19
- CLE FG: 39-86
- ATL points off turnovers: 22
- ATL second chance points: 23

That pushed the game toward Atlanta wing/transition control rather than stable Cleveland frontcourt rebound accumulation.

## Team Stat Notes
### Cleveland
- Rebounds: 40
- Offensive Rebounds: 9
- Defensive Rebounds: 31
- FG: 39-86
- 3PT: 7-27
- Turnovers: 19

### Atlanta
- Rebounds: 46
- Offensive Rebounds: 14
- Defensive Rebounds: 32
- FG: 45-93
- 3PT: 16-44
- Turnovers: 11

## Tags
- MISS_REGISTERED
- BLOWOUT_MINUTES_SUPPRESSION
- HOOK_BURN
- REB_ENVIRONMENT_PARTIAL_HIT
- DYSON_EDGE_CONFIRMED
- MOBLEY_ENVIRONMENT_FAIL

## Final Assessment
Daniels was a clean hit and the best expression of the pregame rebound thesis. Johnson was a variance/hook burn. Mobley was the true failure point due to blowout compression and a broken Cleveland environment. This should be logged as a partial-hit rebound card rather than a full-system miss.
