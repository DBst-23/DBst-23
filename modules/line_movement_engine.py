from __future__ import annotations

from typing import Dict, Any


def detect_line_movement(payload: Dict[str, Any]) -> Dict[str, Any]:
    open_line = float(payload.get("open_line", 0.0))
    current_line = float(payload.get("current_line", 0.0))
    public_pct = float(payload.get("public_pct", 50.0))

    movement = current_line - open_line

    sharp_signal = False
    public_trap = False

    if movement > 1.0 and public_pct < 50:
        sharp_signal = True
    elif movement > 1.0 and public_pct > 65:
        public_trap = True

    return {
        "line_movement": movement,
        "sharp_signal": sharp_signal,
        "public_trap": public_trap
    }
