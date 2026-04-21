import json
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, List


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


@dataclass
class TeamStats:
    team_name: str
    points: int
    fg_made: int
    fg_attempted: int
    three_made: int
    three_attempted: int
    ft_made: int
    ft_attempted: int
    offensive_rebounds: int
    turnovers: int
    fastbreak_points: int
    assists: int
    top_scorers: List[int]


@dataclass
class LiveFlowHeatInput:
    closing_total: float
    live_total: float
    current_total: int
    minutes_remaining: float
    current_fg_pct: float
    current_3p_pct: float
    current_ft_pct: float
    expected_fg_pct: float
    expected_3p_pct: float
    expected_ft_pct: float
    turnovers_total: int
    offensive_rebounds_total: int
    free_throw_attempts_total: int
    fastbreak_points_total: int
    pace_z: float = 0.0
    oreb_z: float = 0.0
    fta_rate_z: float = 0.0
    fastbreak_z: float = 0.0
    primary_scorers_count: int = 0
    assist_rate_delta: float = 0.0


@dataclass
class HalftimeTeamStats:
    team: str
    points: int
    fg_pct: float
    three_pct: float
    ftm: int
    fta: int
    rebounds: int
    offensive_rebounds: int
    assists: int
    turnovers: int
    second_chance_points: int = 0
    fastbreak_points: int = 0
    paint_points: int = 0
    leading_scorers: List[int] = None


@dataclass
class HalftimeEnvironmentInput:
    game: str
    closing_spread: float
    closing_total: float
    halftime_live_spread: float
    halftime_live_total: float
    halftime_score_team1: int
    halftime_score_team2: int
    team1_stats: HalftimeTeamStats
    team2_stats: HalftimeTeamStats


def prompt_float(label: str, default: Optional[float] = None) -> Optional[float]:
    suffix = f" [{default}]" if default is not None else ""
    raw = input(f"{label}{suffix}: ").strip()
    if raw == "":
        return default
    return float(raw)


def prompt_int(label: str, default: int = 0) -> int:
    raw = input(f"{label} [{default}]: ").strip()
    return int(raw) if raw else int(default)


def prompt_text(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    raw = input(f"{label}{suffix}: ").strip()
    return raw if raw else default


def prompt_scores(team_name: str) -> List[int]:
    raw = input(f"Top scorer points for {team_name}, comma-separated: ").strip()
    if not raw:
        return []
    return [int(x.strip()) for x in raw.split(",") if x.strip()]


def pct(made: int, attempted: int) -> float:
    if attempted <= 0:
        return 0.0
    return round((made / attempted) * 100.0, 2)


def combined_fg_pct(team_a: TeamStats, team_b: TeamStats) -> float:
    return pct(team_a.fg_made + team_b.fg_made, team_a.fg_attempted + team_b.fg_attempted)


def combined_3p_pct(team_a: TeamStats, team_b: TeamStats) -> float:
    return pct(team_a.three_made + team_b.three_made, team_a.three_attempted + team_b.three_attempted)


def combined_ft_pct(team_a: TeamStats, team_b: TeamStats) -> float:
    return pct(team_a.ft_made + team_b.ft_made, team_a.ft_attempted + team_b.ft_attempted)


def build_live_odds_snapshot() -> LiveOddsSnapshot:
    print("=== SharpEdge Odds Ingestion ===")
    game_label = prompt_text("Game label", "Team A @ Team B")
    sportsbook = prompt_text("Sportsbook / source", "manual_entry")
    return LiveOddsSnapshot(
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


def prompt_team_stats(team_name: str) -> TeamStats:
    print(f"\n=== Enter stats for {team_name} ===")
    return TeamStats(
        team_name=team_name,
        points=prompt_int("Points"),
        fg_made=prompt_int("FG made"),
        fg_attempted=prompt_int("FG attempted"),
        three_made=prompt_int("3PT made"),
        three_attempted=prompt_int("3PT attempted"),
        ft_made=prompt_int("FT made"),
        ft_attempted=prompt_int("FT attempted"),
        offensive_rebounds=prompt_int("Offensive rebounds"),
        turnovers=prompt_int("Turnovers"),
        fastbreak_points=prompt_int("Fastbreak points"),
        assists=prompt_int("Assists"),
        top_scorers=prompt_scores(team_name),
    )


def compute_liveflow_heat_index(inp: LiveFlowHeatInput) -> Dict:
    fg_delta = max(0.0, inp.current_fg_pct - inp.expected_fg_pct)
    tp_delta = max(0.0, inp.current_3p_pct - inp.expected_3p_pct)
    ft_delta = max(0.0, inp.current_ft_pct - inp.expected_ft_pct)

    shooting_heat_score = (
        fg_delta * 0.8 +
        tp_delta * 1.4 +
        ft_delta * 0.3
    )

    pace_support_score = (
        inp.pace_z * 1.2 +
        inp.oreb_z * 0.8 +
        inp.fta_rate_z * 0.7 +
        inp.fastbreak_z * 0.6
    )

    clean_possession_penalty = 0
    if inp.turnovers_total <= 10:
        clean_possession_penalty += 8
    if inp.offensive_rebounds_total <= 10:
        clean_possession_penalty += 6
    if inp.free_throw_attempts_total <= 20:
        clean_possession_penalty += 5

    market_inflation = max(0.0, inp.live_total - inp.closing_total)
    market_inflation_score = market_inflation * 2.0

    required_remaining_points = inp.live_total - inp.current_total
    baseline_ppm = inp.closing_total / 48.0
    required_ppm = required_remaining_points / max(inp.minutes_remaining, 1.0)

    if required_ppm > baseline_ppm + 0.25:
        market_inflation_score += 10

    star_sustainability_offset = 0
    if inp.primary_scorers_count >= 3:
        star_sustainability_offset += 8
    if inp.assist_rate_delta >= 0:
        star_sustainability_offset += 5
    if pace_support_score >= 12:
        star_sustainability_offset += 5

    heat_index = (
        shooting_heat_score +
        market_inflation_score +
        clean_possession_penalty -
        pace_support_score -
        star_sustainability_offset
    )

    heat_index = max(0, min(100, round(heat_index)))

    if heat_index < 25:
        classification = "COOL"
        action_tag = "NO_EDGE"
    elif heat_index < 45:
        classification = "WARM"
        action_tag = "WATCH_UNDER"
    elif heat_index < 65:
        classification = "HOT"
        action_tag = "UNDER_TRIGGER"
    else:
        classification = "EXTREME_HEAT"
        action_tag = "UNDER_TRIGGER"

    if pace_support_score >= 14 and inp.primary_scorers_count >= 3 and inp.free_throw_attempts_total >= 20:
        action_tag = "DO_NOT_FADE"

    return {
        "heat_index": heat_index,
        "classification": classification,
        "action_tag": action_tag,
        "shooting_heat_score": round(shooting_heat_score, 2),
        "market_inflation_score": round(market_inflation_score, 2),
        "clean_possession_penalty": clean_possession_penalty,
        "pace_support_score": round(pace_support_score, 2),
        "star_sustainability_offset": star_sustainability_offset,
        "required_remaining_points": round(required_remaining_points, 2),
        "required_points_per_minute": round(required_ppm, 3),
    }


def _safe_avg(values: List[float]) -> float:
    vals = [v for v in values if v is not None]
    return sum(vals) / len(vals) if vals else 0.0


def _count_double_digit_scorers(points_list: List[int]) -> int:
    return sum(1 for p in (points_list or []) if p >= 10)


def classify_environment(inp: HalftimeEnvironmentInput) -> Dict:
    notes: List[str] = []
    inflation_delta = round(inp.halftime_live_total - inp.closing_total, 2)
    score_total = inp.halftime_score_team1 + inp.halftime_score_team2

    t1 = inp.team1_stats
    t2 = inp.team2_stats

    combined_assists = t1.assists + t2.assists
    combined_turnovers = t1.turnovers + t2.turnovers
    combined_fta = t1.fta + t2.fta
    combined_oreb = t1.offensive_rebounds + t2.offensive_rebounds
    avg_fg = _safe_avg([t1.fg_pct, t2.fg_pct])
    avg_three = _safe_avg([t1.three_pct, t2.three_pct])
    dbl_fig_scorers = _count_double_digit_scorers(t1.leading_scorers or []) + _count_double_digit_scorers(t2.leading_scorers or [])

    high_assist_environment = combined_assists >= 22
    balanced_scoring = dbl_fig_scorers >= 4
    whistle_heavy = combined_fta >= 26
    strong_extra_possessions = combined_oreb >= 9 or combined_turnovers >= 18
    hot_shooting = avg_fg >= 51.0 or avg_three >= 41.0
    cold_shooting = avg_fg <= 42.0 and avg_three <= 31.0

    continuation_score = 0
    regression_score = 0
    suppression_score = 0
    recovery_score = 0

    if inflation_delta >= 8:
        notes.append(f"halftime live total inflated by {inflation_delta} vs close")
        if high_assist_environment:
            continuation_score += 2
            notes.append("assist structure supports sustainable offense")
        else:
            regression_score += 1
            notes.append("assist profile not strong enough to fully validate inflation")

        if balanced_scoring:
            continuation_score += 2
            notes.append("multi-source scoring confirmed")
        else:
            regression_score += 1
            notes.append("scoring concentrated in limited sources")

        if whistle_heavy:
            regression_score += 1
            notes.append("free-throw volume may be inflating score")

        if strong_extra_possessions:
            continuation_score += 1
            notes.append("extra possessions support continuation")

        if hot_shooting and not high_assist_environment:
            regression_score += 2
            notes.append("hot shooting without strong ball movement suggests fragility")
        elif hot_shooting:
            continuation_score += 1
            notes.append("hot shooting supported by offensive structure")

        if continuation_score >= regression_score + 2:
            env = "REAL_INFLATION"
            confidence = min(0.90, 0.55 + 0.05 * continuation_score)
            action_bias = "DO_NOT_AUTO_FADE"
        elif regression_score >= continuation_score + 2:
            env = "FAKE_INFLATION"
            confidence = min(0.90, 0.55 + 0.05 * regression_score)
            action_bias = "LEAN_UNDER"
        else:
            env = "MIXED_NO_FIRE"
            confidence = 0.58
            action_bias = "NO_FIRE"

    elif inflation_delta <= -8:
        notes.append(f"halftime live total suppressed by {abs(inflation_delta)} vs close")
        if cold_shooting:
            recovery_score += 2
            notes.append("cold shooting suggests possible offensive rebound / scoring recovery")
        else:
            suppression_score += 1
            notes.append("shooting profile does not strongly indicate fake suppression")

        if strong_extra_possessions:
            recovery_score += 1
            notes.append("extra possessions suggest score may be artificially low")
        else:
            suppression_score += 1
            notes.append("low extra-possession pressure supports real suppression")

        if high_assist_environment:
            recovery_score += 1
            notes.append("offense still generating creation despite low score")
        else:
            suppression_score += 1
            notes.append("limited ball movement supports slow environment")

        if recovery_score >= suppression_score + 2:
            env = "FAKE_SUPPRESSION"
            confidence = min(0.90, 0.55 + 0.05 * recovery_score)
            action_bias = "LEAN_OVER"
        elif suppression_score >= recovery_score + 2:
            env = "REAL_SUPPRESSION"
            confidence = min(0.90, 0.55 + 0.05 * suppression_score)
            action_bias = "LEAN_UNDER"
        else:
            env = "MIXED_NO_FIRE"
            confidence = 0.58
            action_bias = "NO_FIRE"

    else:
        env = "MIXED_NO_FIRE"
        confidence = 0.52
        action_bias = "NO_FIRE"
        notes.append("repricing delta not extreme enough for strong halftime classification")

    return {
        "environment_type": env,
        "confidence": round(confidence, 2),
        "inflation_delta": inflation_delta,
        "score_total_at_half": score_total,
        "notes": notes,
        "action_bias": action_bias,
    }


def build_auto_adjustment(heat_result: Dict, classifier_result: Dict) -> Dict:
    recommendation = "NO_FIRE"
    weight_delta = 0.0
    confidence_tier = "LOW"
    reasons: List[str] = []

    heat_action = heat_result.get("action_tag", "NO_EDGE")
    classifier_action = classifier_result.get("action_bias", "NO_FIRE")
    heat_index = int(heat_result.get("heat_index", 0) or 0)
    classifier_conf = float(classifier_result.get("confidence", 0.0) or 0.0)

    if heat_action == "UNDER_TRIGGER" and classifier_action == "LEAN_UNDER":
        recommendation = "FIRE_UNDER"
        weight_delta = 0.10
        confidence_tier = "HIGH" if heat_index >= 60 and classifier_conf >= 0.65 else "MEDIUM"
        reasons.append("heat index and halftime classifier aligned on under")
    elif heat_action == "DO_NOT_FADE" or classifier_action == "DO_NOT_AUTO_FADE":
        recommendation = "STAY_OFF_CONTINUATION"
        weight_delta = -0.05
        confidence_tier = "MEDIUM"
        reasons.append("continuation environment detected")
    elif heat_action == "WATCH_UNDER" and classifier_action == "LEAN_UNDER":
        recommendation = "WATCH_UNDER_BETTER_NUMBER"
        weight_delta = 0.03
        confidence_tier = "MEDIUM"
        reasons.append("partial under alignment, wait for better price")
    elif heat_action == "NO_EDGE" and classifier_action == "NO_FIRE":
        recommendation = "NO_FIRE"
        weight_delta = 0.0
        confidence_tier = "LOW"
        reasons.append("no alignment or signal strength")
    else:
        recommendation = "MIXED_NO_FIRE"
        weight_delta = -0.02
        confidence_tier = "LOW"
        reasons.append("signals mixed across modules")

    return {
        "recommendation": recommendation,
        "weight_delta": round(weight_delta, 3),
        "confidence_tier": confidence_tier,
        "reasons": reasons,
    }


def main() -> None:
    odds = build_live_odds_snapshot()

    print("\n=== Current Box Score Capture ===")
    team_a = prompt_team_stats("Team A")
    team_b = prompt_team_stats("Team B")

    minutes_remaining = prompt_float("Minutes remaining", 24.0)
    expected_fg_pct = prompt_float("Expected FG%", 46.0)
    expected_3p_pct = prompt_float("Expected 3P%", 36.0)
    expected_ft_pct = prompt_float("Expected FT%", 78.0)
    pace_z = prompt_float("Pace z-score", 0.0)
    oreb_z = prompt_float("Offensive rebound z-score", 0.0)
    fta_rate_z = prompt_float("FTA rate z-score", 0.0)
    fastbreak_z = prompt_float("Fastbreak z-score", 0.0)
    assist_rate_delta = prompt_float("Assist rate delta", 0.0)

    primary_scorers_count = sum(1 for p in (team_a.top_scorers + team_b.top_scorers) if p >= 10)

    heat_input = LiveFlowHeatInput(
        closing_total=odds.closing_total,
        live_total=odds.live_total,
        current_total=team_a.points + team_b.points,
        minutes_remaining=minutes_remaining,
        current_fg_pct=combined_fg_pct(team_a, team_b),
        current_3p_pct=combined_3p_pct(team_a, team_b),
        current_ft_pct=combined_ft_pct(team_a, team_b),
        expected_fg_pct=expected_fg_pct,
        expected_3p_pct=expected_3p_pct,
        expected_ft_pct=expected_ft_pct,
        turnovers_total=team_a.turnovers + team_b.turnovers,
        offensive_rebounds_total=team_a.offensive_rebounds + team_b.offensive_rebounds,
        free_throw_attempts_total=team_a.ft_attempted + team_b.ft_attempted,
        fastbreak_points_total=team_a.fastbreak_points + team_b.fastbreak_points,
        pace_z=pace_z,
        oreb_z=oreb_z,
        fta_rate_z=fta_rate_z,
        fastbreak_z=fastbreak_z,
        primary_scorers_count=primary_scorers_count,
        assist_rate_delta=assist_rate_delta,
    )

    classifier_input = HalftimeEnvironmentInput(
        game=odds.game_label,
        closing_spread=odds.closing_spread,
        closing_total=odds.closing_total,
        halftime_live_spread=odds.live_spread,
        halftime_live_total=odds.live_total,
        halftime_score_team1=team_a.points,
        halftime_score_team2=team_b.points,
        team1_stats=HalftimeTeamStats(
            team=team_a.team_name,
            points=team_a.points,
            fg_pct=pct(team_a.fg_made, team_a.fg_attempted),
            three_pct=pct(team_a.three_made, team_a.three_attempted),
            ftm=team_a.ft_made,
            fta=team_a.ft_attempted,
            rebounds=team_a.offensive_rebounds,
            offensive_rebounds=team_a.offensive_rebounds,
            assists=team_a.assists,
            turnovers=team_a.turnovers,
            fastbreak_points=team_a.fastbreak_points,
            leading_scorers=team_a.top_scorers,
        ),
        team2_stats=HalftimeTeamStats(
            team=team_b.team_name,
            points=team_b.points,
            fg_pct=pct(team_b.fg_made, team_b.fg_attempted),
            three_pct=pct(team_b.three_made, team_b.three_attempted),
            ftm=team_b.ft_made,
            fta=team_b.ft_attempted,
            rebounds=team_b.offensive_rebounds,
            offensive_rebounds=team_b.offensive_rebounds,
            assists=team_b.assists,
            turnovers=team_b.turnovers,
            fastbreak_points=team_b.fastbreak_points,
            leading_scorers=team_b.top_scorers,
        ),
    )

    heat_result = compute_liveflow_heat_index(heat_input)
    classifier_result = classify_environment(classifier_input)
    auto_adjustment = build_auto_adjustment(heat_result, classifier_result)

    payload = {
        "odds_snapshot": asdict(odds),
        "team_a": asdict(team_a),
        "team_b": asdict(team_b),
        "heat_input": asdict(heat_input),
        "classifier_input": asdict(classifier_input),
        "heat_result": heat_result,
        "classifier_result": classifier_result,
        "auto_adjustment": auto_adjustment,
    }

    print("\n=== FULL LIVEFLOW ODDS + BRIDGE PAYLOAD ===")
    print(json.dumps(payload, indent=2))

    print("\n=== SHARPEDGE EXECUTION SIGNAL ===")
    print(f"Recommendation: {auto_adjustment['recommendation']}")
    print(f"Confidence Tier: {auto_adjustment['confidence_tier']}")
    print(f"Weight Delta: {auto_adjustment['weight_delta']}")
    for reason in auto_adjustment['reasons']:
        print(f"- {reason}")


if __name__ == "__main__":
    main()
