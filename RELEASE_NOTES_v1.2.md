# SharpEdge Engine — MLB_MODEL_V1.2-FINAL

## What’s new
- ✅ **Unified runner**: `LiveFlow_Backtest_Controller.py` runs LiveFlow + Backtest with one command.
- ✅ **Strict data validation**: `DataValidator.py` + `game_data_schema.json` enforce clean inputs; invalid rows are auto-logged.
- ✅ **Volatility Overlay Toolkit**: `Volatility_Overlay_Toolkit.py` with modular overlays (e.g., ORACLE_SHADOW_BLIND_ZONE, STRETCH_BREAKDOWN, RISP_VOLATILITY).
- ✅ **GitHub Actions**: `.github/workflows/run-controller.yml` auto-executes runs on push/schedule; outputs uploaded as artifacts.

## Outputs
- `output/<YYYY-MM-DD>/<GAME>_SIM_RESULT.json` — per-game results (medians, probabilities, overlays_applied).
- `output/<YYYY-MM-DD>/<DATE>_<MODE>_AGGREGATE.json` — run summary and aggregate edges.
- `logs/<DATE>_<MODE>_invalid_rows.json` — row-level validation errors (only if any).

## Breaking changes
- Controller now expects a strict record shape. Extra/invalid fields are rejected and logged.
- Engines should optionally import:
  ```python
  from Volatility_Overlay_Toolkit import apply_overlays