# The Odds API: NBA halftime calibration findings (2026-11-13)

This report contains findings only. No raw odds responses or key values are committed. The private GitHub Actions runs are the audit record: [secret check](https://github.com/DBst-23/sharpedge-odds-private/actions/runs/43415573751), [event cost probe](https://github.com/DBst-23/sharpedge-odds-private/actions/runs/43416867725), [market discovery](https://github.com/DBst-23/sharpedge-odds-private/actions/runs/43417502795), [first odds window](https://github.com/DBst-23/sharpedge-odds-private/actions/runs/43418175105), [ten games run 1](https://github.com/DBst-23/sharpedge-odds-private/actions/runs/43419289267), [duplicate run 2](https://github.com/DBst-23/sharpedge-odds-private/actions/runs/43469360748). The source repo for the workflows is private.

## Terms gate

The [terms, updated August 31, 2026](https://the-odds-api.com/terms-and-conditions.html), explicitly permit “Storing our data and retaining it indefinitely” and “Using our data to train statistical and machine learning models.” Betting-model use is an inference from those permitted uses and analytical-tool provisions; the terms do not expressly use that phrase. Commercial analytical tools and derived displays are allowed, provided the provider data is not the primary product being sold or redistributed. Resale or redistribution as a standalone raw-data product is prohibited. No raw data should enter this public repo.

## Key, match, and observed markets

The paid key was present in the private repo secret `ODDS_API_HISTORICAL_KEY`; the workflow printed presence and length (32) only. No key value was logged. All ten PR #40 API-NBA games matched one historical Odds API event by teams and UTC commence time. Nine of ten Odds API commence times were ten minutes after the API-NBA scheduled start; the October 2023 game matched at scheduled time. Neither timestamp is proof of the actual opening tip.

The historical market discovery endpoint, rather than guessed keys, returned:

| Intended market | Observed key | Sample finding |
| --- | --- | --- |
| Live full-game moneyline | `h2h` | Present at some selected book on all 10 |
| Live full-game spread | `spreads` | Present on all 10 |
| Live full-game total | `totals` | Present on all 10 |
| Second-half moneyline | `h2h_h2` | Present at some selected book on all 10; not Caesars in this sample |
| Second-half spread | `spreads_h2` | Present on 9/10 |
| Second-half total | `totals_h2` | Present on 9/10 |
| Second-half team totals | No key observed | 0/10; `team_totals` is a full-game key and must not be relabeled |

The Odds API bookmaker key `williamhill_us` was titled **Caesars** in the historical response. DraftKings=`draftkings`, FanDuel=`fanduel`, BetMGM=`betmgm`, Pinnacle=`pinnacle`. Caesars had `spreads_h2` and `totals_h2` in 9/10 but no `h2h_h2`; DraftKings had all three second-half keys in 9/10. Pinnacle had full-game markets but no second-half spread/total in this sample.

## Sample coverage and timing

| Dataset season | Tested | Matched | 2H spread / total | 2H ML at any selected book | 2H team totals |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2023–24 | 5 | 5 | 4/5 | 5/5 | 0/5 |
| 2024–25 | 5 | 5 | 5/5 | 5/5 | 0/5 |

This is *sample coverage*, not verified coverage of every game in either season. [Historical additional markets begin May 3, 2023](https://the-odds-api.com/liveapi/guides/v4/); thus the PR #40 2022–23 regular-season rows cannot supply historical second-half markets from this provider. The tested 2023–24 and 2024–25 games are after that cutoff.

At +68 minutes from the Odds API commence time (which is not necessarily actual tip), nine games had second-half spread/total and a live full-game spread. For those nine, the home full-game spread minus the home second-half spread equaled the negative of the API-NBA halftime margin, an especially strong score-consistency check. The October 2023 Wizards–Grizzlies game had no second-half spread/total at +68, and its official gamebook shows that +68 preceded halftime. It remains unsafe for halftime training. The first Knicks–Celtics game moved from pregame Celtics −6 and total 221.5 to roughly Celtics −16.5 and total 235–236.5 at +62/+68, consistent with its 74–55 halftime lead.

Four offsets (+62, +68, +75, +85) were examined on three games. A fixed +68 offset is **not validated** even for this sample; game-specific clock checks are required. The historical endpoint chooses a snapshot at or before the requested time (typically five-minute resolution); market `last_update` must also be checked. One game had missing second-half markets at +68. Retain all sample odds as **unsafe for training** until gamebook clock checks and other value checks pass.

**Additional clock check:** The [official Wizards–Grizzlies gamebook](https://statsdmz.nba.com/pdfs/20231028/20231028_MEMWAS_book.pdf) records Q2 ending at 8:15 PM ET and Q3 starting at 8:30 PM ET. Odds API commence_time was 7:00 PM ET. Its +68 request was 8:08 PM; the returned 8:05:41 PM snapshot was still in Q2. Even +75 returned an 8:10:41 PM snapshot before halftime. The +85 request returned an 8:20:40 PM snapshot during halftime, yet the selected second-half spread/total markets were absent in discovery at +68. Thus the 9/10 market count is only availability at queried offsets, not 9/10 clock-validated halftime odds. Do not use a universal +68 rule.\n\n**Clock correction after merge:** The [official Knicks–Celtics gamebook](https://statsdmz.nba.com/pdfs/20241022/20241022_NYKBOS_book.pdf) records Q1 starting at 7:35 PM ET, Q2 ending at 8:30 PM ET, and Q3 starting at 8:46 PM ET. The Odds API `commence_time` was 7:40 PM ET, five minutes later than the gamebook tip. The +62 request (8:42 PM) returned an 8:40:39 PM snapshot within halftime; the +68 request (8:48 PM) returned an 8:45:39 PM snapshot just before Q3, while +75 returned an 8:50:39 PM snapshot after Q3 began. Eligibility must use the *returned snapshot and each market last_update* within the official Q2-end-to-Q3-start interval, not a fixed offset alone. The other nine games have not yet had their official period times independently checked. This correction supersedes any reference to Odds API `commence_time` as the actual tip.

## Actual credits and projected full pull

The first historical events call returned `x-requests-last: 1`; each market-discovery call returned 1. The first odds comparison used 20 credits pregame and 30 for each of four three-market snapshots. The ten-game run used 628 credits: 9 additional event lookups, 9 market discoveries, 9 game odds calls (eight at 60 credits and one at 40), three missing markets on the initial game (30), and six one-market extra-offset calls (60). Up to five named books counted as one region. Quota is based on unique markets returned, per the [official v4 documentation](https://the-odds-api.com/liveapi/guides/v4/).

**Budget incident:** The ten-game workflow was manually run twice. Each execution enforced a 655-credit *per-run* ceiling but did not persist a global 800-credit calibration ledger across reruns. Total actual use was 1 + 4 + 140 + 628 + 628 = **1,401 credits**, exceeding the requested 800 cap by 601. The last header reported **18,599 remaining** of the 20,000 monthly credits. The second run produced duplicate data, not ten new games. The manual workflow was removed from the private repo to reduce rerun risk. Do not rerun historical workflows or make a bulk pull without a persistent cross-run spend ledger and explicit owner approval.

A six-market halftime snapshot with up to ten named books cost **60 credits per game** when all six keys were returned; the October sample returned four keys and cost 40. With event match and market discovery at one credit each per game, a conservative working budget is **62 credits/game**. A fresh 20,000-credit allowance covers at most **322 complete games** at that rate (before a reserve); the current 18,599 balance covers at most **283** with a 1,000-credit reserve. The PR #40 2023–24 and 2024–25 table has 2,342 rows: 2,342 × 62 = **145,204 credits** as a planning ceiling for these six markets, assuming every game matches and returns all markets. Shared event discovery, missing markets, and quota resets may change actual spend. The listed 100K plan is insufficient for that one-cycle projection; the listed 5M plan covers it. No upgrade is recommended or authorized. [Plan listing](https://the-odds-api.com/).

## Decision gate

No bulk pull, training join, or claim of verified model probabilities yet. Next, establish a clock-validated halftime rule and a persistent, non-repeatable budget ledger; then present a revised small pilot for approval. Keep raw responses private and all odds rows unsafe for training until matched, time-checked, and sanity-checked.
