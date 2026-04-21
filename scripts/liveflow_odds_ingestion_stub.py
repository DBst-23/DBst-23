import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


@dataclass
class LiveOddsSnapshot:
    game_label: str
    sportsbook: str
    timestamp_utc: str
    closing_spread: float
    closing_total: float
    live_spread: float
    live_total: float
    team_a_moneyline: Optional[float] = None
    team_b_moneyline: Optional[float] = None
    team_a_team_total: Optional[float] = None
    team_b_team_total: Optional[float] = None
    notes: str = ""


def prompt_float(label: str, default: Optional[float] = None) -> Optional[float]:
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"{label}{suffix}: ").strip()
    if raw == "":
        return default
    return float(raw)


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw if raw else default


def build_snapshot() -> LiveOddsSnapshot:
    print("=== SharpEdge Live Odds Ingestion Stub ===")
    print("Enter the current market screen values. Leave optional fields blank if unavailable.")

    game_label = prompt_text("Game label", "Team A @ Team B")
    sportsbook = prompt_text("Sportsbook / source", "manual_entry")

    snapshot = LiveOddsSnapshot(
        game_label=game_label,
        sportsbook=sportsbook,
        timestamp_utc=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        closing_spread=prompt_float("Closing spread", 0.0),
        closing_total=prompt_float("Closing total", 0.0),
        live_spread=prompt_float("Live spread", 0.0),
        live_total=prompt_float("Live total", 0.0),
        team_a_moneyline=prompt_float("Team A moneyline"),
        team_b_moneyline=prompt_float("Team B moneyline"),
        team_a_team_total=prompt_float("Team A team total"),
        team_b_team_total=prompt_float("Team B team total"),
        notes=prompt_text("Notes"),
    )
    return snapshot


def main() -> None:
    snapshot = build_snapshot()
    print("\n=== LIVE ODDS SNAPSHOT ===")
    print(json.dumps(asdict(snapshot), indent=2))
    print("\nSharpEdge Read: odds snapshot captured. Feed these values into the bridge / heat pipeline.")


if __name__ == "__main__":
    main()
