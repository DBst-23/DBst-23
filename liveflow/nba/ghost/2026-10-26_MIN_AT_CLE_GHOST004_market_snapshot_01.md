# SharpEdge GHOST #004 — Market screenshot snapshot 01 (append-only)
Game: MIN at CLE, 2026-10-26; status paper-only. Independent model remains frozen in 2026-10-26_MIN_AT_CLE_GHOST004_premarket_frozen.md.
## Evidence and platform
User screenshot labeled HALFTIME, score MIN 60 CLE 50; EXACT score-state match with frozen model. Screenshot shows dollar volume and 1.38x/3.18x prices: looks like an exchange/prediction-style interface, not verified William Hill sportsbook. Record platform as **unverified screenshot**, not William Hill. Prices assumed to be total decimal payout multipliers, no extra fees or slippage. No wager confirmed.
Screenshot: MIN outright 1.38x, CLE outright 3.18x; MIN full-game team total Over 117.5 1.83x, Under 117.5 1.97x; CLE full-game TT Over 111.5 1.86x, Under 111.5 1.83x. The under price is shown red beside the green Over price; not independently validated other menus. Screenshot full-game market, not second-half team totals. No full-game spread/combined total displayed.
## Frozen-model calculation, no re-fit (N=200000, PCG64 seed 20261026)
Same quarter model and random draws as frozen document. Exact point-threshold simulated probabilities: MIN O117.5 33.963%, U117.5 66.037%; CLE O111.5 34.898%, U111.5 65.102%. Regulation MIN win 64.5055%, CLE win 33.0445%, tie 2.45%. Match payout EV arithmetic: p * multiplier - 1.
| Side | Screenshot multiple | Naive implied p | Model p | Model - implied (pp) | Nominal EV (per 1 staked) |
|---|---:|---:|---:|---:|---:|
| MIN TT Under 117.5 | 1.97x | 50.76% | 66.04% | +15.28 | +30.09% |
| CLE TT Under 111.5 | 1.83x | 54.64% | 65.10% | +10.46 | +19.14% |
| MIN TT Over 117.5 | 1.83x | 54.64% | 33.96% | -20.68 | -37.85% |
| CLE TT Over 111.5 | 1.86x | 53.76% | 34.90% | -18.87 | -35.09% |
| MIN outright | 1.38x | 72.46% | 64.51% regulation winner only | -7.96 pp before OT | NO VALID EV: OT unmodeled |
| CLE outright | 3.18x | 31.45% | 33.04% regulation winner only | +1.60 pp before OT | NO VALID EV: OT unmodeled |
Exact moneyline prices require overtime allocation of 2.45% ties, and possibly exchange settlement/fees; so do not characterize the outright spread as executable EV.
## Interpretation / safeguards
Largest paper-model side is MIN full-game TT Under 117.5 at 1.97x. But model was hand-set without out-of-sample reliability evidence; the large apparent advantage might be model misspecification, especially early-season priors, 2H pace/shot volume and late fouling. It is NOT a verified betting edge and is NOT an endorsed stake. CLE U111.5 likewise unverified. Do not call it William Hill market or claim the market price is a reliable consensus estimate. Screenshot can be stale.
Correlated game totals: both unders can win together; they should not be treated as independent risk.
Postmortem: official final, both team totals, model scoring error and paper settlement, calibration; do not rewrite forecast.
