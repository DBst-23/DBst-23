# Postmortem — MIN @ PHI — 2026-04-03

## Final Score
- Minnesota Timberwolves 103
- Philadelphia 76ers 115

## Invested / Tracked Plays
- Ayo Dosunmu — Higher 4.5 Rebounds ✅ (finished with 5)
- Naz Reid — Higher 5.5 Rebounds ✅ (finished with 7) [signal from related card/workflow]

## Additional Logged Card Context
- User-reported winning 3-leg card included:
  - Ayo Dosunmu Higher 4.5 Rebounds ✅
  - Paolo Banchero Lower 8.5 Rebounds ✅
  - Maxime Raynaud Higher 8.5 Rebounds ✅
- This postmortem focuses on the MIN @ PHI matchup and the rebound workflow tied to it.

## Key Outcome Notes
- Minnesota shot just 38-for-101 from the field (37.6%), creating a high raw rebound environment.
- Minnesota totaled 43 rebounds with 13 offensive rebounds.
- Philadelphia won the glass 53 to 43 overall.
- Rudy Gobert posted a massive 16 rebounds, absorbing a large share of center rebound volume.
- Naz Reid still cleared with 7 rebounds in 29 minutes off the bench.
- Ayo Dosunmu cleared the 4.5 line with 5 rebounds in 36 minutes.

## Why Ayo Dosunmu Over 4.5 Worked
- Stable wing minutes at 36.
- Rebound line remained modest relative to role and game environment.
- Minnesota’s poor shooting efficiency increased total rebound events.
- Ayo’s wing rebound role held despite Gobert’s dominant glass game.

## Why Naz Reid Over 5.5 Worked
- Bench minutes were strong at 29.
- Miss-heavy environment increased second-unit rebound opportunity.
- Naz maintained enough rebound share despite Gobert’s 16-board game.

## Matchup / Environment Takeaways
- Miss-heavy games can support multiple rebound overs simultaneously when role concentration is intact.
- Even with a dominant center rebounder present, secondary rebound overs can still hit if the game creates enough total rebound events.
- Blowout risk did not fully kill rebound overs here because core pieces still logged enough minutes before game separation finalized.

## Model Validation
### Hits
- Ayo Dosunmu Over 4.5 rebounds — validated
- Naz Reid Over 5.5 rebounds — validated

### Structural Notes
- The workflow correctly identified a favorable rebound environment.
- Wing rebound overs remain viable when the line is low and minutes are secure.
- Secondary big overs can still be playable in miss-heavy games if projected bench minutes are solid.

## Patch / Tracking Notes
- Tag: REBOUND_ENVIRONMENT_CONFIRMED
- Tag: LOW_LINE_WING_OVER_VALIDATED
- Tag: MISS_HEAVY_GAME_SUPPORTS_MULTI_OVERS
- Tag: GOBERT_ABSORPTION_DID_NOT_KILL_SECONDARY_OVERS

## Box Score Reference
### Timberwolves Starters
- Julius Randle: 7 rebounds
- Rudy Gobert: 16 rebounds
- Donte DiVincenzo: 0 rebounds
- Anthony Edwards: 2 rebounds
- Ayo Dosunmu: 5 rebounds

### Timberwolves Bench
- Bones Hyland: 5 rebounds
- Naz Reid: 7 rebounds
- Kyle Anderson: 1 rebound
- Terrence Shannon Jr.: 0 rebounds

### 76ers Starters
- Dominick Barlow: 10 rebounds
- Paul George: 6 rebounds
- Joel Embiid: 13 rebounds
- VJ Edgecombe: 2 rebounds
- Tyrese Maxey: 6 rebounds

### 76ers Bench
- Kelly Oubre Jr.: 5 rebounds
- Quentin Grimes: 4 rebounds
- Andre Drummond: 6 rebounds
- Adem Bona: 1 rebound
