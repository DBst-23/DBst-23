# NBA Postmortem — DET @ ORL — 2026-04-06

## Final Score
- Detroit Pistons 107
- Orlando Magic 123

## Logged Bet Result
- ✅ Daniss Jenkins Higher 17.5 Points — **WIN** (18)
- ❌ Jalen Duren Higher 11.5 Rebounds — **LOSS** (9)
- ❌ Wendell Carter Jr. Higher 7.5 Rebounds — **LOSS** (3)
- Ticket result: **1/3 LOSS**

## Market Context
- Jenkins was laddered down from sharper market ranges that were sitting mostly around 18.5 to 19.5, with some 17.5 support and a low-end 16.5 at PolyMarket.
- Rebound thesis was built around expected frontcourt concentration and stable starter minutes on both sides.

## Actual Statlines
### Detroit targets
- Daniss Jenkins: 18 points, 2 rebounds, 7 assists in 34 minutes
- Jalen Duren: 18 points, 9 rebounds, 4 assists in 32 minutes

### Orlando target
- Wendell Carter Jr.: 12 points, 3 rebounds, 3 assists in 18 minutes

## Team Rebound Environment
- Detroit team rebounds: **35**
- Orlando team rebounds: **35**
- Total game rebounds: **70**
- Detroit offensive rebounds: 8
- Orlando offensive rebounds: 6

## Why Jenkins Hit
1. **Role and usage stayed intact**
   - Jenkins played 34 minutes and cleared the laddered 17.5 line with 18.
2. **Ladder was correct**
   - Taking 17.5 instead of a consensus 18.5/19.5 protected the edge and turned a near-threshold scoring performance into a win.
3. **Ball-dominant creation was preserved**
   - He also posted 7 assists, confirming strong on-ball responsibility.

## Why the Rebound Legs Missed
### 1. Rebound environment collapsed versus expectation
- Total team rebounds finished **35-35**, which is flat and relatively muted for two overs that needed concentrated frontcourt volume.
- This game did **not** become the dense miss-volume board environment the pregame read implied.

### 2. Wendell Carter Jr. lost the minutes battle
- Carter played only **18 minutes**.
- Goga Bitadze logged 24 minutes and Jevon Carter chipped in 19, while Orlando spread the rotation in a blowout-friendly script.
- Even with a 16-point Magic win, Carter never had enough floor time to threaten 7.5.

### 3. Duren was solid but not dominant enough
- Duren finished with **9 rebounds in 32 minutes**.
- He was productive scoring-wise, but Detroit’s rebound distribution widened:
  - Paul Reed had 6 in 19 minutes
  - Javonte Green had 6 in 27 minutes
- Shared frontcourt rebounding and a less-dense board environment kept him below the number.

### 4. Orlando efficiency reduced rebound supply
- Orlando shot **50.6% FG** and **42.3% from three**, dramatically cutting available defensive rebound chances for Detroit bigs.
- Detroit also shot nearly **49.4%**, which lowered Orlando’s rebound opportunity pool as well.

## Hidden Failure Points
1. **Efficiency trap**
   - Both teams were too efficient for double rebound overs to thrive.
2. **Minutes fragility on Carter**
   - Carter over was highly sensitive to rotation volatility and failed immediately once his minutes settled at 18.
3. **Distributed board share**
   - Detroit did not funnel rebounds cleanly enough to Duren, especially with Reed and Green active on the glass.

## Model Relevance Summary
### Confirmed signals
- **Ladder discipline matters** on scoring props.
- **Raw starter status is not enough** for rebound overs when minute security is weak.
- **Team efficiency must be weighted more heavily** before green-lighting double rebound overs.

### Patches to apply
- Add a stronger **high-efficiency suppression penalty** for rebound overs when both teams project efficiently.
- Add a **minutes-security gate** for center overs above 7.5 when there is credible bench-center siphon risk.
- Add a **shared-frontcourt rebound tax** when multiple teammates project as active rebound contributors.

## Final Postmortem Verdict
This ticket split cleanly between:
- a **good process scoring leg** on Jenkins, improved by a smart ladder,
- and **two rebound overs that were structurally weaker than they appeared** once efficiency and minutes volatility took over.

Jenkins was a valid edge.
Duren and Carter were not true clean rebound environments by outcome profile.

## Tags
- EDGE_CALL_ACTIVE
- HIT_REGISTERED
- MISS_REGISTERED
- LADDER_EXECUTION_GOOD
- EFFICIENCY_SUPPRESSION_EVENT
- CENTER_MINUTES_VOLATILITY
- SHARED_REBOUND_DISTRIBUTION
