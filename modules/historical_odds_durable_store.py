"""Fail-closed entry point for a provisioned, durable historical-odds SQLite store.

A GitHub Actions checkout, cache or artifact is NOT durable shared storage.
This module does not provision storage or issue paid HTTP requests.
"""
from __future__ import annotations

import os
from pathlib import Path

from modules.historical_odds_credit_guard import CreditLedger
from modules.historical_odds_private_cache import PrivateOddsCache


class StorageNotProvisioned(RuntimeError):
    pass


def open_durable_store(*, cap: int, baseline_spent: int, environ=None):
    """Open only an explicitly provisioned, pre-existing SQLite ledger.

    SHARPEDGE_ODDS_LEDGER_PATH must point to a database file on a mounted,
    persistent volume with reliable SQLite locking, shared by all consumers.
    The operator must provision the database first; this guard cannot verify
    remote volume durability or single-writer guarantees on its own.
    """
    env = os.environ if environ is None else environ
    raw = env.get("SHARPEDGE_ODDS_LEDGER_PATH", "")
    if not raw:
        raise StorageNotProvisioned("Missing SHARPEDGE_ODDS_LEDGER_PATH; paid requests disabled")
    path = Path(raw)
    if not path.is_absolute() or not path.is_file() or path.is_symlink():
        raise StorageNotProvisioned("Ledger must be an existing absolute regular file, not a symlink")
    resolved = path.resolve(strict=True)
    if env.get("GITHUB_ACTIONS") == "true":
        # GitHub-hosted workspaces and runner temp directories are ephemeral.
        for key in ("GITHUB_WORKSPACE", "RUNNER_TEMP", "RUNNER_WORKSPACE"):
            root = env.get(key)
            if root and (resolved == Path(root).resolve() or Path(root).resolve() in resolved.parents):
                raise StorageNotProvisioned("GitHub runner workspace/temp is not durable storage")
    ledger = CreditLedger(resolved, cap=cap, baseline_spent=baseline_spent)
    try:
        cache = PrivateOddsCache(ledger)
        return ledger, cache
    except BaseException:
        ledger.close()
        raise
