# SharpEdge NBA LIVE-FLOW — GHOST #003 final postmortem
**Game:** Memphis Grizzlies at Golden State Warriors | **Date:** 2026-10-23 | **Status:** FINAL / PAPER-ONLY | **Venue:** Chase Center

## Audit trail and sources
- Frozen pre-market model: MEM second half mean ~54, GSW ~59; exploratory 100,000 normal correlated draws (seed 20261023), **not calibrated**.
- Source of William Hill odds: user screenshot, previously locked in `2026-10-23_MEM_AT_GSW_halftime_market_snapshot_01.md`; no live odds API. No real wager verified.
- Official scorer's report supplied by user, final MEM 111, GSW 108.
- Critical discrepancy: frozen official halftime was MEM 60 GSW 56 (116); market screen showed MEM 62 GSW 56 (118). Final official scoring corroborates halftime **60-56**, since actual second half was MEM 51, GSW 52. Do not silently erase screenshot mismatch. Market at screen time was treated as its own timestamp; betting lines were evaluated against settled final score. Correct comparison uses original frozen state for accuracy, and market-adjusted scenario solely for the market snapshot.

## Actual quarter scores
| Quarter | MEM | GSW | Total |
|---|---:|---:|---:|
| Q1 | 33 | 34 | 67 |
| Q2 | 27 | 22 | 49 |
| Halftime | 60 | 56 | 116 |
| Q3 | 24 | 34 | 58 |
| Q4 | 27 | 18 | 45 |
| 2H | 51 | 52 | 103 |
| Final | 111 | 108 | 219 |

## Forecast errors
| Quantity | Frozen forecast official-score anchored | Market-adjusted scenario | Actual | Error (scenario minus actual) |
|---|---:|---:|---:|---:|
| MEM 2H | ~54 | ~54 | 51 | +3 |
| GSW 2H | ~59 | ~59 | 52 | +7 |
| 2H total | ~113 | ~113 | 103 | +10 |
| MEM final | ~114 | 116.03 | 111 | +5.03 adjusted (+3 frozen) |
| GSW final | ~115 | 114.95 | 108 | +6.95 adjusted (+7 frozen) |
| Game final total | ~229 | 230.98 | 219 | +11.98 adjusted (+10 frozen) |
| GSW second-half advantage | ~+5 | ~+4.92 | +1 | +3.92 |
| Final winner | GSW by ~1 in original forecast | MEM by ~1.08 adjusted | MEM by 3 | wrong winner original, right winner adjusted |

**Important:** The adjusted scenario is not a valid independently timed prediction of what the actual half score was; it uses a 2-point screenshot discrepancy which proved not to match official half. Do not credit adjusted final winner as a correctly forecast winner without caveat.

## William Hill screenshot grading — hypothetical $100 staked per independent side
| Side (full-game) | Screen price | Actual | Outcome | Net per $100 hypothetical stake |
|---|---|---|---|---:|
| MEM +2 | -115 | MEM won by 3 | WIN | +$86.96 |
| GSW -2 | -115 | GSW lost by 3 | LOSS | -$100.00 |
| MEM ML | +100 | MEM won | WIN | +$100.00 |
| GSW ML | -130 | GSW lost | LOSS | -$100.00 |
| O 231.5 | -115 | 219 | LOSS | -$100.00 |
| U 231.5 | -115 | 219 | WIN | +$86.96 |
| GSW TT O 116.5 | -110 | 108 | LOSS | -$100.00 |
| GSW TT U 116.5 | -120 | 108 | WIN | +$83.33 |
| MEM TT O 115.5 | -115 | 111 | LOSS | -$100.00 |
| MEM TT U 115.5 | -115 | 111 | WIN | +$86.96 |

The 'book' isn't a directional forecast for totals; the quoted full game total 231.5 missed actual by 12.5 (high). At the team lines, GSW market 116.5 missed high by 8.5, MEM 115.5 missed high by 4.5. Book GSW -2 corresponds to expected GSW win by 2; actual MEM won 3 (margin miss 5 toward GSW).
- **Pre-registered research signal:** MEM +2 -115: hypothetical paper WIN, predicted P(win)=57.82%, P(push)=2.964%, predicted hypothetical EV +11.06% at screenshot. This is **one outcome**, not proof of positive expectation.
- **GSW TT U116.5 -120:** also paper WIN; earlier explicitly classified thin/unreliable +2.65% nominal return, NOT primary play.
- **Totals:** U231.5 wins ex post despite PRE-GAME/AT-SNAPSHOT model *not* establishing EV for the Under (model 51.33% vs 53.49% break-even). DO NOT mark as a model edge or chosen play.
- No actual bets, stakes, prices filled, realized ROI or bankroll change established.

## Diagnostic: why total was too high
1. First half 116, actual second half **103**, model second-half 113 (+10 miss); book full total 231.5 implied ~115.5 from official half (or 113.5 from discrepant screen). Second-half underperformance was consequential.
2. GSW had a **34-point Q3**, a rebound from its 22-point Q2, but only **18 points Q4**. Simple halftime shooting-regression heuristics missed the renewed late offensive stall. GSW Q4 FG 6/21=28.6%, 3PT 4/14=28.6%. Game flow nonstationary.
3. Memphis Q4 scored 27 and outscored GSW 27-18; late comeback from down 106-94 with 3:47 remaining, tying 106-106 at :54.7 and taking lead 108-106 at :20.1.
4. Warriors had 19 turnovers, Memphis 27; these differ from naive clean-possession conditions. Turnover timing and late shot volume should be explicitly tracked rather than treating 2H as a stable normal.
5. Grizzlies fouls entering halftime (GG Jackson four, Jaylen Wells four, Isaiah Stewart four) did not force a collapse; minutes and substitutions are crucial.

## Calibration and next method revision
- Keep frozen forecasts immutable. Separate score-state-vetted input, bookmaker screenshot clock-state, and final official.
- Reject / flag market snapshot when model's score differs from official/market by >=2 before calling EV 'actionable'.
- Explicit two-stage second-half distribution: Q3 and Q4 with shared latent pace and shooting, late-game lineup/intent branch and foul/turnover regime.
- Track market line error (total 12.5 too high) and model MAE (frozen ~10 points total error) separately. Accuracy does not equal value after vig.
- Maintain paper-only until a meaningful out-of-sample backtest and calibration audit.
- Outcome label: **GHOST #003 MEM +2: hypothetical WIN; model total forecast high; under not a recommended edge.** 
