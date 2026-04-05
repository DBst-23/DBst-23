# Postmortem — DET @ PHI — 2026-04-04

## Final Score
- Detroit Pistons 116
- Philadelphia 76ers 93

## Tracked Card
- Paul George — Higher 4.5 Rebounds ✅ (finished with 5)
- Ausar Thompson — Higher 6.5 Rebounds ❌ (finished with 5)

## Core Result
The card split 1-1. Paul George cleared by the hook, while Ausar Thompson fell short by 1.5 rebounds in a Detroit blowout win.

## Box Score Highlights
### Detroit
- Ausar Thompson: 14 points, 5 rebounds, 2 assists, 3 steals, 1 block in 25 minutes
- Jalen Duren: 16 points, 7 rebounds in 30 minutes
- Tobias Harris: 19 points, 4 rebounds in 27 minutes
- Daniss Jenkins: 16 points, 4 rebounds, 14 assists in 31 minutes
- Paul Reed: 10 points, 7 rebounds in 18 minutes
- Ron Holland II: 11 points, 6 rebounds in 20 minutes

### Philadelphia
- Paul George: 20 points, 5 rebounds, 4 assists in 28 minutes
- VJ Edgecombe: 19 points, 6 rebounds in 35 minutes
- Kelly Oubre Jr.: 4 rebounds in 24 minutes
- Andre Drummond: 3 rebounds in 18 minutes
- Adem Bona: 4 rebounds in 23 minutes
- Quentin Grimes: 3 rebounds in 17 minutes

## Why Paul George Over Worked
- Embiid was out, keeping Philadelphia’s rebound distribution more open.
- George played 28 minutes and still got to 5 despite the loss.
- His role stayed active enough on the glass even in a poor team environment.
- The line reduction to 4.5 created a more playable entry than the earlier 5.5 framework.

## Why Ausar Thompson Over Failed
### 1. Blowout compression
- Detroit won by 23.
- Ausar played only 25 minutes.
- Competitive-script minutes never arrived.

### 2. Rebound share got redistributed
- Detroit finished with 45 rebounds, but Ausar only secured 5.
- Duren had 7, Paul Reed had 7, Ron Holland had 6, Huerter had 5.
- The rebound ecosystem distributed across multiple Pistons instead of concentrating through Ausar.

### 3. Offensive stat profile shifted away from boards
- Ausar contributed in steals, blocks, transition activity, and scoring efficiency.
- His impact remained strong, but not through rebound accumulation.

## Structural Takeaways
### 1. Wing rebound overs remain vulnerable in Detroit blowouts
Ausar is a strong chaos-board archetype, but if Detroit wins comfortably and frontcourt depth is active, his rebound ceiling can flatten.

### 2. Distributed rebound environments need stronger concentration filters
Detroit had enough team rebound volume, but the share was split across Duren, Reed, Holland, Huerter, and Ausar. Team volume alone was not enough.

### 3. Hook sensitivity matters
Paul George over became materially better at 4.5 than 5.5. This game validates the need to track late-line changes closely on medium-confidence overs.

## Model Patches / Tags
- BLOWOUT_MINUTES_SUPPRESSION_WING
- DET_REBOUND_DISTRIBUTION_CLUSTER_ACTIVE
- HOOK_VALUE_IMPORTANCE_CONFIRMED
- EMBIID_OUT_WING_REBOUND_LEAKAGE_VALIDATED
- AUSAR_REBOUND_CONCENTRATION_WARNING

## Final Evaluation
### Hit
- Paul George Over 4.5 rebounds ✅

### Miss
- Ausar Thompson Over 6.5 rebounds ❌

## Summary
This was not a bad read on Ausar’s archetype, but it was a bad final environment for a wing rebound over. The game turned into a Detroit-controlled blowout, minutes compressed, and Detroit’s rebound share spread across too many contributors. Paul George, meanwhile, remained the cleaner structural play and got home.
