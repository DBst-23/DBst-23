# NBA LiveFlow Ingestion — LAL @ HOU — 2026-05-01

## Metadata

- Game: Los Angeles Lakers @ Houston Rockets
- Date: 2026-05-01
- Venue: Toyota Center, Houston, TX
- Source: NBA Official Scorer's Report / Official Play-by-Play + Kalshi live market screenshot
- Segment ingested: 1st Quarter through 3rd Quarter 06:02, plus live market checkpoint at LAL 67 - HOU 47
- Officials: Scott Foster, Curtis Blair, Karl Lane, Kevin Cutler
- Mode: LIVE-FLOW ingestion / model training / postgame validation

## Current Score State — 3Q 06:02 Official Book

| Team | Q1 | Q2 | 3Q to 06:02 | Total |
|---|---:|---:|---:|---:|
| Lakers | 23 | 26 | 14 | 63 |
| Rockets | 18 | 13 | 8 | 39 |

- Current margin: Lakers +24
- Current total: 102
- Biggest Lakers lead: 25
- Attendance: 18,055 sellout

## Live Market Checkpoint — User Screen

- Score shown: LAL 67 - HOU 47
- Margin: Lakers +20
- Current total: 114

### Kalshi live lines shown

| Market | Line | Yes | No | LiveFlow Read |
|---|---:|---:|---:|---|
| Lakers spread | LAL by over 16.5 | +113 | -143 | Lean yes, but volatility/bench risk present |
| Full-game total | Over 176.5 | -112 | -108 | No clean edge; total has repriced into fair zone |
| Houston team total | Over 101.5 | +943 | Bid | Avoid over; structural under remains |
| Lakers team total | Over 97.5 | -108 | -117 | Strong path, but not a premium entry at price |

### Market interpretation

The market reacted correctly to the 8-point Houston mini-recovery from the official 63-39 checkpoint to 67-47. The Lakers margin compressed from +24 to +20, while the total climbed to 176.5. Houston still needed 55+ more points to clear 101.5, which remains an extreme recovery requirement given the official-book creation profile: 26.9% FG, 20.0% 3PT, and only 7 assists through 3Q 06:02.

## Availability / Inactive Players

### Lakers

- Luka Doncic: OUT — left hamstring strain

### Rockets

- Steven Adams: OUT — left ankle surgery
- Kevin Durant: OUT — left ankle sprain
- Fred VanVleet: OUT — right knee ACL repair

## Team Stats Through 3Q 06:02

| Category | Lakers | Rockets |
|---|---:|---:|
| FG | 23-55 | 14-52 |
| FG% | 41.8% | 26.9% |
| 3PT | 8-17 | 3-15 |
| 3PT% | 47.1% | 20.0% |
| FT | 9-14 | 8-13 |
| FT% | 64.3% | 61.5% |
| Offensive Rebounds | 6 | 4 |
| Defensive Rebounds | 29 | 23 |
| Total Rebounds | 35 | 27 |
| Assists | 13 | 7 |
| Steals | 3 | 3 |
| Turnovers | 7 | 7 |
| Blocks | 8 | 7 |
| Points in Paint | 28 | 22 |
| 2nd Chance Points | 2 | 2 |
| Fast Break Points | 16 | 4 |

## Quarter Splits

### Q1

| Team | Points | FG | 3PT | Rebounds | Turnovers |
|---|---:|---:|---:|---:|---:|
| Lakers | 23 | 9-25 | 3-7 | 15 | 1 |
| Rockets | 18 | 7-19 | 2-7 | 12 | 4 |

Signal notes:

- Houston offense was competitive early but turnover-prone.
- Sengun had 5 rebounds in Q1.
- Ayton had 4 rebounds in Q1.
- Lakers led 23-18 after Q1.

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

### 3Q Through 06:02

| Team | Points | FG | 3PT | Rebounds | Turnovers |
|---|---:|---:|---:|---:|---:|
| Lakers | 14 | 5-10 | 2-4 | 7 | 2 |
| Rockets | 8 | 2-11 | 1-4 | 7 | 0 |

Signal notes:

- Houston cleaned up turnovers in early 3Q but the shot-making collapse continued.
- Rockets shot 18.2% from the field in the early 3Q window.
- Lakers extended the lead from +18 at halftime to +24 by 06:02.
- Rui Hachimura added two 3PM in the opening 3Q stretch.

## Player Notes Through 3Q 06:02

### Lakers

| Player | Min | Pts | Reb | Ast | FG | 3PT | +/- | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| LeBron James | 26:02 | 22 | 3 | 6 | 8-18 | 2-5 | +20 | Primary engine; controlled tempo and transition |
| Rui Hachimura | 23:26 | 16 | 6 | 1 | 6-10 | 4-5 | +14 | Spacing pop; 3Q separation shooting |
| Deandre Ayton | 21:59 | 4 | 11 | 1 | 1-5 | 0-0 | +6 | Rebound anchor; low scoring but glass control |
| Austin Reaves | 23:51 | 9 | 2 | 2 | 4-9 | 0-2 | +11 | Secondary guard support; 3 blocks |
| Marcus Smart | 23:11 | 0 | 5 | 1 | 0-4 | 0-2 | +19 | Defense/pressure without scoring |
| Luke Kennard | 14:05 | 3 | 3 | 1 | 1-4 | 1-1 | +20 | Bench spacing, positive swing |
| Jaxson Hayes | 7:59 | 2 | 3 | 1 | 0-0 | 0-0 | +18 | Backup energy big |
| Jake LaRavia | 9:17 | 7 | 2 | 0 | 3-5 | 1-2 | +12 | Bench scoring burst |

### Rockets

| Player | Min | Pts | Reb | Ast | FG | 3PT | +/- | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Tari Eason | 21:04 | 11 | 2 | 0 | 4-9 | 2-4 | -11 | Best perimeter scoring signal but foul-pressure context |
| Jabari Smith Jr. | 27:46 | 7 | 7 | 2 | 2-7 | 1-3 | -17 | Frontcourt minutes load, low efficiency |
| Alperen Sengun | 27:29 | 10 | 10 | 1 | 3-10 | 0-0 | -24 | Hub stress; strong boards but poor scoring efficiency |
| Reed Sheppard | 23:15 | 5 | 0 | 1 | 2-12 | 0-6 | -16 | Severe shot creation inefficiency |
| Amen Thompson | 28:38 | 6 | 5 | 3 | 3-10 | 0-0 | -23 | Athletic pressure, low scoring conversion |
| Josh Okogie | 9:36 | 0 | 2 | 0 | 0-2 | 0-1 | -11 | Low offensive impact |
| Aaron Holiday | 6:43 | 0 | 1 | 0 | 0-0 | 0-0 | -8 | Low usage |
| Dorian Finney-Smith | 4:37 | 0 | 0 | 0 | 0-1 | 0-0 | -8 | Minimal impact |
| Jae'Sean Tate | 0:42 | 0 | 0 | 0 | 0-1 | 0-1 | -2 | Garbage/rotation probe |

## LiveFlow Model Signals

### Lakers Positive Signals

- `LEBRON_ENGINE_ACTIVE`
- `LA_TRANSITION_ADVANTAGE_ACTIVE`
- `HOU_TURNOVER_PRESSURE_EXPLOIT`
- `AYTON_REBOUND_ANCHOR_ACTIVE`
- `RUI_SPACING_POP_ACTIVE`
- `BENCH_PLUS_SWING_KENNARD_HAYES_LARAVIA`

### Rockets Negative Signals

- `HOU_PRIMARY_CREATION_DEPLETED`
- `DURANT_OUT_CREATION_LOSS`
- `VANVLEET_OUT_HANDLER_LOSS`
- `ADAMS_OUT_GLASS_PHYSICALITY_LOSS`
- `HOU_Q2_COLLAPSE_SIGNAL`
- `HOU_3Q_SHOT_QUALITY_FAILURE_CONTINUES`
- `HOU_3PT_FAILURE_ACTIVE`
- `SENGUN_USAGE_WITH_LOW_EFFICIENCY`
- `REED_SHEPPARD_CREATION_INEFFICIENCY`
- `LIVE_BALL_TURNOVER_DRAG`

## Key LiveFlow Interpretation

The updated 3Q checkpoint confirms the first-half read. Houston cleaned up turnovers after halftime, but the offensive problem did not correct because the shot profile and creation tree were still broken.

1. Houston's creation tree remained stripped by Durant and VanVleet being out.
2. Sengun reached 10 rebounds by 3Q 06:02, but his hub efficiency remained poor at 3-10 FG.
3. Reed Sheppard reached 2-12 FG and 0-6 from three, keeping Houston's guard-creation profile suppressed.
4. Amen Thompson supplied pressure and athleticism, but only 6 points on 3-10 FG kept the scoring ceiling low.
5. Lakers controlled defensive glass and transition flow with a 35-27 rebounding edge and 16-4 fast-break edge.
6. Rui's 4-of-5 3PT shooting gave Los Angeles the spacing pop that Houston lacked.

## Betting/Model Relevance

### For Live Totals

- Houston live over remains blocked unless there is a clear 3Q/4Q shooting spike.
- Houston team total under remains structurally supported by 26.9% FG and 20.0% 3PT through 3Q 06:02.
- Full-game under risk depends on garbage-time pace and free throws; base scoring environment remains under-friendly.

### For Rebounds

- Ayton 11 rebounds by 3Q 06:02 = strong continuation, but blowout rest risk now rises.
- Sengun 10 rebounds by 3Q 06:02 = strong raw board profile, but same blowout/minute risk applies.
- Jabari 7 rebounds and Amen 5 rebounds are secondary board paths from miss-heavy environment.

### For Spread / Side

- Lakers +24 is structurally supported by Houston offensive depletion, not fluky single-shot variance.
- Houston comeback path requires immediate three-point correction plus Lakers bench/carelessness.

## Updated Summary Tag

```yaml
liveflow_ingestion:
  game: LAL_HOU_2026_05_01
  segment: live_market_checkpoint_LAL_67_HOU_47
  score: LAL_67_HOU_47
  primary_signal: HOU_CREATION_TREE_COLLAPSE_CONFIRMED_WITH_MARKET_REPRICE
  live_lines:
    lakers_spread_16_5_yes: +113
    full_game_total_176_5_over: -112
    houston_tt_101_5_over: +943
    lakers_tt_97_5_over: -108
  lakers_edge:
    - transition
    - defensive_pressure
    - rebounding
    - LeBron_engine
    - Rui_spacing_pop
  rockets_failure:
    - depleted_creation
    - poor_3pt_shooting
    - poor_field_goal_efficiency
    - low_assist_generation
    - Sengun_hub_stress
    - Sheppard_creation_inefficiency
  model_tags:
    - LIVEFLOW_INGESTED
    - LIVE_MARKET_CHECKPOINT
    - HOU_CREATION_DEPLETION_ACTIVE
    - HOU_TEAM_TOTAL_OVER_BLOCKED
    - LAL_SPREAD_LEAN_WITH_BENCH_RISK
    - AYTON_REBOUND_ANCHOR
    - SENGUN_HUB_STRESS_TEST
```
