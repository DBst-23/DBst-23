# WNBA LIVE-FLOW Postmortem — Los Angeles Sparks at Washington Mystics

**Date:** 2026-08-15  
**Venue:** CareFirst Arena, Washington, DC  
**Checkpoint:** Halftime  
**Halftime score:** Washington 41 — Los Angeles 39  
**Final score:** Washington 80 — Los Angeles 70  
**Final total:** 150  
**Status:** FINAL — Los Angeles team-total Under win

## SharpEdge frozen projection — before sportsbook comparison

SharpEdge projected the game market-blind before William Hill prices were revealed.

| Market | SharpEdge projection | Actual | Projection minus actual |
|---|---:|---:|---:|
| Full-game total | 162.5 | 150 | +12.5 |
| Washington team total | 84.0 | 80 | +4.0 |
| Los Angeles team total | 78.5 | 70 | +8.5 |
| Final margin | WAS by 5.5 | WAS by 10 | -4.5 margin pts |

Projected second half: **Washington 43.0 — Los Angeles 39.5**  
Actual second half: **Washington 39 — Los Angeles 31**

Projected second-half combined scoring: **82.5**  
Actual second-half combined scoring: **70**

## Sportsbook reveal

William Hill showed:

- Full-game total: **169.5**
- Spread: **Washington -7.0**
- Washington team total: **88.5**
- Los Angeles team total: **82.5**

Against the frozen SharpEdge numbers, the observed gaps were:

- Full-game total: **7.0 points toward Under**
- Washington team total: **4.5 points toward Under**
- Los Angeles team total: **4.0 points toward Under**

The full-game total did not clear the existing **8+ point `LIVEFLOW_TOTALS_PACE_REGRESSION_GAP_GATE_v1`** requirement, so it remained a lean rather than a strike.

## LIVE-FLOW strike

- **Wager:** Los Angeles Sparks team total UNDER 82.5
- **Odds:** -120
- **Stake:** $10.00
- **Profit:** $8.33
- **Payout:** $18.33
- **Sportsbook:** William Hill
- **Ticket timestamp:** AUG 15 2026, 05:21 PM NV
- **Ticket ID:** `7881da00-9908-11f1-b3b1-9b1297e6ac15`
- **Result:** **WIN**

Los Angeles finished with **70 points**, giving the wager a **12.5-point cushion** under 82.5.

# Core diagnosis

This was a **clean derivative-selection win built on first-half scoring fragility**.

The key halftime question was not whether Los Angeles had scored 39 points. It was whether the process generating those 39 points was sustainable enough to support a live team total of 82.5.

SharpEdge said no.

At halftime Los Angeles had:

- **39 points**
- **45.2% FG**
- **46.2% from three — 6/13**
- **5/5 FT**
- only **31 FGA**
- only **1 offensive rebound**
- **7 turnovers**
- only **16 points in the paint**

That scoring profile carried more efficiency than possession volume.

The market effectively required Los Angeles to score **43.5 more points** to beat 82.5. SharpEdge projected only **39.5 second-half points**, and even that projection proved conservative: Los Angeles scored only **31** after halftime.

## What we got right

### 1. Los Angeles' first-half three-point shooting was vulnerable

Los Angeles entered halftime at **46.2% from three**.

Second half:

- **23.1% from three**
- **33.3% FG**
- **31 points**

Fourth quarter:

- **12 points**
- **25.0% FG**
- **16.7% from three**

The shooting-regression thesis materialized strongly.

### 2. The first-half scoring lacked possession support

The Sparks scored 39 despite having only **31 field-goal attempts**, **1 offensive rebound**, and **7 turnovers**.

That is a fragile construction for a team expected by the market to reach the low 80s.

Los Angeles did not create a second-half possession surge sufficient to offset the efficiency decline. The second half produced only **31 points**.

### 3. Washington's interior and rebounding profile gave the Under structural support

At halftime Washington already had:

- **34 points in the paint**
- **7 offensive rebounds**
- **41 FGA**

Los Angeles had:

- **16 paint points**
- **1 offensive rebound**
- **31 FGA**

By the final whistle Washington had:

- **60 points in the paint**
- **11 offensive rebounds**
- **43 total rebounds**

The Mystics' interior control and extra-possession profile kept Los Angeles from owning the possession battle.

### 4. The derivative selection matched the underlying thesis

This is important after the earlier LIVE-FLOW team-total allocation lessons.

The primary bearish signal belonged specifically to **Los Angeles' scoring process**:

- hot three-point shooting,
- modest shot volume,
- weak offensive rebounding,
- and turnover leakage.

So the chosen derivative was **Los Angeles team-total Under**, not an unrelated opposing team-total Under.

That alignment was correct.

### 5. We respected the full-game total gate

SharpEdge's full-game projection was **162.5** against William Hill **169.5**, a 7-point gap.

The game finished at **150**, so the directional read was excellent.

But the model's existing gate required an 8+ point discrepancy for a full-game total strike.

We did **not** override the gate simply because the Under looked attractive.

That is good process discipline. The full-game Under would have won, but the correct postmortem lesson is not to weaken the threshold after seeing the result.

# Where the projection was still imperfect

The wager won comfortably, but the projection itself remained too high across the scoring environment.

SharpEdge projected:

- Los Angeles **78.5**; actual **70**
- Washington **84.0**; actual **80**
- Total **162.5**; actual **150**

So the model correctly identified the market as inflated but still underestimated the severity of the second-half scoring slowdown.

The largest residual miss was Los Angeles:

> Projected second-half LA scoring: **39.5**  
> Actual: **31**

This suggests the halftime model can improve its downside-tail treatment when a team combines hot perimeter shooting with poor possession-generation metrics.

## Fourth-quarter collapse mechanism

Los Angeles entered Q4 leading 58-55, then scored only **12 points**.

In the fourth quarter the Sparks produced:

- **3/12 FG**
- **1/6 from three**
- **6 turnovers**
- only **4 points in the paint**

Washington meanwhile scored **25**.

The key was not merely missed shots. Los Angeles also lost possession quality and ball security as the game tightened.

That is the kind of downside-tail pathway a team-total Under model should explicitly represent.

## Model validation / patch

### `LIVEFLOW_LOW_VOLUME_HOT_SHOOTING_GATE_v1`

For future halftime team-total projections, flag a team for stronger downside-tail compression when all or most of the following are present:

1. **Elevated 3P% relative to baseline**.
2. **Low FGA volume for the points already scored**.
3. **Low offensive-rebound count**.
4. **Meaningful turnover burden**.
5. **Weak paint-scoring share or limited rim pressure**.
6. Opponent owns a clear **rebounding / possession-generation advantage**.

When triggered, do not merely regress shooting percentage toward baseline. Also reduce the probability of an upper-tail team-total outcome because the team lacks enough possession creation to compensate when shooting cools.

### `DERIVATIVE_THESIS_ALIGNMENT_CHECK`

Validated here:

> Bet the derivative that directly expresses the model thesis.

If the bearish signal is concentrated in Team A's scoring sustainability, Team A Under should receive priority over a more indirect full-game or Team B derivative unless those markets possess clearly superior edge and tail protection.

## New / validated tags

- `DERIVATIVE_SELECTION_VALIDATED`
- `EFFICIENCY_REGRESSION_TRAP`
- `LOW_VOLUME_SCORING_FRAGILITY`
- `THREE_POINT_REGRESSION_CONFIRMED`
- `POSSESSION_SUPPORT_DEFICIT`
- `FOURTH_QUARTER_OFFENSIVE_COLLAPSE`
- `MARKET_BLIND_PROJECTION`
- `LIVEFLOW_TOTALS_PACE_REGRESSION_GAP_GATE_v1`

## Final grade

**MARKET-BLIND DIRECTIONAL READ: A**  
**LOS ANGELES TEAM-TOTAL READ: A**  
**DERIVATIVE SELECTION: A**  
**FULL-GAME TOTAL DISCIPLINE: A**  
**ABSOLUTE SCORE CALIBRATION: B-**  
**PROCESS VALUE OF POSTMORTEM: HIGH**

### Bottom line

This was a strong LIVE-FLOW win because the decision was made from the **quality of the halftime scoring process**, not from the raw 39 points on the scoreboard.

Los Angeles looked offensively healthy on the surface, but underneath that number were several warning signs: hot three-point shooting, low shot volume, almost no offensive rebounding, seven turnovers, and a major interior/possession disadvantage against Washington.

SharpEdge froze Los Angeles at **78.5** before seeing William Hill's **82.5**. The market offered four points of line value, and the Sparks ultimately finished at **70**.

The strongest lesson is worth preserving:

> **When scoring efficiency is carrying a team more than possession generation, a live team-total Over can be much more fragile than the scoreboard makes it appear.**
