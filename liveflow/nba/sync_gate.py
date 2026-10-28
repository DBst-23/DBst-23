"""Fail-closed SharpEdge LIVE-FLOW model/market synchronization gate.

Run: python -m liveflow.nba.sync_gate freeze.json market.json [--output gate.json]
Timestamps must be trustworthy source-generated UTC instants, not inferred from Git commit times.
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

def _instant(value):
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("timestamp must be UTC ISO-8601 ending in Z")
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.utcoffset().total_seconds() != 0:
        raise ValueError("timestamp must be UTC")
    return dt

def evaluate(freeze, market):
    errors = []
    def require(obj, key, side):
        value = obj.get(key)
        if value is None or value == "":
            errors.append(f"{side}: missing {key}")
        return value
    for side, obj in (("freeze", freeze), ("market", market)):
        for key in ("game_id", "period", "clock_seconds_remaining", "home_score", "away_score",
                    "source", "captured_at_utc", "ingested_at_utc", "artifact_sha256"):
            require(obj, key, side)
        if side == "freeze":
            require(obj, "model_total_regulation", side)
            require(obj, "model_version", side)
        else:
            for key in ("sportsbook", "market_type", "total_line", "odds_format", "includes_overtime"):
                require(obj, key, side)
    if errors:
        return {"status": "REJECT", "eligible_for_accuracy_registry": False, "reasons": errors}
    for key in ("game_id", "period", "clock_seconds_remaining", "home_score", "away_score"):
        if freeze[key] != market[key]:
            errors.append(f"state mismatch: {key}")
    if freeze["period"] != "HALFTIME" or market["period"] != "HALFTIME":
        errors.append("not halftime")
    if freeze["clock_seconds_remaining"] != 0:
        errors.append("halftime clock must be 0")
    for side, obj in (("freeze", freeze), ("market", market)):
        for key in ("home_score", "away_score", "clock_seconds_remaining"):
            if type(obj[key]) is not int or obj[key] < 0:
                errors.append(f"{side}: invalid {key}")
        if not isinstance(obj["artifact_sha256"], str) or len(obj["artifact_sha256"]) != 64 or any(c not in "0123456789abcdef" for c in obj["artifact_sha256"]):
            errors.append(f"{side}: invalid artifact_sha256")
    try:
        ft, mt = _instant(freeze["captured_at_utc"]), _instant(market["captured_at_utc"])
        fi, mi = _instant(freeze["ingested_at_utc"]), _instant(market["ingested_at_utc"])
        if not (ft <= fi and mt <= mi):
            errors.append("capture after ingestion")
        if not (ft < mt):
            errors.append("forecast not captured strictly before market")
        if not (fi < mt):
            errors.append("forecast not durably ingested before market capture")
    except (ValueError, TypeError, OverflowError) as exc:
        errors.append(f"timestamp invalid: {exc}")
    if market["market_type"] != "FULL_GAME_TOTAL":
        errors.append("market type must be FULL_GAME_TOTAL")
    if market["includes_overtime"] is not False:
        errors.append("book line must explicitly exclude overtime for regulation-only comparison")
    for side, key, obj in (("freeze", "model_total_regulation", freeze), ("market", "total_line", market)):
        if type(obj[key]) not in (float, int) or not (0 < obj[key] < 500):
            errors.append(f"{side}: invalid {key}")
    return {"status": "PASS" if not errors else "REJECT", "eligible_for_accuracy_registry": not errors,
            "reasons": errors, "game_id": freeze["game_id"],
            "policy": "strict_premarket_regulation_v1"}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("freeze")
    p.add_argument("market")
    p.add_argument("--output")
    args = p.parse_args()
    result = evaluate(json.loads(Path(args.freeze).read_text()), json.loads(Path(args.market).read_text()))
    output = json.dumps(result, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(output)
    print(output, end="")
    raise SystemExit(0 if result["eligible_for_accuracy_registry"] else 2)

if __name__ == "__main__":
    main()
