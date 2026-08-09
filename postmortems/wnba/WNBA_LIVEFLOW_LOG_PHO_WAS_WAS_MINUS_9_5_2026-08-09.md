# WNBA LIVE-FLOW Log — Phoenix Mercury at Washington Mystics — Washington -9.5

## Game ID

- Date: 2026-08-09
- Matchup: Phoenix Mercury at Washington Mystics
- Venue: CareFirst Arena, Washington, DC
- Halftime: Washington 50, Phoenix 37
- First-Half Total: 87
- Status: LIVE WAGER LOCKED — awaiting final postmortem

---

## 1. Wager Record

- Market: Live Full-Game Spread
- Selection: Washington Mystics -9.5
- Odds: -115
- Stake: $10.00
- To Win: $8.70
- Total Payout if Win: $18.70
- Book: William Hill Sportsbook
- Bet Receipt Timestamp: 2026-08-09 12:54 PM screenshot timestamp
- Result: PENDING

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
- Phoenix 1H FG: 14/35 (40.0%)
- Phoenix 1H 3PT: 6/12 (50.0%)
- Phoenix 1H FT: 3/4 (75.0%)
- Phoenix turnovers: 10
- Washington 1H FG: 20/37 (54.1%)
- Washington 1H 3PT: 3/11 (27.3%)
- Washington 1H FT: 7/10 (70.0%)
- Washington turnovers: 2
- Washington paint points: 30
- Phoenix paint points: 12
- Washington fast-break points: 13
- Phoenix fast-break points: 2
- Washington second-chance points: 8
- Phoenix second-chance points: 2

### Key Player State

- Shakira Austin: 16 points, 8 rebounds, 7/13 FG
- Kiki Iriafen: 4 points, 3 rebounds
- Sonia Citron: 3 points, 4 assists
- Alyssa Thomas: 8 points, 6 rebounds, 5 assists, 4 turnovers
- Kahleah Copper: 8 points, 2 assists
- Kelsey Plum: 5 points, 2 assists, 3 turnovers

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

### Rationale

1. The model was frozen before seeing the sportsbook market.
2. SharpEdge projected Washington -16 full game; the actual locked market was only -9.5.
3. That created a 6.5-point model-to-market spread separation, clearing the current 4-point minimum and preferred 5+ point LIVE-FLOW threshold.
4. Washington's first-half scoring was not dependent on unsustainable three-point shooting: only 3/11 from three while scoring 50.
5. Washington controlled the paint 30-12 and the turnover battle 2-10.
6. Phoenix's 50% three-point shooting was one of the few factors keeping its first-half offense afloat and presented regression risk.
7. Washington's offensive structure looked more repeatable than Phoenix's, especially through paint production, low turnover rate, and transition scoring.
8. The actual -9.5 lock was one point better than the -10.5 line originally compared, increasing the edge rather than chasing a worse number.

---

## 5. Guardrails Active

- Market-blind projection first: PASSED
- Minimum model-to-market separation >= 4.0 points: PASSED
- Preferred separation >= 5.0 points: PASSED
- Avoid correlated stacking: ACTIVE
- Do not chase worse number: PASSED — actual entry improved by 1 point
- Halftime spread confidence: elevated but still subject to trailing-team comeback variance

---

## 6. Postmortem Fields to Complete at Final

- Final score
- Actual second-half score
- Actual second-half spread
- Actual full-game margin
- Cover margin versus Washington -9.5
- Model error on Washington 2H points
- Model error on Phoenix 2H points
- Model error on final spread
- Model error on full-game total
- Whether Phoenix 3PT regression occurred
- Whether Phoenix turnover regression occurred
- Whether Washington paint dominance persisted
- Whether Washington's low-turnover profile persisted
- Whether spread allocation outperformed or underperformed the total model
- Final signal classification

---

## 7. Clean Machine-Readable Record

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
  payout_if_win: 18.70
  book: William_Hill
  status: pending
  edge_points_vs_model: 6.5
  line_improvement_vs_observed: 1.0
process:
  projection_frozen_before_market: true
  minimum_edge_threshold_passed: true
  preferred_5_plus_threshold_passed: true
  correlated_stack_avoided: true
```
