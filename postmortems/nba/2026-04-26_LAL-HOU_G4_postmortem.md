# NBA Postmortem — LAL @ HOU Game 4

**Date:** 2026-04-26  
**Final:** Rockets 115, Lakers 96  
**Series Context:** Lakers entered 3-0; Rockets avoided elimination / extended series  
**Logged:** Postmortem GitHub Workflow  

---

## 1. Result Snapshot

| Team | Final | FG | 3P | FT | REB | OREB | TOV | PTS off TOV | FB PTS | PITP | 2nd Chance |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LAL | 96 | 37-74 | 5-22 | 17-21 | 37 | 10 | 24 | 19 | 18 | 54 | 13 |
| HOU | 115 | 39-81 | 12-30 | 25-31 | 35 | 11 | 13 | 30 | 23 | 46 | 20 |

**Core margin source:** Houston won the possession-conversion layer despite losing total rebounds by 2. Turnovers, threes, free throws, and second-chance points drove the final separation.

---

## 2. Bet Card Result

**UD Champions — 3 Picks**  
**Entry:** $15  
**Result:** Lost, 2-for-3

| Leg | Line | Result | Outcome |
|---|---:|---:|---|
| Deandre Ayton higher rebounds | 8.5 | 10 | Hit |
| Jabari Smith Jr. higher rebounds | 7.5 | 8 | Hit |
| Alperen Sengun higher rebounds | 9.5 | 6 | Miss |

---

## 3. Rebound Environment Snapshot

### Environment Classification

**Balanced board count, but Houston rebound allocation was forward-wing driven rather than center-driven.**

LAL finished with 37 rebounds and HOU finished with 35, so this was not a raw rebound-volume failure. The failure came from **Houston rebound distribution**: Jabari Smith Jr. and Tari Eason absorbed the cleaner rebound opportunities while Sengun’s chances skewed longer and more deferred.

---

## 4. Player Rebound Tracking

### Lakers

| Player | MIN | REB | Contested | Chances | Chance% | Adjusted Chance% | Avg Dist |
|---|---:|---:|---:|---:|---:|---:|---:|
| Deandre Ayton | 25.4 | 10 | 4 | 15 | 66.7% | 66.7% | 3.5 |
| LeBron James | 33.2 | 4 | 2 | 6 | 66.7% | 66.7% | 4.2 |
| Jarred Vanderbilt | 14.0 | 4 | 0 | 6 | 66.7% | 66.7% | 6.0 |
| Rui Hachimura | 29.6 | 3 | 0 | 5 | 60.0% | 60.0% | 4.4 |
| Luke Kennard | 32.3 | 3 | 0 | 8 | 37.5% | 37.5% | 4.7 |
| Marcus Smart | 30.6 | 2 | 1 | 8 | 25.0% | 40.0% | 7.2 |

**Ayton read:** Correct. His rebound profile was high-quality and interior-based: 15 chances, 10 boards, 3.5 avg rebound distance.

### Rockets

| Player | MIN | REB | Contested | Chances | Chance% | Adjusted Chance% | Avg Dist |
|---|---:|---:|---:|---:|---:|---:|---:|
| Alperen Sengun | 33.0 | 6 | 1 | 15 | 40.0% | 50.0% | 13.2 |
| Jabari Smith Jr. | 41.5 | 8 | 1 | 12 | 66.7% | 80.0% | 4.2 |
| Tari Eason | 30.4 | 8 | 3 | 9 | 88.9% | 88.9% | 6.1 |
| Amen Thompson | 40.6 | 4 | 2 | 10 | 40.0% | 44.4% | 11.7 |
| Josh Okogie | 18.7 | 4 | 2 | 12 | 33.3% | 36.4% | 8.0 |
| Reed Sheppard | 28.6 | 1 | 0 | 6 | 16.7% | 20.0% | 10.1 |

**Sengun read:** Miss was not from minutes or raw opportunities. He had 15 chances, same as Ayton, but his average rebound distance was 13.2 feet, which signals long-board volatility and non-center collection zones. He also deferred 3 chances.

**Jabari read:** Correct. He had only 12 chances but converted 8, with 80.0% adjusted chance rate and 4.2 avg rebound distance. His boards were cleaner and more local to him.

---

## 5. Box-Out Layer

### Lakers Box-Outs by Position

| Position | MIN | Box Outs | Off | Def | Off% | Def% |
|---|---:|---:|---:|---:|---:|---:|
| Forward | 24.5 | 4 | 1 | 3 | 25.0% | 75.0% |
| Guard | 15.3 | 1 | 0 | 1 | 0.0% | 100% |
| Center | 8.1 | 1 | 0 | 1 | 0.0% | 100% |

### Rockets Box-Outs by Position

| Position | MIN | Box Outs | Off | Def | Off% | Def% |
|---|---:|---:|---:|---:|---:|---:|
| Forward | 27.6 | 2 | 0 | 2 | 0.0% | 100% |
| Center | 6.6 | 3 | 0 | 3 | 0.0% | 100% |
| Guard | 21.9 | 1 | 0 | 1 | 0.0% | 100% |

**Patch note:** Houston center box-outs did not translate into Sengun rebound control. The center position was involved in sealing, but the actual collections flowed to Jabari/Eason. This is a key miss-path for Sengun overs.

---

## 6. Game Phase Notes

### Lakers

- LeBron: 10 points, 4 rebounds, 9 assists, 8 turnovers.
- Ayton: 19 points, 10 rebounds, strong finishing profile.
- Smart/Kennard backcourt produced 6 turnovers combined.
- Lakers committed 24 total turnovers, giving Houston 30 points off turnovers.
- Lakers shot only 5-22 from three.

### Rockets

- Amen Thompson: 23 points, 7 assists, +21.
- Tari Eason: 20 points, 8 rebounds, 5 steals, +31.
- Jabari Smith Jr.: 16 points, 8 rebounds, +24.
- Sengun: 19 points, 6 rebounds, 7-13 FT, +7.
- Reed Sheppard: 17 points, 4-7 from three, +22.
- Houston generated 17 steals and 30 points off turnovers.

---

## 7. Model Diagnosis

### What Worked

- **Ayton over 8.5 rebounds:** correct interior-chance read.
- **Jabari Smith Jr. over 7.5 rebounds:** correct forward rebound redistribution read.
- Houston pressure/turnover edge was directionally correct.

### What Failed

- **Sengun over 9.5 rebounds:** failed due to rebound-distance and allocation profile.
- Sengun had sufficient chances but poor collection efficiency because boards were not center-local.
- Tari Eason and Jabari Smith Jr. captured the stronger rebound lanes.

---

## 8. Patch Tags

```json
{
  "game_id": "2026-04-26_LAL_HOU_G4",
  "postmortem_type": "NBA_PLAYOFF_REBOUND_POSTMORTEM",
  "final_score": {
    "LAL": 96,
    "HOU": 115
  },
  "bet_card": {
    "platform": "Underdog",
    "entry": 15,
    "legs": [
      {
        "player": "Deandre Ayton",
        "market": "rebounds",
        "line": 8.5,
        "actual": 10,
        "result": "hit"
      },
      {
        "player": "Jabari Smith Jr.",
        "market": "rebounds",
        "line": 7.5,
        "actual": 8,
        "result": "hit"
      },
      {
        "player": "Alperen Sengun",
        "market": "rebounds",
        "line": 9.5,
        "actual": 6,
        "result": "miss"
      }
    ],
    "record": "2-1",
    "card_result": "loss"
  },
  "environment_tags": [
    "REBOUND_DISTRIBUTION_SHIFT",
    "CENTER_CHANCE_QUALITY_DOWNGRADE",
    "FORWARD_REBOUND_CAPTURE_SPIKE",
    "LONG_REBOUND_VOLATILITY",
    "TURNOVER_PRESSURE_GAME_SCRIPT",
    "HOU_STEAL_PRESSURE_ACTIVE"
  ],
  "patches": [
    "SENGUN_REBOUND_DISTANCE_RISK",
    "JABARI_FORWARD_GLASS_BOOST",
    "EASON_ACTIVITY_REBOUND_SPIKE",
    "AYTON_INTERIOR_REBOUND_VALIDATED",
    "CENTER_BOXOUT_NOT_EQUAL_COLLECTION"
  ]
}
```

---

## 9. Future Rule

When a center rebound over is tied to a line of 9.5+ and the player shows:

- high rebound chances,
- but average rebound distance above 10 feet,
- plus deferred chances,
- plus active forward rebounders logging 30+ minutes,

then apply:

**CENTER_REBOUND_COLLECTION_RISK_DOWNGRADE**

This does not kill the over automatically, but it moves the play from strong card leg to caution unless pricing is discounted.

---

## 10. Final Read

This was a strong game-script read with one allocation miss. Ayton and Jabari were correctly identified as live rebound paths. Sengun’s miss was a model refinement point: chance volume alone was not enough. The rebound location and Houston forward activity shifted the board distribution away from him.
