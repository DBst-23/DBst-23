# Auto Postmortem Pipeline

## Purpose
This pipeline standardizes SharpEdge postmortem logging into one-file-per-game entries so postmortems can be committed cleanly, audited later, and ingested into downstream backtest tooling.

## Standard File Path
- NBA: `postmortems/nba/YYYY-MM-DD_AWAY_HOME.md`
- MLB: `postmortems/mlb/YYYY-MM-DD_AWAY_HOME.md`
- WNBA: `postmortems/wnba/YYYY-MM-DD_AWAY_HOME.md`

## Recommended Workflow
1. Final box score collected
2. Investment results collected
3. MPZ tags assigned
4. Postmortem markdown generated
5. Commit file into repo
6. Register any patch notes for live system

## Manual Commit Template
Use this structure for every postmortem file:

```md
# [SPORT] Postmortem — AWAY @ HOME — YYYY-MM-DD

## Final Score
HOME xxx – AWAY xxx

## Investments
- Card name / bet / result

## Net Session Result
- Total staked
- Total returned
- Net

## Market Validation Snapshot
- Closing market notes

## Postmortem Read
### What Hit
### What Missed
### Core Lessons

## MPZ Tags
- MISS_REGISTERED / HIT_REGISTERED / EDGE_CALL_ACTIVE

## Patch Notes for Live System
- Any future model adjustments
```

## One-Command Goal
Future target command:
- `retry commit`
- `run mpz tagging`
- `apply patch to live system`
- `build auto-postmortem pipeline`

## Current Status
- Modular postmortem logging active
- GitHub connector write path confirmed through `create_file`
- Best practice is create new file per game instead of overwriting legacy markdown logs
