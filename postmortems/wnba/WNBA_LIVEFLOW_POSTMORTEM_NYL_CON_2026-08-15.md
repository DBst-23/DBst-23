# WNBA LIVE-FLOW Postmortem — NYL at CON — 2026-08-15

## Result

- Final: **New York Liberty 82, Connecticut Sun 75**
- Halftime: **NYL 46, CON 37**
- Second half: **NYL 36, CON 38**
- Final total: **157**

### Wager

- **New York Liberty Team Total Under 89.5 (-105)**
- Stake: **$10.00**
- Payout: **$19.52**
- Profit: **+$9.52**
- Result: **WIN**
- Winning margin: **7.5 points**

---

## 1. Market-blind SharpEdge projection

Before seeing the live market, SharpEdge projected:

- Full-game fair total: **165.0**
- NYL fair team total: **86.0**
- CON fair team total: **79.0**
- Fair spread: **NYL -7**

With the halftime score at NYL 46, CON 37, those fair lines implied a second half of:

- NYL: **40**
- CON: **42**
- Combined: **82**
- Allocation: **CON +2 in the second half**

That allocation call was directionally exact: Connecticut actually won the second half **38-36**, also **CON +2**.

The absolute scoring level was too high, however. Actual second-half scoring was only **74**, eight points below the projected 82.

---

## 2. Market reveal and decision sequence

Initial William Hill reveal:

- Full-game total: **166.5**
- NYL team total: **89.5**
- CON team total: **75.5**
- Spread: **NYL -11.5**

Initial SharpEdge derivative comparison:

- NYL TT 89.5 vs fair 86.0: **3.5-point Under edge**
- CON TT 75.5 vs fair 79.0: **3.5-point Over edge**

The initial preference was **CON Over 75.5** because Connecticut had scored only 37 at halftime despite a severe second-quarter shooting collapse and was projected for positive regression.

Before the wager was placed, the market moved:

- CON TT: **75.5 → 77.5**
- NYL TT: **remained 89.5**

That changed the edge structure:

- CON Over edge compressed from **3.5 points to 1.5 points**
- NYL Under edge remained **3.5 points**

SharpEdge therefore pivoted to the surviving derivative:

> **NYL Team Total Under 89.5 (-105)**

This was a market-selection pivot, not a reversal of the game-environment thesis.

---

## 3. What happened

New York scored only **36 second-half points** and finished at **82**, comfortably below the 89.5 team-total line.

The original Connecticut Over thesis did receive partial support from the direction of second-half regression: Connecticut outscored New York 38-36 after trailing by nine at halftime. But the absolute scoring environment remained too low for the original team-total bet to cash.

Important counterfactual:

- CON Over 75.5 would have **lost by 0.5**
- CON Over 77.5 would have **lost by 2.5**
- NYL Under 89.5 **won by 7.5**

The market pivot therefore did two useful things simultaneously:

1. Avoided the original losing wager.
2. Preserved the stronger remaining mispricing.

---

## 4. Projection diagnostics

### Combined scoring level

SharpEdge fair total: **165**  
Actual final total: **157**  
Error: **-8 points**

SharpEdge projected second-half total: **82**  
Actual second-half total: **74**  
Error: **-8 points**

So the principal model miss was not allocation. It was the absolute level of expected remaining scoring.

### Team allocation

Projected second half:

- NYL 40
- CON 42

Actual second half:

- NYL 36
- CON 38

Both teams finished exactly **4 points below** their projected second-half scoring, while the relative allocation remained intact.

This is an unusually clean diagnostic result: the model got **which team should own more of the remaining scoring exactly right**, but overestimated the scoring environment equally on both sides.

### Spread

SharpEdge fair spread: **NYL -7**  
Actual final margin: **NYL by 7**

Spread error: **0 points**

The live market was NYL -11.5, four-and-a-half points more aggressive than the SharpEdge fair margin.

---

## 5. Why the NYL Under held

Several halftime signals made 89.5 a vulnerable continuation number.

### A. New York's first-half scoring was concentrated

Jonquel Jones had **19 of New York's 46 first-half points**, including **3-of-5 from three**. The Liberty as a team shot **53.8% from three** in the first half.

New York did not need to collapse offensively for 89.5 to be too high. It simply needed a more ordinary second-half conversion rate.

### B. Breanna Stewart had obvious positive regression, but that risk was already embedded

Stewart was only **1-of-8** in the first half. That created clear counter-risk to the team-total Under.

She did improve, but only to 11 total points for the game. The team-level under survived because the rest of New York's first-half shooting efficiency did not continue at the same rate.

### C. The fourth-quarter burst did not invalidate the thesis

Marine Johannes created a late scoring burst and New York shot **64.3% in the fourth quarter**, but the Liberty had scored only **15 in the third quarter**. The total second-half output still landed at 36.

That is important for LIVE-FLOW: an Under can survive a late hot pocket if the prior scoring path creates enough cushion.

---

## 6. Connecticut regression read: direction right, magnitude too high

Connecticut's first half contained a severe shooting trough:

- First-half FG: **36.1%**
- First-half 3PT: **14.3%**
- Second quarter FG: **17.6%**
- Second quarter 3PT: **0-for-10**

The expectation of positive regression was correct.

Second half:

- Connecticut scored **38**, versus 37 in the first half.
- Connecticut shot **40% from three** in the second half.
- Connecticut won the second half **38-36**.

But the original fair team total of 79 required 42 second-half points. That was four points too aggressive.

So the lesson is not to remove positive-regression logic. It is to better control the **magnitude** of regression when the overall possession and scoring environment is modest.

---

## 7. Market-selection lesson

This game is a strong positive example of **DERIVATIVE_REPRICING**.

The initial best-looking derivative changed after the market moved. Instead of anchoring to the first recommendation, SharpEdge rescanned the correlated market family and selected the line whose edge had not been consumed.

That behavior should remain part of the operating workflow:

> If the preferred live derivative moves materially toward SharpEdge fair value before entry, recompute the edge on every correlated derivative before placing a wager.

This is particularly important when two team totals arise from the same underlying total and allocation projection. A move in one derivative can leave the opposite team's number stale.

---

## 8. Diagnostic tags

- `LIVEFLOW_TEAM_TOTAL_ALLOCATION_GATE_v1`
- `MARKET_MOVE_EDGE_COMPRESSION`
- `DERIVATIVE_REPRICING`
- `NYL_TEAM_TOTAL_OVERPRICED`
- `CON_POSITIVE_SHOOTING_REGRESSION`
- `SECOND_HALF_ALLOCATION_DIRECTION_HIT`
- `ABSOLUTE_SCORING_LEVEL_OVERPROJECTED`
- `PIVOT_AVOIDED_ORIGINAL_LOSS`
- `SPREAD_FAIR_LINE_EXACT_HIT`

---

## 9. Model lesson

**What worked:**

- Market-blind derivative construction.
- Relative team allocation.
- Identifying NYL 89.5 as inflated.
- Reacting correctly to live line movement.
- Fair spread projection.

**What needs refinement:**

- Remaining-total level calibration.
- Regression-magnitude control.
- Converting extreme shooting depression into expected points without assuming a full rebound to mean within one half.

The most useful takeaway is that the two-stage framework held up conceptually:

1. Estimate remaining combined scoring.
2. Allocate it between teams.

In this game, **Stage 2 was excellent while Stage 1 was eight points too high**. That distinction should be preserved in future calibration work rather than treating the entire projection as one undifferentiated miss.

---

## Final classification

**WIN — GOOD PROCESS / GOOD MARKET PIVOT / TOTAL LEVEL OVERPROJECTED**

The bet won for the right structural reason: the NYL team total remained stale after Connecticut's number was repriced. The postmortem also reveals a useful calibration flaw: SharpEdge accurately projected the relative second-half allocation and final margin, but overstated the absolute scoring level for both teams by four points each.