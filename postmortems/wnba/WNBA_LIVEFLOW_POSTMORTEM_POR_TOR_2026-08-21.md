# WNBA LIVE-FLOW Postmortem — Portland Fire at Toronto Tempo

## Game Identity
- Date: 2026-08-21
- Venue: Rogers Arena, Vancouver, BC
- Final: Toronto 82, Portland 79
- Final total: **161**
- Halftime: Portland 44, Toronto 44
- Halftime total: **88**
- Game ID: `WNBA_2026-08-21_POR_TOR`

## Wager Logged
William Hill ticket:

| Checkpoint | Market | Line | Odds | Stake | Result | Final Total | Net |
|---|---|---:|---:|---:|---|---:|---:|
| Halftime | Full-game total | **Under 175.5** | -115 | **$15.00** | **WIN** | **161** | **+$13.04** |

- Total risk: **$15.00**
- Paid: **$28.04**
- Profit: **+$13.04**
- Halftime score: **44-44**
- Book line at entry: **175.5**
- Book-implied remaining scoring: **87.5 points**
- Actual second-half scoring: **73 points**
- Closing margin versus wager line: **14.5 points Under**

## Projection-Persistence Note
The exact frozen SharpEdge fair total from the pre-market projection is not currently recoverable from repository search, so this postmortem does **not** manufacture a number after the fact. The preserved directional decision is clear: SharpEdge attacked **Under 175.5** at halftime.

The process can still be graded cleanly from the halftime state, the market requirement, the injury/rotation context, and the actual second-half path.

## Halftime State
The game was tied **44-44** after 20 minutes.

### Portland first half
- 17/39 FG — **43.6%**
- 5/15 3PT — **33.3%**
- 5/7 FT — 71.4%
- 12 rebounds
- 13 assists
- 7 turnovers
- 24 points in the paint
- 11 second-chance points
- 2 fast-break points

### Toronto first half
- 13/29 FG — **44.8%**
- 3/10 3PT — **30.0%**
- 15/17 FT — **88.2%**
- 17 rebounds
- 10 assists
- 9 turnovers
- 18 points in the paint
- 3 second-chance points
- 4 fast-break points

### Quarter scoring
- Q1: Portland 24, Toronto 16 — 40 total
- Q2: Portland 20, Toronto 28 — 48 total
- Halftime: **88 total**

## Why the Under Was Structurally Attractive
The market required **87.5 additional points** for Over 175.5 to cash. That meant the second half essentially needed to reproduce the entire 88-point first half.

The live state gave several reasons to project less scoring rather than an exact replay.

### 1. Toronto's first-half scoring was heavily free-throw supported
Toronto scored 44 despite making only **13 field goals** and only **3 threes**.

A massive **15 of Toronto's 44 points (34.1%)** came at the free-throw line.

Toronto attempted **17 first-half free throws**, including:
- Laura Juskaite: 8/8
- Isabelle Harrison: 4/4
- Kiki Rice: 1/2
- Julie Allemand: 1/1
- Temi Fagbenle: 1/2

Repeating 17 FTA in the second half was not a sound median assumption.

### 2. Portland's offense was already ordinary outside the first-quarter shooting burst
Portland opened with five made threes in Q1, including Bridget Carleton going 3-for-4 from deep.

But in Q2 Portland went:
- 8/21 FG — **38.1%**
- 0/7 3PT — **0%**
- 20 points

That second-quarter profile better reflected a half-court offense that was not generating sustained high-efficiency scoring.

### 3. Toronto entered severely short-handed and got even thinner live
Pregame DNDs:
- Marina Mabrey — right adductor
- Nyara Sabally — left calf
- Maria Conde — left calf

Live losses:
- Brittney Sykes exited after **1:31** with a foot injury
- Aneesah Morrow later exited with a knee issue

That reduced Toronto's perimeter creation and tightened the usable rotation.

This was an important **offensive-depth suppression signal**, especially for second-half scoring sustainability.

### 4. The first-half total was not built by clean offensive efficiency on both sides
The 88-point halftime total could look superficially neutral, but its composition mattered.

Toronto's offense was dependent on free throws.
Portland's Q1 was supported by hot three-point shooting.
Neither team displayed a stable, high-efficiency scoring engine that justified simply doubling the first-half total.

The correct LIVE-FLOW question was not:

> “They scored 88 in the first half, so can they score another 88?”

It was:

> “What components created those 88 points, and which of them are repeatable?”

The answer favored suppression.

## What Happened in the Second Half
Second-half score:
- Toronto: **38**
- Portland: **35**
- Combined: **73**

That was **14.5 points below** the 87.5 points needed to beat the Under.

### Portland second half
- 10/31 FG — **32.3%**
- 6/16 3PT — 37.5%
- 9/10 FT — 90.0%
- 35 points

### Toronto second half
- 12/30 FG — **40.0%**
- 3/12 3PT — **25.0%**
- 11/16 FT — 68.8%
- 38 points

### Combined second half
- 22/61 FG — **36.1%**
- 9/28 3PT — **32.1%**
- 20/26 FT — 76.9%
- **73 points**

The Under was not dependent on one freak cold quarter. Both teams were held below 40 points in the second half.

## Third-Quarter Confirmation
Q3 finished Toronto 22, Portland 15 — only **37 combined points**.

Portland Q3:
- 4/14 FG — **28.6%**
- 3/9 3PT
- 15 points

Toronto Q3:
- 7/15 FG — 46.7%
- 1/6 3PT
- 7/11 FT
- 22 points

At the end of Q3 the game total stood at **125**, meaning the Under 175.5 had a **50.5-point cushion** for the final quarter.

That is exactly the type of path a halftime Under thesis should produce: not necessarily immediate offensive collapse from both teams, but a meaningful reduction in combined scoring rate.

## Fourth-Quarter Stress Test
The game became competitive late, which is important because close games can damage Unders through:
- late fouling,
- timeouts,
- free throws,
- intentional possession extension.

Portland erased a 12-point deficit with a **13-0 run** and actually took a 76-75 lead with 3:28 remaining.

Despite that high-leverage finish, Q4 produced only:
- Portland 20
- Toronto 16
- **36 combined points**

That is a strong validation of the Under process because the bet survived the exact late-game environment that typically threatens it.

## Key Late-Game Sequence
Toronto led 75-63 with 6:26 remaining.

Portland then scored 13 straight:
- Nyadiew Puoch 3PT
- Serah Williams interior scoring
- Bridget Carleton 3PT
- Emily Engstler 3PT

Portland took a 76-75 lead with 3:28 left.

But after that:
- Isabelle Harrison scored at 1:38
- Kiki Rice scored at 1:06
- Carla Leite split late free throws
- Julie Allemand split late free throws
- Harrison made both at 0:09.8
- Carleton missed the tying three

The final 3:28 generated just **10 combined points**.

The close-game tail never accelerated enough to threaten 175.5.

## Injury / Rotation Audit
This game gives LIVE-FLOW a particularly useful signal around **in-game offensive attrition**.

Toronto entered without three rotation players and then lost Sykes almost immediately.

That forced larger second-half roles onto:
- Isabelle Harrison
- Kiki Rice
- Laura Juskaite
- Julie Allemand
- Temi Fagbenle
- Kia Nurse
- Ornella Bankole
- Teonni Key

The surviving group defended and competed well, but Toronto no longer had the profile of a deep, high-pace offensive team.

### Toronto final usage concentration
- Harrison: 28:22, 18 FGA, 10 FTA, 25 pts
- Rice: 31:48, 9 FGA, 6 FTA, 19 pts
- Juskaite: 30:27, 6 FGA, 10 FTA, 15 pts
- Allemand: 30:54, 4 FGA, 5 pts

The offense became highly concentrated rather than broadly explosive.

This is exactly the type of rotation compression that can support a live Under when the market is still pricing the earlier game environment.

## Why This Under Worked
### 1. First-half scoring composition was correctly questioned
The 88 points were not treated as a clean run-rate baseline.

### 2. Free-throw inflation was identified as a regression candidate
Toronto's 17 first-half attempts fell to 16 in the second half — still elevated, but their conversion dropped from 88.2% to 68.8%.

### 3. Portland's Q1 three-point burst did not become a full-game offensive explosion
Portland finished only **38.6% FG** for the game.

### 4. Toronto's injury-depleted rotation lowered offensive ceiling
The team still generated enough to win, but not enough to push the game anywhere near the market total.

### 5. Second-half shot-making stayed modest
Combined second-half FG%: **36.1%**.

### 6. The Under survived a competitive final quarter
This matters because the result was not protected by a blowout or empty garbage time.

## Process Audit
### What SharpEdge got right
1. **Did not blindly extrapolate the 88-point first half.**
2. **Recognized unstable scoring components.**
3. **Properly valued Toronto's depleted rotation.**
4. **Captured Portland's offensive inconsistency.**
5. **Selected a line with substantial room for second-half scoring regression.**
6. **The edge survived real late-game pressure rather than lucking into a noncompetitive finish.**

### Remaining caution
The bet won comfortably, but we should not overlearn from the result.

Toronto still attempted **16 second-half free throws**, and Portland made six second-half threes. If the field-goal environment had merely been average rather than poor, the total could have finished materially higher.

So the lesson is **not** “short-handed teams automatically mean Under.”

The lesson is:

> Injury-driven rotation compression becomes a valuable Under input when the current live total is also being supported by non-repeatable scoring components.

## New / Reinforced LIVE-FLOW Rules

### Rule 1 — `HALFTIME_SCORING_COMPOSITION_AUDIT`
Never use first-half points alone as the second-half baseline.

Decompose scoring into:
- field-goal volume
- 2PT efficiency
- 3PT efficiency
- free-throw volume
- offensive rebounds
- transition points
- turnover-created points

### Rule 2 — `FTA_INFLATION_REGRESSION_FLAG`
When one team's halftime scoring is disproportionately supported by free throws, do not automatically project that rate forward.

Flag especially when:
- FTA rate is far above normal possession flow
- bonus entry came unusually early
- multiple bench defenders accumulated fouls

### Rule 3 — `IN_GAME_OFFENSIVE_ATTRITION`
A live injury to a primary creator must immediately reduce:
- expected pace ceiling
- transition creation
- rim pressure
- half-court shot quality
- lineup offensive depth

### Rule 4 — `ROTATION_COMPRESSION_UNDER_GATE`
Short-handed status is strongest as an Under signal when rotation compression coincides with:
- high live market total
- unstable first-half efficiency
- missing primary creators
- no obvious pace acceleration

### Rule 5 — `FIRST_QUARTER_HOT_SHOOTING_DECAY`
Do not let an early three-point burst anchor the full-game run rate after later quarters show clear offensive deterioration.

Portland:
- Q1: 5/8 from three
- Q2: 0/7

The halftime model should weight the **trajectory** of shot quality and efficiency, not simply the cumulative percentage.

### Rule 6 — `CLOSE_GAME_UNDER_STRESS_TEST`
For every halftime Under, estimate a late-foul scoring tail.

This bet passed despite a one-possession finish, strengthening confidence that the entry had genuine cushion rather than relying on game-state luck.

## Comparison With Recent LIVE-FLOW Results
This game is the opposite archetype of the Aug. 20 Atlanta-Los Angeles loss.

### ATL-LAS
- Blowout
- Expected suppression
- Defensive relaxation instead
- 56-point Q4
- Under lost

### POR-TOR
- Competitive finish
- Expected efficiency/rotation suppression
- Actual second-half scoring fell
- 36-point Q4 despite late-game pressure
- Under won

The distinction reinforces a major SharpEdge principle:

**Score margin is not the primary Under signal. Scoring composition, lineup environment, and expected possession quality are.**

## Postmortem Grade
### Directional read
**A**

Under 175.5 closed with 14.5 points of room.

### Halftime-state interpretation
**A**

The market's implied 87.5-point second half was meaningfully above the sustainable scoring environment.

### Injury / rotation interpretation
**A-**

Toronto's attrition strongly supported a lower offensive ceiling and was validated by the second-half path.

### Market selection
**A**

The line provided meaningful cushion against a close-game finish and late fouling.

### Result quality
**A**

This was not a sweatless blowout Under. The game became highly competitive, yet still finished 14.5 points below the ticket line.

## Final Classification
- Result: **WIN**
- Market: **Full-game Under**
- Checkpoint: **Halftime**
- Score at checkpoint: Portland 44, Toronto 44
- Halftime total: **88**
- Bet: **Under 175.5 -115**
- Market-implied second half: **87.5 points**
- Actual second half: **73 points**
- Final total: **161**
- Margin to line: **14.5 points Under**
- Stake: **$15.00**
- Profit: **+$13.04**
- Process tag: **SCORING_COMPOSITION_EDGE / ROTATION_ATTRITION_EDGE / HALFTIME_UNDER_VALIDATED**

## Tags
- HALFTIME_LIVEFLOW
- UNDER_WIN
- POR_TOR
- SCORING_COMPOSITION_AUDIT
- FTA_INFLATION_REGRESSION
- IN_GAME_OFFENSIVE_ATTRITION
- ROTATION_COMPRESSION
- TOR_SHORT_HANDED
- SYKES_EXIT
- MORROW_EXIT
- FIRST_QUARTER_HOT_SHOOTING_DECAY
- SECOND_HALF_SUPPRESSION
- CLOSE_GAME_UNDER_SURVIVAL
- MARKET_CUSHION_VALIDATED
- PROCESS_WIN

```yaml
game_id: WNBA_2026-08-21_POR_TOR
checkpoint: halftime
score_at_checkpoint:
  POR: 44
  TOR: 44
  total: 88
wager:
  market: full_game_total
  selection: under
  line: 175.5
  odds_american: -115
  stake_usd: 15.00
  result: win
  payout_usd: 28.04
  profit_usd: 13.04
book_implied_remaining_points: 87.5
actual_second_half:
  POR: 35
  TOR: 38
  total: 73
q3:
  POR: 15
  TOR: 22
  total: 37
q4:
  POR: 20
  TOR: 16
  total: 36
final:
  POR: 79
  TOR: 82
  total: 161
wager_margin_points: 14.5
halftime_inputs:
  POR_fg_pct: 43.6
  POR_3p_pct: 33.3
  POR_fta: 7
  TOR_fg_pct: 44.8
  TOR_3p_pct: 30.0
  TOR_fta: 17
  TOR_ftm: 15
injury_context:
  pregame_dnd:
    - Marina Mabrey
    - Nyara Sabally
    - Maria Conde
  in_game_exits:
    - Brittney Sykes
    - Aneesah Morrow
projection_persistence:
  exact_frozen_fair_total_available: false
  directional_call_preserved: under_175.5
process:
  scoring_composition_read: pass
  rotation_attrition_read: pass
  market_selection: pass
  close_game_tail_survival: pass
rules_reinforced:
  - HALFTIME_SCORING_COMPOSITION_AUDIT
  - FTA_INFLATION_REGRESSION_FLAG
  - IN_GAME_OFFENSIVE_ATTRITION
  - ROTATION_COMPRESSION_UNDER_GATE
  - FIRST_QUARTER_HOT_SHOOTING_DECAY
  - CLOSE_GAME_UNDER_STRESS_TEST
status: POSTMORTEM_COMPLETE
```
