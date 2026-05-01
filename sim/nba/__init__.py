"""NBA simulation package.

Keep optional modules guarded so core engine imports do not fail inside
GitHub Actions when experimental files are absent.
"""

try:
    from .lineups_synergy import build_lineup_synergy_table
except ModuleNotFoundError:
    build_lineup_synergy_table = None

__all__ = ["build_lineup_synergy_table"]
