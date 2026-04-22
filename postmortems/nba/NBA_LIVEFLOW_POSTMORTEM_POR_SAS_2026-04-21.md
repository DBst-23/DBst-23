# NBA LIVEFLOW Postmortem — POR @ SAS — 2026-04-21

## Game Info
- Matchup: Portland Trail Blazers @ San Antonio Spurs
- Final Score: POR 106 - SAS 103
- LiveFlow Position: San Antonio Team Total Under 120.5
- Result: WIN ✅

## Halftime State
- Halftime Score: POR 57 - SAS 57
- Halftime Total: 114
- Live Board:
  - SAS -7.5
  - Full Game Total 222.5
  - SAS Team Total 120.5
  - POR Team Total 114.5

## Thesis at Halftime
Primary read was that the Spurs team total was inflated by a false-pace first half. The score was tied, but the offensive environment was not clean enough to justify a 121-point team total.

Core reasons:
- Spurs offense was balanced but not dominant.
- Portland interior resistance and rebounding kept possessions contested.
- High-pace appearance masked unstable efficiency.
- Better angle was Spurs team total under rather than spread or full game total.

## Final Outcome
- Spurs closed on 103 points.
- Margin versus live line: 17.5 points under.
- Strong, clean team-total win.

## Statistical Drivers

### San Antonio
- 103 points
- 44.2% FG
- 7/24 from three (29.2%)
- 20/28 FT
- 15 turnovers
- 19 assists

### Portland defensive disruption
- 13 steals forced
- 10 blocks
- 15 offensive rebounds
- 23 second-chance points
- 24 points off turnovers

## Why the Edge Hit

### 1. False pace signal
- 57-57 halftime looked like over fuel.
- But the game was not being driven by elite offensive control.
- Market overreacted to raw score and priced SAS TT too high.

### 2. Spurs shot profile was weak
- Only 29.2% from three.
- Fox, Castle, and Vassell all needed high volume for middling efficiency.
- Team never built sustainable scoring separation.

### 3. Portland disruption profile was elite
- This was the game-deciding signal.
- Steals + blocks + offensive rebounding made the Spurs' path to 121 highly unstable.

## Model Tags
- `FALSE_PACE_OVERTRAP`
- `DEFENSIVE_DISRUPTION_SPIKE`
- `LOW_EFFICIENCY_HIGH_VOLUME`
- `TT_INFLATION_CORRECT`
- `PURE_EDGE_HIT`

## Edge Metrics
- Projected SAS final range at halftime: 108-112
- Median: 110
- Market line: 120.5
- Effective edge: +8.5 to +12.5 points
- Closing result: 103

## Final Grading
- Read Quality: A
- Execution Quality: A
- Edge Identification: A+
- Postmortem Label: `LIVEFLOW_POR_SAS_TT_UNDER_0421`

## Key Takeaway
Not all tied, high-scoring halves are over environments. This was a classic fake-pace trap: visible scoring pace, but weak enough offensive efficiency and enough defensive disruption to make the Spurs team total under the cleanest angle on the board.
