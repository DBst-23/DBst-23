# NBA Pregame Position Locks — DET @ ORL — 2026-05-01

## Metadata

- Game: Detroit Pistons @ Orlando Magic
- Slate Game: 1
- Date: 2026-05-01
- Mode: Pregame conservative lock due to iOS copy/paste and screenshot issues
- Book/market: Kalshi
- Workflow state: manual hunt / pregame lock / LiveFlow attack window pending

## Market Board Context

### Game Lines

- DET spread: -4.5 (+113)
- DET moneyline: -161
- DET team total: 106.5, Over -117 / Under -108
- ORL spread: +4.5 (-137)
- ORL moneyline: +134
- ORL team total: 103.5, Over -112 / Under -108
- Full game total: 211.5, Over +105.5 / Under -126

## Expected Lineups / Availability

### Detroit

- PG Cade Cunningham
- SG Duncan Robinson
- SF Ausar Thompson
- PF Tobias Harris
- C Jalen Duren
- Kevin Huerter: OUT

Projected minutes:

- Cade Cunningham: 41
- Tobias Harris: 34
- Ausar Thompson: 33
- Jalen Duren: 32
- Duncan Robinson: 27

### Orlando

- PG Jalen Suggs
- SG Desmond Bane
- SF Jamal Cain
- PF Paolo Banchero
- C Wendell Carter
- Jonathan Isaac: OUT
- Franz Wagner: OUT

Projected minutes:

- Paolo Banchero: 38-40
- Jamal Cain: 26
- Desmond Bane: 34-37
- Jalen Suggs: 36-38
- Wendell Carter: 34
- Anthony Black: 33-38
- Da Silva: 16-20

## Profile Tags

### Detroit

- `DET_CADE_PNR_ENGINE`
- `CADE_41_MIN_ENGINE`
- `DUREN_32_MIN_GLASS_VALVE`
- `AUSAR_33_MIN_CHAOS_BOARD`
- `DUNCAN_SPACING_27_MINUTES`
- `HUERTER_OUT_SECONDARY_SPACING_DOWN`
- `DET_OREB_PRESSURE`

### Orlando

- `ORL_FRANZ_OUT_CREATION_DOWN`
- `ORL_ISAAC_OUT_DEFENSIVE_LENGTH_DOWN`
- `PAOLO_40_MIN_USAGE_SPIKE`
- `ORL_BLACK_SUGGS_DEFENSE_BACKCOURT`
- `ORL_SPACING_COMPRESSION_ACTIVE`
- `CARTER_34_MIN_REB_ANCHOR`

## Model Projections

### Game / Team Totals

| Market | Mean | Median | Probability | Edge Read |
|---|---:|---:|---:|---|
| ORL Team Total Under 103.5 | 101.7 | 102 | 56-58% | Best pregame lean |
| Full Game Under 211.5 | 208.5 | 209 | 54-56% | Correct direction, price heavy |
| DET -4.5 | DET +5.1 margin | DET +5 | 50-52% cover | Thin plus-money lean |
| DET Team Total Over 106.5 | 106.8 | 107 | 51-53% | Too thin |

### Rebound Markets

| Player | Line | Price | Mean | Median | Hit Probability | Edge Read |
|---|---:|---:|---:|---:|---:|---|
| Jalen Duren | 10+ | -121 | 10.4 | 10 | 55-57% | Safest but priced tight |
| Wendell Carter | 8+ | -121 | 7.8 | 8 | 51-53% | Too expensive |
| Paolo Banchero | 10+ | +158 | 8.7 | 8 | 34-38% | Thin ladder only |
| Tobias Harris | 7+ | +128 | 6.2 | 6 | 39-43% | Pass |
| Ausar Thompson | 8+ | +101 | 7.8 | 8 | 49-52% | Best plus-money profile |
| Cade Cunningham | 8+ | +252 | 6.1 | 6 | 24-29% | Longshot only |

## Position Locks

### Lock 1

- Market: Orlando team total under 103.5
- Entry: Under 103.5
- Price: -108
- Stake: $1.50
- Status: OPEN

Rationale:

- Franz Wagner OUT lowers Orlando wing creation.
- Jonathan Isaac OUT lowers defensive/rebound chaos but also removes size/energy support.
- Suggs/Black/Cain/Carter minutes compress spacing around Paolo.
- Paolo usage spike can become isolation-heavy against Detroit help.
- Detroit has Duren/Ausar/Tobias rebounding and size to slow second-chance scoring.

Projection:

- Mean: 101.7
- Median: 102
- Hit probability: 56-58%

### Lock 2

- Market: Ausar Thompson 8+ rebounds
- Entry: Yes, 8+ rebounds
- Price: +101
- Stake: $1.50
- Status: OPEN

Rationale:

- Ausar projected 33 minutes.
- Orlando's compressed spacing and Paolo/Bane usage create rebound opportunities.
- Ausar benefits from weak-side crash lanes when help rotates toward Cade/Duren actions.
- Detroit rolling profile already tags Ausar as a major chaos-board and stocks signal.

Projection:

- Mean: 7.8
- Median: 8
- Hit probability: 49-52%

## Risk Control

- Stake intentionally conservative due to iOS system glitches and reduced ability to copy/paste/screenshot.
- Do not over-stack pregame exposure.
- LIVE-FLOW window remains the primary attack zone.
- Re-check first quarter shot profile, ORL spacing, DET turnover pressure, and Ausar rebounding lane activity before adding anything live.

## LiveFlow Trigger Map

### Watch For ORL TT Under

- ORL below 25 in Q1 with poor halfcourt spacing.
- Paolo high-usage isolation without efficient rim/FT production.
- Suggs/Black/Cain lineups producing defensive stops but weak spacing.
- DET defensive rebounding limiting second chances.

### Watch For Ausar 8+ Rebounds

- Ausar 2+ rebounds by mid-Q1 or 3+ by Q1 close.
- Orlando miss volume high.
- Ausar staying above 16 minutes by halftime.
- Detroit using Ausar as weak-side help/crash wing.

### Avoid Early Live Adds If

- ORL shooting efficiency spikes from Bane/Suggs threes.
- Cade turnovers create ORL transition scoring.
- Ausar foul trouble appears early.
- Duren dominates all available rebound chances and squeezes Ausar share.

## Final Pregame Status

```yaml
pregame_locks:
  - ORL_TT_UNDER_103_5:
      stake: 1.50
      price: -108
      status: OPEN
  - AUSAR_THOMPSON_8_PLUS_REB:
      stake: 1.50
      price: +101
      status: OPEN
risk_mode: CONSERVATIVE_PREGAME
next_mode: LIVEFLOW_ATTACK_WINDOW
```
