# NBA Finals 2026 — Game 3 Postmortem

**Game:** San Antonio Spurs at New York Knicks  
**Date:** 2026-06-08  
**Venue:** Madison Square Garden, New York, NY  
**Series state after game:** NYK leads 2-1  
**Final:** SAS 115, NYK 111  
**Final total:** 226

---

## Ticket Results

| Ticket | Entry | Stake | Result | Payout | Profit |
|---|---:|---:|---|---:|---:|
| Full Game Over 216.5 | -104 | $6.14 | Win | $12.09 | +$5.95 |
| LIVE-FLOW Halftime Over 225.5 | +105 | $7.14 | Win | $14.64 | +$7.50 |

**Combined stake:** $13.28  
**Combined payout:** $26.73  
**Combined profit:** +$13.45

---

## Closing / Market Context

Pregame market snapshot before lock-in showed:

- Full-game total around **216.5**.
- NYK team total around **108.5**.
- SAS team total around **106.5**.
- Game line around **NYK -1.5 / SAS +1.5**.

Primary pregame lock was **Over 216.5 -104**.

At halftime, live market moved to:

- Score: **NYK 64, SAS 57**.
- Halftime total: **121**.
- Live full-game total: **225.5**.
- LIVE-FLOW continuation lock: **Over 225.5 +105**.

The final landed exactly **226**, clearing both positions by:

- Pregame Over 216.5: **+9.5 points**.
- Halftime Over 225.5: **+0.5 points**.

---

## Model / Projection Record

### Pregame projection posture

The pregame model identified the total as the cleanest playable edge rather than forcing a side. The market sat near 216.5 while our scoring expectation had enough clearance to justify Over exposure.

### Halftime LIVE-FLOW projection posture

At halftime:

- Score pace was elevated at **121 first-half points**.
- Market asked for only **105 second-half points** to clear 225.5.
- We projected continuation probability above break-even at the +105 price.

Recorded LIVE-FLOW board:

| Market | Price | Needed | Model Mean | Model Median | Hit Probability | Break-even | Edge |
|---|---:|---:|---:|---:|---:|---:|---:|
| Over 225.5 | +105 | 226+ | 231.2 | 230 | 60.8% | 48.8% | +12.0% |

Fair price estimate: **-155**.

---

## Game Flow Summary

| Quarter | SAS | NYK | Total |
|---|---:|---:|---:|
| 1Q | 33 | 22 | 55 |
| 2Q | 24 | 42 | 66 |
| 3Q | 35 | 27 | 62 |
| 4Q | 23 | 20 | 43 |
| Final | 115 | 111 | 226 |

The game opened with SAS efficiency and Knicks turnovers creating a 33-22 Spurs 1Q. NYK answered with a massive 42-point 2Q, producing the high-leverage halftime total of 121. The 3Q stayed strong at 62 combined points, giving the live Over 225.5 meaningful cushion into the 4Q. The 4Q slowed hard to 43 points, but the prior scoring bank held just enough for the hook win.

---

## Statistical Anchors

### Final box efficiency

**SAS:**

- 39/84 FG, 46.4%.
- 12/34 3P, 35.3%.
- 25/32 FT, 78.1%.
- 28 assists, 8 turnovers.
- 115 points.

**NYK:**

- 40/88 FG, 45.5%.
- 13/37 3P, 35.1%.
- 18/22 FT, 81.8%.
- 18 assists, 13 turnovers.
- 111 points.

### Scoring contributors

**SAS:**

- Victor Wembanyama: 32 points, 8 rebounds, 6 assists, 3 blocks.
- Stephon Castle: 23 points, 5 rebounds, 5 assists.
- Dylan Harper: 13 points, 9 rebounds.
- De'Aaron Fox: 12 points, 8 assists.
- Julian Champagnie: 12 points.

**NYK:**

- Jalen Brunson: 32 points, 5 rebounds, 5 assists.
- OG Anunoby: 28 points.
- Josh Hart: 16 points, 9 rebounds, 5 assists.
- Karl-Anthony Towns: 11 points, 8 rebounds.
- Jordan Clarkson: 10 points.

---

## Rebounding / Physicality Notes

SAS won with Wembanyama as the primary defensive and late-clock stabilizer, but NYK created major second-chance pressure:

- NYK offensive rebounds: **12**.
- SAS offensive rebounds: **6**.
- NYK second-chance points: **21**.
- SAS second-chance points: **10**.

The Knicks did not lose because of possession generation; they lost because second-half shot quality and late-game conversion collapsed relative to the possession volume.

Key final rebound signals:

- Josh Hart: 9 rebounds.
- Dylan Harper: 9 rebounds.
- Victor Wembanyama: 8 rebounds.
- Karl-Anthony Towns: 8 rebounds.
- Luke Kornet: 5 rebounds in 9:16.

---

## Critical Inflection Points

1. **NYK 2Q explosion**  
   Knicks scored 42 in the second quarter on 14/19 FG and 6/9 from three. This validated the pregame Over and created the live-flow strike window.

2. **SAS 3Q counterpunch**  
   Spurs won the 3Q 35-27. That gave the halftime Over 225.5 a strong bank entering the 4Q.

3. **4Q pace collapse**  
   Final quarter produced only 43 points. The LIVE-FLOW Over survived by exactly 0.5 because the first three quarters had already produced 183 points.

4. **Late foul/free-throw sequence**  
   Wembanyama and Castle late free throws helped push and preserve the final total to 226.

---

## Betting Grade

| Market | Grade | Notes |
|---|---|---|
| Pregame Over 216.5 | A | Correct market disagreement; won by 9.5. |
| Halftime Over 225.5 +105 | A- | Correct edge and price capture; result landed by hook. |
| Side exposure | Pass was correct | Side was volatile and changed direction multiple times. |

Overall grade: **A**

---

## Rolling Window Tags

```json
{
  "series": "NBA_Finals_2026_NYK_SAS",
  "game": 3,
  "date": "2026-06-08",
  "venue": "Madison Square Garden",
  "final_score": {
    "SAS": 115,
    "NYK": 111
  },
  "final_total": 226,
  "series_result_after_game": "NYK leads 2-1",
  "primary_pre_game_position": {
    "market": "Full Game Total",
    "side": "Over 216.5",
    "odds": -104,
    "stake": 6.14,
    "result": "win",
    "payout": 12.09,
    "profit": 5.95
  },
  "live_flow_position": {
    "market": "Full Game Total",
    "side": "Over 225.5",
    "odds": 105,
    "stake": 7.14,
    "result": "win",
    "payout": 14.64,
    "profit": 7.50,
    "entry_state": "halftime",
    "halftime_score": {
      "NYK": 64,
      "SAS": 57,
      "total": 121
    },
    "model_mean_total": 231.2,
    "model_median_total": 230,
    "hit_probability": 0.608,
    "break_even_probability": 0.488,
    "edge": 0.120,
    "fair_price": -155
  },
  "game_flow_tags": [
    "high_first_half_total",
    "live_flow_over_continuation",
    "third_quarter_confirmation",
    "fourth_quarter_pace_collapse",
    "hook_win",
    "SAS_late_free_throw_preservation",
    "NYK_second_chance_pressure",
    "Wembanyama_two_way_anchor"
  ],
  "next_game_preparation_notes": [
    "Recheck NYK offensive rebounding sustainability",
    "Monitor Bridges role/minutes after low usage game",
    "Track Knicks late-game shot quality vs SAS length",
    "Continue pricing Wembanyama FT/paint pressure impact",
    "Treat full-game total as sensitive to 4Q slowdown risk despite strong first-half pace"
  ]
}
```

---

## Game 4 Prep Notes

- NYK generated enough offensive boards and second-chance points to remain dangerous, but their late-clock offense degraded badly.
- SAS showed they can win on the road despite losing the offensive glass, because Wembanyama/Castle/Fox created enough late pressure and free throws.
- Totals remain live, but Game 4 needs a stricter 4Q pace discount unless market gives a clear number gap.
- Watch for NYK adjustment toward more Brunson/KAT screening action and less low-yield Bridges/Shamet spacing possessions.
- SAS road shot profile was strong enough to respect, but their 4Q half-court efficiency still needs monitoring.
