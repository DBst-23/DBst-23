# SharpEdge Model Logging OS

This repository stores the SharpEdge postgame workflow, including NBA postmortems, rolling recent-form summaries, patch notes, liveflow snapshots, prompt instructions, and validation cases. ChatGPT is connected to this repo and uses these files as source material for ongoing analysis, regression detection, and model-patch decisions.

---

## Folder Structure

```text
README.md
prompts/
postmortems/
rolling_form/
patches/
tests/
logs/nba/liveflow/
```

### `prompts/`
Canonical prompt instructions, output schemas, and workflow rules.

### `postmortems/`
One markdown file per completed game or series. Used for hit/miss review, regression detection, and retraining notes.

### `rolling_form/`
Current last-5, last-10, and series-level summaries for teams, players, and market behavior.

### `patches/`
Model changes, version notes, feature toggles, retraining flags, and bug fixes.

### `tests/`
Sample inputs, validation cases, smoke tests, and engine checks.

### `logs/nba/liveflow/`
Live in-game snapshots created during LIVEFLOW_STRIPPED_MODE_ACTIVE. These are not final postmortems; they are decision-time model state records.

---

## Standard Workflow

1. Create a liveflow snapshot when a live edge is identified.
2. After the game, create a postmortem markdown file.
3. Update rolling-form summaries.
4. Add or revise patch notes if the game reveals a model blind spot.
5. Use the repo as the canonical source of truth for future simulations.

---

## Minimum Required Postmortem Fields

- Game metadata
- Pre-game assumptions
- LiveFlow decision points, if applicable
- Market line and price
- Actual result
- Rebound-environment notes
- Rotation notes
- Model hit / miss
- Patch recommendation
- Next-game carryover

---

## Regression Detection Priorities

The most important file class is `rolling_form/`, because it tracks:

- last 5 games
- last 10 games
- series-level trend
- opponent-specific behavior
- patch effect notes
- market adjustment pattern

---

## SharpEdge Rule

No model edge is considered final until it is:

1. logged,
2. graded,
3. tied to a market price,
4. checked against game script,
5. assigned a patch/no-patch decision.
