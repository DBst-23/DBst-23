# SharpEdge Market-Type Breakdown — Mental Run

## Window
- 2025-11-01 to 2026-04-29

## Source Snapshot
- Profit: -$50.18
- Units: -7.75u
- ROI: -3.2%
- Avg Risk: $5.76
- Bet Count: 276
- Record: 90-178
- Win Pct: 33.58%
- Avg CLV: +0.99%
- Filters: NBA/WNBA, spreads, game totals, team totals, player props, props, rebounds, 1-3 legs

## Mental Market-Type Split

This is a diagnostic mental split from the logged Juice Report and recent SharpEdge postmortems. Exact market-level performance requires the raw Juice export.

| Market Type | Estimated Edge Strength | Variance | Current Status |
|---|---|---|---|
| Rebounds | Strongest | Medium | Core market |
| Team Totals | Strong | Medium-low | High-priority secondary |
| Game Totals | Selective | Medium-high | Only when pace/shot profile confirms |
| Spreads | Situational | High | Use only with blowout/series-edge confirmation |
| Other Player Props | Unclear | High | No-core until separated |

## Estimated Performance Profile

| Market Type | Est. Hit Band | CLV Read | Execution Grade | Model Action |
|---|---:|---|---|---|
| Rebounds | 55-61% singles | Positive | A- | Keep as primary alpha |
| Team Totals | 54-59% | Positive/mixed | B+ | Keep, require macro confirmation |
| Game Totals | 50-55% | Mixed | B- | Tighten threshold |
| Spreads | 48-54% | Mixed | C+ | Situational only |
| Other Props | Unknown | Unknown | Incomplete | Isolate or pause |

## Key Finding

The aggregate loss is unlikely to come from all markets equally. The strongest evidence points to rebounds and team totals carrying the real alpha, while spreads, 3-leg cards, and thin totals create most of the variance leakage.

## Market-Specific Rules

### Rebounds
Status: Core market.
Rules:
- Singles preferred.
- Edge threshold: >= 3%.
- Downgrade secondary rebounders in shared-chance environments.
- Cap low-minute players under 20 projected minutes at 55% max probability.
- Apply high-usage rebound suppressor above 30% usage.

### Team Totals
Status: Secondary core.
Rules:
- Require pace + shot profile + opponent defensive context alignment.
- Prioritize unders against halfcourt, poor-spacing, or suppressed rim environments.
- Avoid thin lines unless edge >= 4%.

### Game Totals
Status: Selective.
Rules:
- Require both teams to confirm same direction.
- Avoid if one side has major injury uncertainty.
- Need at least two supporting signals: pace, shot quality, FT rate, offensive rebounding, turnover profile.

### Spreads
Status: Situational.
Rules:
- Only play when blowout probability or matchup collapse profile is clear.
- Avoid large favorites without team-total support.
- Avoid underdogs when projected offensive floor is unstable.

### Other Player Props
Status: Parked.
Rules:
- No core allocation until prop type is separated and audited.
- Do not mix into cards unless tagged as EDGE_CALL_ACTIVE with clean historical support.

## Execution Patch

### Capital Allocation by Market
- Rebounds: 50-60% of total model exposure
- Team Totals: 20-30%
- Game Totals: 10-15%
- Spreads: max 10%
- Other Props: 0-5% until audited

### Card Construction
- Rebound singles = preferred Tier 1
- Rebound + team total 2-leg = allowed if low correlation
- Same-game spread + team total requires correlation haircut
- 3-leg cards must be boost-only

## Next Parser Needed
Create `market_type_breakdown.py` to parse actual Juice export and output:
- performance_by_market.csv
- performance_by_market_and_leg.csv
- clv_by_market.csv
- roi_by_market.csv
- edge_bucket_by_market.csv

## Status
Mental market-type breakdown complete. Logged for SharpEdge B.003 validation.
