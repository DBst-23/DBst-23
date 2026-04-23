from modules.game_type_detection import detect_game_types


def print_result(title: str, result: dict) -> None:
    print(f"\n=== {title} ===")
    print(f"Primary Game Type: {result['primary_game_type']}")
    print("\nTags:")
    for tag in result["tags"]:
        print(f"- {tag}")

    print("\nScores:")
    for key, value in result["scores"].items():
        print(f"- {key}: {value}")

    print("\nBetting Implications:")
    for key, value in result["betting_implications"].items():
        print(f"- {key}: {value}")

    print("\nNotes:")
    for note in result["notes"]:
        print(f"- {note}")


def build_live_sample() -> dict:
    return detect_game_types(
        halftime_total_points=122,
        favorite_halftime_points=65,
        underdog_halftime_points=57,
        live_full_game_total=227.5,
        live_favorite_team_total=122.5,
        live_underdog_team_total=105.5,
        live_spread=15.5,
        favorite_off_rtg_1h=132.7,
        underdog_off_rtg_1h=116.3,
        favorite_ts_1h=62.7,
        underdog_ts_1h=62.3,
        favorite_tov_1h=4,
        underdog_tov_1h=11,
        favorite_oreb_final=12,
        underdog_oreb_final=15,
        favorite_reb_final=40,
        underdog_reb_final=44,
        favorite_boxouts=0.0,
        underdog_boxouts=5.0,
    ).to_dict()


if __name__ == "__main__":
    print_result("LIVE SAMPLE", build_live_sample())
