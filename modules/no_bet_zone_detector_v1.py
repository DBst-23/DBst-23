from dataclasses import dataclass


@dataclass
class BetProfile:
    player: str
    stat: str
    line: float
    mean_projection: float
    median_projection: float
    win_probability: float
    player_archetype: str
    under_play: bool
    suppression_factors: int
    projected_minutes_uncertainty: str
    required_game_script: str
    market_consensus_support: str
    platform_outlier_only: bool


def classify_bet_zone(profile: BetProfile) -> str:
    edge_delta = abs(profile.mean_projection - profile.line)

    if edge_delta < 0.6 and profile.win_probability < 0.56:
        return "NO_BET_ZONE"

    if profile.player_archetype in ["ELITE_CENTER", "PRIMARY_HUB", "CEILING_REBOUNDER"] and profile.under_play:
        if profile.suppression_factors < 2:
            return "CEILING_TRAP"

    if profile.projected_minutes_uncertainty.upper() == "HIGH":
        return "ROLE_UNSTABLE"

    if profile.required_game_script in ["BLOWOUT_ONLY", "LOW_MISS_ONLY", "HOT_SHOOTING_ONLY"]:
        return "SCRIPT_DEPENDENT"

    if (
        profile.market_consensus_support.upper() == "WEAK"
        and profile.platform_outlier_only
        and profile.win_probability < 0.58
    ):
        return "MARKET_ONLY_EDGE"

    if profile.win_probability >= 0.58 and edge_delta >= 0.8:
        return "PLAYABLE_EDGE"

    return "THIN_EDGE"


def explain_bet_zone(profile: BetProfile) -> dict:
    edge_delta = abs(profile.mean_projection - profile.line)
    classification = classify_bet_zone(profile)

    return {
        "player": profile.player,
        "stat": profile.stat,
        "line": profile.line,
        "mean_projection": profile.mean_projection,
        "median_projection": profile.median_projection,
        "win_probability": profile.win_probability,
        "edge_delta": round(edge_delta, 3),
        "classification": classification,
    }
