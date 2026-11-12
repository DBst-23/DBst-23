"""Probe one official NBA game book for a first-half box score.

This is a feasibility check. It does not backfill or train a model.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import tempfile
import urllib.request

GAMEBOOK = "https://statsdmz.nba.com/pdfs/20241022/20241022_NYKBOS_book.pdf"
EXPECTED = {"home": 74, "away": 55}


def inspect(text: str) -> dict:
    pages = text.split("\f")
    first_half = next(
        (p for p in pages if re.search(r"OFFICIAL SCORER'S REPORT\s+FIRST HALF", p)),
        "",
    )
    scores = {}
    for side, name in (("away", "Knicks"), ("home", "CELTICS")):
        match = re.search(
            rf"^\s*{name}\s+\d+\s+\d+\s+(\d+)\s*$",
            first_half, flags=re.I | re.M,
        )
        scores[side] = int(match.group(1)) if match else None
    return {
        "api_nba_game_id": 14115,
        "official_gamebook": GAMEBOOK,
        "first_half_page_found": bool(first_half),
        "first_half_scores": scores,
        "matches_api_nba": scores == EXPECTED,
        "player_box_score_present": all(
            value in first_half for value in ("Jayson Tatum", "Jalen Brunson")
        ),
        "official_play_by_play_present": "OFFICIAL PLAY-BY-PLAY" in text,
        "safe_for_model_training": False,
    }


def main() -> None:
    request = urllib.request.Request(
        GAMEBOOK,
        headers={"User-Agent": "Mozilla/5.0 (compatible; SharpEdgeGamebookProbe/1.0)"},
    )
    with tempfile.TemporaryDirectory() as folder:
        pdf = Path(folder) / "gamebook.pdf"
        with urllib.request.urlopen(request, timeout=40) as response:
            pdf.write_bytes(response.read())
        if not pdf.read_bytes().startswith(b"%PDF"):
            raise RuntimeError("NBA game book response is not a PDF")
        text = subprocess.check_output(
            ["pdftotext", "-layout", str(pdf), "-"], text=True, timeout=30
        )
    result = inspect(text)
    Path("diagnostics").mkdir(exist_ok=True)
    Path("diagnostics/nba_gamebook_halftime_probe.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps(result))
    if not result["matches_api_nba"] or not result["player_box_score_present"]:
        raise SystemExit("Halftime game book could not be reconciled with API-NBA")


if __name__ == "__main__":
    main()
