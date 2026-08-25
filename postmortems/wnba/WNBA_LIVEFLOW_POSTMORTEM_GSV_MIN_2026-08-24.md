# WNBA LIVE-FLOW Postmortem — Golden State Valkyries at Minnesota Lynx

**Date:** 2026-08-24  
**Checkpoint:** Halftime  
**Venue:** Target Center, Minneapolis, MN  
**Platform:** Kalshi  
**Investment:** NO on Over 149.5 (equivalent to Under 149.5)  
**Displayed market chance at entry:** 59%  
**Cost:** $40.00  
**Paid out:** $65.90  
**Profit:** +$25.90  
**ROI:** +64.75%  
**Result:** WIN  
**Final:** Golden State 80, Minnesota 66  
**Final Total:** 146

---

## 1. Frozen Trigger State

**Halftime:** Golden State 34, Minnesota 32  
**Combined:** 66

SharpEdge generated the fair lines before comparing them with the live market:

- Projected final: **Minnesota 72, Golden State 70**
- Projected full-game total: **142**
- Projected second-half total: **76**

Kalshi subsequently showed a **149.5** total strike.

That created a **7.5-point model-market gap toward the Under**.

Because 66 points had already been scored, the market required **84 second-half points** to finish Over 149.5, while SharpEdge projected approximately **76**.

**Classification:** STRIKE  
**Primary Attack:** NO on Over 149.5

---

## 2. Why the Under Qualified

The first half was unusually low scoring, but SharpEdge did **not** simply extrapolate the 66-point pace.

The model explicitly allowed for positive scoring regression on both sides:

### Golden State
- 34 first-half points
- 39.5% FG
- 25.0% from three
- 0 free-throw attempts

### Minnesota
- 32 first-half points
- 35.5% FG
- 35.3% from three
- 11 turnovers

The critical point was that the model still landed at only **142** even after accounting for likely improvement.

That meant the Under thesis did not require the first-half suppression to persist unchanged. It only required the second half to remain below the market's aggressive 84-point requirement.

---

## 3. Price / Execution Audit

The entry screen displayed **59%** when the position was purchased.

The settled ticket shows:

- Cost: **$40.00**
- Paid out: **$65.90**
- Net profit: **+$25.90**

Using realized ticket economics, the all-in break-even is approximately **60.70%**, which is roughly **-154 American odds**.

SharpEdge's standard max-price threshold is **-125**.

This was therefore a deliberate **price-threshold exception**.

The exception was accepted because the model had a **7.5-point edge to the strike**, materially larger than the usual minimum gap required to justify paying beyond the preferred price cap.

This result does **not** change the -125 standard. It confirms that exceptions must be explicitly labeled and tied to unusually strong model-market separation.

---

## 4. What Actually Happened

The second half produced **80 combined points**:

- Golden State: **46**
- Minnesota: **34**

Final:

**Golden State 80, Minnesota 66 — 146 total**

The wager won by **3.5 points** versus the 149.5 strike.

### Quarter scoring

| Quarter | Golden State | Minnesota | Combined |
|---|---:|---:|---:|
| Q1 | 17 | 16 | 33 |
| Q2 | 17 | 16 | 33 |
| Q3 | 21 | 16 | 37 |
| Q4 | 25 | 18 | 43 |
| **Final** | **80** | **66** | **146** |

The scoring environment accelerated after halftime, exactly as the model anticipated in direction, but the acceleration was stronger than projected.

---

## 5. Projection Audit

| Metric | SharpEdge | Actual | Error |
|---|---:|---:|---:|
| Golden State final | 70 | 80 | +10 |
| Minnesota final | 72 | 66 | -6 |
| Full-game total | 142 | 146 | +4 |
| Second-half total | 76 | 80 | +4 |

The total projection remained useful enough to produce a winning market decision, but the team-level allocation was wrong.

Golden State exceeded its projection by **10**, while Minnesota finished **6 below** projection.

This is an important distinction: the model got the aggregate total direction right while misreading how the points would be distributed.

---

## 6. Golden State's Upside Tail Was Stronger Than Expected

Golden State's first-half perimeter shooting was an obvious positive-regression signal at **25.0% from three**.

That regression arrived forcefully in the second half:

- Golden State second-half FG: **48.5%**
- Golden State second-half 3P: **47.1%**
- Golden State Q4 3P: **6/10 — 60.0%**

The Valkyries scored **25 in Q4** and finished with 80.

SharpEdge correctly identified upward pressure on Golden State scoring, but the realized magnitude exceeded the frozen projection.

This should not be treated as a model failure on the total. It should be stored as evidence that positive regression can have a wider upside tail than the point estimate captures.

---

## 7. Minnesota Failed to Deliver the Expected Offensive Normalization

Minnesota's 11 first-half turnovers suggested likely shot-volume normalization.

That did not translate into a sustained scoring rebound.

Minnesota finished:

- **66 points**
- **35.6% FG**
- **33.3% from three**
- **17 turnovers**

The Lynx scored only:

- 16 in Q3
- 18 in Q4

So the expected positive regression in offensive volume was offset by continued inefficiency and ball-security problems.

This was the primary reason the total remained below 149.5 despite Golden State's second-half surge.

---

## 8. Why the Bet Still Won Despite a +4 Total Projection Error

The pre-market projection was **142** against a **149.5** strike.

That 7.5-point cushion absorbed a 4-point miss in the model's final-total center.

This is exactly why line shopping and model-market separation matter.

A projection does not need to land on the exact final total to create a profitable decision. It needs enough separation from the market that ordinary model error can occur without eliminating the edge.

The final result:

- Model: **142**
- Market: **149.5**
- Actual: **146**

SharpEdge missed the final by **4**, while the market missed it by **3.5 in the opposite direction** relative to the wager threshold.

---

## 9. What SharpEdge Got Right

1. **Projected first, priced second.** The 142 fair total was frozen before the Kalshi line was revealed.
2. **Did not blindly extrapolate the 66-point first half.** The model explicitly expected scoring to rise.
3. **Captured both positive-regression forces.** Golden State's 3-point shooting and Minnesota's turnover profile were recognized.
4. **Maintained enough margin to market.** A 7.5-point edge provided error tolerance.
5. **Selected the cleaner aggregate market.** The game total won even though the team-level projections were directionally split from reality.
6. **Accepted a price exception for a documented reason.** The exception was tied to a large modeled edge rather than emotion or chasing.

---

## 10. What Needs Refinement

### `ASYMMETRIC_REGRESSION_DISTRIBUTION_v1`
Positive regression should not be forced symmetrically across both teams.

Golden State's shooting regression materialized strongly; Minnesota's turnover normalization did not produce corresponding scoring recovery.

### `TEAM_ALLOCATION_ERROR_TRACKING_v1`
Continue tracking:
- full-game total error
- team-total error
- remaining-game total error

A good aggregate total can hide poor team allocation. Those are separate model skills.

### `PRICE_THRESHOLD_EXCEPTION_LOG_v1`
Every investment outside the normal **-125** maximum price must log:
- exact displayed price/probability
- effective all-in break-even if available
- standard threshold
- model edge at entry
- explicit exception rationale

### `EDGE_BUFFER_VALUE_v1`
Large point-value separation should be treated as an error buffer, not as a guarantee of accuracy.

The model missed the actual total by 4 but still produced a winning trade because the market was 7.5 points above the frozen fair value.

---

## 11. Tags

- `LIVE_FLOW_HALFTIME_STRIKE`
- `MARKET_BLIND_EDGE_CONFIRMED`
- `FULL_GAME_TOTAL_UNDER`
- `MODEL_MARKET_DIVERGENCE_7_5`
- `POSITIVE_REGRESSION_MODELED`
- `GSV_3P_REGRESSION_STRONG`
- `MIN_OFFENSIVE_NORMALIZATION_FAILED`
- `TEAM_ALLOCATION_ERROR`
- `EDGE_BUFFER_WORKED`
- `KALSHI_POSITION`
- `PRICE_THRESHOLD_EXCEPTION`
- `PRICE_EXECUTION_LOGGED`
- `WIN`

---

## Final Grade

**STRONG_PROCESS_WIN / TEAM-ALLOCATION MISS**

The investment won, but the useful lesson is more specific than simply recording a green result.

SharpEdge projected **142** before seeing a **149.5** live strike, creating a strong 7.5-point Under edge. The game finished at **146**, so the model was 4 points low but still correctly identified market overpricing.

Golden State's positive regression was stronger than forecast, while Minnesota's expected offensive recovery never fully appeared. That produced a significant team-level allocation error even though the aggregate total thesis survived.

The process remains valid: **project first, compare second, demand meaningful separation, log exact execution price, and explicitly document any exception to the normal -125 price cap.**
