from dataclasses import dataclass
from typing import List, Dict


@dataclass
class CardCandidate:
    player: str
    stat: str
    line: float
    side: str
    score: float
    tier: str
    classification: str
    market: str
    game: str
    correlation_group: str


def build_card(
    candidates: List[CardCandidate],
    max_legs: int = 3,
    max_same_correlation_group: int = 2,
) -> Dict:
    sorted_candidates = sorted(candidates, key=lambda x: x.score, reverse=True)

    selected: List[CardCandidate] = []
    correlation_counts: Dict[str, int] = {}

    for candidate in sorted_candidates:
        if candidate.tier == "PASS":
            continue

        if candidate.classification in [
            "NO_BET_ZONE",
            "CEILING_TRAP",
            "ROLE_UNSTABLE",
            "SCRIPT_DEPENDENT",
            "MARKET_ONLY_EDGE",
        ]:
            continue

        group_count = correlation_counts.get(candidate.correlation_group, 0)
        if group_count >= max_same_correlation_group:
            continue

        selected.append(candidate)
        correlation_counts[candidate.correlation_group] = group_count + 1

        if len(selected) >= max_legs:
            break

    if not selected:
        return {
            "card_status": "NO_CARD",
            "selected_legs": [],
            "certainty_tier": "NONE",
            "average_score": 0.0,
        }

    avg_score = round(sum(c.score for c in selected) / len(selected), 1)

    if avg_score >= 85:
        certainty_tier = "LOCK"
    elif avg_score >= 70:
        certainty_tier = "PLAYABLE"
    elif avg_score >= 55:
        certainty_tier = "THIN"
    else:
        certainty_tier = "PASS"

    return {
        "card_status": "READY",
        "selected_legs": [
            {
                "player": c.player,
                "stat": c.stat,
                "line": c.line,
                "side": c.side,
                "score": c.score,
                "tier": c.tier,
                "classification": c.classification,
                "market": c.market,
                "game": c.game,
                "correlation_group": c.correlation_group,
            }
            for c in selected
        ],
        "certainty_tier": certainty_tier,
        "average_score": avg_score,
    }
