# MIN @ DET Postmortem — 2026-04-02

## Final Score
- **Detroit Pistons 113**
- **Minnesota Timberwolves 108**

## Closing Context
- **Confirmed lineup changes:** Anthony Edwards out, Jaden McDaniels out, Cade Cunningham out, Isaiah Stewart out
- **Close:** Detroit moved from **-3.5 to -5.5**, ML from **-162 to -210**, total from **224.5 to 221**

## Invested Plays
### 1. Ayo Dosunmu — Over 4.5 Rebounds
- **Result:** ✅ HIT
- **Final:** 5 rebounds in 33 minutes
- **Pre-game model read:** role expansion confirmed with Edwards and McDaniels out
- **Closing market confirmation:** strong. Over 4.5 heavily juiced across the market, with several books shading toward 5.5.
- **Postmortem tags:** `HIT_REGISTERED`, `CLV_WIN_CONFIRMED`, `ROLE_EXPANSION_CONFIRMED`

### 2. Jalen Duren — Under 11.5 Rebounds
- **Result:** ❌ MISS
- **Final:** 13 rebounds in 36 minutes
- **Pre-game model read:** Gobert suppression plus mixed-to-slight under lean
- **Closing market confirmation:** mixed. Under support existed, but not enough to qualify as dominant consensus.
- **Failure mode:** Duren’s minutes held, he collected 5 offensive rebounds, and Detroit won the glass overall 48–40.
- **Postmortem tags:** `MISS_REGISTERED`, `CLV_MIXED`, `THIN_UNDER_FAILURE`, `OFFENSIVE_REBOUND_SPIKE`

## Box Score Notes
- Minnesota total rebounds: **40**
- Detroit total rebounds: **48**
- Offensive rebounds: Minnesota **5**, Detroit **9**
- Duren: **14 rebounds (5 offensive)**
- Ayo Dosunmu: **5 rebounds**
- Kyle Anderson: **7 rebounds**
- Naz Reid: **6 rebounds**

## Game Flow / Rebounding Notes
- Detroit generated a stronger second-chance profile than expected.
- Duren’s offensive rebound path was the main killer on the under.
- Minnesota’s missing wing depth did help concentrate peripheral rebound chances toward Ayo and the remaining starters.
- The Ayo over was the true sharp capture on the card and aligned with both injury context and closing-line confirmation.

## Model Verdict
This was **not a full-card read failure**.

### Correct Read
- Ayo’s role-expanded rebound over was valid and closed as a strong market-confirmed edge.

### Incorrect / Thin Read
- Duren under was too thin for pairing. Market support was not strong enough, and the offensive rebound downside was underweighted.

## Actionable Patch
### Card Construction Rule
Do **not** pair a strong confirmed edge with a thinner rebound under unless both legs clear all of the following:
- median separation from line
- market confirmation / CLV alignment
- stable minutes assumption
- low offensive rebound volatility risk

### New Detector Trigger
If a center under depends on defensive suppression but the opposing team projects to lose wing size / scoring efficiency, flag:
- `NO_BET_ZONE_DETECTOR = OFFENSIVE_REBOUND_BACKFILL_RISK`

## Final Grading Summary
- **Ayo Dosunmu O4.5 REB** → Sharp win
- **Jalen Duren U11.5 REB** → Thin miss
- **Card verdict:** strong anchor + weak pairing leg

## Registry Labels
- `CLV_WIN_CONFIRMED`
- `ROLE_EXPANSION_CONFIRMED`
- `THIN_UNDER_FAILURE`
- `OFFENSIVE_REBOUND_SPIKE`
- `CARD_CONSTRUCTION_FAILURE`
