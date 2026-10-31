# SharpEdge NBA LIVE-FLOW | LAL @ GSW | 2026-10-30

**Status:** FINAL / POSTMORTEM / NO CONFIRMED WAGER. **Venue:** Chase Center, San Francisco, CA. **Source:** user-supplied official NBA scorer's reports (quarter, half, final) and play-by-play; GitHub Q3-opening market record.

## Official score reconciliation

| Period | LAL | GSW | Total |
|---|---:|---:|---:|
| Q1 | 38 | 15 | 53 |
| Q2 | 15 | 38 | 53 |
| First half | 53 | 53 | 106 |
| Q3 | 27 | 32 | 59 |
| Q4 | 15 | 27 | 42 |
| Second half | 42 | 59 | 101 |
| **Final** | **95** | **112** | **207** |

No overtime; GSW final margin +17. Period and half sums reconcile.

## Model accuracy (previously recorded, provenance limited)

The existing immutable Q3-opening log (`liveflow/nba/ghost/2026-10-30_LAL_AT_GSW_Q3_OPEN_MARKET_ADJUSTMENT.json`) records a **frozen model** of LAL 108, GSW 110, full total 218, second-half total 112. It does **not** independently establish an original market-blind halftime freeze timestamp. This game's forecast must remain **excluded from authenticated MAE** pending provenance verification.

| Metric | Recorded forecast | Actual | Actual minus forecast |
|---|---:|---:|---:|
| LAL final | 108 | 95 | -13 |
| GSW final | 110 | 112 | +2 |
| Regulation total | 218 | 207 | -11 |
| Second-half total | 112 | 101 | -11 |
| GSW margin | +2 | +17 | +15 |

**Total absolute error: 11 points.** Directional calls (GSW win, lower total) were right, but neither precision nor EV was sufficient to retroactively establish a qualified bet.

## Historical market comparison — paper-only

- Prior halftime market: total 220.5, Under -105; final 207 (hypothetical Under wins by 13.5).
- **Q3 12:00 market, not a market-blind halftime freeze:** total 219.5, Under -115; final 207 (hypothetical Under wins by 12.5). Model/market gap 1.5 points.
- Q3 12:00 GSW +1.5 (-120) covered by 18.5 points against final GSW +17; LAL -1.5 (-110) lost.
- The contemporaneous assessment was **PASS**, because no validated probability distribution or demonstrated EV existed. **No wager or realized P&L confirmed.** Do not count hypothetical results as actual wins.

## Scoring mechanism

1. LAL scored only **42** after halftime, shooting **14/37 FG (37.8%)** and **3/16 3P (18.8%)**; fourth quarter just **15** points. The Lakers' 13-point negative team forecast residual explains more than the 11-point combined total error.
2. GSW made **10/23** second-half threes (43.5%) and **22/46** for the game (47.8%); Curry scored 31 with **8/14** threes. Golden State second-half turnovers: **2**, versus Lakers **9**.
3. Huge game-state reversal: LAL won Q1 **38–15**, GSW won Q2 **38–15**, then GSW won the second half **59–42**. Lakers' largest lead was 25; GSW won by 17, a 42-point swing.
4. Diagnostic tags: `SECOND_HALF_OFFENSIVE_COLLAPSE`, `ASYMMETRIC_THREE_POINT_PRODUCTION`, `EARLY_LEAD_REVERSAL`. These are retrospective descriptors, not pregame predictive features or a basis for fitting this result into the model.

## Data integrity

- Preserve the prior Q3 model/market file unchanged.
- Distinguish regulation total, second-half total, margin, and team-specific errors.
- No simulation distribution, mean/median estimate beyond recorded point forecast, win probability, EV, or Tier-1 edge validated from this record.
- Exclude from the nine authenticated numeric forecasts and existing MAE until an independently time-stamped original halftime freeze is verified.
