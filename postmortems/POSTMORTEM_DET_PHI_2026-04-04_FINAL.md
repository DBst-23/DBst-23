# Postmortem — DET @ PHI — 2026-04-04

## Final Score
- Detroit Pistons 116
- Philadelphia 76ers 93

## Card Result
- Paul George Higher 4.5 Rebounds ✅
- Ausar Thompson Higher 6.5 Rebounds ❌
- Final card result: 1-1

## Final Statlines
### Detroit Pistons
- Ausar Thompson: 14 PTS, 5 REB, 2 AST, 3 STL, 1 BLK in 25 MIN
- Jalen Duren: 16 PTS, 7 REB, 3 AST in 30 MIN
- Tobias Harris: 19 PTS, 4 REB, 2 AST, 4 STL in 27 MIN
- Daniss Jenkins: 16 PTS, 4 REB, 14 AST in 31 MIN
- Kevin Huerter: 5 REB in 25 MIN
- Ron Holland II: 6 REB in 20 MIN
- Paul Reed: 7 REB in 18 MIN

### Philadelphia 76ers
- Paul George: 20 PTS, 5 REB, 4 AST in 28 MIN
- VJ Edgecombe: 19 PTS, 6 REB in 35 MIN
- Kelly Oubre Jr.: 4 REB in 24 MIN
- Andre Drummond: 3 REB in 18 MIN
- Adem Bona: 4 REB in 23 MIN
- Quentin Grimes: 3 REB in 17 MIN
- Tyrese Maxey: 1 REB in 33 MIN

## Team Context
- Detroit won the game by 23 points.
- Detroit finished with 45 rebounds to Philadelphia’s 33.
- Detroit offensive rebounds: 16
- Philadelphia offensive rebounds: 10
- Detroit second chance points: 21
- Detroit points in paint: 54

## Edge Review
### Paul George Higher 4.5 Rebounds — HIT
This edge survived the environment. Even in a poor overall Philadelphia team performance, George still cleared by the hook. With Embiid out, his rebound role remained viable enough to hold.

### Ausar Thompson Higher 6.5 Rebounds — MISS
This edge failed because the rebound environment was not concentrated through Ausar. Detroit had enough total rebound volume, but the boards were distributed across several Pistons.

## Root Cause Analysis
### 1. Blowout minutes suppression
Detroit controlled the game and Ausar played only 25 minutes. The model needed a stronger penalty for wing rebound overs in blowout-friendly environments.

### 2. Rebound share fragmentation
Detroit’s rebound distribution spread across multiple players:
- Duren: 7
- Reed: 7
- Holland: 6
- Huerter: 5
- Ausar: 5
This was a distributed rebound ecosystem, not a concentrated one.

### 3. Wrong rebound ownership assumption
The read on available rebounds was reasonable, but the ownership of those rebounds was misallocated. Ausar functioned as a rebound participant, not the primary rebound owner.

## Model Tags to Register
- BLOWOUT_MINUTES_SUPPRESSION_WING
- REBOUND_SHARE_FRAGMENTATION
- DET_REBOUND_CLUSTER_ACTIVE
- AUSAR_REBOUND_OWNER_MISCLASSIFICATION
- EMBIID_OUT_WING_REBOUND_LEAKAGE_VALIDATED
- HOOK_VALUE_IMPORTANCE_CONFIRMED

## Lessons
1. Team rebound environment alone is not enough. We must rank who owns the rebound share.
2. Wing rebound overs need a stricter downgrade in likely blowout scripts.
3. Distributed frontcourts should automatically reduce confidence on wing rebound overs.
4. Hook changes matter. Paul George at 4.5 was materially better than earlier higher thresholds.

## Final Summary
The Paul George leg validated the structural read. The Ausar leg failed due to rebound concentration error, not because the whole environment was wrong. Going forward, the model should separate rebound availability from rebound ownership more aggressively in Detroit-style distributed environments.
