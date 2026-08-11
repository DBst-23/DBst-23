# WNBA LIVE-FLOW Log — Toronto Tempo at Atlanta Dream — 3Q Checkpoint

## Game ID

- Date: 2026-08-10
- Matchup: Toronto Tempo at Atlanta Dream
- Venue: Gateway Center Arena @ College Park, Atlanta, GA
- Checkpoint: End of 3rd Quarter
- Score: Atlanta 80, Toronto 67
- Through-3Q Total: 147
- Atlanta Lead: 13
- Status: LIVE-FLOW MARKET COMPARED — PASS / NO STRIKE

---

## 1. Through-3Q State

### Toronto Tempo
- Points: 67
- FG: 26/53 (49.1%)
- 3PT: 9/22 (40.9%)
- FT: 6/10 (60.0%)
- Rebounds: 17
- Assists: 16
- Turnovers: 10
- Fouls: 19
- Paint Points: 34
- Fast Break Points: 6
- Second-Chance Points: 4

### Atlanta Dream
- Points: 80
- FG: 25/50 (50.0%)
- 3PT: 10/24 (41.7%)
- FT: 20/27 (74.1%)
- Rebounds: 31
- Assists: 20
- Turnovers: 10
- Fouls: 12
- Paint Points: 30
- Fast Break Points: 1
- Second-Chance Points: 6

### Quarter Scores
- Q1: Atlanta 24, Toronto 22
- Q2: Atlanta 30, Toronto 17
- Q3: Toronto 28, Atlanta 26

---

## 2. Key LIVE-FLOW Read

1. Atlanta owns a major rebounding advantage despite equal turnovers: 31-17 on the glass through three quarters.
2. Toronto's offense is being materially supported by strong perimeter shooting, especially Marina Mabrey (24 points, 6/10 from three through 3Q).
3. Atlanta's scoring profile is broader and more stable: 20 assists, strong rim/paint creation, and a large free-throw-volume edge.
4. Toronto has accumulated 19 team fouls, with Isabelle Harrison at four and multiple rotation players at three. That increases Atlanta's late-game free-throw and bonus pathways.
5. Atlanta's 20/27 FT production is a major component of the 80-point output and should not simply be extrapolated at the same rate.
6. Toronto cut a 25-point Atlanta lead to 13 by the end of Q3, so the final-quarter projection respects comeback momentum rather than blindly extending the maximum lead.
7. Both teams are above 40% from three through three quarters; some combined perimeter cooling is more likely than a continued shooting spike.

---

## 3. SharpEdge Market-Blind Projection — FROZEN BEFORE MARKET

### Projected 4th Quarter
- Toronto: 22
- Atlanta: 24
- 4Q Fair Spread: Atlanta -2
- 4Q Fair Total: 46

### Projected Final
- Toronto Tempo: 89
- Atlanta Dream: 104
- SharpEdge Fair Full-Game Spread: Atlanta -15
- SharpEdge Fair Full-Game Total: 193
- SharpEdge Fair Atlanta Team Total: 104
- SharpEdge Fair Toronto Team Total: 89

### Practical Fair Ranges
- Atlanta final points: 101-106
- Toronto final points: 86-92
- Full-game total: 188-198
- Final Atlanta margin: 11-19

---

## 4. William Hill Market Comparison

Market captured after the market-blind projection was frozen.

### Full-Game Spread
- SharpEdge fair: Atlanta -15
- William Hill: Atlanta -15.5 (-120) / Toronto +15.5 (-110)
- Separation: 0.5 point toward Toronto
- Strike threshold: 4.0+ points
- Decision: PASS

### Full-Game Total
- SharpEdge fair: 193
- William Hill: Over 192.5 (-120) / Under 192.5 (-110)
- Separation: 0.5 point toward Over
- Strike threshold: 5.0+ points
- Decision: PASS

### Atlanta Team Total
- SharpEdge fair: 104
- William Hill: Over 104.5 (-105) / Under 104.5 (-125)
- Separation: 0.5 point toward Under
- Strike threshold: 4.0+ points
- Decision: PASS

### Toronto Team Total
- SharpEdge fair: 89
- William Hill: Over 88.5 (-105) / Under 88.5 (-125)
- Separation: 0.5 point toward Over
- Strike threshold: 4.0+ points
- Decision: PASS

### Market Verdict
The sportsbook and SharpEdge projection are essentially in equilibrium across every available market. No line provides enough model-to-market separation to justify exposure. This is a disciplined no-bet checkpoint.

---

## 5. Strike Thresholds

- Spread: prefer >= 4.0 points model-to-market separation; 5+ is premium.
- Total: prefer >= 5.0 points separation unless possession/rotation evidence is unusually strong.
- Team total: prefer >= 4.0 points separation.
- Avoid stacking strongly correlated positions unless one market is materially more mispriced.
- Do not chase a worse number after comparison.

---

## 6. Clean Machine-Readable Record

```yaml
game_id: WNBA_2026-08-10_TOR_ATL
checkpoint: end_3q
score:
  TOR: 67
  ATL: 80
through_3q_total: 147
lead: ATL_13
team_stats:
  TOR:
    fg: 26/53
    fg_pct: 49.1
    three_pt: 9/22
    three_pt_pct: 40.9
    ft: 6/10
    ft_pct: 60.0
    rebounds: 17
    assists: 16
    turnovers: 10
    fouls: 19
  ATL:
    fg: 25/50
    fg_pct: 50.0
    three_pt: 10/24
    three_pt_pct: 41.7
    ft: 20/27
    ft_pct: 74.1
    rebounds: 31
    assists: 20
    turnovers: 10
    fouls: 12
model_frozen:
  fourth_quarter_score:
    TOR: 22
    ATL: 24
  fourth_quarter_total: 46
  fourth_quarter_spread: ATL_-2
  final_score:
    TOR: 89
    ATL: 104
  full_game_total: 193
  full_game_spread: ATL_-15
  team_totals:
    TOR: 89
    ATL: 104
market:
  sportsbook: William_Hill
  spread:
    TOR: +15.5_-110
    ATL: -15.5_-120
  total:
    over: 192.5_-120
    under: 192.5_-110
  team_totals:
    ATL:
      over: 104.5_-105
      under: 104.5_-125
    TOR:
      over: 88.5_-105
      under: 88.5_-125
edges:
  spread_points: 0.5_TOR
  total_points: 0.5_OVER
  atl_team_total_points: 0.5_UNDER
  tor_team_total_points: 0.5_OVER
market_seen: true
wager_status: PASS_NO_STRIKE
pass_reason: no_market_exceeded_minimum_edge_threshold
```
