from modules.rebound_monte_carlo import (
    build_hou_lal_game3_context,
    build_hou_lal_game3_players,
    simulate_player_rebounds,
    simulate_rebound_combo,
)


def print_player_card(result: dict) -> None:
    print("=" * 64)
    print(f"PLAYER: {result['player']}")
    print(f"LINE: {result['line']}+")
    print(f"MEAN: {result['mean']}")
    print(f"MEDIAN: {result['median']}")
    print(f"HIT PROBABILITY: {result['hit_probability']:.2%}")
    print(f"EXPECTED CHANCES: {result['expected_chances']}")
    print(f"CONVERSION: {result['conversion']:.2%}")
    print(f"RANGE: {result['min']} to {result['max']}")


def print_combo_card(result: dict) -> None:
    print("\n" + "#" * 64)
    print("COMBO SUMMARY")
    print(f"COMBO HIT PROBABILITY: {result['combo_hit_probability']:.2%}")
    print("LEGS:")
    for leg in result["leg_summaries"]:
        print(
            f"- {leg['player']} {leg['line']}+ | mean={leg['mean']} | "
            f"median={leg['median']} | hit={leg['hit_probability']:.2%}"
        )
    print("#" * 64)


def main() -> None:
    context = build_hou_lal_game3_context()
    players = build_hou_lal_game3_players()

    print("SharpEdge Rebound Monte Carlo Runner")
    print("Context:", context["notes"])
    print()

    player_results = []
    for player in players:
        result = simulate_player_rebounds(player, context, iterations=10000)
        player_results.append(result)
        print_player_card(result)

    combo_players = [
        next(player for player in players if player["name"] == "Tari Eason"),
        next(player for player in players if player["name"] == "LeBron James"),
    ]
    combo_result = simulate_rebound_combo(combo_players, context, iterations=10000)
    print_combo_card(combo_result)


if __name__ == "__main__":
    main()
