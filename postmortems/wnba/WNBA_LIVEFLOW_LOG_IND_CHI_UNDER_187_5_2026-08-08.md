# WNBA LIVE-FLOW Postmortem — Indiana Fever at Chicago Sky Under 187.5

## Game ID

- Date: 2026-08-08
- Matchup: Indiana Fever at Chicago Sky
- Venue: United Center, Chicago, IL
- Halftime: Indiana 53, Chicago 42
- Final: Indiana 90, Chicago 86
- Final Total: 176

---

## 1. Wager Record

- Market: Live Full-Game Total
- Selection: Under 187.5
- Odds: -115
- Stake: $10.00
- To Win: $8.70
- Total Paid: $18.70
- Profit: +$8.70
- Book: William Hill Sportsbook
- Bet Time: 2026-08-08 1:36 PM local screenshot timestamp
- Result: WIN
- Margin to Line: 11.5 points Under

---

## 2. Halftime State

- Halftime Score: Indiana 53, Chicago 42
- First-Half Total: 95
- Indiana 1H FG: 20/36 (55.6%)
- Indiana 1H 3PT: 4/9 (44.4%)
- Indiana 1H FT: 9/12 (75.0%)
- Chicago 1H FG: 16/35 (45.7%)
- Chicago 1H 3PT: 3/10 (30.0%)
- Chicago 1H FT: 7/8 (87.5%)
- Indiana Q2 FG: 10/14 (71.4%)
- DiJonai Carrington: ejected in Q1 (Flagrant 2)

---

## 3. SharpEdge Market-Blind Halftime Model

- Projected 2H Score: Indiana 46, Chicago 40
- Projected 2H Total: 86.0
- Projected Final Score: Indiana 99, Chicago 82
- Fair 2H Spread: Indiana -6
- Fair Full-Game Spread: Indiana -17
- Fair Full-Game Total: 181.0
- Fair Indiana Team Total: 99
- Fair Chicago Team Total: 82

### Sportsbook Halftime Market

- Full-Game Spread: Indiana -12.5 (-115)
- Full-Game Total: 187.5 (-115)
- Indiana Team Total: 100.5
- Chicago Team Total: 87.5

### Edge Comparison at Entry

- Full-Game Under 187.5 vs model 181.0: +6.5 points toward Under
- Chicago Under 87.5 vs model 82: +5.5 points toward Under
- Indiana -12.5 vs model -17: +4.5 points toward Indiana
- Indiana Under 100.5 vs model 99: +1.5 points toward Under

### LIVE-FLOW Decision

- Primary Strike: Under 187.5 at -115
- Stake Classification: 0.5-unit / $10 process-validation position
- Rationale: Model-to-market separation of 6.5 points cleared the updated postmortem threshold after NYL-LVA. Indiana's 71.4% Q2 shooting was expected to regress, while Chicago's offensive ceiling was downgraded by Carrington's ejection and foul pressure on perimeter personnel.

---

## 4. Actual Second-Half Outcome

### Second-Half Score

- Indiana: 37
- Chicago: 44
- Actual 2H Total: 81
- Actual 2H Margin: Chicago +7

### Second-Half Team Efficiency

#### Indiana

- FG: 15/32 (46.9%)
- 3PT: 5/13 (38.5%)
- FT: 2/4 (50.0%)
- Turnovers: 9
- Paint Points: 18

#### Chicago

- FG: 15/33 (45.5%)
- 3PT: 6/12 (50.0%)
- FT: 8/12 (66.7%)
- Turnovers: 7
- Paint Points: 18

---

## 5. Model vs Actual

| Market | Halftime Model | Actual | Error |
|---|---:|---:|---:|
| 2H total | 86.0 | 81 | -5.0 |
| Full-game total | 181.0 | 176 | -5.0 |
| IND 2H points | 46 | 37 | -9 |
| CHI 2H points | 40 | 44 | +4 |
| 2H spread | IND -6 | CHI +7 | 13 points wrong side |
| Full-game spread | IND -17 | IND -4 | 13 points toward CHI |
| Indiana team total | 99 | 90 | -9 |
| Chicago team total | 82 | 86 | +4 |

### Market Settlement

- Under 187.5: WIN by 11.5 points
- Chicago Under 87.5: WIN by 1.5 points
- Indiana -12.5: LOSS
- Indiana Under 100.5: WIN by 10.5 points

---

## 6. Why the Under Won

### A. Indiana Shooting Regression Was Correctly Identified

Indiana's 71.4% shooting in the second quarter was unsustainable and regressed materially after halftime.

- 1H FG: 55.6%
- 2H FG: 46.9%
- Q2 FG: 71.4%
- 2H points: only 37

The halftime model preserved a solid 46-point Indiana second-half projection rather than assuming a collapse, but Indiana cooled even more than projected.

Primary driver: the model correctly identified first-half scoring inflation.

### B. Indiana Turnovers Became a Major Second-Half Suppressor

Indiana committed nine second-half turnovers after only five in the first half.

That reduced possession quality and helped pull the game below both the sportsbook total and our 181 fair total.

### C. Chicago Offensive Suppression Was Overstated

This part of the halftime thesis was not confirmed.

Despite Carrington's ejection, Chicago scored 44 second-half points, four above our projection of 40.

Chicago also shot:

- 45.5% FG in the second half
- 50.0% from three

Therefore Carrington's absence did not materially suppress Chicago's second-half scoring enough to validate our original 40-point center.

The Under won primarily because Indiana scored much less than projected, not because Chicago's offense collapsed.

### D. Endgame Foul Extension Was Limited

The game tightened late, but the final minute did not create a large scoring burst.

- Clark split two free throws with 17.9 seconds remaining.
- Cardoso missed two free throws with 4.1 seconds remaining.

There was no major late intentional-foul explosion to threaten the total.

### E. The Total Read Was Better Than the Side Read

The total model correctly recognized inflated first-half scoring and produced a final total center of 181, five points above the actual 176.

However, the same halftime framework badly overestimated Indiana's second-half margin.

This is an important distinction:

- Total environment signal: correct.
- Team allocation / spread signal: incorrect.

The model's 86-point 2H total was useful even though the projected split of Indiana 46 / Chicago 40 was not.

---

## 7. Patch Validation

This wager was the first clean test of the updated LIVE-FLOW threshold after the NYL-LVA Under miss.

### Updated Rules Tested

1. Do not strike live totals on marginal 2–3 point discrepancies.
2. Require at least 4.0 points of model-to-market separation.
3. Prefer 5+ points when uncertainty is elevated.
4. Avoid stacking correlated team-total and full-game total positions at full size.

### Test Result

- Model fair total: 181.0
- Sportsbook total: 187.5
- Separation: 6.5 points
- Actual final: 176
- Result: WIN

### Patch Classification

- Minimum-edge threshold: CONFIRMED FOR THIS TEST
- 5+ point preference: CONFIRMED FOR THIS TEST
- Avoid correlated stacking: RETAIN
- Total projection framework: RETAIN WITH MODIFICATION
- Spread projection framework: REQUIRES MODIFICATION

One successful test is not enough to declare the threshold universally validated. It is a positive confirmation and should remain active pending a larger sample.

---

## 8. Model Lessons

### Keep

- Market-blind halftime projection before viewing sportsbook prices.
- Regression detection on extreme quarter-level shooting.
- 4-point minimum total edge threshold.
- 5+ point preference for elevated uncertainty.
- Single primary strike instead of correlated stacking.

### Modify

1. Separate total-environment forecasting from team-score allocation more aggressively.
2. Do not let an ejection automatically create an aggressive team-offense downgrade without evidence of usage replacement failure.
3. Add second-half turnover volatility to team scoring distributions.
4. Reduce confidence in halftime spread projections when one team has a large lead but the trailing team retains enough shooting/creation to rally.
5. Widen team-level score intervals even when the combined-total estimate is relatively stable.

### Do Not Overlearn

- The Under won by 11.5 points, but our final fair total missed by only five points, not 11.5. The remaining difference came from the sportsbook being 6.5 points above our number.
- Chicago exceeded our team projection by four, so the Carrington-ejection thesis was weaker than the final ticket result might imply.
- Indiana's large scoring undershoot drove most of the model-to-actual difference.

---

## 9. Signal Classification

- Full-game Under 187.5: SIGNAL CONFIRMED / WIN
- Indiana Q2 shooting regression: SIGNAL CONFIRMED
- Chicago offensive suppression from Carrington ejection: SIGNAL WEAKENED
- 2H total model: SIGNAL CONFIRMED
- Team-score allocation model: SIGNAL WEAKENED
- Indiana spread edge: SIGNAL BROKEN FOR THIS GAME
- Revised minimum-edge patch: POSITIVE VALIDATION, SAMPLE STILL SMALL
- Variance contribution: moderate
- Confidence in diagnosis: HIGH

---

## 10. Final Status

- LIVE-FLOW total framework: KEEP WITH MODIFICATION
- 4+ point threshold patch: KEEP
- Prefer 5+ point separation: KEEP
- Spread allocation logic: MODIFY
- Carrington/ejection offensive downgrade rule: MODIFY

---

## 11. Clean Machine-Readable Record

```yaml
game_id: WNBA_2026-08-08_IND_CHI
halftime:
  score:
    IND: 53
    CHI: 42
  total: 95
model:
  second_half_total: 86.0
  second_half_score:
    IND: 46
    CHI: 40
  full_game_total: 181.0
  final_score:
    IND: 99
    CHI: 82
market:
  full_game_total: 187.5
  odds: -115
  spread: IND_-12.5
wager:
  selection: under_187.5
  stake: 10.00
  payout: 18.70
  profit: 8.70
  result: win
actual:
  second_half_score:
    IND: 37
    CHI: 44
  second_half_total: 81
  final_score:
    IND: 90
    CHI: 86
  final_total: 176
errors:
  second_half_total: -5.0
  full_game_total: -5.0
  IND_second_half_points: -9
  CHI_second_half_points: 4
  spread_points: 13
patch_evaluation:
  minimum_edge_4_points: keep
  prefer_5_plus_points: keep
  correlated_stacking_guardrail: keep
  total_framework: keep_with_modification
  spread_allocation: modify
confidence: high
```
