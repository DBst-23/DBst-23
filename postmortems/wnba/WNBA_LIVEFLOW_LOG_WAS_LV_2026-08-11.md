# WNBA LIVE-FLOW Postmortem — Washington Mystics at Las Vegas Aces

**Date:** 2026-08-11  
**Venue:** Michelob ULTRA Arena, Las Vegas, NV  
**Checkpoint:** Halftime  
**Halftime score:** Washington Mystics 41 — Las Vegas Aces 41  
**Final score:** Las Vegas Aces 86 — Washington Mystics 76  
**Final total:** 162  
**Status:** FINAL — 2 LIVE-FLOW wagers, 2 wins

## SharpEdge frozen projection — before sportsbook comparison

| Market | SharpEdge projection | Actual | Error |
|---|---:|---:|---:|
| Full-game total | 166.0 | 162 | +4.0 |
| Las Vegas team total | 85.0 | 86 | -1.0 |
| Washington team total | 81.0 | 76 | +5.0 |
| Las Vegas spread | -4.0 | -10 | 6 pts toward LV |

Projected second half: **Las Vegas 44 — Washington 40**  
Projected final: **Las Vegas 85 — Washington 81**  
Actual second half: **Las Vegas 45 — Washington 35**  
Actual final: **Las Vegas 86 — Washington 76**

## Sportsbook market at halftime

| Market | William Hill line | SharpEdge | Difference | Final result |
|---|---:|---:|---:|---|
| Full-game total | 172.5 | 166.0 | 6.5 toward Under | **Under by 10.5** |
| Las Vegas team total | 88.5 | 85.0 | 3.5 toward Under | Under by 2.5 |
| Washington team total | 84.5 | 81.0 | 3.5 toward Under | **Under by 8.5** |
| Las Vegas spread | -4.5 | -4.0 | 0.5 toward Washington | LV won by 10 |

## LIVE-FLOW strikes

### Strike 1 — Full-game total

- **Wager:** UNDER 172.5
- **Odds:** -115
- **Stake:** $10.00
- **Paid:** $18.70
- **Net profit:** **+$8.70**
- **Sportsbook:** William Hill
- **Ticket timestamp:** AUG 11 2026, 07:50 PM NV
- **Ticket ID:** `a4bb1c70-95f8-11f1-88d4-f54afcc751f9`
- **Result:** **WIN**

The game finished at **162**, clearing the under by **10.5 points**. The sportsbook's halftime number was 6.5 points above the frozen SharpEdge projection.

### Strike 2 — Washington team total

- **Wager:** Washington Mystics UNDER 84.5
- **Odds:** -115
- **Stake:** $5.00
- **Paid:** $9.35
- **Net profit:** **+$4.35**
- **Sportsbook:** William Hill
- **Ticket timestamp:** AUG 11 2026, 07:53 PM NV
- **Ticket ID:** `fbda1ec0-95f8-11f1-8943-532e9a061b2f`
- **Result:** **WIN**

Washington finished with **76 points**, clearing its team-total under by **8.5 points**. SharpEdge had Washington at **81.0**, 3.5 points below the book's 84.5.

## Combined wager result

| Metric | Result |
|---|---:|
| Total staked | $15.00 |
| Total paid | $28.05 |
| Net profit | **+$13.05** |
| Record | **2-0** |

## Postmortem — projection vs reality

### 1. Full-game total read was correct

At halftime the game had **82 points**. The book hung **172.5**, which implied roughly **90.5 second-half points** were needed to reach the over. SharpEdge projected only **84 second-half points**.

Actual second-half scoring was **80 points**, four points below the SharpEdge projection and 10.5 below the pace required to beat the sportsbook total.

- SharpEdge projected final total: **166**
- Actual final total: **162**
- Absolute projection error: **4 points**
- Book line: **172.5**
- Actual margin to book: **10.5 points Under**

This was a strong LIVE-FLOW read because the projection was reasonably close to the final while the sportsbook number sat materially farther away.

### 2. Washington team-total under was the sharper derivative

Washington scored **41 in the first half** and only **35 in the second half**. The halftime team total of **84.5** required Washington to score **44 more points** after halftime. SharpEdge projected **40 second-half Washington points** and an **81-point final**.

Washington actually scored only **35** after halftime and finished at **76**.

The second-half offensive drop was driven by:

- **35.3% FG** after halftime
- **16.7% from three** after halftime
- only **35 second-half points**
- **7 second-half turnovers**
- Las Vegas turning those mistakes into transition/control possessions

Washington's final total landed **5 points below our projection** and **8.5 below the book line**.

### 3. Las Vegas scoring projection was almost exact

SharpEdge projected Las Vegas at **85**. The Aces finished at **86** — an error of only **1 point**.

Las Vegas scored **45 second-half points**, almost exactly matching our projected **44**. That matters because the full-game under did not require the Aces offense to collapse. The edge came primarily from correctly identifying Washington's likely scoring ceiling.

### 4. Halftime shooting profile contained real regression signals

Washington entered halftime shooting **50% FG, 50% from three and 100% FT**, despite committing **9 turnovers**. That combination was unstable: efficient shooting was masking possession loss.

After halftime Washington fell to **35.3% FG** and **16.7% from three**. The regression signal materialized directly.

Las Vegas, meanwhile, had shot only **41.7% FG** in the first half yet still reached 41 points. Their second-half offense improved to **50% FG**, but the total remained safely under because Washington's offense deteriorated more sharply.

### 5. Defensive disruption remained a valid LIVE-FLOW input

At halftime Las Vegas already had **5 steals and 3 recorded blocks** in the official first-half report. Washington had committed **9 turnovers**.

Washington ultimately finished with **16 turnovers**, while Las Vegas finished with **9 steals and 5 blocks**. The possession-pressure thesis therefore persisted rather than disappearing after halftime.

### 6. Spread pass was correct process even though Las Vegas covered

SharpEdge projected **Las Vegas -4.0** while the book offered **Las Vegas -4.5**. There was no meaningful pricing edge, so the spread was passed.

Las Vegas eventually won by **10**, but that does not retroactively make the spread a good model bet. The LIVE-FLOW process correctly concentrated exposure where the model-to-market disagreement was largest: the total markets.

## What SharpEdge learned

**Confirmed signal:** When a halftime total is inflated above the independent projection while one offense is carrying unsustainably strong shooting alongside elevated turnovers, the full-game Under can offer a legitimate LIVE-FLOW edge.

**Confirmed derivative signal:** Team-total derivatives can expose where the total edge is actually concentrated. Here, Las Vegas landed almost exactly on projection (**86 vs 85**), while Washington undershot projection (**76 vs 81**). The strongest underlying mispricing was therefore Washington's scoring expectation.

**Process reinforcement:** Freeze the projection first, then compare to sportsbook pricing. The winning signal was not simply that 82 first-half points 'looked low.' The edge was that **SharpEdge 166.0** materially disagreed with **William Hill 172.5**, and the component team projections explained why.

## Final grade

**LIVE-FLOW TOTAL READ: A**  
**WASHINGTON TEAM-TOTAL READ: A**  
**PROJECTION ACCURACY: A-**  
**MARKET SELECTION: A**  
**DISCIPLINE / PROCESS: A**

### Final result

**2-0 | +$13.05 net profit**

The primary full-game Under beat the sportsbook line by **10.5 points**, and Washington's team-total Under beat its line by **8.5 points**. Most importantly, the frozen model finished only **4 points off the actual game total**, with the Las Vegas team projection missing by just **1 point**.
