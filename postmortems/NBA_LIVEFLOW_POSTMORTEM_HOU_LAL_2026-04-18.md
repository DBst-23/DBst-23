# NBA LiveFlow Postmortem — HOU @ LAL — 2026-04-18

## Summary
- **Game:** Houston Rockets @ Los Angeles Lakers
- **Final:** Lakers 107, Rockets 98
- **LiveFlow Entry:** Full game over 195.5
- **Ticket Price:** 41%
- **Result:** ✅ WIN
- **Classification:** FAKE_SUPPRESSION
- **Primary Edge Type:** live total over recovery

## Pregame Context
The game entered LiveFlow with a market environment that had already priced in a moderate-scoring NBA script, but the in-game board later compressed enough to open a recovery lane.

## LiveFlow Snapshot and Entry Logic
The LiveFlow card was:
- **Over 195.5 points scored**
- Entry price: **41%**

This was a classic suppression-recovery setup.

### Why the over became attractive
At the time of the live entry, the market had dropped the total to a level that implied an overly damaged scoring environment. But the game profile still had enough structural offense left to support recovery.

The key distinction:
- this was **not** real suppression
- it was **fake suppression** created by temporary inefficiency and game-state distortion

## Final Outcome
- **Houston:** 98
- **Lakers:** 107
- **Final total:** **205**
- **Live over 195.5:** ✅ WIN by **9.5 points**

## Why the Bet Won
### 1. The Lakers offensive side remained highly functional
Final LAL profile:
- **107 points**
- **40-66 FG (60.6%)**
- **10-19 3PT (52.6%)**
- **29 assists**

This is a highly efficient offensive output and validates that the game never truly died.

### 2. Houston still contributed enough volume
Final HOU profile:
- **98 points**
- **35-93 FG**
- **44 rebounds**
- **21 offensive rebounds**
- **24 assists**

Houston was inefficient, but they still generated enough possessions and second-chance opportunities to keep the total alive.

### 3. Possession count and extra-chance ecology supported recovery
The Rockets produced:
- **21 offensive rebounds**
- **23 second-chance points**

That is exactly the kind of hidden structural support that can rescue a depressed live total.

### 4. The live market overcorrected to temporary suppression
A total of **195.5** proved too low once the full possession environment and Lakers scoring quality were accounted for.

## Environment Diagnosis
### FAKE_SUPPRESSION confirmed
This game should be tagged as a benchmark case where the board looked under-friendly at first glance, but the underlying mechanics said otherwise.

#### Supporting signals
- Lakers shot quality and conversion remained strong
- Houston generated enough volume and offensive rebounds to extend possessions
- The total was depressed below the true scoring floor of the environment

## Diagnostic Tags
- `LIVEFLOW_WIN`
- `FAKE_SUPPRESSION_CONFIRMED`
- `LIVE_TOTAL_OVER_RECOVERY`
- `OFFENSIVE_REBOUND_SUPPORT`
- `SECOND_CHANCE_SCORING_VALIDATED`
- `LAL_EFFICIENCY_DRIVER`

## Model Relevance Summary
This game matters because it reinforces a core LiveFlow rule:

> When a live total is pushed too low in a game where at least one offense is still highly efficient and the possession ecology remains active, the over can become the best recovery lane.

### What the model should retain
- Do not confuse temporary scoring drag with true suppression.
- Offensive rebound volume can keep an over alive even when one side shoots poorly.
- A live total in the mid-190s can be too cheap if the stronger offense still has structural efficiency and the weaker side still has enough attempts / second chances.

## Final SharpEdge Lesson
This was not a blind over. It was a **market correction bet** on a falsely compressed total.

That distinction should remain central in future LiveFlow reads.

---

## Addendum — LiveFlow Bet Result: Minnesota @ Denver Under 245.5

### Bet Details
- **Bet:** Full Game Under 245.5
- **Game:** Minnesota Timberwolves @ Denver Nuggets
- **Entry Timing:** Halftime, tied 64-64
- **Result:** ✅ WIN
- **Final Score:** Minnesota 119, Denver 114
- **Final Total:** 233
- **Margin vs Line:** 12.5 points under

### Why the Bet Won
The live under cashed because the halftime number was repriced too aggressively off first-half shotmaking.

At the break, both teams had produced an extremely hot offensive half:
- **Minnesota 11-22 from three (50.0%)**
- **Denver 10-20 from three (50.0%)**
- both teams above **64 TS%**
- only **5 turnovers each**

That environment was real enough to justify a high live total, but **245.5** priced in too much continued perfection.

### Key Drivers
1. **Three-point heat cooled enough in the second half**
   - Minnesota finished **14-34 from three (41.2%)**
   - Denver finished **15-41 from three (36.6%)**
   - Both teams fell back toward a more sustainable conversion range

2. **Shot volume stayed high, but not at elite enough efficiency to clear 246**
   - Minnesota finished with **119**
   - Denver finished with **114**
   - Combined total reached only **233**

3. **Denver offensive ceiling was lower than the halftime number implied**
   - Denver needed a huge second-half scoring continuation to threaten the number
   - They finished at **114**, well below the live expectation path attached to a 245.5 total

4. **Minnesota’s offensive support was broad but not explosive enough to break the number alone**
   - Randle: **24**
   - Edwards: **30**
   - DiVincenzo: **16**
   - Naz Reid: **11**
   - Ayo Dosunmu: **9**
   - Bones Hyland: **13**
   - Strong output, but still within an under-friendly final structure once the shooting normalized

5. **The game was driven by first-half heat more than true unstoppable pace ecology**
   - There was scoring quality, but not enough second-half continuation to justify 118 more points after halftime

### Diagnostic Tags
- `LIVEFLOW_WIN`
- `HALFTIME_HEAT_FADE_CONFIRMED`
- `LIVE_TOTAL_UNDER_VALIDATED`
- `THREE_POINT_REGRESSION_HELD`
- `NO_PERFECTION_CONTINUATION`
- `EDGE_CALL_ACTIVE`

### Model Relevance
This addendum should reinforce a core LiveFlow rule:

**When a halftime total is inflated mainly by elite first-half shooting rather than true possession-chaos ecology, the under becomes the better side if the new number requires continued perfection.**

Minnesota @ Denver is now a clean example of a **halftime heat-fade under** that held comfortably once both teams regressed toward more sustainable shooting levels.
