# WNBA LIVE-FLOW Postmortem — Indiana Fever at Chicago Sky

**Date:** 2026-08-23  
**Checkpoint:** Halftime  
**Venue:** Wintrust Arena, Chicago, IL  
**Sportsbook/Market Screen:** Kalshi live market supplied after SharpEdge projection  
**Decision:** NO BET / NO WAGER LOGGED  
**Final:** Indiana Fever 113, Chicago Sky 90  
**Final Total:** 203

---

## 1. Trigger State

**Halftime:** Chicago 51, Indiana 50  
**Combined:** 101

The live market screen subsequently showed:

- Indiana live spread: **-1.5**
- Full-game total: **192.5**
- Chicago team total: **97.5**

The 192.5 total required **91.5 second-half points** to finish Over.

No wager ticket was logged before SharpEdge moved to the next LIVE-FLOW strike, so this checkpoint is graded as a **PASS / NO BET** rather than retrospectively assigning a wager.

---

## 2. Halftime Profile

The first half was already high-scoring at **101 points**, but the scoring path was unusual.

### Indiana first half
- 50 points
- 20/45 FG — **44.4%**
- 5/16 3PT — **31.2%**
- 5/8 FT — 62.5%
- 13 assists
- 6 turnovers

### Chicago first half
- 51 points
- 19/38 FG — **50.0%**
- 2/8 3PT — **25.0%**
- 11/11 FT — **100%**
- 14 assists
- 6 turnovers

### Important halftime signals

1. Chicago reached 51 despite making only **two threes**.
2. Chicago was perfect at the foul line, creating some scoring inflation.
3. Indiana was only 31.2% from three despite Caitlin Clark already having 18 points.
4. Both offenses were producing efficiently inside the arc.
5. The game had been highly competitive: **9 lead changes and 8 ties** by halftime.

This was not a clean one-direction regression setup. Chicago had obvious free-throw and shooting-normalization risk, while Indiana had meaningful positive 3-point regression potential.

---

## 3. What Actually Happened

The second half produced **102 points**:

- Indiana: **63**
- Chicago: **39**

Final:

**Indiana 113, Chicago 90 — 203 total**

Relative to the displayed live total of 192.5:

- Actual final: **203**
- Market line: **192.5**
- Result: **10.5 points Over**

Relative to Chicago's 97.5 team total:

- Actual Chicago: **90**
- Market line: **97.5**
- Result: **7.5 points Under**

Indiana turned the second half into an offensive eruption while Chicago's offense collapsed in the fourth quarter.

---

## 4. Quarter-by-Quarter Path

| Quarter | Indiana | Chicago | Combined |
|---|---:|---:|---:|
| Q1 | 28 | 28 | 56 |
| Q2 | 22 | 23 | 45 |
| Q3 | 33 | 26 | 59 |
| Q4 | 30 | 13 | 43 |
| **Final** | **113** | **90** | **203** |

The key distinction is that the game did **not** remain symmetrically high-scoring.

Indiana scored **63 second-half points**, while Chicago scored only **39**.

That means a full-game Over and a Chicago team-total Under could both be correct simultaneously.

---

## 5. Third-Quarter Breakout

Indiana's third quarter was the decisive regime change.

### Indiana Q3
- 33 points
- 12/20 FG — **60.0%**
- 8/11 3PT — **72.7%**
- only 1 turnover

Kelsey Mitchell and Caitlin Clark combined for **25 Q3 points**:

- Mitchell: 14
- Clark: 11

Chicago also shot well in Q3:

- 26 points
- 11/17 FG — **64.7%**

So the quarter produced **59 combined points** and moved the game from 101 at halftime to **160 through three quarters**.

At that point the original 192.5 market total needed only 32.5 more points to go Over.

---

## 6. Fourth-Quarter Divergence

The fourth quarter is where the team-total paths separated sharply.

### Indiana Q4
- 30 points
- 10/14 FG — **71.4%**
- 5/6 3PT — **83.3%**
- 5/6 FT

### Chicago Q4
- 13 points
- 5/14 FG — **35.7%**
- 0/7 3PT
- 5 turnovers

Indiana's perimeter shooting remained scorching, while Chicago's offense completely lost its spacing and shot-making.

This is a strong example of why LIVE-FLOW cannot treat a full-game total and both team totals as equivalent expressions of the same thesis.

---

## 7. Star-Driven Offensive Regime

Indiana's offense became concentrated in two elite creators.

### Caitlin Clark
- 37 points
- 13/24 FG
- 8/12 from three
- 10 assists

### Kelsey Mitchell
- 30 points
- 10/19 FG
- 6/9 from three

Together:

- **67 points**
- **14 made threes**

Indiana as a team finished **18/33 from three (54.5%)**.

The central postmortem lesson is that Indiana's first-half 31.2% from three was not evidence of a low-scoring game state. With Clark and Mitchell carrying heavy creation volume, it also represented substantial upside if shot-making normalized upward.

---

## 8. Chicago Offensive Collapse

Chicago's halftime 51-point output did not persist.

Second half:

- 39 points
- 16/31 FG
- 2/13 from three
- 8 turnovers

Fourth quarter specifically:

- **13 points**
- **0/7 from three**
- **5 turnovers**

Chicago finished only **4/21 from three (19.0%)** for the game.

The team total of 97.5 therefore failed despite Chicago being on pace for 102 at halftime.

This reinforces that raw halftime pace extrapolation is not enough. Shot profile, ball security, foul dependence and sustainable half-court creation must be separated.

---

## 9. Projection/Market Audit

The exact numeric market-blind SharpEdge frozen projection from immediately before the Kalshi screen is not stored in the repository, so this postmortem does **not invent one**.

The preserved market values are:

| Metric | Market | Actual |
|---|---:|---:|
| Full-game total | 192.5 | 203 |
| Remaining points at HT | 91.5 implied | 102 |
| Chicago team total | 97.5 | 90 |
| Indiana live spread | -1.5 | won by 23 |

### Market misses

- Full-game total: **10.5 points low**
- Chicago team total: **7.5 points high**
- Indiana -1.5: Indiana won by **23**

The market materially underestimated Indiana's second-half offensive ceiling and overestimated Chicago's ability to sustain its first-half scoring rate.

---

## 10. What SharpEdge Should Learn

### `ASYMMETRIC_TOTAL_DECOMPOSITION_v1`
Do not treat a high game total as requiring both teams to remain offensively strong.

A full-game Over can be driven by one team exploding while the other regresses sharply.

### `STAR_BACKCOURT_POSITIVE_REGRESSION_GATE_v1`
When elite high-volume perimeter creators are below expected 3-point efficiency at halftime, model the upside tail explicitly instead of automatically interpreting the state as total regression.

Indiana moved from 5/16 from three in the first half to **13/17 from three in the second half**.

### `TEAM_TOTAL_SUSTAINABILITY_SPLIT_v1`
For team totals, separate:
- free-throw dependence
- 3-point sustainability
- turnover risk
- half-court shot creation
- opponent defensive adjustment

Chicago's 51 first-half points were supported by **11/11 free throws** despite only 2 made threes. That scoring composition was less stable than the raw point total suggested.

### `Q3_REGIME_CHANGE_CONFIRMATION_v1`
A third-quarter shooting breakout from primary creators can represent a genuine live regime change, not merely noise to fade.

Clark and Mitchell repeatedly generated clean high-value shots and Indiana's turnover control improved dramatically.

### `FULL_GAME_VS_TEAM_TOTAL_DIVERGENCE_v1`
Always score each market independently:
- Full-game total
- Favorite team total
- Underdog team total
- Spread

This game produced:
- Full-game **Over**
- Chicago TT **Under**
- Indiana spread **cover**

Those outcomes were not contradictory; they came from the same asymmetric second-half structure.

---

## 11. Process Grade

### Discipline
**A**

No wager was logged at the checkpoint, so SharpEdge did not force exposure into an ambiguous halftime state.

### Market decomposition
**B- / needs refinement**

The final result emphasizes that game-total and team-total paths need to be separated more aggressively.

### Regression handling
**B-**

Chicago had legitimate regression risk, but Indiana had equally important positive shooting-regression potential. Future projections should explicitly model both directions rather than collapsing them into one net regression assumption.

### Capital management
**A**

No forced wager means no bankroll loss from an uncertain edge.

---

## 12. Tags

- `NO_BET_DISCIPLINE`
- `HALFTIME_LIVEFLOW`
- `ASYMMETRIC_SECOND_HALF`
- `INDIANA_OFFENSIVE_EXPLOSION`
- `CLARK_MITCHELL_CREATION`
- `POSITIVE_3PT_REGRESSION`
- `CHICAGO_Q4_COLLAPSE`
- `TEAM_TOTAL_DIVERGENCE`
- `FULL_GAME_OVER_TEAM_TOTAL_UNDER`
- `MARKET_UNDERESTIMATED_FAVORITE_OFFENSE`
- `CAPITAL_PRESERVED`

---

## Final Classification

**PASS / NO BET — PROCESS PRESERVED**

The live total was **192.5** at halftime with 101 points already scored. The game ultimately reached **203**, but the path was highly asymmetric: Indiana erupted for 63 second-half points while Chicago managed only 39.

The strongest lesson is not simply that the Over won. It is that LIVE-FLOW must decompose the total into separate team scoring distributions. Indiana's positive perimeter regression and Chicago's unstable first-half scoring composition pointed in opposite directions, making the halftime state more complex than a single Over/Under label.

No wager was forced, and the checkpoint is retained as a clean model-learning event.
