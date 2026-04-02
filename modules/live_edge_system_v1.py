from dataclasses import dataclass
from typing import List, Dict


@dataclass
class LiveEdgeCandidate:
    player: str
    stat: str
    market: str
    game: str
    side: str
    line: float
    model_line: float
    win_probability: float
    score: float
    market_timestamp: str
    book: str


def calculate_edge_delta(line: float, model_line: float, side: str) -> float:
    if side.upper() == "OVER":
        return round(model_line - line, 3)
    return round(line - model_line, 3)


def classify_live_edge(candidate: LiveEdgeCandidate) -> Dict:
    edge_delta = calculate_edge_delta(candidate.line, candidate.model_line, candidate.side)

    if candidate.win_probability >= 0.60 and candidate.score >= 80 and edge_delta >= 1.0:
        alert_level = "FIRE_NOW"
    elif candidate.win_probability >= 0.56 and candidate.score >= 70 and edge_delta >= 0.6:
        alert_level = "STRONG_WATCH"
    elif candidate.win_probability >= 0.53 and candidate.score >= 55 and edge_delta >= 0.3:
        alert_level = "WATCH"
    else:
        alert_level = "NO_ALERT"

    return {
        "player": candidate.player,
        "stat": candidate.stat,
        "market": candidate.market,
        "game": candidate.game,
        "side": candidate.side,
        "book": candidate.book,
        "line": candidate.line,
        "model_line": candidate.model_line,
        "edge_delta": edge_delta,
        "win_probability": candidate.win_probability,
        "score": candidate.score,
        "market_timestamp": candidate.market_timestamp,
        "alert_level": alert_level,
    }


def scan_live_edges(candidates: List[LiveEdgeCandidate]) -> Dict:
    results = [classify_live_edge(c) for c in candidates]
    actionable = [r for r in results if r["alert_level"] != "NO_ALERT"]
    actionable = sorted(actionable, key=lambda x: (x["alert_level"], x["score"], x["edge_delta"]), reverse=True)

    return {
        "total_candidates": len(candidates),
        "actionable_count": len(actionable),
        "actionable_edges": actionable,
    }
