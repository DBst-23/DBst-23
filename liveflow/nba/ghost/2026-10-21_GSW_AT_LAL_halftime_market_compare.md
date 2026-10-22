# GSW @ LAL — October 21 2026 — Halftime market comparison (ghost only)

## Integrity / source
- Linked frozen premarket forecast: `liveflow/nba/ghost/2026-10-21_GSW_AT_LAL_halftime_freeze.md` (commit b0e6dac910222722e9ca2e88a6615ce56749cd63).
- Score at screen: GSW 52, LAL 66. Halftime. Total 118.
- User-provided book screenshots: live **full-game** spread GSW +13.5 -110, LAL -13.5 -120; ML GSW +600, LAL -1000; **full-game** totals Over 236.5 -120 and Under 236.5 -110. Team **full-game** totals LAL O/U 124.5 -115/-115 and GSW O111.5 -125 / U111.5 -105.
- Screenshots show NO second-half-only spread/total, therefore do not label live full-game lines as 2H lines.

## Fixed assumptions for analytical replay
Independent from book: jointly normal GSW second-half points mean 56.0 sd 8.7; Lakers 58.5 sd 9.0; correlation 0.06; rounded integer outputs. RNG seed 20261021; n=100000. These parameters are speculative exploratory priors, not historically calibrated probabilities, and published decimals are not reliable betting edges.
Simulated score: 2H GSW mean 55.95463, LAL mean 58.50646; full total mean 232.46109, median 232.

| Market | Price | Sim p | Implied p | Apparent p difference | Modeled expected ROI | Ghost classification |
|---|---|---:|---:|---:|---:|---|
| GSW full game Under 111.5 | -105 | 65.91% | 51.22% | +14.69pp | +28.67% | GHOST_A watch highest apparent edge |
| Full game Under 236.5 | -110 | 62.30% | 52.38% | +9.92pp | +18.94% | GHOST_B watch |
| LAL full game -13.5 | -120 | 59.82% | 54.55% | +5.27pp | +9.67% | GHOST_C provisional |
| LAL Under 124.5 | -115 | 49.90% | 53.49% | -3.59pp | -6.71% | PASS |
| GSW full game +13.5 | -110 | 40.18% | 52.38% | -12.20pp | -23.29% | PASS |
| GSW ML | +600 | 8.12% | 14.29% | -6.17pp | -43.18% | PASS |
| LAL ML | -1000 | 90.62% | 90.91% | -0.29pp | -0.31% | PASS |

**Important thresholds**: GSW U111.5 requires 2H scoring <=59; game U236.5 requires 2H combined <=118; Lakers -13.5 needs win by 14+ (halftime margin 14 means second half tied or won by LAL).

## Model-risk policy
All rankings are PAPER/GHOST signals, NOT verified profit edges. A single unvalidated halftime model can be wrong; especially GSW team total under is sensitive to 3P shooting rebound and late garbage-time rotations. The overall under and GSW under are positively correlated, and should not be counted as independent wins. No money stakes.
Capture exact screenshot odds, no look-ahead, resolve all final markets once official final box arrives, calculate realized accuracy and Brier/log losses before promoting.
