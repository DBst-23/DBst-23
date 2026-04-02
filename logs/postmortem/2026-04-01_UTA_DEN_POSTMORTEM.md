# UTA @ DEN Postmortem — 2026-04-01

## Final score
- Nuggets 130
- Jazz 117

## Invested plays tied to this matchup
1. Nikola Jokic UNDER 13.5 rebounds — **LOSS**
   - Final: 17 rebounds
2. Kyle Filipowski OVER 7.5 rebounds — **WIN**
   - Final: 12 rebounds

## Matchup-linked combo outcomes
- Mikal Bridges UNDER 3.5 rebounds + Nikola Jokic UNDER 13.5 rebounds — **Lost**
- Kevin Durant OVER 4.5 assists + Kyle Filipowski OVER 7.5 rebounds — **Won**

## Pre-game grading recap
### Nikola Jokic UNDER 13.5 rebounds
- Projected mean: ~13.4-13.9
- Median: 13
- Grade: C+ / thin value at 13.5
- Read before tip: playable only because the line sat above broader market consensus, but still fragile due to Jokic ceiling and matchup history.

### Kyle Filipowski OVER 7.5 rebounds
- Projected mean: ~8.4-8.8
- Median: 8
- Grade: B
- Read before tip: viable because of expanded Utah frontcourt role and stable minute path.

## Outcome assessment
### What the model got right
- Correctly identified **Filipowski OVER 7.5** as the best Utah rebound position on the board.
- Correctly recognized that Jokic under at **13.5** was only a number play, not a structural smash.
- The model was directionally honest: Jokic under was thin, Filipowski over was stronger.

### What failed on Jokic under
- Jokic finished with **17 rebounds**, well above both mean and median expectation.
- Denver won the rebound battle **53–44**.
- Utah shot **46.3% FG**, but produced enough misses and enough second-chance structure to keep Jokic rebound volume elevated.
- Jokic logged **33 minutes** and still got there comfortably, meaning this was not purely overtime- or minute-driven.

### What worked on Filipowski over
- Filipowski finished with **12 rebounds** in 31 minutes.
- Utah frontcourt role stayed intact and game script did not suppress his board volume.
- He cleared by a healthy margin, confirming the minutes + role thesis.

## Structural notes
### Jokic under lessons
This loss reinforces a recurring truth:
- Jokic rebounds are not only driven by opponent weakness; they are also driven by **possession control, role certainty, and Denver’s willingness to let him vacuum defensive boards as a transition starter**.
- A line of **13.5** can still be too low if the game environment provides full minutes plus ordinary miss volume.

### Filipowski over lessons
- When Utah is stripped of interior competition, Filipowski becomes a very stable rebound source.
- This was a cleaner role edge than the Jokic fade.

## Patch note for future workflow
Add / reinforce:
- `JOKIC_REBOUND_CEILING_PROTECTION`
- `TRANSITION_STARTER_DEF_REBOUND_CAPTURE`
- `ELITE_CENTER_UNDER_REQUIRES_STRONGER_SUPPRESSION`

Rule suggestion:
- Do not treat elite-center rebound unders as primary card material unless at least two of the following are present:
  1. Minutes cap risk
  2. Shared rebounder competition spike
  3. Opponent low miss volume profile
  4. Blowout suppression likely before 4Q accumulation

## Final grading
- Jokic U13.5: **Process acceptable, result failed, edge was too thin**
- Filipowski O7.5: **Strong hit**
- Matchup portfolio grade: **B-**

## Tags
- `MISS_REGISTERED`
- `THIN_EDGE_BURN`
- `ELITE_CENTER_CEILING_PUNISHED`
- `WIN_REGISTERED`
- `ROLE_REBOUND_EDGE_CONFIRMED`
