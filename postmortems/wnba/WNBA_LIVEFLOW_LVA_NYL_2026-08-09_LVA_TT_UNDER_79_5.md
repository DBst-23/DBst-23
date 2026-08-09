# WNBA LIVE-FLOW Log — Las Vegas Aces at New York Liberty

## Game ID

- Date: 2026-08-09
- Matchup: Las Vegas Aces at New York Liberty
- Venue: Barclays Center, Brooklyn, NY
- Halftime: New York 50, Las Vegas 39
- Status: PENDING

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
- 5/9 3PT (55.6%)
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

| Market | Book | SharpEdge Fair | Difference | Decision |
|---|---:|---:|---:|---|
| Full-game total | 175.5 | 172 | 3.5 toward Under | PASS |
| New York spread | -14.5 | -22 | 7.5 toward NYL | Strong lean / no primary strike |
| New York team total | 94.5 | 97 | 2.5 toward Over | PASS |
| Las Vegas team total | 79.5 | 75 | 4.5 toward Under | STRIKE |

---

## 3. Wager

- Market: Las Vegas Aces Team Total Points Live
- Selection: Under 79.5
- Odds: -110
- Stake: $10.00
- To Win: $9.09
- Total Payout: $19.09
- Sportsbook: William Hill
- Ticket status: PLACED / PENDING
- Bet timestamp shown on ticket: 2026-08-09 10:25 AM NV

### Edge at entry

- Sportsbook team total: 79.5
- SharpEdge fair Las Vegas team total: 75
- Raw model edge: 4.5 points toward Under
- Las Vegas halftime points: 39
- Points required by Las Vegas in 2H to reach 80: 41
- SharpEdge projected Las Vegas 2H points: 36

### Stake classification

- LIVE-FLOW strike
- 0.5-unit style position
- Cleared active 4-point minimum model-to-market separation threshold

---

## 4. Why This Was the Primary Strike

1. Las Vegas' second-quarter offense was supported by elevated shooting percentages rather than robust shot generation.
2. Core creators Gray, Wilson, and Young were unavailable.
3. Las Vegas produced only 12 first-half paint points and one offensive rebound.
4. New York held a 23-11 rebounding advantage and an 8-1 offensive-rebound advantage.
5. The full-game Under 175.5 showed only 3.5 points of separation, below the active strike threshold.
6. New York -14.5 showed a large raw spread edge but carried greater team-allocation and garbage-time variance.
7. The Las Vegas team-total Under isolated the strongest structural read directly: depleted creation plus likely shooting regression.

---

## 5. Postgame Fields — Pending

To complete after final:

- Final score: TBD
- Las Vegas final points: TBD
- Las Vegas 2H points: TBD
- Wager result: TBD
- Profit/loss: TBD
- Margin vs 79.5: TBD
- Model error vs fair team total 75: TBD
- Model error vs projected Las Vegas 2H points 36: TBD
- Full-game total actual vs fair 172: TBD
- New York final points vs fair 97: TBD
- Spread actual vs fair New York -22: TBD
- Whether Las Vegas shooting regression occurred: TBD
- Whether garbage-time scoring materially affected team allocation: TBD
- Decision-quality grade: TBD
- Model-quality grade: TBD

---

## 6. Clean Record

```yaml
game_id: WNBA_2026-08-09_LVA_NYL
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
  status: pending
```
