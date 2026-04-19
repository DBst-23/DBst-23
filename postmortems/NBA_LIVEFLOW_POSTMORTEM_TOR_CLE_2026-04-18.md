# NBA LiveFlow Postmortem — TOR @ CLE — 2026-04-18

## Summary
- **Game:** Toronto Raptors @ Cleveland Cavaliers
- **Final:** Cavaliers 126, Raptors 113
- **LiveFlow Focus:** halftime market scan on spread / total / team totals
- **Halftime Score:** TOR 54, CLE 61
- **Result Context:** no clean single-fire edge was formally activated from the halftime board provided; postmortem logged for script validation and future model refinement

## Halftime Game State
At halftime, Cleveland led **61–54** in a game that was already outperforming the pregame total environment. The market repriced the board aggressively:
- **Live spread:** CLE -8.5 to -9.5
- **Live total:** 228.5
- **Live team totals:** CLE 120.5, TOR 111.5

Pregame baseline was much lower:
- **Closing spread:** CLE favored by a moderate number pregame
- **Closing total context:** materially below the live 228.5 number

That created a classic LiveFlow tension point: Cleveland had scoreboard control, but the market had already inflated both the side and total into a much more expensive zone.

## Why the Halftime Board Was Difficult
1. **Cleveland efficiency was already elevated**  
   The Cavaliers reached **61 first-half points** on strong offensive execution, and the market priced that continuation aggressively into the second half. That removed much of the clean value from Cleveland side and team-total overs.

2. **Toronto was still offensively alive**  
   Despite trailing, the Raptors had already scored **54** and were shooting well enough to keep backdoor and total volatility active. That made a heavy Cleveland margin lay less attractive in LiveFlow.

3. **228.5 live total was rich**  
   The halftime total was pushed into a zone that required continued high-end shotmaking and pace carryover. That type of repricing can create under value in some spots, but Toronto’s offense was still functioning enough that the board did not offer a clean no-doubt single-fire entry from the snapshot alone.

4. **Both team totals were stretched**  
   Cleveland **120.5** and Toronto **111.5** both required sustained scoring from a game that had already produced a hot first half. The market was charging for continuation rather than leaving behind a soft number.

## Full-Game Outcome
The second half stayed productive enough for the full game to finish at **239 total points**, clearing the inflated live total of **228.5**.

Final team scoring:
- **Toronto:** 113
- **Cleveland:** 126

That means:
- Cleveland team total finished **over 120.5**
- Toronto team total finished **over 111.5**
- Full game total finished **over 228.5**
- Cleveland final margin finished at **+13**, covering the live halftime spread range of **-8.5 / -9.5**

## Final Team Drivers
### Raptors
- RJ Barrett: **24 PTS**
- Scottie Barnes: **21 PTS, 7 AST**
- Brandon Ingram: **17 PTS, 4 AST**
- Jamal Shead: **17 PTS**
- Sandro Mamukelashvili: **8 REB off bench**

### Cavaliers
- Donovan Mitchell: **32 PTS**
- James Harden: **22 PTS, 10 AST**
- Max Strus: **24 PTS off bench**
- Evan Mobley: **17 PTS, 7 REB, 4 AST**
- Jarrett Allen: **10 PTS, 7 REB**

## Market Validation Notes
This game is useful because it shows a case where the halftime market looked expensive but still was not expensive enough. Cleveland maintained control and both offenses continued to score efficiently.

Key takeaways:
- Cleveland’s offensive environment remained scalable after halftime
- Toronto kept enough offensive pressure to sustain the game total even while losing
- A simple "inflated halftime number = auto under" approach would have been wrong here
- Spread and team-total continuation remained viable because Cleveland’s control was real, not cosmetic

## Diagnostic Tags
- `LIVEFLOW_NO_FIRE_ZONE`
- `HALFTIME_INFLATION_REAL`
- `SCORING_ENVIRONMENT_PERSISTED`
- `TEAM_TOTAL_CONTINUATION_VALIDATED`
- `SPREAD_CONTINUATION_VALIDATED`
- `POSTMORTEM_ONLY_NO_ENTRY`

## Model Relevance Summary
This game should be retained as an important caution template for LiveFlow totals and spread analysis. Sometimes the halftime board looks expensive because the game is genuinely being played in a sustainable scoring environment.

The correct lesson is not that every inflated halftime number should be faded. The lesson is to separate:
- **fake inflation driven by unstable variance**, from
- **real inflation driven by scalable offense and valid control**

Cleveland’s lead and scoring environment proved durable enough that:
- live spread continuation held
- both team totals cleared
- full game over still cashed

This postmortem should be used to sharpen the distinction between **cosmetic halftime inflation** and **real continuation environments** in future LiveFlow scans.
