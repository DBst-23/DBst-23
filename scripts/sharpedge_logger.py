from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
AUDIT_DIR = REPO_ROOT / "investor_audit"
DAILY_DIR = AUDIT_DIR / "daily"


@dataclass
class BetEntry:
    entry_id: str
    timestamp_placed: str
    date: str
    sport: str
    matchup: str
    mode: str
    card_type: str
    platform: str
    market: str
    legs: List[str]
    stake: float
    payout_expected: float
    boost_tag: str
    copy_id: str
    screenshot_ref: str
    edge_tags: List[str]
    model_tags: List[str]
    audit_hash: str
    archive_status: str = "archived"


@dataclass
class SettledEntry:
    entry_id: str
    timestamp_settled: str
    date: str
    sport: str
    matchup: str
    status: str
    result: str
    legs_hit: int
    legs_miss: int
    return_actual: float
    net: float
    roi: float
    final_score: str
    settlement_notes: str
    audit_hash: str
    archive_status: str = "reconciled"


@dataclass
class PostmortemEntry:
    entry_id: str
    timestamp_postmortem: str
    date: str
    sport: str
    matchup: str
    postmortem_type: str
    result_type: str
    hit_legs: List[str]
    missed_legs: List[str]
    environment_tags: List[str]
    variance_tags: List[str]
    model_notes: str
    patch_required: bool
    finalized: bool = True


def ensure_dirs() -> None:
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)


def slug_team(team: str) -> str:
    return "".join(ch for ch in team.upper() if ch.isalnum())


# Expects format like: "MIA @ CHA"
def build_entry_id(date_str: str, sport: str, matchup: str, sequence: int) -> str:
    away, home = [part.strip() for part in matchup.split("@")]
    yyyy, mm, dd = date_str.split("-")
    return f"SE_{yyyy}_{mm}_{dd}_{sport.upper()}_{slug_team(away)}_{slug_team(home)}_{sequence:03d}"


def build_screenshot_ref(date_str: str, sport: str, matchup: str, sequence: int, status: str) -> str:
    away, home = [part.strip() for part in matchup.split("@")]
    return f"{date_str}_{sport.lower()}_{away.lower()}_{home.lower()}_{sequence:03d}_{status}.png".replace(" ", "")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def compute_audit_hash(
    entry_id: str,
    timestamp_placed: str,
    sport: str,
    matchup: str,
    stake: float,
    platform: str,
    legs: List[str],
) -> str:
    legs_raw = "; ".join(legs)
    payload = f"{entry_id}|{timestamp_placed}|{sport}|{matchup}|{stake}|{platform}|{legs_raw}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def write_jsonl_line(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def build_placed_file(date_str: str, batch: str = "001") -> Path:
    yyyy, mm, dd = date_str.split("-")
    return DAILY_DIR / f"placed_bets_{yyyy}_{mm}_{dd}_batch_{batch}.jsonl"


def build_settled_file(date_str: str, batch: str = "001") -> Path:
    yyyy, mm, dd = date_str.split("-")
    return DAILY_DIR / f"settled_bets_{yyyy}_{mm}_{dd}_batch_{batch}.jsonl"


def build_postmortem_file(date_str: str, batch: str = "001") -> Path:
    yyyy, mm, dd = date_str.split("-")
    return DAILY_DIR / f"postmortems_{yyyy}_{mm}_{dd}_batch_{batch}.jsonl"


def log_bet(
    *,
    date_str: str,
    sport: str,
    matchup: str,
    mode: str,
    card_type: str,
    platform: str,
    market: str,
    legs: List[str],
    stake: float,
    payout_expected: float,
    sequence: int,
    boost_tag: str = "None",
    copy_id: str = "",
    edge_tags: Optional[List[str]] = None,
    model_tags: Optional[List[str]] = None,
    batch: str = "001",
) -> BetEntry:
    ensure_dirs()

    timestamp_placed = now_iso()
    entry_id = build_entry_id(date_str, sport, matchup, sequence)
    screenshot_ref = build_screenshot_ref(date_str, sport, matchup, sequence, "placed")
    edge_tags = edge_tags or []
    model_tags = model_tags or []

    audit_hash = compute_audit_hash(
        entry_id=entry_id,
        timestamp_placed=timestamp_placed,
        sport=sport,
        matchup=matchup,
        stake=stake,
        platform=platform,
        legs=legs,
    )

    entry = BetEntry(
        entry_id=entry_id,
        timestamp_placed=timestamp_placed,
        date=date_str,
        sport=sport.upper(),
        matchup=matchup,
        mode=mode,
        card_type=card_type,
        platform=platform,
        market=market,
        legs=legs,
        stake=round(stake, 2),
        payout_expected=round(payout_expected, 2),
        boost_tag=boost_tag,
        copy_id=copy_id,
        screenshot_ref=screenshot_ref,
        edge_tags=edge_tags,
        model_tags=model_tags,
        audit_hash=audit_hash,
    )

    write_jsonl_line(build_placed_file(date_str, batch), asdict(entry))
    return entry


def log_settlement(
    *,
    entry_id: str,
    date_str: str,
    sport: str,
    matchup: str,
    result: str,
    legs_hit: int,
    legs_miss: int,
    stake: float,
    return_actual: float,
    final_score: str,
    settlement_notes: str,
    batch: str = "001",
) -> SettledEntry:
    ensure_dirs()

    timestamp_settled = now_iso()
    net = round(return_actual - stake, 2)
    roi = round(net / stake, 3) if stake else 0.0
    status = "Settled"

    payload_for_hash = (
        f"{entry_id}|{timestamp_settled}|{sport}|{matchup}|{result}|"
        f"{legs_hit}|{legs_miss}|{return_actual}|{net}|{final_score}"
    )
    audit_hash = hashlib.sha256(payload_for_hash.encode("utf-8")).hexdigest()

    entry = SettledEntry(
        entry_id=entry_id,
        timestamp_settled=timestamp_settled,
        date=date_str,
        sport=sport.upper(),
        matchup=matchup,
        status=status,
        result=result,
        legs_hit=legs_hit,
        legs_miss=legs_miss,
        return_actual=round(return_actual, 2),
        net=net,
        roi=roi,
        final_score=final_score,
        settlement_notes=settlement_notes,
        audit_hash=audit_hash,
    )

    write_jsonl_line(build_settled_file(date_str, batch), asdict(entry))
    return entry


def log_postmortem(
    *,
    entry_id: str,
    date_str: str,
    sport: str,
    matchup: str,
    postmortem_type: str,
    result_type: str,
    hit_legs: List[str],
    missed_legs: List[str],
    environment_tags: List[str],
    variance_tags: List[str],
    model_notes: str,
    patch_required: bool,
    batch: str = "001",
) -> PostmortemEntry:
    ensure_dirs()

    entry = PostmortemEntry(
        entry_id=entry_id,
        timestamp_postmortem=now_iso(),
        date=date_str,
        sport=sport.upper(),
        matchup=matchup,
        postmortem_type=postmortem_type,
        result_type=result_type,
        hit_legs=hit_legs,
        missed_legs=missed_legs,
        environment_tags=environment_tags,
        variance_tags=variance_tags,
        model_notes=model_notes,
        patch_required=patch_required,
    )

    write_jsonl_line(build_postmortem_file(date_str, batch), asdict(entry))
    return entry


def parse_csv_list(value: str) -> List[str]:
    if not value.strip():
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="SharpEdge investor audit logger")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_place = subparsers.add_parser("place", help="Log a placed bet")
    p_place.add_argument("--date", required=True, help="YYYY-MM-DD")
    p_place.add_argument("--sport", required=True)
    p_place.add_argument("--matchup", required=True, help="Example: MIA @ CHA")
    p_place.add_argument("--mode", required=True)
    p_place.add_argument("--card-type", required=True)
    p_place.add_argument("--platform", required=True)
    p_place.add_argument("--market", required=True)
    p_place.add_argument("--legs", required=True, help="Use | between legs")
    p_place.add_argument("--stake", required=True, type=float)
    p_place.add_argument("--payout", required=True, type=float)
    p_place.add_argument("--sequence", required=True, type=int)
    p_place.add_argument("--boost-tag", default="None")
    p_place.add_argument("--copy-id", default="")
    p_place.add_argument("--edge-tags", default="")
    p_place.add_argument("--model-tags", default="")
    p_place.add_argument("--batch", default="001")

    p_settle = subparsers.add_parser("settle", help="Log a settled bet")
    p_settle.add_argument("--entry-id", required=True)
    p_settle.add_argument("--date", required=True)
    p_settle.add_argument("--sport", required=True)
    p_settle.add_argument("--matchup", required=True)
    p_settle.add_argument("--result", required=True)
    p_settle.add_argument("--legs-hit", required=True, type=int)
    p_settle.add_argument("--legs-miss", required=True, type=int)
    p_settle.add_argument("--stake", required=True, type=float)
    p_settle.add_argument("--return-actual", required=True, type=float)
    p_settle.add_argument("--final-score", required=True)
    p_settle.add_argument("--notes", required=True)
    p_settle.add_argument("--batch", default="001")

    p_post = subparsers.add_parser("postmortem", help="Log a postmortem")
    p_post.add_argument("--entry-id", required=True)
    p_post.add_argument("--date", required=True)
    p_post.add_argument("--sport", required=True)
    p_post.add_argument("--matchup", required=True)
    p_post.add_argument("--postmortem-type", required=True)
    p_post.add_argument("--result-type", required=True)
    p_post.add_argument("--hit-legs", default="")
    p_post.add_argument("--missed-legs", default="")
    p_post.add_argument("--environment-tags", default="")
    p_post.add_argument("--variance-tags", default="")
    p_post.add_argument("--model-notes", required=True)
    p_post.add_argument("--patch-required", action="store_true")
    p_post.add_argument("--batch", default="001")

    args = parser.parse_args()

    if args.command == "place":
        entry = log_bet(
            date_str=args.date,
            sport=args.sport,
            matchup=args.matchup,
            mode=args.mode,
            card_type=args.card_type,
            platform=args.platform,
            market=args.market,
            legs=parse_csv_list(args.legs),
            stake=args.stake,
            payout_expected=args.payout,
            sequence=args.sequence,
            boost_tag=args.boost_tag,
            copy_id=args.copy_id,
            edge_tags=parse_csv_list(args.edge_tags),
            model_tags=parse_csv_list(args.model_tags),
            batch=args.batch,
        )
        print(json.dumps(asdict(entry), indent=2))

    elif args.command == "settle":
        entry = log_settlement(
            entry_id=args.entry_id,
            date_str=args.date,
            sport=args.sport,
            matchup=args.matchup,
            result=args.result,
            legs_hit=args.legs_hit,
            legs_miss=args.legs_miss,
            stake=args.stake,
            return_actual=args.return_actual,
            final_score=args.final_score,
            settlement_notes=args.notes,
            batch=args.batch,
        )
        print(json.dumps(asdict(entry), indent=2))

    elif args.command == "postmortem":
        entry = log_postmortem(
            entry_id=args.entry_id,
            date_str=args.date,
            sport=args.sport,
            matchup=args.matchup,
            postmortem_type=args.postmortem_type,
            result_type=args.result_type,
            hit_legs=parse_csv_list(args.hit_legs),
            missed_legs=parse_csv_list(args.missed_legs),
            environment_tags=parse_csv_list(args.environment_tags),
            variance_tags=parse_csv_list(args.variance_tags),
            model_notes=args.model_notes,
            patch_required=args.patch_required,
            batch=args.batch,
        )
        print(json.dumps(asdict(entry), indent=2))


if __name__ == "__main__":
    main()
