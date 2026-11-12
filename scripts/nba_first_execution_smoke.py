#!/usr/bin/env python3
"""First end-to-end SharpEdge NBA engine smoke test. SAMPLE DATA ONLY."""
import json
import math
from pathlib import Path
from sim.nba_runner import simulate_nba

root = Path(__file__).resolve().parents[1]
fixture = root / "config/nba.inputs.sample.json"
data = json.loads(fixture.read_text(encoding="utf-8"))
result = simulate_nba(data)
projection = result["projection"]
probabilities = result["probabilities"]
for key in ("total_mean", "total_median", "total_stdev"):
    assert math.isfinite(projection[key]), f"Invalid {key}"
assert projection["total_stdev"] > 0
for key in ("over_probability", "under_probability", "home_win_probability", "away_win_probability"):
    assert 0 <= probabilities[key] <= 1, f"Invalid {key}"
assert abs(probabilities["over_probability"] + probabilities["under_probability"] - 1) < 0.0002
assert abs(probabilities["home_win_probability"] + probabilities["away_win_probability"] - 1) < 0.0002
# This engine currently uses parametric normal-CDF heuristics, not actual Monte Carlo draws.
# The sample fixture is not a verified historical game, and its odds are not executable.
report = {
    "status": "ENGINE_SMOKE_PASSED",
    "fixture": "config/nba.inputs.sample.json",
    "data_provenance": "UNVERIFIED_SAMPLE",
    "game": result["game"],
    "engine_model_version": result["model_version"],
    "simulation_method": "PARAMETRIC_HEURISTIC_NOT_MONTE_CARLO",
    "mean": projection["total_mean"],
    "median": projection["total_median"],
    "stdev": projection["total_stdev"],
    "line": data["market"]["total_line"],
    "line_probabilities_uncalibrated": probabilities["line_probabilities"],
    "p_model_calibrated": None,
    "edge_pp": None,
    "EV_per_unit": None,
    "qualification": "GHOST_PASS",
    "safe_for_training": False,
    "real_money_authorized": False,
}
out = root / "outputs/nba/first_execution_report.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, indent=2))
