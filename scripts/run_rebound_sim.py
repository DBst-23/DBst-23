from modules.rebound_monte_carlo import (
    simulate_player_rebounds,
    simulate_rebound_combo,
    build_hou_lal_game3_context,
    build_hou_lal_game3_players,
)

# Load base context + players
context = build_hou_lal_game3_context()
players = build_hou_lal_game3_players()

# --- SINGLE PLAYER RUNS ---
print("\n=== PLAYER SIM RESULTS ===\n")

for p in players:
    result = simulate_player_rebounds(p, context, iterations=10000)

    print(f"{result['player']} | Line: {result['line']}")
    print(f"Mean: {result['mean']} | Median: {result['median']}")
    print(f"Hit Prob: {result['hit_probability']}")
    print("-" * 40)


# --- COMBO RUN ---
print("\n=== COMBO SIM (EASON + LEBRON) ===\n")

combo = simulate_rebound_combo(
    [players[0], players[1]],  # Tari + LeBron
    context,
    iterations=10000
)

print("Combo Hit Probability:", combo["combo_hit_probability"])

for leg in combo["leg_summaries"]:
    print(f"{leg['player']} -> {leg['hit_probability']}")
