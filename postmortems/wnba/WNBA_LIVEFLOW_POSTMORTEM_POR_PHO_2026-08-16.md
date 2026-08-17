# WNBA LIVE-FLOW Postmortem — Portland Fire at Phoenix Mercury

## Game Identity
- Date: 2026-08-16
- Venue: Mortgage Matchup Center, Phoenix, AZ
- Final: Portland 88, Phoenix 85
- Final total: 173
- Game ID: `WNBA_2026-08-16_POR_PHO`

## Important Logging Note
No exact market-blind Portland-Phoenix halftime or end-3Q SharpEdge projection file was found in the GitHub repository during this postmortem review.

Therefore this postmortem does **not** reconstruct or invent prior model fair lines from memory. The wager lines, checkpoint scores, and actual game data are audited directly from the betting tickets and official scorer reports supplied after the game.

This is itself a process issue: every actionable LIVE-FLOW checkpoint must have the market-blind projection persisted before market reveal.

## Wagers Logged

| Checkpoint | Market | Line | Odds | Stake | Result | Final Total | Net |
|---|---|---:|---:|---:|---|---:|---:|
| Halftime | Full-game total | Under 163.5 | -115 | $30.00 | LOSS | 173 | -$30.00 |
| Early Q4 / End-3Q re-entry | Full-game total | Under 169.5 | -110 | $14.77 | LOSS | 173 | -$14.77 |

**Total risk:** $44.77  
**Net result:** **-$44.77**

## Checkpoint 1 — Halftime Under 163.5

### Halftime state
- Phoenix 42, Portland 36
- Halftime total: 78
- Portland: 14/37 FG (37.8%), 7/23 3PT (30.4%), 1/4 FT (25.0%)
- Phoenix: 13/32 FG (40.6%), 5/15 3PT (33.3%), 11/14 FT (78.6%)
- Portland turnovers: 6
- Phoenix turnovers: 7
- Portland offensive rebounds: 6
- Phoenix offensive rebounds: 4

### What was required for U163.5
With 78 points already scored, the wager needed the second half to finish at **85 points or fewer**.

### Actual second half
- Portland: 52
- Phoenix: 43
- Second-half total: **95**
- Final total: 173

The second half exceeded the Under requirement by **10 points**.

### Process diagnosis
Unlike Fever-Dream, this was **not** an overtime-tail loss. The scoring thesis itself broke during regulation.

The biggest halftime warning signs were on Portland's side:
- Portland was only 37.8% from the field.
- Portland had made just 1 of 4 free throws.
- Portland had already generated 37 FGA, 23 3PA, 6 offensive rebounds, and 10 assists despite scoring only 36.
- That combination showed substantial unused scoring capacity if conversion improved even modestly.

The Fire then scored **52 second-half points on 52.9% FG**, even while making only 21.4% from three. The comeback was driven primarily by two-point efficiency, paint creation, offensive pressure, and free throws rather than unsustainable perimeter shooting.

**Verdict:** The halftime Under failed because the model/decision process overweighted the low first-half score and underweighted Portland's positive conversion-regression profile and underlying opportunity volume.

## Checkpoint 2 — Under 169.5

### End-3Q state
- Phoenix 64, Portland 61
- Total through three quarters: **125**
- Q3 scoring: Portland 25, Phoenix 22 = 47

### What was required for U169.5
The wager needed the fourth quarter to finish at **44 points or fewer**.

### Actual fourth quarter
- Portland: 27
- Phoenix: 21
- Q4 total: **48**
- Final total: 173

The Under lost by **3.5 points**.

### Q4 scoring anatomy
Portland shot:
- 9/16 FG = **56.2%**
- 1/5 3PT = 20.0%
- 8/11 FT = 72.7%

Phoenix shot:
- 7/19 FG = 36.8%
- 2/7 3PT = 28.6%
- 5/5 FT = 100%

The key failure was not a three-point avalanche. Portland generated **14 paint points** in the fourth quarter and Carla Leite scored **15 points in Q4**, repeatedly getting to the rim and creating late-game scoring pressure.

## Late-Game Foul / Competitive-State Tail
The game was Phoenix 80, Portland 81 with 1:53 remaining.

From that point to the final buzzer, the teams added **12 points**.

Most importantly, the final 20.3 seconds produced **8 points** through deliberate fouling and late-game execution:
- Katie Lou Samuelson FT: +1
- Bridget Carleton FTs: +2
- Alyssa Thomas 3PT: +3
- Carla Leite FTs: +2

This is the core tail that pushed the End-3Q Under from a plausible winning position to a 173 final.

**Verdict:** The U169.5 re-entry was much closer than the halftime Under, but it still lacked sufficient protection against a one-possession late-game foul sequence.

## Player / Rotation Signals That Mattered

### Carla Leite
- Halftime: 8 points, 3/6 FG, 1/3 FT, 3 fouls
- End 3Q: still 8 points, 4 fouls
- Final: **23 points**
- Q4 alone: **15 points on 6/8 FG**

Leite was the decisive miss. Foul trouble appeared to create suppression risk, but instead she played the entire fourth quarter and became Portland's primary closer.

### Emily Engstler
- 4 fouls by halftime
- 5 fouls by 2:00 remaining in Q3
- Still contributed a key late driving layup at :54.9 of Q4

This game shows that foul trouble cannot automatically be treated as a scoring suppressor when the player remains available and the game is close enough to force normal closing rotations.

### Portland scoring profile
Portland finished:
- 45.1% FG
- only 27.0% from three
- 36 paint points
- 14/21 FT

The Fire reached 88 without elite three-point shooting. That is important because it means the Over result was supported by **interior efficiency and late-game free-throw volume**, not just high-variance perimeter luck.

## What SharpEdge Read Poorly

### 1. Low-score anchoring
The halftime total of 78 made the Under look attractive, but the process did not sufficiently separate **low realized points** from **low offensive opportunity quality**.

Portland's 37 first-half shots, 23 threes, 6 offensive rebounds, and poor FT conversion indicated that 36 points understated its available scoring paths.

### 2. Positive-regression asymmetry was underweighted
Portland had more obvious room to improve than the raw score suggested:
- 37.8% FG
- 25% FT
- multiple missed interior and perimeter opportunities

The second half validated that pressure with 52 points.

### 3. Foul trouble was treated too much as an Under signal
Leite and Engstler carried heavy foul counts, but a competitive game protected their closing usage rather than eliminating it.

### 4. Endgame foul tail was underpriced
At 64-61 after three quarters, the game was one possession apart. A close game makes intentional-foul scoring materially more likely late.

The final 20 seconds alone added eight points.

### 5. Correlated re-entry compounded the same thesis
The second Under increased total risk from $30.00 to $44.77 on essentially the same underlying game-total opinion.

This was not independent diversification; it was a larger bet on the same scoring assumption.

## What SharpEdge Read Correctly
1. The game did not become a three-point shootout.
2. Phoenix's offense remained relatively contained, scoring only 43 in the second half and 21 in Q4.
3. The End-3Q U169.5 was much closer to the true distribution than the halftime U163.5; it lost by only 3.5 points.
4. The game state remained competitive, which was visible before the final foul sequence and should now become an explicit modeling input.

## LIVE-FLOW Rule Upgrades From This Game

### `REALIZED_SCORE_VS_OPPORTUNITY_GATE`
Do not classify a low-scoring half as Under-friendly until checking whether the low score came from:
- low possession volume / low shot volume,
- poor shot quality,
- or merely poor conversion.

A low score created by poor conversion with healthy opportunity volume should trigger regression caution, not automatic Under pressure.

### `TEAM_REGRESSION_ASYMMETRY_GATE`
Before taking a full-game Under, identify which team has the strongest positive-regression path. If one side has depressed FG/FT conversion but normal or strong opportunity creation, raise the total floor accordingly.

### `FOUL_TROUBLE_USAGE_OVERRIDE`
Foul count alone is not a scoring-suppression signal in a close game. If a high-usage player remains active into Q4, closing usage can override earlier foul-based rotation expectations.

### `LATE_GAME_FOUL_TAIL_GATE`
For End-3Q totals in games within roughly one possession, explicitly add a late intentional-foul / timeout-extension tail before declaring an Under edge.

### `CORRELATED_REENTRY_THRESHOLD`
A second wager in the same direction on the same game must clear a higher edge threshold than the original entry. Re-entry is an exposure increase, not a new independent opportunity.

### `CHECKPOINT_FREEZE_REQUIRED`
Persist every market-blind halftime and end-3Q fair line before sportsbook reveal. This game cannot receive a complete model-vs-market calibration grade because the exact pre-market SharpEdge lines were not found in GitHub.

## Classification
- Halftime U163.5: **BAD TOTAL READ / REGRESSION UNDERWEIGHTED**
- End-3Q U169.5: **CLOSE BUT INCOMPLETE READ / LATE-FOUL TAIL UNDERPRICED**
- Overtime factor: **NONE**
- Regulation scoring model: **FAIL at halftime / PARTIAL at end 3Q**
- Correlated exposure control: **FAIL**
- Checkpoint persistence: **FAIL**
- Primary lesson: **Do not confuse depressed conversion with suppressed scoring opportunity.**

## Machine-Readable Summary
```yaml
game_id: WNBA_2026-08-16_POR_PHO
final:
  POR: 88
  PHO: 85
  total: 173
  overtime: false
halftime:
  POR: 36
  PHO: 42
  total: 78
  por_fg_pct: 37.8
  por_3p_pct: 30.4
  por_ft_pct: 25.0
  pho_fg_pct: 40.6
  pho_3p_pct: 33.3
  pho_ft_pct: 78.6
end_3q:
  POR: 61
  PHO: 64
  total: 125
q4:
  POR: 27
  PHO: 21
  total: 48
wagers:
  - checkpoint: halftime
    market: full_game_total
    selection: under
    line: 163.5
    odds_american: -115
    stake_usd: 30.00
    result: loss
    margin_to_line: 9.5
    loss_driver: second_half_scoring_regression
  - checkpoint: end_3q_or_early_q4
    market: full_game_total
    selection: under
    line: 169.5
    odds_american: -110
    stake_usd: 14.77
    result: loss
    margin_to_line: 3.5
    loss_driver: q4_portland_efficiency_plus_late_foul_tail
risk_usd: 44.77
net_usd: -44.77
model_audit:
  exact_market_blind_halftime_projection_found_in_github: false
  exact_market_blind_end3q_projection_found_in_github: false
process:
  halftime_total_read: fail
  end3q_total_read: partial
  overtime_tail: not_applicable
  regression_handling: fail
  late_game_foul_tail: fail
  correlated_exposure_control: fail
  checkpoint_persistence: fail
new_tags:
  - REALIZED_SCORE_VS_OPPORTUNITY_GATE
  - TEAM_REGRESSION_ASYMMETRY_GATE
  - FOUL_TROUBLE_USAGE_OVERRIDE
  - LATE_GAME_FOUL_TAIL_GATE
  - CORRELATED_REENTRY_THRESHOLD
  - CHECKPOINT_FREEZE_REQUIRED
status: POSTMORTEM_COMPLETE
```
