# WNBA LIVE-FLOW Postmortem — Phoenix Mercury at Washington Mystics — Washington -9.5

## Game ID

- Date: 2026-08-09
- Matchup: Phoenix Mercury at Washington Mystics
- Venue: CareFirst Arena, Washington, DC
- Halftime: Washington 50, Phoenix 37
- Final: Washington 95, Phoenix 75
- Final Margin: Washington +20
- Final Total: 170
- Result: WIN

---

## 1. Wager Record

- Market: Live Full-Game Spread
- Selection: Washington Mystics -9.5
- Odds: -115
- Stake: $10.00
- To Win: $8.70
- Total Paid: $18.70
- Profit: +$8.70
- Book: William Hill Sportsbook
- Bet Receipt Timestamp: 2026-08-09 12:54 PM screenshot timestamp
- Result: WIN
- Cover Margin: 10.5 points

### Entry Improvement

- Initial sportsbook comparison line observed: Washington -10.5 (-115)
- Actual locked line: Washington -9.5 (-115)
- Improvement versus observed line: +1.0 point
- SharpEdge fair full-game spread: Washington -16
- Model-to-entry separation at actual lock: +6.5 points toward Washington

---

## 2. Halftime State

- Halftime Score: Washington 50, Phoenix 37
- Washington lead: 13
- First-Half Total: 87

### Phoenix 1H

- FG: 14/35 (40.0%)
- 3PT: 6/12 (50.0%)
- FT: 3/4 (75.0%)
- Turnovers: 10
- Paint Points: 12
- Fast-Break Points: 2
- Second-Chance Points: 2

### Washington 1H

- FG: 20/37 (54.1%)
- 3PT: 3/11 (27.3%)
- FT: 7/10 (70.0%)
- Turnovers: 2
- Paint Points: 30
- Fast-Break Points: 13
- Second-Chance Points: 8

### Key Player State

- Shakira Austin: 16 points, 8 rebounds, 7/13 FG
- Kiki Iriafen: 4 points, 3 rebounds
- Sonia Citron: 3 points, 4 assists
- Alyssa Thomas: 8 points, 6 rebounds, 5 assists
- Kahleah Copper: 8 points
- Kelsey Plum: 5 points, 2/7 FG, 1/5 3PT

---

## 3. SharpEdge Market-Blind Halftime Model

### Frozen Model Before Sportsbook Comparison

- Projected 2H Score: Washington 44, Phoenix 41
- Projected 2H Total: 85
- Projected Final Score: Washington 94, Phoenix 78
- Fair 2H Spread: Washington -3
- Fair Full-Game Spread: Washington -16
- Fair Full-Game Total: 172
- Fair Washington Team Total: 94
- Fair Phoenix Team Total: 78

### Sportsbook Halftime Market Observed

- Full-Game Spread: Washington -10.5 (-115)
- Full-Game Total: 168.5 (-115)
- Washington Team Total: 89.5 Over -120 / Under -110
- Phoenix Team Total: 78.5 Over -120 / Under -110

### Actual Bet Entry

- Washington -9.5 (-115)

### Edge Comparison at Actual Entry

- Washington -9.5 vs model Washington -16: +6.5 points toward Washington
- Full-game Over 168.5 vs model 172: +3.5 points toward Over
- Washington Over 89.5 vs model 94: +4.5 points toward Over
- Phoenix Under 78.5 vs model 78: +0.5 point toward Under

---

## 4. LIVE-FLOW Decision

### Primary Strike

**Washington Mystics -9.5 (-115)**

### Stake Classification

- $10.00 process-validation position
- Single primary exposure; no correlated stack added at entry

### Rationale at Lock

1. The model was frozen before seeing the sportsbook market.
2. SharpEdge projected Washington -16 full game; the actual locked market was only -9.5.
3. That created a 6.5-point model-to-market spread separation, clearing the 4-point minimum and preferred 5+ point LIVE-FLOW threshold.
4. Washington's first-half scoring was not dependent on hot perimeter shooting: only 3/11 from three while scoring 50.
5. Washington controlled the paint 30-12 and the turnover battle 2-10.
6. Phoenix's 50% first-half three-point shooting was one of the few supports holding up its offense and carried clear regression risk.
7. Washington's offense looked more repeatable through paint production, transition, and low-turnover execution.
8. The actual -9.5 lock was one point better than the -10.5 line originally compared.

---

## 5. Actual Second-Half Outcome

### Second-Half Score

- Washington: 45
- Phoenix: 38
- Actual 2H Margin: Washington +7
- Actual 2H Total: 83

### Washington 2H

- FG: 16/35 (45.7%)
- 3PT: 8/18 (44.4%)
- FT: 5/9 (55.6%)
- Turnovers: 6
- Paint Points: 12
- Fast-Break Points: 2

### Phoenix 2H

- FG: 15/34 (44.1%)
- 3PT: 5/17 (29.4%)
- FT: 3/4 (75.0%)
- Turnovers: 6
- Paint Points: 18
- Fast-Break Points: 2

### Important Post-Entry Development

Kelsey Plum did not play in the second half because of a left calf injury. Lexi Held started the third quarter in her place.

This was favorable to the Washington position, but it must be classified as **post-entry variance / new information**, not retroactively used as justification for the original bet.

---

## 6. Model vs Actual

| Market | Halftime Model | Actual | Error |
|---|---:|---:|---:|
| WAS 2H points | 44 | 45 | +1 |
| PHO 2H points | 41 | 38 | -3 |
| 2H total | 85 | 83 | -2 |
| 2H spread | WAS -3 | WAS -7 | 4 pts more WAS |
| Final WAS points | 94 | 95 | +1 |
| Final PHO points | 78 | 75 | -3 |
| Full-game total | 172 | 170 | -2 |
| Full-game spread | WAS -16 | WAS -20 | 4 pts more WAS |

### Market Settlement

- Washington -9.5: WIN by 10.5 points
- Washington -10.5 observed line: also would have won by 9.5 points
- Washington Over 89.5: WIN by 5.5 points
- Phoenix Under 78.5: WIN by 3.5 points
- Full-game Over 168.5: WIN by 1.5 points

---

## 7. Why the Washington Spread Won

### A. The Core Margin Read Was Correct

The strongest part of the halftime model was not merely that Washington was ahead; it was that the first-half advantage was supported by repeatable possession-quality signals.

At halftime:

- Washington led the paint 30-12.
- Washington led the turnover battle 2-10.
- Washington had only shot 27.3% from three.
- Phoenix had shot 50.0% from three and still trailed by 13.

That asymmetry mattered. Washington had room for perimeter improvement, while Phoenix carried regression risk.

### B. Phoenix Three-Point Regression Hit Cleanly

This signal was strongly confirmed.

- Phoenix 1H 3PT: 6/12 — 50.0%
- Phoenix 2H 3PT: 5/17 — 29.4%

Phoenix's first-half perimeter efficiency did not survive halftime, reducing one of the few mechanisms available for a comeback.

### C. Washington's Three-Point Shooting Improved

Washington moved in the opposite direction.

- Washington 1H 3PT: 3/11 — 27.3%
- Washington 2H 3PT: 8/18 — 44.4%

Sonia Citron was a major driver, scoring 16 second-half points and finishing 5/6 from three for the game.

This was favorable relative to the halftime setup because the Mystics had already built a 13-point lead without strong first-half three-point shooting.

### D. Phoenix's Turnover Problem Improved, So It Was Not the Main 2H Driver

Phoenix committed:

- 10 turnovers in the first half
- 6 turnovers in the second half

So the original turnover edge did not intensify after halftime. Phoenix actually cleaned this area up somewhat.

The spread still covered comfortably, which is useful evidence that the position did not require the first-half turnover gap to persist at the same extreme level.

### E. Washington's Paint Dominance Did Not Persist at the Same Level

Washington scored 30 paint points in the first half but only 12 in the second half.

Phoenix scored 18 second-half paint points.

Therefore the spread win should not be credited to sustained paint domination throughout the game. The first-half paint signal helped identify Washington's structural control at entry, but the second-half scoring mix shifted toward perimeter production.

### F. Kelsey Plum's Injury Was Favorable but Exogenous

Plum did not return after halftime because of a left calf injury.

That reduced Phoenix's available creation and shooting, but the model and bet were already locked before this development was known.

Classification:

- Helpful to result: YES
- Part of original edge thesis: NO
- Should be learned as model skill: NO
- Should be logged as post-entry variance/new information: YES

### G. The Model Was Exceptionally Close on Team Scoring

The frozen model projected:

- Washington 94
- Phoenix 78
- Final total 172
- Washington -16

Actual:

- Washington 95
- Phoenix 75
- Final total 170
- Washington -20

Absolute team-score errors were only 1 point for Washington and 3 points for Phoenix. The combined total missed by only 2 points.

This is a strong process result independent of the wager settlement.

---

## 8. Entry Quality and Closing Logic

The actual ticket was better than the first observed market.

- Observed: Washington -10.5
- Locked: Washington -9.5
- Same price: -115

That one-point improvement mattered because LIVE-FLOW is sensitive to entry quality. We did not chase a worse line and instead captured a superior number.

The final margin was large enough that the point did not decide settlement, but preserving line quality remains a core rule.

---

## 9. Guardrail / Patch Validation

### Rules Tested

1. Market-blind projection before sportsbook comparison.
2. Minimum 4-point model-to-market separation.
3. Prefer 5+ points when uncertainty is elevated.
4. Single primary strike rather than stacking correlated positions.
5. Do not chase worse numbers.

### Result

- Model fair spread: Washington -16
- Actual entry: Washington -9.5
- Separation: 6.5 points
- Final margin: Washington +20
- Result: WIN by 10.5 points

### Classification

- Market-blind projection: CONFIRMED
- 4+ point threshold: POSITIVE VALIDATION
- 5+ point preference: POSITIVE VALIDATION
- Entry discipline: CONFIRMED
- Correlated-stack guardrail: RETAIN
- Spread-allocation model: STRONG RESULT FOR THIS TEST

This remains one game, so it should strengthen rather than prove the framework.

---

## 10. Model Lessons

### Keep

- Independent halftime projection before market exposure.
- Regression analysis on unsustainably hot shooting.
- Comparing structural scoring sources, not just raw halftime score.
- 4-point minimum edge threshold.
- Preference for 5+ points of separation.
- Line-shopping / refusal to chase worse live numbers.
- Single primary position when correlated markets all point in the same direction.

### Modify / Track

1. Separate first-half structural indicators from assumptions that they must persist identically after halftime.
2. Paint dominance can identify underlying control even if the second-half scoring mix changes.
3. Track post-entry injuries separately from pre-entry information so favorable variance is not mistaken for predictive skill.
4. Continue measuring team-score allocation accuracy independently from wager result.
5. Add a post-entry event field for injuries, ejections, foul-outs, and rotation changes that occur after the bet is locked.

### Do Not Overlearn

- Washington won by 20, but our fair margin was 16; the model did not predict the entire 20-point result.
- Plum's injury materially changed Phoenix's second-half rotation and should not be credited to the halftime read.
- Washington's second-half three-point spike helped the cover and represents favorable shooting variance relative to the first-half profile.
- The process success is best measured by the frozen projection being close to the final distribution and the entry being materially better than the market, not merely by the ticket winning.

---

## 11. Signal Classification

- Washington -9.5: SIGNAL CONFIRMED / WIN
- Washington structural halftime control: CONFIRMED
- Phoenix 3PT regression: STRONGLY CONFIRMED
- Phoenix turnover suppression persistence: NOT CONFIRMED
- Washington paint-dominance persistence: NOT CONFIRMED
- Washington perimeter upside from low 1H 3PT%: CONFIRMED
- Team-score allocation: STRONG
- Full-game total projection: STRONG
- Spread projection: STRONG FOR THIS GAME
- Entry discipline / line improvement: CONFIRMED
- Post-entry Plum injury: FAVORABLE EXOGENOUS EVENT
- Confidence in diagnosis: HIGH

---

## 12. Final Status

- LIVE-FLOW halftime spread framework: KEEP
- 4+ point minimum edge threshold: KEEP
- Prefer 5+ point separation: KEEP
- Market-blind projection rule: KEEP
- Line-quality discipline: KEEP
- Correlated-stack guardrail: KEEP
- Post-entry event logging: ADD / RETAIN
- Result classification: CLEAN WIN WITH FAVORABLE POST-ENTRY INJURY VARIANCE

---

## 13. Clean Machine-Readable Record

```yaml
game_id: WNBA_2026-08-09_PHO_WAS
halftime:
  score:
    PHO: 37
    WAS: 50
  total: 87
  lead: WAS_13
  team_stats:
    PHO:
      fg: 14/35
      fg_pct: 40.0
      three_pt: 6/12
      three_pt_pct: 50.0
      ft: 3/4
      turnovers: 10
      paint_points: 12
    WAS:
      fg: 20/37
      fg_pct: 54.1
      three_pt: 3/11
      three_pt_pct: 27.3
      ft: 7/10
      turnovers: 2
      paint_points: 30
model:
  second_half_score:
    PHO: 41
    WAS: 44
  second_half_total: 85
  full_game_score:
    PHO: 78
    WAS: 94
  full_game_total: 172
  full_game_spread: WAS_-16
  team_totals:
    PHO: 78
    WAS: 94
market_observed:
  full_game_spread: WAS_-10.5
  full_game_total: 168.5
  team_totals:
    PHO: 78.5
    WAS: 89.5
wager:
  market: live_full_game_spread
  selection: WAS_-9.5
  odds: -115
  stake: 10.00
  to_win: 8.70
  payout: 18.70
  profit: 8.70
  book: William_Hill
  result: win
  cover_margin: 10.5
  edge_points_vs_model: 6.5
  line_improvement_vs_observed: 1.0
actual:
  second_half_score:
    PHO: 38
    WAS: 45
  second_half_total: 83
  second_half_spread: WAS_-7
  final_score:
    PHO: 75
    WAS: 95
  final_total: 170
  full_game_spread: WAS_-20
errors:
  WAS_second_half_points: 1
  PHO_second_half_points: -3
  second_half_total: -2
  WAS_final_points: 1
  PHO_final_points: -3
  full_game_total: -2
  full_game_spread_points: 4
signals:
  PHO_three_point_regression: confirmed
  PHO_turnover_suppression_persistence: not_confirmed
  WAS_paint_dominance_persistence: not_confirmed
  WAS_perimeter_upside: confirmed
  spread_signal: confirmed
  team_score_allocation: strong
post_entry_events:
  - event: Kelsey_Plum_left_calf_injury
    timing: halftime_to_second_half
    effect: favorable_to_WAS_position
    included_in_original_model: false
    classification: exogenous_new_information
process:
  projection_frozen_before_market: true
  minimum_edge_threshold_passed: true
  preferred_5_plus_threshold_passed: true
  correlated_stack_avoided: true
  line_chase_avoided: true
final_classification: clean_win_with_favorable_post_entry_injury_variance
confidence: high
```
