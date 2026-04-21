# NBA LiveFlow Playoff Results Snapshot — 2026-04-20

## Summary
SharpEdge LiveFlow playoff tracking to date based on settled slips shown by the user.

- Record: **5-1**
- Net settled payout shown: **$90.05**
- Win rate: **83.3%**

## Settled Results

| Date Bucket | Matchup | Market | Pick | Result | Payout |
|---|---|---|---|---|---:|
| Playoffs | Golden State at Phoenix | Spread | No — Phoenix wins by over 2.5 points | Loss | $0.00 |
| Game 1 | Toronto at Cleveland | Team Total | Yes — Toronto over 111.5 points | Win | $15.07 |
| Game 1 | Minnesota at Denver | Total | No — Over 243.5 points scored | Win | $18.60 |
| Game 1 | Houston at Los Angeles L | Total | Yes — Over 195.5 points scored | Win | $11.18 |
| Game 1 | Phoenix at Oklahoma City | Team Total | No — Phoenix over 93.5 points | Win | $13.88 |
| Game 2 | Atlanta at New York | Team Total | No — Atlanta over 108.5 points | Win | $14.38 |
| Game 2 | Minnesota at Denver | Total | No — Over 245.5 points scored | Win | $17.94 |

## Validated LiveFlow Reads

### 1. Halftime Heat Fade / Total Inflation
Validated by:
- MIN @ DEN Game 1 — Under 243.5 hit
- MIN @ DEN Game 2 — Under 245.5 hit

Takeaway:
- Inflated live totals in playoff environments remained vulnerable when price expansion exceeded sustainable scoring structure.

### 2. Team Total Ceiling Suppression
Validated by:
- PHX @ OKC — PHX TT under 93.5 hit
- ATL @ NYK Game 2 — ATL TT under 108.5 hit

Takeaway:
- Team-total unders performed when offense was overdependent on limited creators or when rebound/paint/second-chance pressure worked against sustainable scoring.

### 3. Fake Suppression / Over Recovery
Validated by:
- HOU @ LAL — Over 195.5 hit
- TOR @ CLE — Toronto over 111.5 hit

Takeaway:
- The card shows the model also captured select over environments when the live number was pushed too low relative to recovery potential.

## Running Diagnostic Notes

### Strengths observed
- Strong playoff total read quality
- Team-total environment detection holding up
- Repeatable success on repriced live markets

### Current caution flag
- One early miss on GSW @ PHX spread indicates side markets may still require stricter trigger thresholds than totals/team totals.

## Module Validation Tags
- `HALFTIME_HEAT_FADE_MODULE`
- `TEAM_TOTAL_CEILING_LIMIT`
- `FAKE_SUPPRESSION_OVER_RECOVERY`
- `LIVEFLOW_CLASSIFIER_ALIGNMENT`

## Audit Note
This file is based on the settled tickets visible in the user-provided image and should be treated as a playoff LiveFlow performance snapshot. Unit-level ROI requires original stake amounts for every ticket, which were not all visible in the screenshot.
