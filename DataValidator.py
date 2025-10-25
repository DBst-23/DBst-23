from __future__ import annotations
from typing import Dict, Any, List, Tuple
from datetime import datetime

REQUIRED = [
    "date","team_1","team_2","score_1","score_2",
    "odds_open_team_1","odds_open_team_2",
    "odds_close_team_1","odds_close_team_2",
    "line_movement","outcome"
]

def _is_date(s: str) -> bool:
    try:
        datetime.strptime(s, "%Y-%m-%d"); return True
    except Exception:
        return False

def _gt_one(x) -> bool:
    try:
        return float(x) > 1.0
    except Exception:
        return False

def _nonneg_int(x) -> bool:
    return isinstance(x, int) and x >= 0

def _nonneg_num(x) -> bool:
    try:
        return float(x) >= 0.0
    except Exception:
        return False

def validate_record(rec: Dict[str, Any]) -> Tuple[bool, List[str]]:
    errs: List[str] = []

    for k in REQUIRED:
        if k not in rec:
            errs.append(f"missing field: {k}")

    if "date" in rec and not _is_date(rec["date"]):
        errs.append("invalid date format (YYYY-MM-DD expected)")

    for k in ("team_1","team_2"):
        if k in rec and (not isinstance(rec[k], str) or len(rec[k].strip()) == 0):
            errs.append(f"{k} must be non-empty string")

    for k in ("score_1","score_2"):
        if k in rec and not _nonneg_int(rec[k]):
            errs.append(f"{k} must be integer >= 0")

    for k in ("odds_open_team_1","odds_open_team_2","odds_close_team_1","odds_close_team_2"):
        if k in rec and not _gt_one(rec[k]):
            errs.append(f"{k} must be a number > 1.0")

    if "line_movement" in rec and not _nonneg_num(rec["line_movement"]):
        errs.append("line_movement must be a number >= 0")

    if "outcome" in rec and rec["outcome"] not in (0,1):
        errs.append("outcome must be 0 or 1")

    allowed = set(REQUIRED) | {"injuries","weather_summary","venue","referee_id"}
    extra = [k for k in rec.keys() if k not in allowed]
    if extra:
        errs.append("unexpected fields: " + ", ".join(extra))

    return (len(errs) == 0, errs)

def validate_dataset(records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    good, bad = [], []
    for i, r in enumerate(records, start=1):
        ok, errs = validate_record(r)
        if ok:
            good.append(r)
        else:
            bad.append({"row": i, "errors": errs, "record": r})
    return good, bad