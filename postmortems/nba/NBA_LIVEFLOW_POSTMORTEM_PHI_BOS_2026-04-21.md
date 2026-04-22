# NBA LIVEFLOW Postmortem — PHI @ BOS — 2026-04-21

## Game Info
- Matchup: Philadelphia 76ers @ Boston Celtics
- Final Score: PHI 111 - BOS 97
- Closing Spread: BOS -13.5
- Closing Total: 217.5
- Closing Team Totals:
  - BOS TT: 115.5-116.5 market band
  - PHI TT: 101.5-102.5 market band

## LiveFlow Positions Logged
1. PHI Team Total Under 108.5
2. PHI Team Total Under 111.5

## Result Summary
- PHI final team total: 111
- PHI TT Under 108.5: LOSS
- PHI TT Under 111.5: WIN
- Net interpretation: split-band ladder captured middle zone 109-111 effectively.

## Halftime State
- Halftime Score: PHI 62 - BOS 54
- Halftime Total: 116
- Core live read at halftime:
  - PHI scoring profile inflated by hot shotmaking, especially VJ Edgecombe and secondary support.
  - BOS underperformed chance quality despite offensive rebound and foul-drawing support.
  - Primary thesis was PHI scoring regression in 2H rather than a clean BOS spread recovery.

## Why the Read Was Reasonable
- PHI closed around 101.5-102.5 TT and posted 62 at half, creating an inflated live number.
- PHI first-half profile was efficiency heavy rather than pressure heavy:
  - 10/19 from three at halftime
  - only 2 made FTs on 4 attempts
  - Edgecombe 20 points on 8/13 FG and 4/6 from three
  - Drummond and Grimes also contributed hot ancillary scoring
- This supported a live regression thesis.

## What Happened
- PHI closed on 111, which produced the exact middle band outcome:
  - 108.5 under lost
  - 111.5 under won
- The second entry at 111.5 functioned as protection after the market moved upward.
- This validates the usefulness of selective same-thesis layering when the market is still confirming the original read.

## Key Statistical Drivers
### Philadelphia
- 111 points on 47.8% FG
- 19/39 from three (48.7%)
- only 11 FT attempts
- Maxey: 29 points, 9 assists
- Edgecombe: 30 points, 10 rebounds, 6 threes
- Drummond: 10 points, 8 rebounds, 1/1 from three

### Boston
- 97 points on 39.3% FG
- 13/50 from three (26.0%)
- 18 offensive rebounds but only 97 total points
- Brown: 36 points
- Tatum: 19 points, 14 rebounds, 9 assists
- White/Pritchard backcourt efficiency lagged badly

## Diagnostic Takeaways
### What was right
- Live PHI team total was inflated versus pregame baseline.
- BOS spread recovery was not the cleanest angle.
- Same-thesis staggered entries improved outcome coverage.

### What was wrong / incomplete
- PHI shotmaking sustainability was underestimated.
- Edgecombe explosion held deeper into the game than expected.
- BOS defense did not suppress perimeter variance enough in 2H.

## Model Notes
- Tag this as: `MIDDLE_CAPTURE_SUCCESS / PRIMARY_EDGE_PARTIAL_MISS`
- The first number (108.5) had the sharper edge and stronger CLV.
- The second number (111.5) served as a protection leg and salvaged the thesis.
- Future note: when the live under is primarily anti-variance based, monitor whether the opposing defense is actually capable of forcing the regression.

## Final Grading
- Read Quality: B+
- Execution Quality: A-
- Risk Structuring: A
- Postmortem Label: `LIVEFLOW_PHI_BOS_TT_UNDER_SPLIT_0421`
