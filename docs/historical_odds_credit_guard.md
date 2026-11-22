# Historical odds paid-request safety gate

This module **does not activate API retrieval**. `CreditLedger` is an offline,
SQLite-backed reservation mechanism for a future private Odds API runner.

## Mandatory deployment controls

1. The SQLite database must be on **durable storage shared by every worker/run
   using the same Odds API key**. Do not put it in a disposable GitHub Actions
   workspace, an Actions artifact, or a separately copied per-run file. SQLite
   locking requires a filesystem with reliable cross-process locking; use a
   transactional database service instead for distributed runners.
2. Initialize a fixed approved project cap and an **audited opening spend**.
   The previous historical study documented **1,401 already-spent credits**
   against its former 800-credit research cap. Do not reset that cap or silently
   use a new one. A new allocation requires explicit owner approval.
3. Generate a canonical request fingerprint covering endpoint, event, market
   keys, bookmakers, regions, snapshot timestamp and other cost-changing
   parameters. Store a privately retained response cache indexed by this
   fingerprint; never commit responses or secrets to the public repository.
4. Before a paid request, look for a valid cache entry; if absent, atomically
   reserve a **conservative upper bound** for that exact request. If
   `reserve` returns False, **do not send HTTP again**: use the cached
   response or stop for manual reconciliation. A crashed/uncertain request
   retains its full reservation.
5. Only after reading a verified provider charge header, settle the reservation.
   Unknown, missing or unexpectedly high charges require manual reconciliation,
   not an automatic refund or retry. A request costing more than its estimate
   is a hard stop; never hide overages.
6. Enforce single-flight per fingerprint across workers. A different request ID
   alone is not sufficient to prevent duplicate paid calls. Provider account
   monthly remaining-credits headers are a secondary safety check, not a
   substitute for the project ledger. The private runner must enforce both.
7. Keep all historical retrieval disabled until private storage, caching,
   fingerprint deduplication, persistent deployment and tests are verified.

**Not yet implemented:** private authenticated HTTP integration, canonical
fingerprint uniqueness, cache, provider-header reconciliation, shared storage
deployment, CI integration, and end-to-end paid request testing. This PR is
foundation only; it is **not** approval to spend credits.
