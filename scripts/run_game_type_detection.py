from modules.game_type_detection import build_orl_det_example, build_phx_okc_example


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


if __name__ == "__main__":
    print_result("ORL @ DET", build_orl_det_example())
    print_result("PHX @ OKC", build_phx_okc_example())
