"""Metadata-only structural inspection of SportsDataIO scrambled-trial LiveOdds.

PUBLIC LOG SAFE: output contains only pre-approved, canonical field names,
record counts, null/non-null flags and data types. No source strings, numeric
odds, line values, team scores, or credential-bearing payloads.
"""
import re
from collections import Counter

SAFE_FIELD = re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,63}$")
BOOK_WORDS = ("sportsbook", "bookmaker", "operator", "provider", "bettingpartner")
MONEY_WORDS = ("moneyline", "money_line", "h2h")
SPREAD_WORDS = ("spread", "handicap", "pointspread")
TOTAL_WORDS = ("total", "overunder", "over_under")
HALF_WORDS = ("half", "period", "quarter")
TEAM_WORDS = ("teamtotal", "team_total", "hometeamtotal", "awayteamtotal")
NEST_LIMIT = 7
ARRAY_LIMIT = 100
RECORD_LIMIT = 50


def safe_key(k):
    return k if isinstance(k, str) and SAFE_FIELD.fullmatch(k) else None


def structural_audit(rows):
    if not isinstance(rows, list):
        return {"status": "unexpected_response_shape"}
    summary = {
        "records_returned": len(rows),
        "records_inspected": min(len(rows), RECORD_LIMIT),
        "liveodds_present": 0,
        "liveodds_nonempty": 0,
        "liveodds_shapes": {},
        "nested_field_paths": [],
        "bookmaker_identifier_field_paths": [],
        "moneyline_field_paths": [],
        "spread_field_paths": [],
        "game_total_field_paths": [],
        "second_half_or_period_field_paths": [],
        "team_total_field_paths": [],
        "possible_team_total_fields": False,
        "explicit_second_half_market_value_verified": False,
        "numeric_values_accepted_for_training": False,
        "scrambled_trial": True,
    }
    paths = Counter()
    shapes = Counter()

    def walk(obj, prefix, depth):
        if depth > NEST_LIMIT:
            return
        if isinstance(obj, dict):
            for key, value in obj.items():
                k = safe_key(key)
                if k is None:
                    continue
                # Preserve only schemas, never print original source data.
                path = prefix + "." + k if prefix else k
                paths[path] += 1
                walk(value, path, depth + 1)
        elif isinstance(obj, list):
            for item in obj[:ARRAY_LIMIT]:
                walk(item, prefix + "[]", depth + 1)

    for record in rows[:RECORD_LIMIT]:
        if not isinstance(record, dict) or "LiveOdds" not in record:
            continue
        summary["liveodds_present"] += 1
        val = record["LiveOdds"]
        typ = type(val).__name__
        shapes[typ] += 1
        if val not in (None, [], {}):
            summary["liveodds_nonempty"] += 1
        walk(val, "LiveOdds", 0)

    def matched(words):
        return sorted([p for p in paths if any(w in p.lower().replace("_", "") for w in words)])[:40]

    def normed(words):
        return tuple(w.replace("_", "") for w in words)

    summary["liveodds_shapes"] = dict(shapes)
    summary["nested_field_paths"] = sorted(paths)[:100]
    summary["bookmaker_identifier_field_paths"] = matched(normed(BOOK_WORDS))
    summary["moneyline_field_paths"] = matched(normed(MONEY_WORDS))
    summary["spread_field_paths"] = matched(normed(SPREAD_WORDS))
    summary["game_total_field_paths"] = matched(normed(TOTAL_WORDS))
    summary["second_half_or_period_field_paths"] = matched(normed(HALF_WORDS))
    summary["team_total_field_paths"] = matched(normed(TEAM_WORDS))
    summary["possible_team_total_fields"] = bool(summary["team_total_field_paths"])
    return summary
