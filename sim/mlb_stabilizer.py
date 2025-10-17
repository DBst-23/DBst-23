import math
import statistics

def apply_static_stabilizers(ctx):
    """Master stabilizer call."""
    cfg = ctx.get("config", {}).get("stabilizer", {})
    if not cfg.get("enabled", True):
        return ctx

    ctx = inning_cluster_dampener(ctx, cfg)
    ctx = relief_chain_normalizer(ctx, cfg)
    ctx = hr_spike_flag(ctx, cfg)
    ctx = umpire_bounds(ctx, cfg)
    ctx = lineup_uncertainty(ctx, cfg)
    return ctx


def inning_cluster_dampener(ctx, cfg):
    if not cfg.get("inning_cluster_dampener", {}).get("enabled", True):
        return ctx
    q_lo, q_hi = 0.08, 0.92
    run_env = ctx.get("run_env", {})
    runs = run_env.get("inning_run_dist", [0,1,2,3,4,5])
    floor = statistics.quantiles(runs, n=100)[int(q_lo*100)]
    cap = statistics.quantiles(runs, n=100)[int(q_hi*100)]
    clamped = [min(max(r, floor), cap) for r in runs]
    run_env["inning_run_dist"] = clamped
    ctx["run_env"] = run_env
    return ctx


def relief_chain_normalizer(ctx, cfg):
    if not cfg.get("relief_chain_normalizer", {}).get("enabled", True):
        return ctx
    bullpen = ctx.get("bullpen", {})
    for role, data in bullpen.items():
        data["ip"] = min(max(data.get("ip", 1.0), 0.1), 3.0)
    ctx["bullpen"] = bullpen
    return ctx


def hr_spike_flag(ctx, cfg):
    if not cfg.get("hr_spike_flag", {}).get("enabled", True):
        return ctx
    env = ctx.get("weather", {})
    z = env.get("z_hr_env", 0)
    if z >= cfg["hr_spike_flag"].get("trigger_z", 1.1):
        hr_rate = ctx.get("hr_rate", 1.0)
        prior = ctx.get("hr_prior", 1.0)
        w = cfg["hr_spike_flag"].get("regress_strength", 0.45)
        ctx["hr_rate"] = hr_rate - (hr_rate - prior) * w
    return ctx


def umpire_bounds(ctx, cfg):
    if not cfg.get("umpire_bounds", {}).get("enabled", True):
        return ctx
    capK = cfg["umpire_bounds"].get("k_rate_delta_cap", 0.015)
    capB = cfg["umpire_bounds"].get("bb_rate_delta_cap", 0.010)
    ctx["k_rate_delta"] = max(-capK, min(ctx.get("k_rate_delta", 0.0), capK))
    ctx["bb_rate_delta"] = max(-capB, min(ctx.get("bb_rate_delta", 0.0), capB))
    return ctx


def lineup_uncertainty(ctx, cfg):
    if not cfg.get("lineup_uncertainty", {}).get("enabled", True):
        return ctx
    lineup = ctx.get("lineup", [])
    for p in lineup:
        play_prob = p.get("play_prob", 1.0)
        inactive_prob = cfg["lineup_uncertainty"].get("inactive_prob_default", 0.06)
        star_boost = cfg["lineup_uncertainty"].get("star_player_boost", 0.5)
        if p.get("is_star", False):
            inactive_prob *= (1 - star_boost)
        p["play_prob"] = max(0.0, min(1.0, play_prob * (1 - inactive_prob)))
    ctx["lineup"] = lineup
    return ctx