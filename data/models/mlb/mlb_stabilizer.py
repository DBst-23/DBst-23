def clamp(x, lo, hi): 
    return max(lo, min(hi, x))

def apply_static_stabilizers(ctx):
    if not getattr(ctx, "config", None): 
        return ctx
    c = ctx.config
    if c.get("inning_cluster_dampener", {}).get("enabled", False):
        ctx = inning_cluster_dampener(ctx, c["inning_cluster_dampener"])
    if c.get("relief_chain_normalizer", {}).get("enabled", False):
        ctx = relief_chain_normalizer(ctx, c["relief_chain_normalizer"])
    if c.get("hr_spike_flag", {}).get("enabled", False):
        ctx = hr_spike_flag(ctx, c["hr_spike_flag"])
    if c.get("umpire_bounds", {}).get("enabled", False):
        ctx = umpire_bounds(ctx, c["umpire_bounds"])
    if c.get("lineup_uncertainty", {}).get("enabled", False):
        ctx = lineup_uncertainty(ctx, c["lineup_uncertainty"])
    return ctx

def inning_cluster_dampener(ctx, cfg): return ctx
def relief_chain_normalizer(ctx, cfg): return ctx
def hr_spike_flag(ctx, cfg): return ctx
def umpire_bounds(ctx, cfg): return ctx
def lineup_uncertainty(ctx, cfg): return ctx