# WNBA LIVE-FLOW Postmortem — Las Vegas Aces at New York Liberty

## Game ID

- Date: 2026-08-09
- Matchup: Las Vegas Aces at New York Liberty
- Venue: Barclays Center, Brooklyn, NY
- Halftime: New York 50, Las Vegas 39
- Final: New York 111, Las Vegas 71
- Status: FINAL — WIN

---

## 1. Halftime Market-Blind SharpEdge Projection

### Frozen projection before sportsbook comparison

- Projected 2H score: New York 47, Las Vegas 36
- Fair 2H spread: New York -11
- Fair 2H total: 83
- Projected final score: New York 97, Las Vegas 75
- Fair full-game spread: New York -22
- Fair full-game total: 172
- Fair New York team total: 97
- Fair Las Vegas team total: 75

### Halftime structural read

Las Vegas was without:

- Chelsea Gray — Rest
- A'ja Wilson — Rest
- Jackie Young — Rest
- Cheyenne Parker-Tyus — Concussion Protocol

Las Vegas first-half profile:

- 39 points
- 13/28 FG (46.4%)
- 5/10 3PT (50.0%)
- 8/10 FT (80%)
- 12 paint points
- 1 offensive rebound
- 6 turnovers

Second-quarter scoring was efficiency-supported rather than volume-supported:

- 24 points
- 7/12 FG (58.3%)
- 3/4 3PT (75%)
- 7/8 FT (87.5%)

Primary pre-market thesis: Las Vegas' second-quarter shooting efficiency was unlikely to sustain given the depleted creation profile, low shot volume, weak offensive-rebounding presence, and limited paint production.

New York first-half profile:

- 50 points
- 18/39 FG (46.2%)
- 5/17 3PT (29.4%)
- 9/11 FT (81.8%)
- 26 paint points
- 8 offensive rebounds
- 23 total rebounds vs Las Vegas 11

Primary New York read: structural control was stronger than three-point shooting, leaving room for perimeter improvement while maintaining interior/rebounding advantage.

---

## 2. Sportsbook Halftime Board

William Hill posted:

- Full-game spread: New York -14.5 (-105) / Las Vegas +14.5 (-125)
- Full-game total: 175.5 (-115 both sides)
- New York team total: 94.5 (Over -120 / Under -110)
- Las Vegas team total: 79.5 (Over -120 / Under -110)

### Model-to-market comparison

| Market | Book | SharpEdge Fair | Difference | Decision | Actual |
|---|---:|---:|---:|---|---:|
| Full-game total | 175.5 | 172 | 3.5 toward Under | PASS | 182 |
| New York spread | -14.5 | -22 | 7.5 toward NYL | Strong lean / no primary strike | NYL -40 |
| New York team total | 94.5 | 97 | 2.5 toward Over | PASS | 111 |
| Las Vegas team total | 79.5 | 75 | 4.5 toward Under | STRIKE | 71 |

The market-selection decision mattered. The full-game Under would have lost, while the isolated Las Vegas team-total Under won comfortably.

---

## 3. Wager Result

- Market: Las Vegas Aces Team Total Points Live
- Selection: Under 79.5
- Odds: -110
- Stake: $10.00
- To Win: $9.09
- Total Payout: $19.09
- Sportsbook: William Hill
- Bet timestamp shown on ticket: 2026-08-09 10:25 AM NV
- Ticket result: WON
- Profit/Loss: +$9.09

### Edge at entry

- Sportsbook team total: 79.5
- SharpEdge fair Las Vegas team total: 75
- Raw model edge: 4.5 points toward Under
- Las Vegas halftime points: 39
- Points required by Las Vegas in 2H to reach 80: 41
- SharpEdge projected Las Vegas 2H points: 36
- Actual Las Vegas 2H points: 32
- Actual Las Vegas final points: 71
- Closing margin beneath 79.5: 8.5 points

### Stake classification

- LIVE-FLOW strike
- 0.5-unit style position
- Cleared active 4-point minimum model-to-market separation threshold

---

## 4. What Happened After Halftime

### Las Vegas offense regressed exactly in the direction identified

First half:

- 39 points
- 46.4% FG
- 50.0% 3PT

Second half:

- 32 points
- 12/35 FG (34.3%)
- 5/19 3PT (26.3%)
- 3/4 FT
- 8 turnovers

Quarter split:

- Q3: 12 points
- Q4: 20 points

The key halftime signal was not simply that Las Vegas had only 39 points. It was that the 24-point second quarter had been created through unusually efficient shooting on limited volume. Once that efficiency normalized, the depleted Aces offense did not possess enough creation, paint pressure, or second-chance volume to sustain the book's 79.5 expectation.

### New York exceeded our upside estimate

New York scored 61 second-half points against our projection of 47.

Second-half Liberty shooting:

- 22/36 FG (61.1%)
- 9/15 3PT (60.0%)
- 8/10 FT

Fourth quarter alone:

- 37 points
- 15/21 FG (71.4%)
- 5/9 3PT (55.6%)

That explosion drove the final game total to 182 and the final margin to 40, well beyond our projected 172 total and NYL -22 fair spread.

This is important calibration: the Las Vegas suppression read was strong, while the model materially underweighted New York's offensive ceiling against the exhausted/depleted Aces rotation.

---

## 5. Projection vs Actual

| Component | SharpEdge Projection | Actual | Error |
|---|---:|---:|---:|
| Las Vegas 2H points | 36 | 32 | -4 |
| Las Vegas final points | 75 | 71 | -4 |
| New York 2H points | 47 | 61 | +14 |
| New York final points | 97 | 111 | +14 |
| 2H total | 83 | 93 | +10 |
| Full-game total | 172 | 182 | +10 |
| Final NYL margin | 22 | 40 | +18 |

### Isolated wager-model accuracy

For the market actually attacked, the model was directionally and numerically strong:

- Fair Las Vegas total: 75
- Actual: 71
- Absolute error: 4 points
- Book: 79.5
- Winning cushion: 8.5 points

The model also projected 36 Las Vegas second-half points; they scored 32, again a 4-point miss in the correct direction.

---

## 6. Why the Strike Won

1. **Shooting-regression signal was real.** Las Vegas went from 50.0% from three in the first half to 26.3% in the second half.
2. **The depleted creation profile mattered.** Gray, Wilson and Young were all unavailable.
3. **Low-volume offense never became durable offense.** The Aces attempted only 35 second-half field goals and finished with 63 for the game.
4. **Paint and rebounding structure remained weak.** Las Vegas finished with only 26 paint points and 5 offensive rebounds.
5. **Turnovers increased under pressure.** Las Vegas committed 8 second-half turnovers and 14 for the game.
6. **The team-total market isolated the correct variable.** We did not need New York's scoring to behave normally for the wager to cash.
7. **Market discipline prevented contamination.** The full-game Under 175.5 was below the 4-point strike threshold and was passed; it ultimately lost by 6.5 points.

---

## 7. Garbage-Time Assessment

Garbage time was present, but it did not invalidate the wager thesis.

New York led 74-51 entering the fourth quarter and eventually won by 40. Las Vegas scored 20 fourth-quarter points after only 12 in the third. That late scoring created some team-total risk, but the Aces still finished at 71 — 8.5 points below the betting line.

This reinforces why team-total unders need a cushion rather than relying on a razor-thin projection. The 4.5-point pre-bet edge plus the structural offensive weakness provided enough room to absorb late-game variance.

---

## 8. Postmortem Grades

### Decision-quality grade: A+

The strongest element was **market selection**:

- Full-game Under 175.5: PASS → would have lost
- NYL team total Over 94.5: PASS → would have won, but edge was below threshold
- NYL -14.5: strong lean/no primary strike → covered easily
- LVA Under 79.5: STRIKE → won by 8.5 points

The LIVE-FLOW process correctly isolated the most defensible signal rather than forcing exposure across every apparent edge.

### Model-quality grade: A- for the targeted market / B- for full-game state

The Las Vegas component was strong: both the final team total and second-half points missed by only 4 points and in the expected direction.

The broader game-state model underestimated New York by 14 points and the final margin by 18. Future calibration should increase opponent offensive-upside weighting when a heavily rested/healthy favorite faces a road team missing multiple elite starters and playing its third game in four days.

---

## 9. Model Lesson to Carry Forward

### New LIVE-FLOW tag: `DEPLETED_CREATION_EFFICIENCY_FADE`

Use when:

- multiple primary creators are unavailable,
- first-half scoring is supported by elevated shooting efficiency,
- shot volume / paint production / offensive rebounding are weak,
- and the sportsbook still prices the team as though the first-half efficiency is reasonably sustainable.

### Secondary calibration tag: `REST_ROTATION_ASYMMETRY_OFFENSIVE_CEILING`

When one team is well rested and the opponent is on severe travel/rest disadvantage with multiple stars sitting, widen the favorite's upper-tail scoring distribution. This game showed that the opponent team-total Under can be correctly identified even while the favorite's offensive ceiling is materially underestimated.

---

## 10. Clean Record

```yaml
game_id: WNBA_2026-08-09_LVA_NYL
sport: WNBA
workflow: LIVE_FLOW
status: final
halftime_score:
  LVA: 39
  NYL: 50
sharpedge_frozen_projection:
  second_half_score:
    LVA: 36
    NYL: 47
  second_half_total: 83
  second_half_spread: NYL_-11
  final_score:
    LVA: 75
    NYL: 97
  full_game_total: 172
  full_game_spread: NYL_-22
  lva_team_total: 75
  nyl_team_total: 97
sportsbook_halftime:
  full_game_total: 175.5
  full_game_spread: NYL_-14.5
  lva_team_total: 79.5
  nyl_team_total: 94.5
wager:
  market: LVA_team_total
  selection: under_79.5
  odds: -110
  stake: 10.00
  to_win: 9.09
  payout: 19.09
  edge_points: 4.5
  result: win
  profit_loss: 9.09
actual:
  second_half_score:
    LVA: 32
    NYL: 61
  final_score:
    LVA: 71
    NYL: 111
  second_half_total: 93
  full_game_total: 182
  final_margin: NYL_40
  lva_team_total_margin_vs_bet: -8.5
model_error:
  lva_second_half_points: -4
  lva_final_points: -4
  nyl_second_half_points: 14
  nyl_final_points: 14
  second_half_total: 10
  full_game_total: 10
  final_margin: 18
validation:
  lva_shooting_regression: true
  garbage_time_present: true
  targeted_market_thesis_confirmed: true
grades:
  decision_quality: A_plus
  targeted_market_model_quality: A_minus
  full_game_state_model_quality: B_minus
tags:
  - DEPLETED_CREATION_EFFICIENCY_FADE
  - REST_ROTATION_ASYMMETRY_OFFENSIVE_CEILING
  - TEAM_TOTAL_ISOLATION
  - HALFTIME_STRIKE
  - DISCIPLINE_THRESHOLD_VALIDATED
```
