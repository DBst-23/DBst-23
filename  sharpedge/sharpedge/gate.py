from __future__ import annotations
from typing import Any, Dict, List, Tuple

def _get_path(obj: Dict[str, Any], path: str) -> Any:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur

def gate_check(
    payload: Dict[str, Any],
    required_paths: List[str],
    pass_ratio: float = 0.65
) -> Tuple[bool, float, List[str]]:
    missing: List[str] = []
    present = 0

    for p in required_paths:
        if _get_path(payload, p) is None:
            missing.append(p)
        else:
            present += 1

    quality = present / max(1, len(required_paths))
    passed = quality >= pass_ratio
    return passed, quality, missing