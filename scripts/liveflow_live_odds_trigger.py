from dataclasses import dataclass, asdict
import json
from typing import Dict, Optional


@dataclass
class LiveOddsTriggerInput:
    game_label: str
    market_type: str
    closing_line: float
    live_line: float
    current_total: float = 0.0
    minutes_remaining: float = 24.0
    heat_index: int = 0
    heat_action: str = "NO_EDGE"
    classifier_action: str = "NO_FIRE"
    classifier_confidence: float = 0.0
    recommendation: str = "NO_FIRE"
    pace_support_score: float = 0.0
    shooting_heat_score: float = 0.0
    primary_scorers_count: int = 0


CONFIDENCE_TIER_RULES = {
    "LOCK": {"min_score": 80, "emoji": "🔒"},
    "STRONG": {"min_score": 65, "emoji": "⚠️"},
    "LEAN": {"min_score": 50, "emoji": "🟡"},
    "PASS": {"min_score": 0, "emoji": "⚪"},
}

MARKET_TYPE_WEIGHTS = {
    "team_total": 8,
    "total": 6,
    "spread": -6,
    "moneyline": -4,
}

RECOMMENDATION_WEIGHTS = {
    "FIRE_UNDER": 12,
    "WATCH_UNDER_BETTER_NUMBER": 4,
    "STAY_OFF_CONTINUATION": -12,
    "NO_FIRE": -10,
    "MIXED_NO_FIRE": -8,
    None: 0,
}


def compute_confidence_from_trigger(inp: LiveOddsTriggerInput) -> Dict:
    live_total_delta = inp.live_line - inp.closing_line
    score = 0.0
    reasons = []

    heat_component = max(0, min(35, (inp.heat_index / 100.0) * 35))
    score += heat_component
    reasons.append(f"heat index contribution: +{round(heat_component, 1)}")

    classifier_component = max(0, min(25, inp.classifier_confidence * 25))
    score += classifier_component
    reasons.append(f"classifier confidence contribution: +{round(classifier_component, 1)}")

    if inp.heat_action == "UNDER_TRIGGER" and inp.classifier_action == "LEAN_UNDER":
        score += 18
        reasons.append("full under alignment across heat + classifier: +18")
    elif inp.heat_action == "WATCH_UNDER" and inp.classifier_action == "LEAN_UNDER":
        score += 8
        reasons.append("partial under alignment: +8")
    elif inp.heat_action == "DO_NOT_FADE" or inp.classifier_action == "DO_NOT_AUTO_FADE":
        score -= 18
        reasons.append("continuation risk penalty: -18")
    elif inp.classifier_action == "NO_FIRE":
        score -= 10
        reasons.append("classifier no-fire penalty: -10")

    market_weight = MARKET_TYPE_WEIGHTS.get(inp.market_type, 0)
    score += market_weight
    reasons.append(f"market type adjustment ({inp.market_type}): {market_weight:+}")

    rec_weight = RECOMMENDATION_WEIGHTS.get(inp.recommendation, 0)
    score += rec_weight
    if rec_weight:
        reasons.append(f"recommendation adjustment ({inp.recommendation}): {rec_weight:+}")

    if inp.market_type in {"total", "team_total"} and abs(live_total_delta) >= 10:
        score += 6
        reasons.append("meaningful repricing delta supports edge clarity: +6")
    elif inp.market_type in {"total", "team_total"} and abs(live_total_delta) < 4:
        score -= 4
        reasons.append("small repricing delta reduces edge clarity: -4")

    if inp.minutes_remaining <= 24:
        score += 4
        reasons.append("halftime or later signal maturity: +4")
    if inp.minutes_remaining <= 18:
        score += 3
        reasons.append("late-game compression bonus: +3")

    if inp.primary_scorers_count >= 4 and inp.heat_action == "UNDER_TRIGGER":
        score -= 5
        reasons.append("multiple scorers reduce under stability: -5")
    elif inp.primary_scorers_count <= 2 and inp.heat_action == "UNDER_TRIGGER":
        score += 4
        reasons.append("scoring concentration supports under fade: +4")

    if inp.pace_support_score >= 12:
        score -= 6
        reasons.append("pace support penalty: -6")
    elif inp.pace_support_score <= 4:
        score += 3
        reasons.append("limited pace support bonus: +3")

    if inp.shooting_heat_score >= 18 and inp.heat_action == "UNDER_TRIGGER":
        score += 4
        reasons.append("strong shooting heat increases fade value: +4")

    score = max(0, min(100, round(score)))

    tier_name = "PASS"
    tier_emoji = "⚪"
    for name, rule in CONFIDENCE_TIER_RULES.items():
        if score >= rule["min_score"]:
            tier_name = name
            tier_emoji = rule["emoji"]
            break

    if tier_name == "LOCK":
        recommended_units = "1.00u"
    elif tier_name == "STRONG":
        recommended_units = "0.50u"
    elif tier_name == "LEAN":
        recommended_units = "0.25u"
    else:
        recommended_units = "0.00u"

    should_fire = tier_name in {"LOCK", "STRONG"} and inp.recommendation in {"FIRE_UNDER", "WATCH_UNDER_BETTER_NUMBER"}

    return {
        "confidence_score": score,
        "confidence_tier": tier_name,
        "confidence_emoji": tier_emoji,
        "recommended_units": recommended_units,
        "live_line_delta": round(live_total_delta, 2),
        "should_fire": should_fire,
        "reasons": reasons,
    }


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw if raw else default


def prompt_float(label: str, default: float = 0.0) -> float:
    raw = input(f"{label} [{default}]: ").strip()
    return float(raw) if raw else float(default)


def prompt_int(label: str, default: int = 0) -> int:
    raw = input(f"{label} [{default}]: ").strip()
    return int(raw) if raw else int(default)


def main() -> None:
    print("=== SharpEdge Live Odds Trigger ===")
    inp = LiveOddsTriggerInput(
        game_label=prompt_text("Game label", "Team A @ Team B"),
        market_type=prompt_text("Market type", "team_total"),
        closing_line=prompt_float("Closing line", 0.0),
        live_line=prompt_float("Live line", 0.0),
        current_total=prompt_float("Current total", 0.0),
        minutes_remaining=prompt_float("Minutes remaining", 24.0),
        heat_index=prompt_int("Heat index", 60),
        heat_action=prompt_text("Heat action", "UNDER_TRIGGER"),
        classifier_action=prompt_text("Classifier action", "LEAN_UNDER"),
        classifier_confidence=prompt_float("Classifier confidence", 0.65),
        recommendation=prompt_text("Recommendation", "FIRE_UNDER"),
        pace_support_score=prompt_float("Pace support score", 5.0),
        shooting_heat_score=prompt_float("Shooting heat score", 12.0),
        primary_scorers_count=prompt_int("Primary scorers count", 3),
    )

    result = compute_confidence_from_trigger(inp)
    payload = {
        "trigger_input": asdict(inp),
        "trigger_result": result,
    }

    print("\n=== LIVE ODDS TRIGGER PAYLOAD ===")
    print(json.dumps(payload, indent=2))

    print("\n=== SHARPEDGE LIVE TRIGGER OUTPUT ===")
    print(f"Tier: {result['confidence_emoji']} {result['confidence_tier']}")
    print(f"Score: {result['confidence_score']}")
    print(f"Recommended Size: {result['recommended_units']}")
    print(f"Should Fire: {result['should_fire']}")
    for reason in result['reasons']:
        print(f"- {reason}")


if __name__ == "__main__":
    main()
