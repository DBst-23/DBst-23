# NBA LiveFlow Ingestion — LAL @ HOU — 2026-05-01 — First Half

## Metadata

- Game: Los Angeles Lakers @ Houston Rockets
- Date: 2026-05-01
- Venue: Toyota Center, Houston, TX
- Source: NBA Official Scorer's Report / Official Play-by-Play
- Segment ingested: First Half, including Q1 and Q2 splits
- Officials: Scott Foster, Curtis Blair, Karl Lane, Kevin Cutler
- Mode: LIVE-FLOW ingestion / model training / postgame validation

## First Half Score

| Team | Q1 | Q2 | 1H Total |
|---|---:|---:|---:|
| Lakers | 23 | 26 | 49 |
| Rockets | 18 | 13 | 31 |

- 1H margin: Lakers +18
- 1H total: 80
- Period duration: 1:04

## Availability / Inactive Players

### Lakers

- Luka Doncic: OUT — left hamstring strain

### Rockets

- Steven Adams: OUT — left ankle surgery
- Kevin Durant: OUT — left ankle sprain
- Fred VanVleet: OUT — right knee ACL repair

## First Half Team Stats

| Category | Lakers | Rockets |
|---|---:|---:|
| FG | 18-45 | 12-41 |
| FG% | 40.0% | 29.3% |
| 3PT | 6-13 | 2-11 |
| 3PT% | 46.2% | 18.2% |
| FT | 7-11 | 5-8 |
| FT% | 63.6% | 62.5% |
| Offensive Rebounds | 6 | 2 |
| Defensive Rebounds | 22 | 18 |
| Total Rebounds | 28 | 20 |
| Assists | 10 | 5 |
| Steals | 3 | 1 |
| Turnovers | 6 | 10 |
| Blocks | 7 | 6 |
| Points in Paint | 22 | 20 |
| 2nd Chance Points | 2 | 2 |
| Fast Break Points | 14 | 4 |
| Biggest Lead | 19 | 5 |

## Quarter Splits

### Q1

| Team | Points | FG | 3PT | Rebounds | Turnovers |
|---|---:|---:|---:|---:|---:|
| Lakers | 23 | 9-25 | 3-7 | 15 | 1 |
| Rockets | 18 | 7-19 | 2-7 | 12 | 4 |

Signal notes:

- Lakers led 23-18 after Q1.
- Houston offense was still competitive early but turnover-prone.
- Sengun had 5 rebounds in Q1.
- Ayton had 4 rebounds in Q1.

### Q2

| Team | Points | FG | 3PT | Rebounds | Turnovers |
|---|---:|---:|---:|---:|---:|
| Lakers | 26 | 9-20 | 3-6 | 13 | 5 |
| Rockets | 13 | 5-22 | 0-4 | 8 | 6 |

Signal notes:

- Lakers won Q2 26-13.
- Houston shot 22.7% from the field and 0% from three in Q2.
- Rockets committed 6 turnovers in Q2, producing a collapse profile.
- Lakers generated 9 Q2 fast-break points.

## Player First Half Notes

### Lakers

| Player | Min | Pts | Reb | Ast | FG | 3PT | +/- | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| LeBron James | 20:04 | 18 | 3 | 5 | 7-14 | 2-4 | +14 | Primary engine; transition creator |
| Rui Hachimura | 17:28 | 10 | 4 | 1 | 4-8 | 2-3 | +8 | Efficient secondary scorer |
| Deandre Ayton | 16:01 | 2 | 8 | 0 | 0-3 | 0-0 | 0 | Rebound anchor despite low scoring |
| Austin Reaves | 17:53 | 7 | 2 | 2 | 3-7 | 0-1 | +5 | Secondary handler |
| Marcus Smart | 17:55 | 0 | 3 | 0 | 0-4 | 0-2 | +15 | Defensive pressure / disruption |
| Luke Kennard | 13:23 | 3 | 3 | 1 | 1-4 | 1-1 | +18 | Bench spacing, positive swing |
| Jaxson Hayes | 7:59 | 2 | 3 | 1 | 0-0 | 0-0 | +18 | Backup big energy |
| Jake LaRavia | 9:17 | 7 | 2 | 0 | 3-5 | 1-2 | +12 | Bench scoring burst |

### Rockets

| Player | Min | Pts | Reb | Ast | FG | 3PT | +/- | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Tari Eason | 15:44 | 7 | 2 | 0 | 3-7 | 1-3 | -8 | Early scoring, foul pressure |
| Jabari Smith Jr. | 21:48 | 7 | 4 | 1 | 2-6 | 1-3 | -11 | Frontcourt minutes load |
| Alperen Sengun | 21:35 | 8 | 7 | 0 | 3-8 | 0-0 | -17 | Primary interior hub, turnover drag |
| Reed Sheppard | 17:59 | 5 | 0 | 1 | 2-10 | 0-4 | -12 | Shot creation inefficient |
| Amen Thompson | 22:40 | 4 | 4 | 3 | 2-7 | 0-0 | -17 | Rim pressure, defensive activity, low scoring |
| Josh Okogie | 9:36 | 0 | 2 | 0 | 0-2 | 0-1 | -11 | Low offensive impact |
| Aaron Holiday | 6:01 | 0 | 1 | 0 | 0-0 | 0-0 | -6 | Low usage |
| Dorian Finney-Smith | 4:37 | 0 | 0 | 0 | 0-1 | 0-0 | -8 | Minimal impact |

## LiveFlow Model Signals

### Lakers Positive Signals

- `LEBRON_ENGINE_ACTIVE`
- `LA_TRANSITION_ADVANTAGE_ACTIVE`
- `HOU_TURNOVER_PRESSURE_EXPLOIT`
- `AYTON_REBOUND_ANCHOR_ACTIVE`
- `BENCH_PLUS_SWING_KENNARD_HAYES_LARAVIA`

### Rockets Negative Signals

- `HOU_PRIMARY_CREATION_DEPLETED`
- `DURANT_OUT_CREATION_LOSS`
- `VANVLEET_OUT_HANDLER_LOSS`
- `ADAMS_OUT_GLASS_PHYSICALITY_LOSS`
- `HOU_Q2_COLLAPSE_SIGNAL`
- `HOU_3PT_FAILURE_ACTIVE`
- `SENGUN_USAGE_WITH_LOW_EFFICIENCY`
- `LIVE_BALL_TURNOVER_DRAG`

## Key LiveFlow Interpretation

The first-half profile was not simply a Lakers shooting edge. It was a full structure failure from Houston:

1. Houston's creation tree was stripped by Durant and VanVleet being out.
2. Sengun was forced into a heavy hub role but did not generate efficient offense or assists.
3. Reed Sheppard volume was inefficient at 2-10 FG and 0-4 from three.
4. The Rockets had only 5 assists against 10 turnovers.
5. Lakers turned Houston misses and turnovers into a 14-4 fast-break edge.
6. Lakers controlled the glass 28-20 despite Ayton scoring only 2 points.

## Betting/Model Relevance

### For Live Totals

- Q2 Houston 13-point output activates severe offensive suppression.
- Any Houston live team total over should require proof of 3Q shot-quality recovery.
- Lakers defensive activity plus Houston missing creators creates under-friendly Houston scoring environment.

### For Rebounds

- Ayton 8 rebounds by half = strong continuation profile if minutes hold.
- Sengun 7 rebounds by half = strong raw board path, but blowout/minute risk must be monitored.
- Rockets poor shooting created extra defensive board volume for Lakers bigs/wings.

### For Spread / Side

- Lakers +18 at half was supported by turnover margin, transition edge, and Houston creation deficit.
- Houston comeback path required immediate 3Q shooting correction and turnover cleanup.

## First Half Summary Tag

```yaml
liveflow_ingestion:
  game: LAL_HOU_2026_05_01
  segment: first_half
  score: LAL_49_HOU_31
  primary_signal: HOU_Q2_COLLAPSE_SIGNAL
  lakers_edge:
    - transition
    - defensive_pressure
    - rebounding
    - LeBron_engine
  rockets_failure:
    - depleted_creation
    - poor_3pt_shooting
    - high_turnover_rate
    - low_assist_generation
  model_tags:
    - LIVEFLOW_INGESTED
    - FIRST_HALF_REPORT
    - HOU_CREATION_DEPLETION_ACTIVE
    - LAL_TRANSITION_RUNOUT_EDGE
    - AYTON_REBOUND_ANCHOR
    - SENGUN_HUB_STRESS_TEST
```
