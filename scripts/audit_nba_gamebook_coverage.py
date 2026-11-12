"""Stratified source audit for official NBA first-half game-book team totals.

Input is the validated API-NBA halftime outcome JSONL from the backfill.
This samples ten chronologically spaced regulation games per season, downloads
official PDFs without retaining them, and writes only compact validation data.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

TEAM_CODES = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS",
    "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE",
    "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET", "Golden State Warriors": "GSW",
    "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "LA Clippers": "LAC", "Los Angeles Clippers": "LAC",
    "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM",
    "Miami Heat": "MIA", "Milwaukee Bucks": "MIL",
    "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP",
    "New York Knicks": "NYK", "Oklahoma City Thunder": "OKC",
    "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI",
    "Phoenix Suns": "PHX", "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS",
    "Toronto Raptors": "TOR", "Utah Jazz": "UTA",
    "Washington Wizards": "WAS",
}


def canonical_name(name: str) -> str:
    name = re.sub(r"\([^)]*\)", "", name)
    name = name.lower().replace("l.a.", "la").replace("los angeles clippers", "la clippers")
    return re.sub(r"[^a-z0-9]", "", name)


def sample(rows: list[dict], per_season: int) -> list[dict]:
    groups = defaultdict(list)
    for row in rows:
        groups[int(row["season"])].append(row)
    chosen = []
    for season in (2022, 2023, 2024):
        games = sorted(groups[season], key=lambda row: (row["start_utc"], row["game_id"]))
        if len(games) < per_season:
            raise ValueError(f"Insufficient games in season {season}")
        chosen.extend(games[round(i * (len(games) - 1) / (per_season - 1))]
                      for i in range(per_season))
    return chosen


def parse_first_half(text: str, row: dict) -> dict:
    page = next(
        (p for p in text.split("\f")
         if re.search(r"OFFICIAL SCORER'S REPORT\s+FIRST HALF", p)), "")
    if not page:
        return {"status": "missing_first_half_page"}
    visitor = re.search(r"^\s*VISITOR:\s*(.+)$", page, flags=re.M)
    home = re.search(r"^\s*HOME:\s*(.+)$", page, flags=re.M)
    if not visitor or not home:
        return {"status": "missing_team_headers"}
    if (canonical_name(visitor.group(1)) != canonical_name(row["away_team"])
            or canonical_name(home.group(1)) != canonical_name(row["home_team"])):
        return {"status": "team_identity_mismatch",
                "pdf_visitor": visitor.group(1).strip(),
                "pdf_home": home.group(1).strip()}

    try:
        section = page.split("SCORE BY PERIOD", 1)[1].split("Inactive:", 1)[0]
    except IndexError:
        return {"status": "missing_score_section"}
    score_rows = re.findall(
        r"^\s*(.*?)\s+(\d+)\s+(\d+)\s+(\d+)\s*$",
        section, flags=re.M)
    if len(score_rows) != 2:
        return {"status": "ambiguous_score_rows", "count": len(score_rows)}
    extracted = [int(line[3]) for line in score_rows]
    if extracted != [int(row["halftime_away"]), int(row["halftime_home"])]:
        return {"status": "halftime_score_mismatch", "pdf_scores": extracted}

    # Two half-team-minute rows, in visitor/home order.
    team_totals = []
    for line in page.splitlines():
        match = re.match(r"^\s*120:00\s+(.+)$", line)
        if match:
            cells = match.group(1).split()
            if len(cells) == 16 and all(re.fullmatch(r"-?\d+", x) for x in cells):
                team_totals.append([int(x) for x in cells])
    if len(team_totals) != 2:
        return {"status": "ambiguous_team_totals", "count": len(team_totals)}
    for side, values in zip(("away", "home"), team_totals):
        fgm, fga, tpm, tpa, ftm, fta = values[:6]
        points = int(row[f"halftime_{side}"])
        if not (points == values[15] == 2 * fgm + tpm + ftm
                and 0 <= tpm <= fgm <= fga and tpm <= tpa <= fga
                and 0 <= ftm <= fta and values[6] + values[7] == values[8]):
            return {"status": "invalid_team_totals", "side": side}
    player_rows = re.findall(
        r"^\s*\d{1,2}\s+[^\n]+\d{2}:\d{2}\s+\d+",
        page, flags=re.M)
    if len(player_rows) < 10:
        return {"status": "missing_player_stat_rows", "count": len(player_rows)}
    return {
        "status": "validated_first_half_team_totals",
        "halftime_away": extracted[0], "halftime_home": extracted[1],
        "player_stat_rows_present": len(player_rows),
        "team_totals": {
            side: {
                "fgm": v[0], "fga": v[1], "tpm": v[2], "tpa": v[3],
                "ftm": v[4], "fta": v[5], "off_reb": v[6], "def_reb": v[7],
                "reb": v[8], "assists": v[9], "fouls": v[10],
                "steals": v[11], "turnovers": v[12], "blocks": v[13],
                "points": v[15],
            } for side, v in zip(("away", "home"), team_totals)
        },
    }


def audit_one(row: dict) -> dict:
    result = {"season": row["season"], "api_game_id": row["game_id"],
              "game_date_eastern": row["game_date_eastern"],
              "away_team": row["away_team"], "home_team": row["home_team"]}
    away_code = TEAM_CODES.get(row["away_team"])
    home_code = TEAM_CODES.get(row["home_team"])
    if not away_code or not home_code:
        result["status"] = "unknown_team_code"
        return result
    date = row["game_date_eastern"].replace("-", "")
    url = f"https://statsdmz.nba.com/pdfs/{date}/{date}_{away_code}{home_code}_book.pdf"
    result["official_gamebook_url"] = url
    try:
        request = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (SharpEdgeCoverageAudit/1.0)"})
        with tempfile.TemporaryDirectory() as folder:
            pdf = Path(folder) / "gamebook.pdf"
            with urllib.request.urlopen(request, timeout=30) as response:
                pdf.write_bytes(response.read())
            if not pdf.read_bytes().startswith(b"%PDF"):
                result["status"] = "non_pdf_response"
                return result
            text = subprocess.check_output(
                ["pdftotext", "-layout", str(pdf), "-"], text=True, timeout=30)
        result.update(parse_first_half(text, row))
    except urllib.error.HTTPError as exc:
        result["status"] = "http_error"
        result["http_status"] = exc.code
    except (urllib.error.URLError, subprocess.SubprocessError, TimeoutError) as exc:
        result["status"] = type(exc).__name__
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-season", type=int, default=10)
    args = parser.parse_args()
    if not 2 <= args.per_season <= 20:
        parser.error("--per-season must be between 2 and 20")
    rows = [json.loads(line) for line in args.dataset.read_text().splitlines()
            if line.strip()]
    results = []
    for row in sample(rows, args.per_season):
        results.append(audit_one(row))
        time.sleep(0.2)
    counts = Counter(r["status"] for r in results)
    report = {"sample_strategy": "chronological quantiles per season",
              "sampled": len(results), "counts_by_status": dict(counts),
              "by_season": {
                  str(y): dict(Counter(r["status"] for r in results if r["season"] == y))
                  for y in (2022, 2023, 2024)},
              "results": results, "safe_for_model_training": False,
              "note": "Sample coverage only. No player stat parsing, all-game coverage, "
                      "or archived halftime odds; do not promote model from this audit."}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"sampled": report["sampled"],
                      "counts_by_status": report["counts_by_status"],
                      "by_season": report["by_season"],
                      "safe_for_model_training": False}))


if __name__ == "__main__":
    main()
