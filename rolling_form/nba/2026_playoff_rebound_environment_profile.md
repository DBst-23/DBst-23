# 2026 NBA Playoff Rebound Environment Profile Chart

Updated: 2026-05-01

Purpose: maintain a corrected SharpEdge playoff rebound/spacing profile using confirmed 2025-26 playoff rosters, official gamebooks, rolling postmortems, and current injury/series context.

## Correction Log vs NBA Beta Draft

```yaml
corrections:
  BOS:
    remove:
      - Kristaps Porzingis
      - Jrue Holiday
    active_core:
      - Jayson Tatum
      - Jaylen Brown
      - Derrick White
      - Sam Hauser
      - Neemias Queta
      - Payton Pritchard
      - Nikola Vucevic
  ATL:
    note:
      - Kristaps Porzingis belongs to ATL roster context, not BOS.
  HOU:
    remove_from_current_playoff_core:
      - Jalen Green
      - Dillon Brooks
    active_core:
      - Alperen Sengun
      - Amen Thompson
      - Jabari Smith Jr.
      - Tari Eason
      - Reed Sheppard
      - Steven Adams
      - Clint Capela
    injury_note:
      - Kevin Durant ruled out for Game 6 vs LAL with left ankle injury.
  MIN:
    correct_context:
      - Anthony Edwards out
      - Donte DiVincenzo out
      - Ayo Dosunmu out
      - Kyle Anderson out/illness in Game 6
      - Terrence Shannon Jr. elevated into start
  DEN:
    correct_context:
      - Aaron Gordon out Game 6
      - Peyton Watson out Game 6
  OKC:
    remove:
      - Josh Giddey
    active_core:
      - Shai Gilgeous-Alexander
      - Jalen Williams
      - Chet Holmgren
      - Isaiah Hartenstein
      - Luguentz Dort
      - Cason Wallace
      - Alex Caruso
```

## Eastern Conference Profiles

| Team | Series State | Spacing / Positioning | Rebound Funnel Effect | Primary Beneficiaries | Model Tags |
|---|---|---|---|---|---|
| DET | vs ORL active | Cade Cunningham controls spread PnR. Duren anchors rim. Ausar/Tobias/Holland/Stewart roles create mixed spacing, not pure five-out. | Strong OREB valve through Duren and weak-side athlete crashes. Ausar has been a major playoff glass/stocks signal. | Duren -> Ausar Thompson -> Tobias Harris / Isaiah Stewart | `DET_OREB_PRESSURE`, `AUSAR_STOCKS_REB_SPIKE`, `DUREN_PRIMARY_VALVE` |
| ORL | vs DET active | Jumbo wing creation through Paolo and Franz with Desmond Bane/Jalen Suggs spacing. Carter/Bitadze/Isaac give size layers. | Physical defensive rebounding, but offensive spacing can compress when multiple bigs share floor. | Banchero -> Carter/Bitadze -> Franz/Isaac | `ORL_SIZE_REBOUND_WALL`, `PAOLO_USAGE_GLASS`, `SPACING_COMPRESSION_RISK` |
| NYK | advanced, beat ATL 4-2 | Brunson engine with KAT stretch/inside gravity, OG/Mikal wing spacing, Hart/Robinson crash layers. | KAT spacing pulls bigs out; Hart/OG/Mitch collect weak-side and chaos boards. | Towns -> Hart -> Anunoby -> Robinson | `NYK_WING_GLASS_SURGE`, `KAT_SPACING_FUNNEL`, `OG_TWO_WAY_REB_FORM` |
| BOS | vs PHI tied 3-3 | Tatum/Brown/White/Hauser perimeter structure with Queta/Vucevic center minutes. Less pure five-out than Beta draft stated. | Long-miss environment exists, but recent series issue is creation collapse, not rebound failure. | Tatum -> Brown -> Queta/Vucevic -> Pritchard long boards | `BOS_3Q_CREATION_COLLAPSE`, `BROWN_FOUL_TURNOVER_DRAG`, `TATUM_TREATMENT_VOL` |
| PHI | vs BOS tied 3-3 | Maxey speed PnR, Embiid short-roll/post hub, Paul George/Oubre/Edgecombe spacing and transition pressure. | Embiid anchors defensive boards. Edgecombe/Oubre attack long and transition boards. | Embiid -> Edgecombe -> Oubre -> George | `PHI_SURVIVAL_CORE_CONFIRMED`, `GEORGE_SPACING_RESURGENCE`, `EMBIID_HUB_REB` |
| CLE | vs TOR active | Mitchell-Harden spread PnR with Mobley/Allen dual-big pressure and shooters like Merrill/Tyson/Strus. | Allen/Mobley absorb paint boards; Tyson/Wade/Nance type wings become opportunistic. | Allen -> Mobley -> Tyson/Wade | `CLE_TWIN_BIG_PUTBACKS`, `MITCHELL_HARDEN_PULLUP_MISS_FUNNEL` |
| TOR | vs CLE active | Barnes/Ingram/RJ point-forward/wing creation, Poeltl interior, Murray-Boyles/Quickley/Walter/Shead context. | Barnes and Poeltl lead size-based rebound floor; Murray-Boyles can spike OREB in compact-floor games. | Barnes -> Poeltl -> Murray-Boyles -> Barrett | `TOR_COMPACT_SIZE_CRASH`, `BARNES_REB_ENGINE`, `MURRAY_BOYLES_OREB_SPIKE` |

## Western Conference Profiles

| Team | Series State | Spacing / Positioning | Rebound Funnel Effect | Primary Beneficiaries | Model Tags |
|---|---|---|---|---|---|
| MIN | advanced, beat DEN 4-2 | Injury-driven big lineup. With Edwards/DiVincenzo/Dosunmu out, Shannon Jr. started and McDaniels/Gobert/Randle/Reid size carried the offense. | Elite Game 6 glass/paint funnel: +17 rebounds, +13 OREB, +16 second-chance points. | Gobert -> McDaniels -> Reid -> Randle/Shannon | `MIN_BIG_LINEUP_COUNTEREDGE`, `MIN_REBOUND_ENVIRONMENT_DOMINANCE`, `MCDANIELS_TWO_WAY_BREAKOUT` |
| SAS | awaiting MIN | Wembanyama/Fox vertical-spread engine; Castle/Vassell/Keldon/Olynyk/Kornet depth provides varied spacing. | Wemby stretches coverage and still controls glass; Fox/Vassell can collect long boards and push. | Wembanyama -> Kornet/Olynyk -> Castle/Fox | `WEMBY_VERTICAL_SPACING`, `SAS_LONG_REB_TEMPO`, `FOX_EARLY_OFFENSE_BOARD_PUSH` |
| OKC | awaiting LAL/HOU | SGA/Jalen Williams/Chet five-out/drive economy with Hartenstein power-big option. No Giddey in current core. | OKC can trade OREB for transition defense, but Hartenstein/Chet lineups improve defensive clean-up. | Holmgren -> Hartenstein -> Jalen Williams/Dort | `OKC_GANG_REBOUND`, `CHET_DREB_FUNNEL`, `HARTENSTEIN_GLASS_STABILIZER` |
| LAL | leads HOU 3-2 | LeBron/AD core with Reaves/Russell/Reddish/Wood-type spacing if active. Must confirm game-day availability before slate lock. | AD remains primary board valve; LeBron creates secondary wing-board chances from post touches. | Davis -> LeBron -> Wood/Vanderbilt-type crashers | `LAL_AD_PRIMARY_GLASS`, `LEBRON_POST_REB_FUNNEL`, `LAL_ROLE_PLAYER_VERIFY` |
| HOU | trails LAL 2-3 | Durant unavailable for Game 6; active build shifts to Sengun/Amen/Jabari/Tari/Reed with Adams/Capela interior depth. | Without Durant, less pull-up gravity but more crash/paint pressure. Sengun and Eason are main funnel beneficiaries. | Sengun -> Eason -> Jabari -> Capela/Adams | `HOU_DURANT_OUT_RESHAPE`, `SENGUN_GLASS_HUB`, `EASON_ACTIVITY_SPIKE` |

## SharpEdge Rebound Environment Summary

| Team | Spacing Profile | Rebound Funnel | Primary Beneficiaries | Current Betting Use |
|---|---|---|---|---|
| DET | Organized Cade PnR, mixed 4-out | High OREB pressure | Duren / Ausar / Tobias | Rebound overs and DET second-chance/team total boosts |
| ORL | Jumbo wings, mixed shooting | Size wall, compressed paint | Paolo / Carter / Franz | Rebounds yes, overs need pace/efficiency check |
| NYK | Brunson + KAT gravity | Wing/chaos glass | KAT / Hart / OG / Mitch | Hart/OG/KAT rebound props; NYK TT if pace stable |
| BOS | Wing creation, center rotation | Long-miss boards but creation fragile | Tatum / Brown / Queta/Vucevic | Downgrade overs if Brown foul drag or 3Q stall appears |
| PHI | Maxey speed + Embiid hub | Embiid anchor, Oubre/Edgecombe long boards | Embiid / Edgecombe / Oubre | Survival-mode rebound/transition props |
| CLE | Mitchell-Harden PnR + twin bigs | Putback/twin tower | Allen / Mobley | Big rebound props and CLE interior scoring |
| TOR | Barnes/Ingram/RJ size creation | Compact crash | Barnes / Poeltl / Murray-Boyles | Barnes/Pöltl boards; watch Quickley/Ingram status |
| MIN | Big injury lineup | Elite OREB/paint | Gobert / McDaniels / Reid | Team total if OREB+paint live; Gobert/McDaniels boards |
| SAS | Wemby/Fox vertical-spread | Wemby + long-board guards | Wemby / Castle-Fox / support bigs | Wemby boards, SAS transition if misses go long |
| OKC | SGA/Chet 5-out plus Hartenstein option | Team gang boards | Chet / Hartenstein / Dort-JDub | Defensive reb props, transition-friendly game scripts |
| LAL | LeBron/AD pressure | AD primary glass | AD / LeBron | AD boards; Lakers size verification required |
| HOU | Durant-out crash profile | Sengun/Eason activity | Sengun / Eason / Jabari | HOU rebound overs if KD out and crash lineup active |

## Global Model Rules Added

```yaml
global_rules:
  - Do not trust AI-generated roster charts without roster validation.
  - Apply injury-state lineup overrides before rebound projections.
  - Rebound beneficiaries must be ordered by actual role, minute path, and game environment, not name value.
  - Team-total support must identify whether scoring comes from 3P efficiency, paint pressure, OREB, or FT closure.
  - Live rebound ladders require halftime rebound-share confirmation, not just individual early pace.
```
