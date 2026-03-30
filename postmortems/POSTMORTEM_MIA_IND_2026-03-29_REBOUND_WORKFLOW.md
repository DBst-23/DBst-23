# Postmortem — MIA @ IND — 2026-03-29

## Final score
- Heat 118
- Pacers 135

## Rebound plays logged
- ✅ Pascal Siakam **Higher 6.5 rebounds** — finished with **11**
- ✅ Bam Adebayo **Higher 10.5 rebounds** — finished with **12**

## Result summary
- Card result: **2-0**
- Entry: **$5.00**
- Paid: **$17.91**
- Multiplier shown: **3.57x**

## Workflow context used
- Rebound environment scan
- ON/OFF lineup tool
- Confirmed lineup context
- Projected minutes input
- Anchor-style rebound selection from each team

## Pre-play rationale recap
### Pacers side — Pascal Siakam over 6.5
- Stable projected minutes
- Clean rebound lane versus Miami frontcourt allocation
- Strong enough line relative to role and matchup
- Cleared with room, finishing at 11

### Heat side — Bam Adebayo over 10.5
- Center rebound anchor role
- Competitive enough game environment for full workload
- Closed as the stronger Miami rebound pathway
- Cleared with room, finishing at 12

## Actual rebound outcomes
### Heat
- Bam Adebayo: 12
- Jaime Jaquez Jr.: 8
- Andrew Wiggins: 6
- Pelle Larsson: 5
- Tyler Herro: 3
- Davion Mitchell: 3
- Kel'el Ware: 3

### Pacers
- Pascal Siakam: 11
- Micah Potter: 5
- Jay Huff: 5
- Jalen Slawson: 4
- Kobe Brown: 4
- Andrew Nembhard: 3
- Quenton Jackson: 3

## Team rebound result
- Miami: 42
- Indiana: 42
- Offensive rebounds: Miami 10, Indiana 3
- Defensive rebounds: Miami 32, Indiana 39

## What the model got right
1. **Correct anchor identification**
   - The workflow successfully isolated the cleanest rebound alpha on both sides.
2. **ON/OFF tool translated well here**
   - This matchup behaved more cleanly than some of the prior noisier boards.
3. **Minutes + role stability mattered**
   - Both plays had enough floor time and role security to realize volume.
4. **Stable environment paid off**
   - This was a less noisy matchup and the result reflected that.

## Sharp notes
- Strong example of the rebound workflow functioning best in **stable role environments**.
- Supports continued use of the ON/OFF tool when combined with:
  - confirmed lineup integrity
  - projected minutes
  - role clarity
  - reasonable line tax

## Confidence ladder grading
- Pascal Siakam O6.5 REB — **Anchor**
- Bam Adebayo O10.5 REB — **Anchor**

## Tag summary
- `ON_OFF_TOOL_APPLIED`
- `PROJECTED_MINUTES_APPLIED`
- `CONFIRMED_LINEUP_APPLIED`
- `ANCHOR_HIT`
- `REBOUND_WORKFLOW_SUCCESS`
- `MIA_IND_0329`

## Overall postmortem verdict
**Success case.**
This matchup is a strong proof point that the ON/OFF rebound workflow adds value when the environment is stable and the role tree is clear. Both identified anchors cleared with room.
