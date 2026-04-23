# NBA POSTMORTEM REPORT – ORL @ DET (2026-04-22)

## Final Score
- Orlando Magic 83
- Detroit Pistons 98
- Final Total: 181

## Betting Results Logged
- ✅ Full Game Total Under 201.5 — WIN
- ❌ Full Game Total Over 196.5 — LOSS
- ✅ Detroit Team Total Under 103.5 — WIN
- ❌ Orlando Team Total Over 96.5 — LOSS
- ✅ Detroit -4.5 — WIN

---

## Phase 1 — Game Phase Analysis

### 1Q
- DET led 25–21 after one quarter.
- Early read showed a halfcourt, physical game with limited clean shot creation and some rebound activity on both sides.
- Orlando was process-stable enough to stay live but not efficient enough to convert possessions into scoring.

### 2Q / Halftime
- Game reached halftime tied 46–46.
- Halftime environment classified as a halfcourt grind with high misses and heavy rebound volume.
- At halftime, the strongest live edge identified was Full Game Under 201.5.
- Secondary angle identified was Detroit Team Total Under 103.5.
- Orlando Team Total Over 96.5 was graded only as a thin bounceback lean.
- Detroit -4.5 was graded as playable later because Detroit looked structurally stronger despite the tie.

### 3Q
- Detroit asserted control with cleaner interior offense and superior rebound leverage.
- Orlando’s offense failed to recover from poor shotmaking despite offensive rebounding and free throw volume.
- Detroit’s size and physicality became more decisive as the game moved deeper into the second half.

### 4Q
- Detroit closed the game comfortably and won by 15.
- Orlando never mounted enough offensive stability to threaten the total or its live team total over.
- Final total stayed well below both live full-game numbers.

---

## Phase 2 — Pivotal Moments

1. **Orlando’s offensive collapse from the field**
   - Orlando finished 26-of-80 from the field (32.5%) and 8-of-32 from three (25.0%).
   - Despite 32 free throw attempts and 13 offensive rebounds, the Magic could not convert enough live-ball or halfcourt possessions.

2. **Detroit’s rebound and paint dominance**
   - Detroit won the rebound battle 57–42 and posted 17 offensive rebounds.
   - Detroit also won points in the paint 54–34.
   - This created sustained second-possession pressure and prevented Orlando from climbing back in.

3. **Shot quality mismatch despite similar raw possession noise**
   - Orlando generated steals (16) and blocks (6), but Detroit still finished with the more repeatable offensive profile.
   - Detroit’s interior finishing and rebounding edge overpowered Orlando’s defensive activity.

4. **Live middle-band failure**
   - The paired structure of Under 201.5 and Over 196.5 created a 197–201 middle band.
   - Final total of 181 missed the middle entirely, so only the under side cashed.

---

## Phase 3 — Defensive / Psychological Variables

### Detroit
- Detroit imposed the more physical identity.
- Strong rebounding concentration from Tobias Harris, Jalen Duren, Ausar Thompson, and Isaiah Stewart stabilized the game.
- Cade Cunningham’s 27 points and 11 assists gave Detroit the cleanest offensive engine on the floor.

### Orlando
- Orlando generated defensive events (16 steals, 6 blocks), but their offense remained too unstable.
- Paolo Banchero and Franz Wagner both failed to convert efficiently enough to lift team scoring.
- Wendell Carter Jr. posted high rebound-chance volume but poor shooting and limited finishing impact.
- The Magic’s inability to turn extra possessions into clean points was the defining failure mode.

---

## Phase 4 — Model Relevance Summary

## What the model got right
- **Full Game Under 201.5** was the correct primary live edge.
- **Detroit Team Total Under 103.5** was correctly identified as a cleaner under than the full-game side for Detroit-specific inflation control.
- **Detroit -4.5** ultimately validated because Detroit’s structural rebounding and interior edge became decisive.
- The game texture was correctly classified as physical, rebound-heavy, and not a true shootout.

## What missed
- **Orlando Team Total Over 96.5** was too thin and should not have been treated as anything stronger than a fringe bounceback angle.
- **Over 196.5** middle-band protection failed because Orlando’s offense was much worse than its halftime process suggested.

## Rebound / tracking insights
- Detroit tracking data showed stronger, cleaner rebound capture from core rotation pieces:
  - Tobias Harris: 11 rebounds on 15 chances
  - Jalen Duren: 9 rebounds on 15 chances
  - Ausar Thompson: 8 rebounds on 9 chances
- Orlando showed decent rebound opportunity volume but lower scoring conversion off those extended possessions.
- Team box-outs were modest on both sides, but Detroit’s frontcourt physicality still won the practical rebounding environment.

## Tags
- EDGE_CALL_ACTIVE
- HIT_REGISTERED: FG Under 201.5
- HIT_REGISTERED: Detroit TT Under 103.5
- HIT_REGISTERED: Detroit -4.5
- MISS_REGISTERED: Orlando TT Over 96.5
- MISS_REGISTERED: Middle Band Protection Over 196.5
- REBOUND_EDGE_SIGNAL
- HALFCOURT_GRIND_ENVIRONMENT
- OFFENSIVE_COLLAPSE_FLAG_ORL

## Retraining Notes
1. Orlando-style bounceback team total overs must require stronger shot-quality recovery evidence before activation.
2. Rebound-heavy games should not automatically imply scoring recovery when shotmaking collapse is team-wide and persistent.
3. Middle-band protection should be sized more carefully when one side of the game has clear offensive fragility.
4. Detroit’s rebound cluster (Harris / Duren / Ausar / Stewart) should be flagged as a series-level strength for follow-up rebound markets.
