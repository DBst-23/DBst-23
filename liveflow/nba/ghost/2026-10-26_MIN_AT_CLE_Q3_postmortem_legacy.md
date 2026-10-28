# SharpEdge LIVE-FLOW Postmortem — MIN @ CLE — 2026-10-26

Source: user-provided NBA official final scorer's report and contemporaneous William Hill screenshots. This is an observational postmortem, not a verified simulation run or proof of model calibration.

## Checkpoint: End Q3
Score MIN 86, CLE 86 (combined 172).
Previously recorded SharpEdge indicative projections: final total 228.0; CLE team total 114.5; MIN team total 113.5; CLE -1.0; CLE win probability 53%, MIN 47%. Estimated total median ~228 (normal approximation), not observed simulation output.
William Hill: game total 231.5 (Over -120, Under -110), CLE team total 116.5 (Over -120, Under -110), MIN team total 115.5 (Over -110, Under -120), CLE -2.5 (-105), MIN +2.5 (-125), CLE ML -140, MIN ML +110.

## Outcome and grading
End Q4 (regulation): 113–113, 226 points. Q4 27–27, total 54 points. OT 14–12 CLE. Final CLE 127–125 MIN, 252 points.
- Full game Under 231.5 -110: LOSS (OT included). Regulation-only total was 226 (under) but is NOT the settlement outcome.
- CLE Under 116.5 -110: LOSS (127 final; 113 regulation would be under).
- MIN Under 115.5 -120: LOSS (125 final; 113 regulation would be under).
- CLE -2.5 -105: LOSS (CLE won by 2); MIN +2.5 -125: WIN.
- CLE ML -140: WIN; MIN ML +110: LOSS.

## Error decomposition
- Q4 projection: total +56 versus actual +54 (2 points too high). Component final-total projection 228 versus regulation 226 (2 too high), versus official final 252 (24 too low due to OT).
- Team projected final 114.5 CLE/113.5 MIN versus regulation 113/113 (errors +1.5/+0.5). Versus official final 127/125 (errors -12.5/-11.5).
- Spread indicative CLE -1.0 versus final CLE -2 (actual -2); initial spread direction correct, market CLE -2.5 lost.
- Earlier postmortem probability/EV estimates were uncalibrated normal approximations, not validated Monte Carlo outputs. No claim of realized bet or verified EV.

## Failure modes / corrective action
1. Overtime settlement risk: full-game markets typically include OT. Add tie-at-end-regulation probability, explicit OT point distribution, and correlations to every final-total/team-total simulation.
2. Separately publish expected regulation and official full-game means/medians, and probability of OT; model not yet calibrated.
3. Q3 Under screen was directionally accurate for regulation, but not for official settlement. Never label regulation-only model discrepancy a confirmed edge.
4. Scoreline 86-86 after three quarters amplified extra-time risk. Need tie-state OT gate before betting unders.
5. Preserve snapshot timestamp, quoted price, implied probability, estimated edge, simulations count, and whether any bet was actually placed.

Status: Postmortem complete. Next workflow: GSW @ DEN halftime, model-first projection before book comparison.
