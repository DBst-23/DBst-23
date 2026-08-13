# WNBA LIVE-FLOW Postmortem — Minnesota Lynx at Portland Fire

**Date:** 2026-08-12  
**Checkpoint:** Halftime  
**Halftime score:** Minnesota 57 — Portland 33  
**Final:** Minnesota 85 — Portland 81  
**Final total:** 166  
**Status:** FINAL — LIVE-FLOW wager won

## Executed wager
- **Minnesota Lynx team total UNDER 101.5**
- Odds: **-115**
- Stake: **$10.00**
- Paid: **$18.70**
- Net: **+$8.70**
- Result: **WIN**
- Win margin: **16.5 points**

## Frozen SharpEdge projection
- Minnesota: **98**
- Portland: **76**
- Full-game total: **174**
- Projected second half: Portland 43 — Minnesota 41

## Sportsbook at halftime
- Minnesota TT: **101.5**
- Full-game total: **178.5**
- Portland TT: **76.5**
- Spread: Minnesota **-25.5**

SharpEdge's largest clean derivative disagreement was Minnesota TT Under 101.5, with the model 3.5 points lower at 98.

## What actually happened
Minnesota scored only **28 second-half points** after posting 57 in the first half. Portland scored **48** after halftime and nearly erased a 29-point deficit.

Second-half split:
- Minnesota: **28 points**, 37.0% FG, **0/9 from three**, 8/13 FT, 7 turnovers
- Portland: **48 points**, 52.8% FG, 4/15 from three, 6/8 FT

Quarter scoring:
- Minnesota: 26 — 31 — 11 — 17
- Portland: 23 — 10 — 18 — 30

## Why the Minnesota TT Under won
### 1. First-half three-point efficiency was unsustainable
Minnesota hit **6/11 from three (54.5%)** in the first half. SharpEdge explicitly flagged perimeter regression risk before seeing the market.

The regression was stronger than expected: Minnesota went **0/9 from three in the second half**.

The important lesson is not to expect 0/9 specifically. The model should continue identifying when a favorite's live team total requires first-half perimeter shooting to remain unusually hot.

### 2. The 24-point halftime lead changed offensive incentives
Minnesota led 57-33 at halftime and reached a 29-point lead early in the third quarter. From that point, Portland became the urgency team.

Minnesota's offensive output dropped to 11 points in Q3 and 17 in Q4. Even though the Lynx had to re-engage late after Portland's comeback, the early second-half slowdown had already done major damage to the Over 101.5 path.

This confirms that blowout state is not simply a side/spread variable. It can be directly useful in live favorite team-total unders when the market prices continued first-half scoring pressure.

### 3. Portland positive regression was correctly identified
Portland entered halftime after scoring only **10 points in Q2**, shooting 21.4% in that quarter and 3/8 from the line in the first half.

SharpEdge expected Portland to improve. Portland scored **48 second-half points**, including 30 in Q4.

This mattered because Portland's comeback increased the game's competitive intensity without rescuing Minnesota's team total. The under therefore survived even in a much more competitive game than the halftime margin suggested.

### 4. The derivative was better than the parent total
SharpEdge projected a full-game total of 174 versus the market's 178.5. The actual final was 166, so the full-game Under also would have won.

But the Minnesota TT Under was the cleaner target because the identifiable first-half distortion was concentrated on Minnesota:
- hot 3-point shooting
- 57 first-half points
- huge lead
- reduced urgency risk

The market asked Minnesota to reach **102**, meaning 45 second-half points were needed. SharpEdge projected only 41. Actual: **28**.

This is exactly the type of situation where a derivative can express the model thesis more efficiently than the full-game total.

## What the model still got wrong
This was a betting win, not a perfect projection.

Projection errors:
- Minnesota: projected 98, actual 85 — **13 points high**
- Portland: projected 76, actual 81 — **5 points low**
- Total: projected 174, actual 166 — **8 points high**

SharpEdge correctly identified direction, but underestimated the magnitude of Minnesota's second-half offensive collapse and Portland's comeback surge.

Do not treat the 16.5-point cushion as evidence that the model was 16.5 points 'right.' The sportsbook was too high, and our own fair number was also too high.

## Model patch
### `LIVEFLOW_FAVORITE_CONTINUATION_FADE_v1`

Add these rules to LIVE-FLOW team-total evaluation:

1. If a team leads by 20+ at halftime and has materially elevated first-half 3P%, reduce continuation confidence before approving its TT Over and increase scrutiny of its TT Under.
2. Separate **first-half scoring output** from **repeatable scoring process**. High assist quality and paint scoring can be real while hot perimeter conversion still regresses.
3. When the favorite has a huge lead, model a lower offensive-urgency state in Q3 before assuming normal starter-level scoring pressure.
4. Do not assume garbage time only benefits Overs. It can create asymmetric scoring: trailing team urgency rises while leading team pace, shot quality, and starter usage can fall.
5. If the trailing team also owns strong positive-regression indicators, consider favorite TT Under before full-game Under because comeback scoring can threaten the parent total without helping the favorite's team total.
6. Preserve a wide tail: a large favorite can be forced back into competitive rotations if the underdog rallies, so the edge should be based on distribution rather than deterministic bench assumptions.

## New tags
- `DOMINANT_FIRST_HALF_CONTINUATION_FADE`
- `FAVORITE_OFFENSE_DECELERATION`
- `TRAILING_TEAM_REGRESSION_SURGE`
- `TEAM_TOTAL_DERIVATIVE_OUTPERFORMS_PARENT`
- `HOT_3P_FAVORITE_FADE`
- `BLOWOUT_STATE_ASYMMETRIC_SCORING`

## SharpEdge grade
- **Market selection:** A
- **Direction:** A
- **Derivative selection:** A
- **Projection accuracy:** B-
- **Volatility framing:** B+
- **Execution:** A

## Core lesson
**This win came from fading continuation, not from predicting a dead second half.**

Minnesota's first-half scoring environment was too efficient to extrapolate, while Portland had obvious positive-regression potential. The sharp expression was therefore not 'the whole game must slow down.' It was: **Minnesota is being priced too aggressively to continue scoring like the first half.**

That distinction is exactly what LIVE-FLOW should preserve going forward.
