# SharpEdge LIVE-FLOW — Ghost Pick SOP v1.0

Effective: 2026-10-31 (next LIVE-FLOW session).
Purpose: prospectively paper-trade every qualifying live-flow strike before risking capital. Ghost picks are simulations of decisions, **not real wagers** and do not imply profitability.

## Required sequence
1. Capture game, date, teams, official score, clock, quarter, injuries, and timestamps. Verify score/time synchronization.
2. **Freeze model first**: projected second-half points by team, second-half total, final score/total, spread margin, assumptions and volatility tags. Mark uncalibrated forecasts as heuristic; do not invent Monte Carlo results.
3. Capture sportsbook **William Hill Nevada** exact market, line, price, timestamp and market type; optionally record sharp-book comparisons. Never use pregame odds as halftime odds.
4. Issue **one clearly labeled GHOST PICK** only when the model supports a meaningful discrepancy and the data is complete; otherwise issue **GHOST PASS** with reason. Record market side, line, price, model estimate, model-implied probability if calibrated, break-even probability, estimated EV if justified, and explicit confidence/uncertainty. Missing calibrated probability -> probability/EV null, not fabricated.
5. Lock the ghost pick **before** outcome or material market movement; append a separate immutable timestamped pick record to `liveflow/nba/ghost/picks/`. No retroactive picks. No cash stake, no actual wager, no bankroll debit.
6. After official final, add linked postmortem: settlement under recorded line and rules, closing line value when available, model errors, result, volatility notes. Preserve the original frozen forecast and ghost pick unchanged.
7. Track independently: ghost picks, ghost passes, and confirmed real bets. Report number of observations, wins/losses/pushes, yield at quoted odds, CLV, forecast calibration, and sample-size caveats. **Do not treat paper results as realized profit.**

## Ghost pick JSON record template
```json
{
  "schema_version": "1.0",
  "status": "GHOST_PICK_PRE_OUTCOME_LOCKED",
  "game_id": null,
  "date": null,
  "market_snapshot_timestamp": null,
  "game_clock": null,
  "official_score_at_snapshot": null,
  "sportsbook": "William Hill Nevada",
  "market_type": null,
  "selection": null,
  "line": null,
  "american_odds": null,
  "decimal_odds": null,
  "break_even_probability": null,
  "model_projected_mean": null,
  "model_projected_median": null,
  "model_probability": null,
  "estimated_ev_per_unit": null,
  "simulation_count": 0,
  "model_method": null,
  "model_freeze_file": null,
  "uncertainty_flags": [],
  "hypothetical_stake_units": 1,
  "real_money_staked": 0,
  "real_bet_confirmed": false,
  "result": "PENDING",
  "closing_line": null,
  "postmortem_file": null
}
```

For GHOST PASS set status `GHOST_PASS_PRE_OUTCOME_LOCKED`, selection null and provide `pass_reason`. Never manufacture prices, edges or probabilities. A ghost pick is an evaluation signal, not a recommendation to place a real bet.
