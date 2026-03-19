from __future__ import annotations

from typing import Any, Dict, List

from modules.chaos_bet_sizing_engine import compute_recommended_stake
from modules.rebound_kill_switch_chaos import (
    apply_chaos_kill_switch_to_live_result,
    compute_chaos_kill_switch,
    should_block_live_rebound_entry_chaos_aware,
)
from modules.liveflow_rebound_engine import project_live_rebounds


def compute_live_execution_packet(
    player_name: str,
    player_position: str,
    player_live: Dict[str, Any],
    team_players_live: List[Dict[str, Any]],
    pregame_mean: float,
    pregame_median: float,
    line_live: float,
    expected_minutes: float,
    live_state: Dict[str, Any],
    bankroll: float,
    base_unit_size: float,
    pregame_environment: Dict[str, Any],
    recommendation_hint: str = "",
    max_units: float = 2.0,
) -> Dict[str, Any]:
    base_result = project_live_rebounds(
        player_live=player_live,
        team_players_live=team_players_live,
        pregame_mean=pregame_mean,
        pregame_median=pregame_median,
        line_live=line_live,
        expected_minutes=expected_minutes,
        live_state=live_state,
    )

    chaos_guard = compute_chaos_kill_switch(
        player_name=player_name,
        player_position=player_position,
        team_players_live=team_players_live,
        live_state=live_state,
        pregame_environment=pregame_environment,
    )

    adjusted_result = apply_chaos_kill_switch_to_live_result(
        result=base_result,
        chaos_guard=chaos_guard,
    )

    decision = should_block_live_rebound_entry_chaos_aware(
        result=adjusted_result,
        chaos_guard=chaos_guard,
    )

    recommendation = str(decision.get("recommendation") or recommendation_hint or "")

    sizing = compute_recommended_stake(
        bankroll=bankroll,
        base_unit_size=base_unit_size,
        player_position=player_position,
        win_prob=float(adjusted_result.get("win_prob", 0.0)),
        edge=float(adjusted_result.get("edge", 0.0)),
        recommendation=recommendation,
        chaos_active=bool(adjusted_result.get("chaos_active", False)),
        chaos_tag=str(adjusted_result.get("chaos_tag", "OREB_CHAOS_LOW")),
        chaos_override=str(adjusted_result.get("chaos_override", "NONE")),
        kill_switch_active=bool(adjusted_result.get("kill_switch_active", False)),
        max_units=max_units,
    )

    execution_allowed = (not bool(decision.get("block", False))) and sizing.get("recommended_stake", 0) > 0

    return {
        "player": player_name,
        "position": player_position,
        "line_live": float(line_live),
        "projection": adjusted_result,
        "guard": chaos_guard,
        "decision": decision,
        "sizing": sizing,
        "execution_allowed": execution_allowed,
        "execution_action": "QUEUE_BET" if execution_allowed else "DO_NOT_BET",
    }


def enforce_liveflow_single_bet_rule(
    execution_packets: List[Dict[str, Any]],
    max_open_bets_per_market: int = 1,
) -> Dict[str, Any]:
    approved: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []

    ranked = sorted(
        execution_packets,
        key=lambda packet: (
            float(packet.get("sizing", {}).get("recommended_units", 0.0)),
            float(packet.get("projection", {}).get("win_prob", 0.0)),
            float(packet.get("projection", {}).get("edge", 0.0)),
        ),
        reverse=True,
    )

    for packet in ranked:
        if not packet.get("execution_allowed", False):
            packet["execution_action"] = "DO_NOT_BET"
            rejected.append(packet)
            continue

        if len(approved) >= max_open_bets_per_market:
            packet["execution_action"] = "RISK_CLUSTER_LOCK_BLOCK"
            rejected.append(packet)
            continue

        approved.append(packet)

    return {
        "approved": approved,
        "rejected": rejected,
        "max_open_bets_per_market": max_open_bets_per_market,
    }


if __name__ == "__main__":
    sample_packet = compute_live_execution_packet(
        player_name="Rudy Gobert",
        player_position="C",
        player_live={
            "player_live_minutes": 18,
            "player_live_rebounds": 7,
            "player_live_points": 8,
            "player_live_assists": 1,
            "player_live_fouls": 1,
        },
        team_players_live=[
            {"name": "Rudy Gobert", "live_minutes": 18, "live_rebounds": 7, "expected_minutes": 33, "rebound_rate": 0.36},
            {"name": "Julius Randle", "live_minutes": 18, "live_rebounds": 3, "expected_minutes": 35, "rebound_rate": 0.22},
            {"name": "Wing A", "live_minutes": 16, "live_rebounds": 2, "expected_minutes": 30, "rebound_rate": 0.12},
        ],
        pregame_mean=13.1,
        pregame_median=13.0,
        line_live=12.5,
        expected_minutes=33,
        live_state={
            "quarter": 2,
            "time_remaining_sec": 720,
            "team_rebounds_for": 24,
            "team_rebounds_against": 20,
            "spread_live": -6.5,
            "fg_pct_for": 0.47,
            "fg_pct_against": 0.42,
        },
        bankroll=500.0,
        base_unit_size=10.0,
        pregame_environment={
            "opponent_fg_pct_allowed": 0.43,
            "opponent_three_pa_allowed": 38,
            "own_team_bench_big_minutes": 20,
            "opponent_def_reb_pct": 0.69,
            "opponent_oreb_allowed": 12,
            "projected_pace": 100,
            "opponent_long_rebound_profile": 0.68,
        },
        recommendation_hint="OREB_CHAOS_BIG_BOOST",
    )

    print(sample_packet)
