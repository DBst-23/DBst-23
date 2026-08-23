# WNBA LIVE-FLOW Postmortem — Connecticut Sun at Los Angeles Sparks

**Date:** 2026-08-22  
**Market:** Full Game Total — Live  
**Sportsbook:** William Hill  
**Wager:** Under 162.5 (-115)  
**Stake:** $15.00  
**Profit:** +$13.04  
**Payout:** $28.04  
**Result:** WIN  
**Final:** Los Angeles Sparks 77, Connecticut Sun 68  
**Final Total:** 145

---

## 1. Trigger State

**Halftime:** Los Angeles 44, Connecticut 36  
**Combined:** 80

SharpEdge generated its fair lines **before sportsbook comparison**:

- Projected final: **Los Angeles 83, Connecticut 73**
- Projected full-game total: **156**
- Projected second half: **Los Angeles 39, Connecticut 37 — 76 combined**
- Projected spread: **Los Angeles -10**

William Hill then showed:

- Full-game total: **162.5**
- Los Angeles team total: **85.5**
- Connecticut team total: **76.5**
- Los Angeles spread: **-9.5**

This created a **6.5-point gap toward the Under**. The book's 162.5 also implied approximately **82.5 second-half points**, compared with SharpEdge's 76.

**Classification:** STRIKE  
**Primary Attack:** Full Game Under 162.5

---

## 2. Why the Under Qualified

The 80-point halftime total was misleading if treated as a flat scoring-rate environment.

Los Angeles scored **32 points in Q1 on 78.6% field-goal shooting**, an extreme conversion level. The game then shifted sharply in Q2, where the teams combined for only **26 points**.

The important signal was not simply that scoring slowed. It was that the slowdown was supported by the underlying profile:

- Connecticut halftime FG%: **35.1%**
- Connecticut halftime 3P%: **15.4%**
- Los Angeles halftime FG%: **45.2%**
- Los Angeles halftime 3P%: **40.0%**
- Q1 combined scoring: **54**
- Q2 combined scoring: **26**

SharpEdge therefore treated the explosive first quarter as the less sustainable regime and projected the second half independently instead of extrapolating the first-half average.

A key structural confirmation was that **both team-total projections were below market**:

- Los Angeles: SharpEdge **83** vs book **85.5**
- Connecticut: SharpEdge **73** vs book **76.5**

That made the full-game Under a cleaner derivative than attacking only one team total.

---

## 3. What Actually Happened

The second half produced only **65 points**, 11 below the SharpEdge projection and 17.5 below the sportsbook's implied second-half requirement.

### Quarter scoring

| Quarter | Connecticut | Los Angeles | Combined |
|---|---:|---:|---:|
| Q1 | 22 | 32 | 54 |
| Q2 | 14 | 12 | 26 |
| Q3 | 10 | 22 | 32 |
| Q4 | 22 | 11 | 33 |

The game never returned to the Q1 scoring environment.

Connecticut scored only **10 points in Q3 on 25.0% shooting**, and although Los Angeles was efficient during that quarter, Connecticut's offensive suppression kept the total well controlled.

In Q4, the scoring burden reversed: Connecticut produced 22 while Los Angeles managed only 11.

---

## 4. Projection Audit

| Metric | SharpEdge | Actual | Error (Actual - Projection) |
|---|---:|---:|---:|
| Connecticut final | 73 | 68 | -5 |
| Los Angeles final | 83 | 77 | -6 |
| Full-game total | 156 | 145 | -11 |
| Second-half total | 76 | 65 | -11 |

The wager line was **162.5**, so the Under finished with a **17.5-point cushion**.

That final cushion should not be confused with the original modeled edge. The pre-wager edge was **6.5 points**. The rest came from realized game variance.

---

## 5. What SharpEdge Got Right

1. **Market-blind fair value was established first.** The 156 projection existed before the sportsbook number was revealed.
2. **The first-quarter spike was not over-weighted.** Los Angeles' 78.6% Q1 shooting was correctly treated as unstable.
3. **The quarter regime shift mattered.** The 26-point Q2 was a meaningful state change rather than automatically being dismissed as noise.
4. **Both team totals supported the same direction.** That reduced the allocation risk that had hurt prior team-total derivatives.
5. **Connecticut's perimeter weakness persisted.** The Sun were 15.4% from three at halftime and finished 16.7%.
6. **Second-half scoring was correctly priced below market expectation.** SharpEdge projected 76; the book effectively required 82.5; actual scoring was 65.

---

## 6. Important Variance That Should NOT Be Back-Fitted

Los Angeles finished with **25 turnovers**, while Connecticut recorded **15 steals**. Those events can sometimes accelerate transition scoring and threaten an Under. Here, the Sun did not convert them efficiently enough to do so.

More importantly, **Dearica Hamby was ejected on a flagrant-2 with 8:39 remaining in Q4**. That likely added downside to Los Angeles' late scoring ceiling, but it occurred after the wager was placed.

It must therefore be logged as **post-wager variance**, not as evidence that the original projection was somehow more accurate than it really was.

---

## 7. Model Reinforcement

### `LIVEFLOW_HALFTIME_REGIME_CONFIRMATION_v1`

- When a high-scoring Q1 is followed by a materially slower Q2, do not anchor to the first-half average. Identify which scoring regime has the stronger sustainable support.
- Continue producing the full projection before sportsbook comparison and preserve that number in the audit trail.
- Prefer the full-game total when **both independently projected team totals** point in the same direction against market.
- Track three-point efficiency separately from total field-goal percentage; sustained perimeter suppression can materially lower a live total ceiling.
- Treat post-wager injuries, ejections, and other game-state shocks as realized variance unless they were visible at the moment of execution.
- Continue separating **modeled edge** from **final margin of victory**. A large win does not justify inflating future confidence.

---

## 8. Tags

- `MARKET_BLIND_EDGE_CONFIRMED`
- `Q1_SCORING_REGRESSION`
- `Q2_REGIME_CONFIRMATION`
- `BOTH_TEAM_TOTALS_UNDER_MARKET`
- `FULL_GAME_DERIVATIVE_ALIGNMENT`
- `PERSISTENT_THREE_POINT_SUPPRESSION`
- `POST_WAGER_EJECTION_VARIANCE`

---

## Final Grade

**STRONG_MODEL_WIN**

The most important part of this result was not that the Under won by 17.5 points. It was that the process stayed clean: **project first, compare second, attack the market only after the model-market gap is known**.

SharpEdge had a 156 fair total against a 162.5 market, and both team-total projections supported the same Under direction. The game then finished at 145.

This is a positive LIVE-FLOW template to retain, especially as a contrast to earlier cases where the combined total read was correct but the selected team-total derivative introduced unnecessary allocation risk.
