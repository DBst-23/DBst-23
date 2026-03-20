# POSTMORTEM_2026_03_19_TRI_CARD_WEMBY_MOBLEY_PORTIS_LOSS

- Date: 2026-03-19
- Sport: NBA
- Mode: Pregame
- Platform: Underdog
- Card Type: Champions 3-pick (50% boost)
- Result: LOSS
- Stake: $10.00
- Payout: $0.00
- Profit: -$10.00
- Matchups:
  - PHX @ SAS
  - CLE @ CHI
  - MIL @ UTA

## Locked card
- Victor Wembanyama Higher 11.5 Rebounds
- Evan Mobley Higher 10.5 Rebounds
- Bobby Portis Higher 6.5 Rebounds

## Final leg results
- Victor Wembanyama: 12 rebounds — WIN
- Evan Mobley: 13 rebounds — WIN
- Bobby Portis: 6 rebounds — LOSS by 0.5

## Final scores
- Suns 100, Spurs 101
- Cavaliers 115, Bulls 110
- Bucks 96, Jazz 128

## Team rebound environment
### PHX @ SAS
- PHX rebounds: 47
- SAS rebounds: 42
- PHX offensive rebounds: 10
- SAS offensive rebounds: 9

### CLE @ CHI
- CLE rebounds: 54
- CHI rebounds: 47
- CLE offensive rebounds: 16
- CHI offensive rebounds: 12

### MIL @ UTA
- MIL rebounds: 35
- UTA rebounds: 47
- MIL offensive rebounds: 8
- UTA offensive rebounds: 12

## Postmortem notes
Two legs were correctly identified as anchor-big overs. Wembanyama cleared with 12 and Mobley cleared with 13, confirming both the pregame rebound-chance read and the role-based concentration thesis. The miss came from Bobby Portis, who finished with 6 rebounds in 24 minutes and missed by half a board.

The loss mechanism was environment failure in MIL @ UTA. Milwaukee lost the game by 32, was beaten 47-35 on the glass, and never established interior control. Portis did not lose because the line was wildly wrong; he lost because the game state collapsed his rebound pathway. Utah generated stronger pace, stronger transition pressure, and superior possession control, while Milwaukee's frontcourt minutes and rebound distribution flattened across Kuzma, Turner, Sims, AJ Green, and others.

This is a strong example of why the system should continue treating Portis-style mid-tier rebound overs differently from true anchor-big overs. Mobley and Wembanyama were protected-anchor profiles. Portis was a conditional environment-dependent over that required cleaner frontcourt control than Milwaukee actually delivered.

## SharpEdge format analysis
### Phase 1 — Game Flow Analysis
- Wembanyama and Mobley both validated the core thesis: strong interior role plus healthy rebound-chance profile converted into wins.
- Milwaukee never controlled the game flow against Utah. The Bucks trailed badly, lost the glass, and produced only 35 team rebounds.
- Utah's 128-96 win created a hostile environment for a Portis over despite the ladder down from 7.5 to 6.5.

### Phase 2 — Pivotal Moments
- Wembanyama finished with 12 in a close 101-100 game, clearing by 0.5.
- Mobley finished with 13 in a Cleveland-controlled glass environment, clearing by 2.5.
- Portis played 24 minutes and stopped at 6 rebounds, missing by the hook.
- Utah's frontcourt and rebounding pressure suppressed Milwaukee's second-chance ecosystem all night.

### Phase 3 — Defensive / Psychological Variables
- Wembanyama: protected anchor big, clean central rebounding role, minimal cannibalization.
- Mobley: protected anchor big with Jarrett Allen out, elite structural upgrade confirmed.
- Portis: non-anchor conditional over, vulnerable to game-state collapse and rebound-share flattening.

### Phase 4 — Model Relevance Summary
#### What worked
- Protected-anchor-big logic worked exactly as intended.
- Rebound tracking support on Mobley and Wembanyama translated directly to winning outcomes.
- Laddering Portis down reduced the loss severity from a full rebound gap to a hook miss.

#### What failed
- Milwaukee environment quality was overestimated.
- Portis required more stable frontcourt control than the Bucks provided.
- The card combined two high-quality anchors with one weaker environment-sensitive leg, which reduced overall card durability.

## Tags
- PREGAME_LOSS
- TWO_OF_THREE_HIT
- HOOK_BURN
- ANCHOR_BIG_OVER_WIN
- CONDITIONAL_OVER_FAIL
- MIL_ENVIRONMENT_COLLAPSE
- EDGE_CALL_ACTIVE
- MISS_REGISTERED

## Lessons
- Keep anchor-big overs as core legs when rebound-chance profile and role concentration are both strong.
- Treat mid-tier overs like Portis as conditional add-ons, not equal-strength core legs.
- When a leg depends on a fragile team environment, prefer keeping it out of boosted 3-leg cards unless the team-control outlook is cleaner.
