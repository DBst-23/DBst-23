"""Check first-half official NBA game books against API-NBA across three seasons."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.error
import urllib.request

CASES = (
    {"season": 2022, "api_game_id": 11050, "date": "20221018",
     "away_code": "PHI", "home_code": "BOS", "away_label": "76ers",
     "home_label": "CELTICS", "expected_away": 63, "expected_home": 63},
    {"season": 2023, "api_game_id": 12549, "date": "20231024",
     "away_code": "LAL", "home_code": "DEN", "away_label": "Lakers",
     "home_label": "NUGGETS", "expected_away": 54, "expected_home": 63},
    {"season": 2024, "api_game_id": 14115, "date": "20241022",
     "away_code": "NYK", "home_code": "BOS", "away_label": "Knicks",
     "home_label": "CELTICS", "expected_away": 55, "expected_home": 74},
)


def inspect(text: str, case: dict) -> dict:
    pages = text.split("\f")
    first_half = next(
        (page for page in pages
         if re.search(r"OFFICIAL SCORER'S REPORT\s+FIRST HALF", page)), ""
    )
    scores = {}
    for side in ("away", "home"):
        label = re.escape(case[f"{side}_label"])
        match = re.search(
            rf"^\s*{label}\s+\d+\s+\d+\s+(\d+)\s*$",
            first_half, flags=re.I | re.M,
        )
        scores[side] = int(match.group(1)) if match else None
    player_lines = re.findall(r"^\s*\d{1,2}\s+[^\n]+\d{2}:\d{2}\s+\d+",
                              first_half, flags=re.M)
    # The two 120:00 rows in the FIRST HALF page are away and home totals.
    # MIN is 120:00 team minutes for each half; the next 16 cells are the
    # standard FGM, FGA, 3PM, 3PA, FTM, FTA, OR, DR, REB, AST, PF, STL,
    # TOV, BLK, +/-, PTS fields.
    total_rows = []
    for line in first_half.splitlines():
        match = re.match(r"^\s*120:00\s+(.+)$", line)
        if not match:
            continue
        fields = match.group(1).split()
        if len(fields) == 16 and all(re.fullmatch(r"-?\d+", f) for f in fields):
            total_rows.append([int(f) for f in fields])
    totals = {}
    for side, fields in zip(("away", "home"), total_rows):
        fgm, fga, tpm, tpa, ftm, fta = fields[:6]
        totals[side] = {
            "fgm": fgm, "fga": fga, "three_made": tpm,
            "three_attempted": tpa, "ftm": ftm, "fta": fta,
            "offensive_rebounds": fields[6], "defensive_rebounds": fields[7],
            "total_rebounds": fields[8], "assists": fields[9],
            "personal_fouls": fields[10], "steals": fields[11],
            "turnovers": fields[12], "blocks": fields[13],
            "points": fields[15],
        }
        totals[side]["valid_arithmetic"] = (
            fields[15] == 2 * fgm + tpm + ftm
            and 0 <= tpm <= tpa <= fga
            and 0 <= tpm <= fgm <= fga
            and 0 <= ftm <= fta
            and fields[6] + fields[7] == fields[8]
            and fields[15] == scores[side]
        )
    return {
        "season": case["season"],
        "api_nba_game_id": case["api_game_id"],
        "first_half_page": bool(first_half),
        "scores": scores,
        "scores_match_api_nba": (scores["away"] == case["expected_away"]
                                 and scores["home"] == case["expected_home"]),
        "player_stat_lines": len(player_lines),
        "team_totals_lines": len(re.findall(r"\b120:00\b", first_half)),
        "team_totals": totals,
        "team_totals_valid": (
            len(totals) == 2 and all(t["valid_arithmetic"] for t in totals.values())
        ),
        "play_by_play": "OFFICIAL PLAY-BY-PLAY" in text,
    }


def fetch_and_inspect(case: dict) -> dict:
    date = case["date"]
    url = (f"https://statsdmz.nba.com/pdfs/{date}/"
           f"{date}_{case['away_code']}{case['home_code']}_book.pdf")
    result = {"url": url, "season": case["season"], "api_nba_game_id": case["api_game_id"]}
    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (SharpEdgeSourceAudit/1.0)"})
        with tempfile.TemporaryDirectory() as folder:
            pdf = Path(folder) / "book.pdf"
            with urllib.request.urlopen(request, timeout=40) as response:
                pdf.write_bytes(response.read())
            if not pdf.read_bytes().startswith(b"%PDF"):
                raise ValueError("not a PDF")
            text = subprocess.check_output(
                ["pdftotext", "-layout", str(pdf), "-"], text=True, timeout=30)
        result.update(inspect(text, case))
    except (urllib.error.URLError, ValueError, subprocess.SubprocessError) as exc:
        result["error_type"] = type(exc).__name__
        result["scores_match_api_nba"] = False
    return result


def main() -> None:
    rows = [fetch_and_inspect(case) for case in CASES]
    report = {
        "sample_size": len(rows),
        "matched": sum(r["scores_match_api_nba"] for r in rows),
        "rows": rows,
        "safe_for_model_training": False,
        "limitation": "Small sample only. Team/player stat fields and broad coverage "
                      "are not yet validated; no archived halftime prices.",
    }
    Path("diagnostics").mkdir(exist_ok=True)
    Path("diagnostics/nba_gamebook_season_audit.json").write_text(
        json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))
    if (report["matched"] != len(rows)
            or not all(r.get("team_totals_valid") for r in rows)):
        raise SystemExit("Official first-half scores or team totals failed validation")


if __name__ == "__main__":
    main()
