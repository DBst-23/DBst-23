# NBA Postmortem — SAS @ POR Game 4

**Date:** 2026-04-26  
**Final:** Spurs 114, Trail Blazers 93  
**Primary Card:** UD Champions 3-pick — SAS -5.5, Wembanyama higher 11.5 rebounds, Avdija higher 6.5 rebounds  
**Result:** 3-for-3 sweep  
**Logged:** Postmortem GitHub Workflow

---

## 1. Result Snapshot

| Team | Final | FG | 3P | FT | REB | OREB | AST | STL | BLK | TOV | PTS off TOV | PITP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SAS | 114 | 43-87 | 14-33 | 14-17 | 40 | 9 | 26 | 12 | 10 | 13 | 29 | 52 |
| POR | 93 | 32-80 | 10-31 | 19-23 | 39 | 7 | 14 | 6 | 5 | 18 | 18 | 38 |

**Core margin source:** San Antonio won the clean execution layer: +12 assists, +6 steals, +5 blocks, +11 points off turnovers, +14 paint points, and +10.1 TS%.

---

## 2. Bet Card Result

| Leg | Line | Result | Outcome |
|---|---:|---:|---|
| SAS spread | -5.5 | Won by 21 | Hit |
| Victor Wembanyama higher rebounds | 11.5 | 12 | Hit |
| Deni Avdija higher rebounds | 6.5 | 7 | Hit |

**Card result:** 3-for-3 sweep.

---

## 3. Game Script Summary

San Antonio survived Portland's early push and flipped the game with defensive disruption, paint pressure, and elite two-way center dominance from Wembanyama. Portland's offense was narrow: Avdija and Holiday created most of the usable scoring, while Scoot Henderson finished scoreless and Clingan struggled badly as a shooter.

The Spurs' decisive edge came from the combination of Wembanyama rim protection, Fox downhill shot creation, Castle passing pressure, and Portland's 18 turnovers.

---

## 4. Spurs Player Notes

| Player | MIN | PTS | REB | AST | STL | BLK | +/- | TS% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Victor Wembanyama | 34 | 27 | 12 | 3 | 4 | 7 | +28 | 65.8 |
| De'Aaron Fox | 39 | 28 | 6 | 7 | 1 | 2 | +21 | 74.6 |
| Stephon Castle | 26 | 16 | 1 | 8 | 1 | 0 | +17 | 55.4 |
| Devin Vassell | 35 | 11 | 6 | 3 | 1 | 1 | +14 | 61.1 |
| Luke Kornet | 12 | 2 | 7 | 0 | 1 | 0 | -10 | 14.3 |

**Wembanyama:** Fully validated as both anchor and rebound leg. He had 19 rebound chances, 12 boards, 5 contested rebounds, 7 blocks, and a +28. His over hit by a thin margin but the process was strong.

**Fox:** Secondary all-around driver. His 28 points, 7 assists, 6 rebounds, and 74.6 TS% made the spread leg much cleaner than the market implied.

---

## 5. Portland Player Notes

| Player | MIN | PTS | REB | AST | STL | BLK | +/- | TS% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Deni Avdija | 37 | 26 | 7 | 3 | 1 | 0 | -16 | 72.4 |
| Jrue Holiday | 37 | 20 | 6 | 4 | 1 | 0 | -25 | 63.9 |
| Donovan Clingan | 14 | 5 | 6 | 0 | 0 | 1 | -14 | 25.0 |
| Robert Williams III | 26 | 4 | 6 | 2 | 0 | 2 | +3 | 50.0 |
| Scoot Henderson | 27 | 0 | 0 | 2 | 1 | 0 | -22 | 0.0 |

**Avdija:** Rebound over validated, but not because of elite conversion. He had 18 rebound chances and only converted 7. Volume and minutes carried the leg.

**Portland failure point:** Scoot's zero-point game and Clingan's 2-10 shooting created too much offensive drag.

---

## 6. Rebound Tracking Layer

### Spurs

| Player | MIN | REB | Contested | Chances | Chance% | Adjusted Chance% | Avg Dist |
|---|---:|---:|---:|---:|---:|---:|---:|
| Victor Wembanyama | 34.3 | 12 | 5 | 19 | 63.2% | 63.2% | 3.7 |
| Luke Kornet | 12.2 | 7 | 3 | 11 | 63.6% | 63.6% | 3.2 |
| De'Aaron Fox | 38.8 | 6 | 1 | 9 | 66.7% | 75.0% | 11.2 |
| Devin Vassell | 34.9 | 6 | 1 | 7 | 85.7% | 85.7% | 9.8 |
| Julian Champagnie | 28.9 | 3 | 1 | 7 | 42.9% | 42.9% | 6.5 |

### Trail Blazers

| Player | MIN | REB | Contested | Chances | Chance% | Adjusted Chance% | Avg Dist |
|---|---:|---:|---:|---:|---:|---:|---:|
| Deni Avdija | 36.9 | 7 | 2 | 18 | 38.9% | 41.2% | 5.9 |
| Donovan Clingan | 14.2 | 6 | 3 | 10 | 60.0% | 60.0% | 3.6 |
| Robert Williams III | 26.4 | 6 | 1 | 15 | 40.0% | 46.2% | 3.6 |
| Jrue Holiday | 37.0 | 6 | 0 | 10 | 60.0% | 60.0% | 7.9 |
| Toumani Camara | 31.5 | 5 | 3 | 14 | 35.7% | 41.7% | 8.2 |
| Jerami Grant | 32.9 | 5 | 1 | 11 | 45.5% | 55.6% | 12.7 |

**Tracking note:** The uploaded POR player rebound report confirms Portland's player rebound totals and defensive rebound components, including Holiday 6 rebounds, Avdija 7, Grant 5, Camara 5, Robert Williams 6, and Clingan 6. Source file: POR_player_reb.pdf.

---

## 7. Box-Out Layer

### Spurs Box-Outs by Position

| Position | MIN | Box Outs | Off | Def | Off% | Def% |
|---|---:|---:|---:|---:|---:|---:|
| Forward | 28.8 | 5 | 1 | 4 | 20.0% | 80.0% |
| Center | 9.6 | 4 | 1 | 3 | 25.0% | 75.0% |
| Guard | 28.7 | 1 | 0 | 1 | 0.0% | 100% |

### Trail Blazers Box-Outs by Position

| Position | MIN | Box Outs | Off | Def | Off% | Def% |
|---|---:|---:|---:|---:|---:|---:|
| Forward | 28.0 | 4 | 0 | 4 | 0.0% | 100% |
| Center | 8.4 | 1 | 0 | 1 | 0.0% | 100% |

**Patch read:** Wembanyama passed the clean center-over profile: high chances, low average rebound distance, no deferred chances, and strong contested collection. This is the positive inverse of the Sengun miss from the prior postmortem.

---

## 8. Model Diagnosis

### What Worked

- **SAS -5.5:** Correct. Final margin +21.
- **Wembanyama higher 11.5 rebounds:** Correct. Strong chance volume and elite collection zone.
- **Avdija higher 6.5 rebounds:** Correct. Minutes and chance volume carried the play despite mediocre conversion efficiency.

### What Matters for Future

Wembanyama and Avdija hit through different mechanisms:

- Wembanyama = high-quality center-local rebounds.
- Avdija = high-volume wing rebound exposure.

That distinction matters for future pricing.

---

## 9. Patch Tags

```json
{
  "game_id": "2026-04-26_SAS_POR_G4",
  "postmortem_type": "NBA_PLAYOFF_REBOUND_AND_SPREAD_POSTMORTEM",
  "final_score": {
    "SAS": 114,
    "POR": 93
  },
  "bet_card": {
    "platform": "Underdog",
    "legs": [
      {
        "market": "spread",
        "team": "SAS",
        "line": -5.5,
        "actual_margin": 21,
        "result": "hit"
      },
      {
        "player": "Victor Wembanyama",
        "market": "rebounds",
        "line": 11.5,
        "actual": 12,
        "result": "hit"
      },
      {
        "player": "Deni Avdija",
        "market": "rebounds",
        "line": 6.5,
        "actual": 7,
        "result": "hit"
      }
    ],
    "record": "3-0",
    "card_result": "win"
  },
  "environment_tags": [
    "CENTER_REBOUND_PROFILE_VALIDATED",
    "LOW_DISTANCE_REBOUND_EDGE",
    "WING_VOLUME_REBOUND_EDGE",
    "SPURS_DEFENSIVE_DISRUPTION",
    "PORTLAND_BACKCOURT_COLLAPSE",
    "TURNOVER_MARGIN_PRESSURE"
  ],
  "patches": [
    "WEMBY_CENTER_REBOUND_OVER_VALIDATED",
    "AVDIJA_VOLUME_REBOUND_PATH",
    "SAS_SPREAD_DEFENSE_TO_OFFENSE_EDGE",
    "POR_SCOOT_ZERO_OUTPUT_DRAG",
    "CLINGAN_OFFENSIVE_EFFICIENCY_DRAG"
  ]
}
```

---

## 10. Future Rule

For rebound overs, separate center profiles into two classes:

1. **Center-local quality rebounds**
   - Avg distance under 5 feet
   - High contested rebound count
   - No deferred chances
   - High block/rim contest role

2. **Center-volatility rebounds**
   - Avg distance above 10 feet
   - Deferred chances present
   - Active forward rebound steal risk

Wembanyama fell into class 1. Sengun from the prior postmortem fell into class 2.

---

## 11. Final Read

This was a clean model win. The spread leg, Wembanyama rebound leg, and Avdija rebound leg all aligned with the actual game script. San Antonio's defensive disruption and Wembanyama's center-local rebound quality created the separation. Avdija's leg was thinner but still process-valid because his minutes and 18 rebound chances gave him enough volume to clear 6.5.
