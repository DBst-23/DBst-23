# POSTMORTEM_2026_03_19_ORL_CHA_LIVEFLOW_BANE_DIABATE_LOSS

- Date: 2026-03-19
- Sport: NBA
- Mode: LiveFlow
- Platform: Underdog
- Matchup: ORL @ CHA
- Result: LOSS
- Stake: $10.00
- Payout: $0.00
- Profit: -$10.00
- Card Type: Champions 2-pick

## Locked card
- Moussa Diabate Lower 6.5 Rebounds
- Desmond Bane Higher 7.5 Rebounds

## Final results
- Moussa Diabate: 5 rebounds — WIN
- Desmond Bane: 7 rebounds — LOSS

## Final score
- Magic 111
- Hornets 130

## Team rebound environment
- ORL rebounds: 31
- CHA rebounds: 41
- ORL offensive rebounds: 12
- CHA offensive rebounds: 10
- ORL second chance points: 18
- CHA second chance points: 17

## SharpEdge Postmortem
### Phase 1 — Game Flow Analysis
At halftime the read correctly identified Diabate as a distributed-glass under because Charlotte was sharing rebound volume across multiple players and shooting efficiently. That leg held. The miss came from Bane over 7.5, who closed with 7 after having 6 at halftime. Orlando never established the stable second-half rebound environment needed for the over, and game flow drifted away from the original chase script.

### Phase 2 — Pivotal Moments
- Diabate finished with only 5 rebounds in 24 minutes, validating the under.
- Bane stopped at 7 rebounds after starting with 6 at halftime.
- Orlando finished with only 31 team rebounds, which was too weak an environment to support a guard/wing over needing two more boards in the second half.
- Charlotte scored 130 and hit 22 threes, which changed possession quality and limited clean defensive board accumulation for Orlando wings.

### Phase 3 — Defensive / Psychological Variables
- Diabate remained a non-dominant rebound distributor in a shared Charlotte frontcourt ecosystem.
- Bane's first-half pace looked live, but his role was still secondary relative to Orlando's big and team rebound ceiling.
- Charlotte's hot shooting and offensive balance reduced the exact type of miss-volume Orlando needed for Bane to clear.

### Phase 4 — Model Relevance Summary
#### What worked
- The Diabate under was structurally correct.
- Shared-glass under logic held in a Charlotte environment with multiple rebound contributors.

#### What failed
- Bane over was over-promoted off halftime count rather than rebound-role strength.
- The live read leaned too hard on trailing-script rebound chase and not enough on team rebound ceiling.
- Orlando's final 31 rebounds exposed the danger of forcing non-anchor overs even when they look close at halftime.

## Tags
- LIVEFLOW_LOSS
- SPLIT_CARD_LOSS
- ONE_OF_TWO_HIT
- HALFTIME_COUNT_TRAP
- NON_ANCHOR_OVER_FAIL
- SHARED_GLASS_UNDER_WIN
- EDGE_CALL_ACTIVE
- MISS_REGISTERED

## Lessons
- Do not promote a non-anchor rebound over just because it is one or two boards away at halftime.
- Require stronger rebound-role confirmation before backing a wing/guard over in LiveFlow.
- Continue favoring distributed-glass unders when rebound share is spread across multiple players.
