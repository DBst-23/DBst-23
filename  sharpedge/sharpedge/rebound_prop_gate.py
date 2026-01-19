# rebound_prop_gate.py
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

# -----------------------------
# Confidence tiers (your system)
# -----------------------------
# 🔒 70%+ : Lock it in everywhere
# ⚠️ 60–69% : Boosts / ladder alt
# 🟡 50–59% : One-book limit
def base_confidence_tier(win_prob: float) -> str:
    if win_prob >= 0.70:
        return "LOCK_70"
    if win_prob >= 0.60:
        return "TIER_60"
    if win_prob >= 0.50:
        return "TIER_50"
    return "NO_PLAY"

@dataclass
class ReboundPropInput:
    player: str
    team: str
    market: str              # "REB"
    side: str                # "OVER" or "UNDER"
    line: float
    odds_american: int
    mean: float
    median: float
    win_prob: float          # model P(hit) BEFORE gate
    edge: float              # optional EV edge metric (your definition)
    tags_active: List[str]   # checklist tags currently ON
    projected_minutes: Optional[float] = None
    is_starter_big: Optional[bool] = None
    bench_big_candidate: Optional[bool] = None

@dataclass
class ReboundPropDecision:
    allowed: bool
    final_tier: str
    tier_overridden: bool
    adj_mean: float
    adj_median: float
    adj_win_prob: float
    adj_edge: float
    blocks: List[str]
    notes: List[str]
    tags_applied: List[str]

# -----------------------------
# Tag penalty configuration
# (tuned to be meaningful but not insane)
# -----------------------------
TAG_PENALTIES = {
    "CENTER_DISPLACEMENT_RISK_ON": {
        "starter_over_median_delta": -0.8,
        "starter_over_mean_delta": -0.6,
        "win_prob_delta": -0.05,
        "edge_delta": -0.015,
        "notes": "Starter C role unstable → downgrade starter REB overs."
    },
    "BENCH_BIG_MINUTES_SPIKE": {
        "starter_over_median_delta": -0.6,
        "starter_over_mean_delta": -0.5,
        "win_prob_delta": -0.04,
        "edge_delta": -0.012,
        "notes": "Bench big path to 20+ minutes → steal rebound share from starters."
    },
    "STARTER_BIG_MINUTES_CAP": {
        "starter_over_median_delta": -0.9,
        "starter_over_mean_delta": -0.7,
        "win_prob_delta": -0.06,
        "edge_delta": -0.018,
        "notes": "Starter minutes cap (<30) → hard suppress rebound volume ceiling."
    },
}

# -----------------------------------------
# Live-Flow rules (single-fire discipline)
# -----------------------------------------
LIVEFLOW_BLOCKS = {
    # When any of the 3 tags are ON, we require stronger numbers for starter OVERs.
    "starter_over_min_winprob_with_tags": 0.62,   # was 0.60 tier gate → raise bar
    "starter_over_min_edge_with_tags": 0.01,      # require real edge, not thin
    # If minutes cap tag is on, be even stricter
    "minutes_cap_extra_winprob": 0.03,            # +3% winprob requirement
}

def apply_tag_penalties(inp: ReboundPropInput) -> Tuple[float, float, float, float, List[str]]:
    """
    Returns adjusted (mean, median, win_prob, edge) plus notes.
    Penalties primarily apply to STARTER BIG OVERs (the trap zone).
    """
    adj_mean, adj_median, adj_wp, adj_edge = inp.mean, inp.median, inp.win_prob, inp.edge
    notes: List[str] = []

    is_starter_over = (inp.side.upper() == "OVER") and (inp.is_starter_big is True)

    for tag in inp.tags_active:
        if tag not in TAG_PENALTIES:
            continue
        cfg = TAG_PENALTIES[tag]

        # Apply penalties only where they matter most (starter big OVER).
        if is_starter_over:
            adj_median += cfg["starter_over_median_delta"]
            adj_mean += cfg["starter_over_mean_delta"]
            adj_wp += cfg["win_prob_delta"]
            adj_edge += cfg["edge_delta"]
            notes.append(f"{tag}: {cfg['notes']}")

    # Bound probability
    adj_wp = max(0.01, min(0.99, adj_wp))
    return adj_mean, adj_median, adj_wp, adj_edge, notes

def confidence_override(base_tier: str, tags_active: List[str], side: str, is_starter_big: Optional[bool]) -> Tuple[str, bool, List[str]]:
    """
    Override tiers when tag-risk is active.
    Core principle:
      - Starter BIG OVER with any of the 3 tags cannot be 🔒.
      - With minutes cap tag, it cannot be higher than 🟡.
    """
    reasons = []
    overridden = False
    tier = base_tier

    if (side.upper() == "OVER") and (is_starter_big is True) and any(t in tags_active for t in TAG_PENALTIES.keys()):
        # downgrade one step minimum
        if tier == "LOCK_70":
            tier = "TIER_60"
            overridden = True
            reasons.append("Tier override: starter REB OVER + volatility tag → no 🔒 allowed.")
        # if minutes cap, force max 🟡
        if "STARTER_BIG_MINUTES_CAP" in tags_active and tier in ("LOCK_70", "TIER_60"):
            tier = "TIER_50"
            overridden = True
            reasons.append("Tier override: STARTER_BIG_MINUTES_CAP → max tier = 🟡 (one-book limit).")

    return tier, overridden, reasons

def liveflow_execution_gate(inp: ReboundPropInput, adj_wp: float, adj_edge: float) -> Tuple[bool, List[str]]:
    """
    Returns (allowed, blocks).
    LiveFlow is strict: single-fire, protect from minutes volatility traps.
    """
    blocks: List[str] = []
    is_starter_over = (inp.side.upper() == "OVER") and (inp.is_starter_big is True)
    tags_on = any(t in inp.tags_active for t in TAG_PENALTIES.keys())

    if is_starter_over and tags_on:
        req_wp = LIVEFLOW_BLOCKS["starter_over_min_winprob_with_tags"]
        req_edge = LIVEFLOW_BLOCKS["starter_over_min_edge_with_tags"]

        if "STARTER_BIG_MINUTES_CAP" in inp.tags_active:
            req_wp += LIVEFLOW_BLOCKS["minutes_cap_extra_winprob"]

        if adj_wp < req_wp:
            blocks.append(f"LiveFlow block: adj_win_prob {adj_wp:.3f} < required {req_wp:.3f} for starter REB OVER w/ volatility tags.")
        if adj_edge < req_edge:
            blocks.append(f"LiveFlow block: adj_edge {adj_edge:.4f} < required {req_edge:.4f} for starter REB OVER w/ volatility tags.")

    allowed = (len(blocks) == 0)
    return allowed, blocks

def evaluate_rebound_prop(inp: ReboundPropInput, mode: str = "PREGAME") -> ReboundPropDecision:
    """
    mode: "PREGAME" | "LIVEFLOW"
    """
    blocks: List[str] = []
    tag_notes: List[str] = []

    base_tier = base_confidence_tier(inp.win_prob)

    adj_mean, adj_median, adj_wp, adj_edge, tag_notes = apply_tag_penalties(inp)
    final_tier, overridden, override_reasons = confidence_override(base_tier, inp.tags_active, inp.side, inp.is_starter_big)

    notes = []
    notes.extend(tag_notes)
    notes.extend(override_reasons)

    allowed = True
    if mode.upper() == "LIVEFLOW":
        allowed, lf_blocks = liveflow_execution_gate(inp, adj_wp, adj_edge)
        blocks.extend(lf_blocks)

    # If tier becomes NO_PLAY, block.
    if final_tier == "NO_PLAY":
        allowed = False
        blocks.append("Tier block: confidence tier = NO_PLAY after gate.")

    return ReboundPropDecision(
        allowed=allowed,
        final_tier=final_tier,
        tier_overridden=overridden,
        adj_mean=adj_mean,
        adj_median=adj_median,
        adj_win_prob=adj_wp,
        adj_edge=adj_edge,
        blocks=blocks,
        notes=notes,
        tags_applied=[t for t in inp.tags_active if t in TAG_PENALTIES]
    )

def decision_to_log_dict(inp: ReboundPropInput, decision: ReboundPropDecision) -> Dict:
    d = {
        "player": inp.player,
        "team": inp.team,
        "market": inp.market,
        "side": inp.side,
        "line": inp.line,
        "odds_american": inp.odds_american,
        "base_mean": inp.mean,
        "base_median": inp.median,
        "base_win_prob": inp.win_prob,
        "base_edge": inp.edge,
        "tags_active": inp.tags_active,
        "decision": asdict(decision),
    }
    return d