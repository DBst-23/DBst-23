# SharpEdge GHOST #003 — William Hill market snapshot 01 (append-only)
Game MEM at GSW | 2026-10-23 | paper-only comparison | USER SCREENSHOT, NOT LIVE API.
## Timing / alignment
Independent model frozen earlier using MEM 60 GSW 56, halftime 116. New screenshot labeled Halftime displays MEM 62 GSW 56 (118 total), a +2 MEM difference. Could be feed lag, scoring correction, or another clock-state discrepancy. No official score correction independently validated. DO NOT conceal discrepancy or rewrite forecast. For this comparison only, condition original simulated second-half score distribution on displayed MEM=62, GSW=56, adding two to final MEM and total, same modeled second-half distributions.
## Market screenshot
Full-game spread MEM +2 -115, GSW -2 -115. ML MEM +100, GSW -130. Total 231.5 O -115 U -115. GSW final team total 116.5 O -110 U -120. MEM final team total 115.5 O -115 U -115. All are displayed full-game lines, not second-half standalone markets. Screenshot odds may change. No bets placed.
## Conditional exploratory distribution
100,000 draws of independent frozen prior scenario: MEM 2H=max(0,round(54+9.7*z1)), GSW 2H=max(0,round(59+10.3*z2)), joint normal correlation .12, seeded 20261023. In this re-generation: total mean 230.98; MEM mean 116.03, GSW mean 114.95, GSW margin -1.08. Changes due solely to displayed MEM first-half +2, NOT parameter refit.
| Market side | Simulated win P | Push P | Book break-even (no push) | Win P - naive BE | Expected net / unit staked including push |
|--|--:|--:|--:|--:|--:|
| U231.5 -115 | 51.33% | 0 | 53.49% | -2.16 pp | -4.03% |
| O231.5 -115 | 48.67% | 0 | 53.49% | -4.82 pp | -9.01% |
| GSW U116.5 -120 | 55.99% | 0 | 54.55% | +1.44 pp | +2.65% |
| GSW O116.5 -110 | 44.01% | 0 | 52.38% | -8.37 pp | -15.98% |
| MEM O115.5 -115 | 52.14% | 0 | 53.49% | -1.35 pp | -2.53% |
| MEM U115.5 -115 | 47.86% | 0 | 53.49% | -5.62 pp | -10.52% |
| MEM +2 -115 | 57.82% | 2.964% | 53.49% of resolved outcomes | n/a | +11.06% |
| GSW -2 -115 | 39.22% | 2.964% | 53.49% of resolved outcomes | n/a | -26.68% |
| MEM ML +100 | 51.87% regulation outright | 2.996% reg tie | 50% | n/a | NOT ESTIMATED: overtime unmodeled |
| GSW ML -130 | 45.13% regulation outright | 2.996% reg tie | 56.52% | n/a | NOT ESTIMATED: overtime unmodeled |
## Interpretation
Largest nominal ghost-paper discrepancy MEM +2 -115; NOT validated edge. Do NOT recommend wager on basis of uncalibrated normal assumptions. Full game total and Memphis TT not favorable in this model; GSW TT U is too thin for confidence. Strength of apparent MEM spread discrepancy sensitive to halftime source 2-point mismatch, marginal minutes/fouls, calibration. Freeze and postmortem after final, recording settled results and calibration loss.
