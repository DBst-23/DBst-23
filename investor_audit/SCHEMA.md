# SharpEdge Audit Schema

## Placed Bet JSONL Schema
Each line is one JSON object.

Required fields:
- entry_id
- timestamp_placed
- date
- sport
- matchup
- mode
- card_type
- platform
- market
- legs (array)
- stake
- payout_expected
- boost_tag
- screenshot_ref
- audit_hash

## Settled Bet JSONL Schema
- entry_id
- timestamp_settled
- result
- legs_hit
- legs_miss
- return_actual
- net
- roi
- final_score

## Postmortem JSONL Schema
- entry_id
- timestamp_postmortem
- result_type
- hit_legs
- missed_legs
- environment_tags
- variance_tags
- model_notes
- patch_required

## Rules
- Never overwrite existing entries
- Only append new lines
- Keep entry_id consistent across all logs
