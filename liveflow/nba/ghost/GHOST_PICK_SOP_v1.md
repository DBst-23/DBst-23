# SharpEdge LIVE-FLOW — Ghost Pick SOP v1.0

Effective: 2026-10-31 (next LIVE-FLOW session).
Purpose: prospectively paper-trade every qualifying live-flow strike before risking capital. Ghost picks are simulations of decisions, **not real wagers** and do not imply profitability.

## Required sequence
1. Capture game, date, teams, official score, clock, quarter, injuries, and timestamps. Verify score/time synchronization.
2. **Freeze model first**: projected second-half points by team, second-half total, final score/total, spread margin, assumptions and volatility tags. Mark uncalibrated forecasts as heuristic; do not invent Monte Carlo results.
3. Capture sportsbook **William Hill Nevada** exact market, line, price, timestamp and market type; optionally record sharp-book comparisons. Never use pregame odds as halftime odds.
4. **Mandatory price-versus-probability gate for every candidate market.** Convert the exact offered odds to break-even probability (`p_break_even = 1 / decimal_odds`; negative American odds `abs(odds)/(abs(odds)+100)`, positive American odds `100/(odds+100)`). Estimate `p_model` only from a documented, out-of-sample calibrated predictive distribution appropriate to that market and time; report mean, median, simulation count, and uncertainty when available. Calculate `EV_per_1_unit = p_model * (decimal_odds - 1) - (1 - p_model)` and `edge_pp = 100 * (p_model - p_break_even)`. A positive estimated edge is not proof of a true edge: require `p_model > p_break_even` **and** a documented uncertainty-aware safety margin before marking a candidate as price-qualified. If probabilities are missing, uncalibrated, unreliable, or margin insufficient, mark `GHOST PASS` and keep probability/EV null where unsupported. Never infer win probability solely from a points difference or fabricate simulations.
5. Issue **one clearly labeled GHOST PICK** only if the price-versus-probability gate passes and all required inputs are available; otherwise issue **GHOST PASS** with the specific reason. Record the market side, line, offered price, estimated probability, break-even probability, EV, margin and calibration provenance. A qualifying ghost pick is still a paper test, **not authorization to risk real money**.
6. Lock the ghost pick **before** outcome or material market movement; append a separate immutable timestamped pick record to `liveflow/nba/ghost/picks/`. No retroactive picks. No cash stake, no actual wager, no bankroll debit.
7. After official final, add linked postmortem: settlement under recorded line and rules, closing line value when available, model errors, result, volatility notes. Preserve the original frozen forecast and ghost pick unchanged.
8. Track independently: ghost picks, ghost passes, and confirmed real bets. Report number of observations, wins/losses/pushes, yield at quoted odds, CLV, forecast calibration, and sample-size caveats. **Do not treat paper results as realized profit.**

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
  "probability_calibration_source": null,
  "edge_percentage_points": null,
  "safety_margin_percentage_points": null,
  "price_qualification": "NOT_ESTABLISHED",
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

## Hard rule: no unpriced risk
For **every** LIVE-FLOW market evaluation, publish offered odds, break-even probability, and a supported model probability/EV (or explicit `NOT_ESTABLISHED`). Never label a market as +EV, a qualified ghost strike, or a real-money recommendation without evidence that its calibrated probability exceeds the break-even threshold by an uncertainty-aware margin. Re-evaluate on material price changes. This rule applies to spreads, totals, team totals, moneylines and props.

## Mandatory postmortem even when the price gate fails
Every halftime game for which a prospective model projection was recorded receives an outcome postmortem after the official final, **including GHOST PASS and no-bet cases**. Compare the original timestamped projected team final scores, full-game total, second-half total, and margin against actual results; calculate signed errors and absolute errors, preserve original forecast and source/provenance, and separately assess offered markets and whether the probability-versus-price gate was satisfied. A postmortem is a **forecast accuracy observation**, not a retroactively created ghost pick or evidence that a bet was placed. Do not overwrite or backdate a projection. If a projection was only conversational and not independently frozen, label provenance unverified and exclude it from authenticated freeze-only accuracy metrics.
