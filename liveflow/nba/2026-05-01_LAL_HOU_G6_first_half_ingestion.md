# NBA LiveFlow Ingestion — LAL @ HOU — 2026-05-01

## Metadata

- Game: Los Angeles Lakers @ Houston Rockets
- Date: 2026-05-01
- Venue: Toyota Center, Houston, TX
- Source: NBA Official Scorer's Report / Official Play-by-Play + Kalshi live market screenshots
- Segment ingested: 1st Quarter through 3rd Quarter 03:37, plus live market checkpoints at LAL 67 - HOU 47 and LAL 71 - HOU 53
- Officials: Scott Foster, Curtis Blair, Karl Lane, Kevin Cutler
- Mode: LIVE-FLOW ingestion / model training / postgame validation

## Current Score State — 3Q 03:37 Official Book

| Team | Q1 | Q2 | 3Q to 03:37 | Total |
|---|---:|---:|---:|---:|
| Lakers | 23 | 26 | 18 | 67 |
| Rockets | 18 | 13 | 16 | 47 |

- Current margin: Lakers +20
- Current total: 114
- Biggest Lakers lead: 25
- Attendance: 18,055 sellout

## Official Book Team Stats Through 3Q 03:37

| Category | Lakers | Rockets |
|---|---:|---:|
| FG | 24-58 | 15-54 |
| FG% | 41.4% | 27.8% |
| 3PT | 8-18 | 3-16 |
| 3PT% | 44.4% | 18.8% |
| FT | 11-18 | 14-20 |
| FT% | 61.1% | 70.0% |
| Offensive Rebounds | 6 | 5 |
| Defensive Rebounds | 29 | 25 |
| Total Rebounds | 35 | 30 |
| Assists | 13 | 8 |
| Steals | 3 | 3 |
| Turnovers | 7 | 7 |
| Blocks | 8 | 7 |
| Points in Paint | 30 | 24 |
| 2nd Chance Points | 2 | 3 |
| Fast Break Points | 16 | 4 |

## Availability / Inactive Players

### Lakers

- Luka Doncic: OUT — left hamstring strain

### Rockets

- Steven Adams: OUT — left ankle surgery
- Kevin Durant: OUT — left ankle sprain
- Fred VanVleet: OUT — right knee ACL repair

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

### 3Q Through 03:37

| Team | Points | FG | 3PT | Rebounds | Turnovers |
|---|---:|---:|---:|---:|---:|
| Lakers | 18 | 6-13 | 2-5 | 7 | 2 |
| Rockets | 16 | 3-13 | 1-5 | 10 | 0 |

Signal notes:

- Houston cleaned up turnovers in 3Q but the shot-making collapse remained severe.
- Houston's scoring recovery came mostly through free throws rather than stable shot creation.
- Lakers extended to a 25-point lead at 63-38/65-40 range, then Houston trimmed to 20.
- Rui Hachimura added two 3PM in the 3Q separation stretch.

## Live Market Checkpoint 1 — User Screen

- Score shown: LAL 67 - HOU 47
- Margin: Lakers +20
- Current total: 114

| Market | Line | Yes | No | LiveFlow Read |
|---|---:|---:|---:|---|
| Lakers spread | LAL by over 16.5 | +113 | -143 | Lean yes, but volatility/bench risk present |
| Full-game total | Over 176.5 | -112 | -108 | No clean edge; total has repriced into fair zone |
| Houston team total | Over 101.5 | +943 | Bid | Avoid over; structural under remains |
| Lakers team total | Over 97.5 | -108 | -117 | Strong path, but not a premium entry at price |

## Live Market Checkpoint 2 — User Screen

- Score shown: LAL 71 - HOU 53
- Margin: Lakers +18
- Current total: 124

| Market | Line | Yes | No | LiveFlow Read |
|---|---:|---:|---:|---|
| Lakers spread | LAL by over 13.5 | -112 | -117 | Stronger cover path than -16.5, but price no longer plus-money |
| Full-game total | Over 176.5 | -112 | -112 | Still no clean edge; total pace requires 53+ more from 124 |
| Houston team total | Over 92.5 | +1462 | -2581 | Under is correct but unplayable price; over remains blocked |
| Lakers team total | Over 100.5 | +373 | -490 | Mathematically alive, but starter rest and tempo compression lower edge quality |

### Checkpoint 2 Interpretation

The market dropped the Lakers spread from -16.5 to -13.5 after Houston trimmed from a 20-point margin to 18. The better line is attractive structurally, but the edge is less clean because the price shifted to -112 and game state now carries more bench and possession-management risk.

Houston team total moved down aggressively to 92.5, but the no side is heavily taxed at -2581. That confirms the market has fully priced the Rockets' offensive collapse. No new fire on Houston over: needing 40 points from 53 in the remaining game state still demands an offensive surge that the underlying shot profile does not support.

## Player Notes Through Official 3Q 03:37

### Lakers

| Player | Min | Pts | Reb | Ast | FG | 3PT | +/- | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| LeBron James | 27:49 | 22 | 3 | 6 | 8-19 | 2-5 | +16 | Primary engine; controlled early separation |
| Rui Hachimura | 25:51 | 16 | 6 | 1 | 6-10 | 4-5 | +10 | Spacing pop; 3Q separation shooting |
| Deandre Ayton | 24:15 | 5 | 11 | 1 | 1-5 | 0-0 | +1 | Rebound anchor; low scoring but glass control |
| Austin Reaves | 25:38 | 11 | 2 | 2 | 5-11 | 0-3 | +7 | Secondary guard support; 3 blocks |
| Marcus Smart | 23:49 | 1 | 5 | 1 | 0-4 | 0-2 | +19 | Defense/pressure without scoring |
| Luke Kennard | 16:30 | 3 | 3 | 1 | 1-4 | 1-1 | +16 | Bench spacing, positive swing |
| Jaxson Hayes | 8:08 | 2 | 3 | 1 | 0-0 | 0-0 | +19 | Backup energy big |
| Jake LaRavia | 9:55 | 7 | 2 | 0 | 3-5 | 1-2 | +12 | Bench scoring burst |

### Rockets

| Player | Min | Pts | Reb | Ast | FG | 3PT | +/- | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Tari Eason | 23:29 | 12 | 3 | 0 | 4-9 | 2-4 | -7 | Best perimeter scoring signal but foul-pressure context |
| Jabari Smith Jr. | 30:11 | 7 | 8 | 2 | 2-8 | 1-4 | -13 | Frontcourt minutes load, low efficiency |
| Alperen Sengun | 27:38 | 10 | 10 | 1 | 3-10 | 0-0 | -25 | Hub stress; strong boards but poor scoring efficiency |
| Reed Sheppard | 23:24 | 5 | 0 | 1 | 2-12 | 0-6 | -17 | Severe shot creation inefficiency |
| Amen Thompson | 31:03 | 12 | 6 | 3 | 4-11 | 0-0 | -19 | Athletic pressure; scoring came from FTs/paint rather than spacing |
| Josh Okogie | 9:36 | 0 | 2 | 0 | 0-2 | 0-1 | -11 | Low offensive impact |
| Aaron Holiday | 8:59 | 0 | 1 | 1 | 0-0 | 0-0 | -3 | Low usage |
| Dorian Finney-Smith | 4:37 | 0 | 0 | 0 | 0-1 | 0-0 | -8 | Minimal impact |
| Jae'Sean Tate | 2:58 | 1 | 0 | 0 | 0-1 | 0-1 | +3 | Emergency/rotation probe |

## LiveFlow Model Signals

### Lakers Positive Signals

- `LEBRON_ENGINE_ACTIVE`
- `LA_TRANSITION_ADVANTAGE_ACTIVE`
- `HOU_TURNOVER_PRESSURE_EXPLOIT`
- `AYTON_REBOUND_ANCHOR_ACTIVE`
- `RUI_SPACING_POP_ACTIVE`
- `BENCH_PLUS_SWING_KENNARD_HAYES_LARAVIA`
- `LAL_SPREAD_CONTROL_ACTIVE`

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
- `HOU_TEAM_TOTAL_OVER_BLOCKED`

## Key LiveFlow Interpretation

The updated official book and 71-53 market checkpoint confirm the first-half read. Houston cleaned up turnovers after halftime, but the offensive problem did not correct because the shot profile and creation tree remain broken.

1. Houston's creation tree remained stripped by Durant and VanVleet being out.
2. Sengun reached 10 rebounds, but his hub efficiency remained poor at 3-10 FG.
3. Reed Sheppard remained 2-12 FG and 0-6 from three, keeping Houston's guard-creation profile suppressed.
4. Amen Thompson improved to 12 points, but this was not a stable spacing signal.
5. Lakers controlled the defensive glass and transition flow with a 35-30 rebounding edge and 16-4 fast-break edge.
6. Rui's 4-of-5 3PT shooting gave Los Angeles the spacing pop that Houston lacked.
7. Houston's market-implied team total suppression is now fully priced; the edge shifted away from new under entries and toward disciplined hold/pass.

## Betting/Model Relevance

### For Live Totals

- Houston live over remains blocked unless there is a clear 4Q shooting spike.
- Houston team total under remains structurally supported, but the price is now too expensive.
- Full-game total over remains unattractive at 176.5 because the market is pricing the late free-throw/gargage-time path.

### For Rebounds

- Ayton 11 rebounds by 3Q 03:37 = strong continuation, but blowout rest risk rises.
- Sengun 10 rebounds by 3Q 03:37 = strong raw board profile, but same blowout/minute risk applies.
- Jabari 8 rebounds and Amen 6 rebounds are secondary board paths from miss-heavy environment.

### For Spread / Side

- Lakers +18 remains structurally supported by Houston offensive depletion, not fluky single-shot variance.
- Lakers -13.5 is the cleanest side number shown, but no longer premium due to -112 price and bench risk.
- Houston comeback path requires immediate three-point correction plus Lakers bench/carelessness.

## Updated Summary Tag

```yaml
liveflow_ingestion:
  game: LAL_HOU_2026_05_01
  segment: live_market_checkpoint_LAL_71_HOU_53
  score: LAL_71_HOU_53
  primary_signal: HOU_CREATION_TREE_COLLAPSE_CONFIRMED_WITH_MARKET_REPRICE
  live_lines:
    lakers_spread_13_5_yes: -112
    full_game_total_176_5_over: -112
    houston_tt_92_5_over: +1462
    lakers_tt_100_5_over: +373
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
    - MARKET_FULLY_REPRICED_HOU_UNDER
```
