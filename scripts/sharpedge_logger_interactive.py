from __future__ import annotations

import json
from typing import List

from scripts.sharpedge_logger_autocommit import (
    auto_commit,
    log_bet,
    log_postmortem,
    log_settlement,
    parse_csv_list,
)


def ask(prompt: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{prompt}{suffix}: ").strip()
    return value if value else default


def ask_bool(prompt: str, default: bool = False) -> bool:
    hint = "Y/n" if default else "y/N"
    value = input(f"{prompt} ({hint}): ").strip().lower()
    if not value:
        return default
    return value in {"y", "yes", "true", "1"}


def ask_int(prompt: str, default: int | None = None) -> int:
    while True:
        raw = ask(prompt, str(default) if default is not None else "")
        try:
            return int(raw)
        except ValueError:
            print("Enter a whole number.")


def ask_float(prompt: str, default: float | None = None) -> float:
    while True:
        raw = ask(prompt, str(default) if default is not None else "")
        try:
            return float(raw)
        except ValueError:
            print("Enter a valid number.")


def ask_pipe_list(prompt: str, default: str = "") -> List[str]:
    raw = ask(prompt, default)
    return parse_csv_list(raw)


def handle_place() -> dict:
    print("\n=== SharpEdge Place Bet Logger ===")
    date_str = ask("Date (YYYY-MM-DD)")
    sport = ask("Sport", "NBA")
    matchup = ask("Matchup (Example: PHX @ MIN)")
    mode = ask("Mode", "LiveFlow")
    card_type = ask("Card Type", "2-Pick")
    platform = ask("Platform", "Underdog")
    market = ask("Market", "Rebounds")
    legs = ask_pipe_list("Legs separated by |")
    stake = ask_float("Stake")
    payout = ask_float("Expected payout")
    sequence = ask_int("Sequence number for the day")
    boost_tag = ask("Boost tag", "None")
    copy_id = ask("Copy ID", "")
    edge_tags = ask_pipe_list("Edge tags separated by |", "")
    model_tags = ask_pipe_list("Model tags separated by |", "")
    batch = ask("Batch", "001")
    auto_commit_flag = ask_bool("Auto-commit to Git", True)
    git_push_flag = ask_bool("Auto-push after commit", False) if auto_commit_flag else False
    commit_message = ask("Custom commit message", "") if auto_commit_flag else ""

    entry, out_file = log_bet(
        date_str=date_str,
        sport=sport,
        matchup=matchup,
        mode=mode,
        card_type=card_type,
        platform=platform,
        market=market,
        legs=legs,
        stake=stake,
        payout_expected=payout,
        sequence=sequence,
        boost_tag=boost_tag,
        copy_id=copy_id,
        edge_tags=edge_tags,
        model_tags=model_tags,
        batch=batch,
    )

    output = {
        "entry": entry.__dict__,
        "file": str(out_file),
    }

    if auto_commit_flag:
        message = commit_message.strip() or f"Log placed bet {entry.entry_id}"
        output["git"] = auto_commit([out_file], message, push=git_push_flag)

    return output


def handle_settle() -> dict:
    print("\n=== SharpEdge Settlement Logger ===")
    entry_id = ask("Entry ID")
    date_str = ask("Date (YYYY-MM-DD)")
    sport = ask("Sport", "NBA")
    matchup = ask("Matchup")
    result = ask("Result", "Win")
    legs_hit = ask_int("Legs hit", 1)
    legs_miss = ask_int("Legs missed", 0)
    stake = ask_float("Stake")
    return_actual = ask_float("Actual return")
    final_score = ask("Final score")
    notes = ask("Settlement notes")
    batch = ask("Batch", "001")
    auto_commit_flag = ask_bool("Auto-commit to Git", True)
    git_push_flag = ask_bool("Auto-push after commit", False) if auto_commit_flag else False
    commit_message = ask("Custom commit message", "") if auto_commit_flag else ""

    entry, out_file = log_settlement(
        entry_id=entry_id,
        date_str=date_str,
        sport=sport,
        matchup=matchup,
        result=result,
        legs_hit=legs_hit,
        legs_miss=legs_miss,
        stake=stake,
        return_actual=return_actual,
        final_score=final_score,
        settlement_notes=notes,
        batch=batch,
    )

    output = {
        "entry": entry.__dict__,
        "file": str(out_file),
    }

    if auto_commit_flag:
        message = commit_message.strip() or f"Log settled bet {entry.entry_id}"
        output["git"] = auto_commit([out_file], message, push=git_push_flag)

    return output


def handle_postmortem() -> dict:
    print("\n=== SharpEdge Postmortem Logger ===")
    entry_id = ask("Entry ID")
    date_str = ask("Date (YYYY-MM-DD)")
    sport = ask("Sport", "NBA")
    matchup = ask("Matchup")
    postmortem_type = ask("Postmortem type", "LiveFlow")
    result_type = ask("Result type", "Win")
    hit_legs = ask_pipe_list("Hit legs separated by |", "")
    missed_legs = ask_pipe_list("Missed legs separated by |", "")
    environment_tags = ask_pipe_list("Environment tags separated by |", "")
    variance_tags = ask_pipe_list("Variance tags separated by |", "")
    model_notes = ask("Model notes")
    patch_required = ask_bool("Patch required", False)
    batch = ask("Batch", "001")
    auto_commit_flag = ask_bool("Auto-commit to Git", True)
    git_push_flag = ask_bool("Auto-push after commit", False) if auto_commit_flag else False
    commit_message = ask("Custom commit message", "") if auto_commit_flag else ""

    entry, out_file = log_postmortem(
        entry_id=entry_id,
        date_str=date_str,
        sport=sport,
        matchup=matchup,
        postmortem_type=postmortem_type,
        result_type=result_type,
        hit_legs=hit_legs,
        missed_legs=missed_legs,
        environment_tags=environment_tags,
        variance_tags=variance_tags,
        model_notes=model_notes,
        patch_required=patch_required,
        batch=batch,
    )

    output = {
        "entry": entry.__dict__,
        "file": str(out_file),
    }

    if auto_commit_flag:
        message = commit_message.strip() or f"Log postmortem {entry.entry_id}"
        output["git"] = auto_commit([out_file], message, push=git_push_flag)

    return output


def main() -> None:
    print("\nSharpEdge Interactive Logger")
    print("1) Place bet")
    print("2) Settle bet")
    print("3) Log postmortem")

    while True:
        choice = ask("Choose 1, 2, or 3")
        if choice in {"1", "2", "3"}:
            break
        print("Invalid choice. Pick 1, 2, or 3.")

    if choice == "1":
        output = handle_place()
    elif choice == "2":
        output = handle_settle()
    else:
        output = handle_postmortem()

    print("\n=== Logged Output ===")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
