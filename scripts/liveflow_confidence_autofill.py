from dataclasses import dataclass, asdict
import json
from typing import Dict, List, Optional


@dataclass
class ConfidenceInputs:
    heat_index: int
    heat_action: str
    classifier_action: str
    classifier_confidence: float
    market_type: str = "total"
    live_total_delta: float = 0.0
    minutes_remaining: float = 24.0
    primary_scorers_count: int = 0
    pace_support_score: float = 0.0
    shooting_heat_score: float = 0.0
    recommendation: Optional[str] = None


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


def compute_confidence_score(inp: ConfidenceInputs) -> Dict:
    score = 0.0
    reasons: List[str] = []

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

    if inp.market_type in {"total", "team_total"} and abs(inp.live_total_delta) >= 10:
        score += 6
        reasons.append("meaningful repricing delta supports edge clarity: +6")
    elif inp.market_type in {"total", "team_total"} and abs(inp.live_total_delta) < 4:
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

    return {
        "confidence_score": score,
        "confidence_tier": tier_name,
        "confidence_emoji": tier_emoji,
        "recommended_units": recommended_units,
        "reasons": reasons,
    }


def autofill_from_bridge_payload(payload: Dict) -> Dict:
    heat_result = payload.get("heat_result", {})
    classifier_result = payload.get("classifier_result", {})
    auto_adjustment = payload.get("auto_adjustment", {})
    heat_input = payload.get("heat_input", {})

    inp = ConfidenceInputs(
        heat_index=int(heat_result.get("heat_index", 0) or 0),
        heat_action=heat_result.get("action_tag", "NO_EDGE"),
        classifier_action=classifier_result.get("action_bias", "NO_FIRE"),
        classifier_confidence=float(classifier_result.get("confidence", 0.0) or 0.0),
        market_type=payload.get("market_type", "total"),
        live_total_delta=float((heat_input.get("live_total", 0.0) or 0.0) - (heat_input.get("closing_total", 0.0) or 0.0)),
        minutes_remaining=float(heat_input.get("minutes_remaining", 24.0) or 24.0),
        primary_scorers_count=int(heat_input.get("primary_scorers_count", 0) or 0),
        pace_support_score=float(heat_result.get("pace_support_score", 0.0) or 0.0),
        shooting_heat_score=float(heat_result.get("shooting_heat_score", 0.0) or 0.0),
        recommendation=auto_adjustment.get("recommendation"),
    )

    result = compute_confidence_score(inp)
    return {
        "autofilled_inputs": asdict(inp),
        "confidence_result": result,
    }


def prompt_multiline_json() -> Dict:
    print("Paste full bridge payload JSON, then enter an empty line twice:")
    lines: List[str] = []
    blank_count = 0
    while True:
        line = input()
        if line.strip() == "":
            blank_count += 1
            if blank_count >= 2:
                break
        else:
            blank_count = 0
        lines.append(line)
    raw = "\n".join(lines).strip()
    if not raw:
        raise ValueError("No JSON payload pasted.")
    return json.loads(raw)


def main() -> None:
    print("=== SharpEdge Confidence Autofill ===")
    payload = prompt_multiline_json()
    result = autofill_from_bridge_payload(payload)

    print("\n=== AUTOFILLED CONFIDENCE PAYLOAD ===")
    print(json.dumps(result, indent=2))

    confidence = result["confidence_result"]
    print("\n=== SHARPEDGE CONFIDENCE OUTPUT ===")
    print(f"Tier: {confidence['confidence_emoji']} {confidence['confidence_tier']}")
    print(f"Score: {confidence['confidence_score']}")
    print(f"Recommended Size: {confidence['recommended_units']}")
    for reason in confidence["reasons"]:
        print(f"- {reason}")


if __name__ == "__main__":
    main()
