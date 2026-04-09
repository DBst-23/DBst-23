# NBA LiveFlow Postmortem — UTA @ NOP — 2026-04-07

## Summary
- **Game:** Utah Jazz @ New Orleans Pelicans
- **Final:** Pelicans 156, Jazz 137
- **Ghost Pick Logged:** NOP +3.5 live at halftime
- **Halftime Score:** UTA 69, NOP 61
- **Result:** ✅ WIN

## Live-Flow Read
At halftime, New Orleans trailed by 8 despite still showing enough offensive creation to project a live comeback path. The Pelicans had only made **3 threes** in the first half while still scoring **61**, which implied room for offensive normalization if they cleaned up transition defense and turnover sequencing. Utah’s first-half offensive burst looked fragile because it was being driven by strong perimeter efficiency and elevated assist flow, while New Orleans still held interior scoring viability.

## Halftime Indicators
- Utah led 69–61 at the break
- Utah shot **28-52 FG (53.8%)** and **9-17 from three (52.9%)** in the first half
- New Orleans shot **25-49 FG (51.0%)** but only **3-15 from three (20.0%)**
- Paint scoring favored New Orleans, **40–34**
- Fastbreak points favored New Orleans, **18–12**
- Utah had the better assist profile early, **21–13**

## Why NOP +3.5 Was Live-Flow Viable
1. **Three-point regression angle**  
   Utah’s 52.9% first-half three-point shooting looked difficult to sustain, while New Orleans had clear room to improve from 20.0%.

2. **Interior pressure remained with NOP**  
   The Pelicans were already winning the paint battle at halftime and finished with a dominant **90 paint points**, confirming the live read that they could reclaim control through downhill scoring.

3. **Transition and turnover upside**  
   Even before the comeback was complete, New Orleans had better fastbreak pressure and enough defensive activity to create swing potential. They finished with **15 steals** and **28 points off turnovers**.

4. **Pelicans shot profile still had room to expand**  
   NOP was underperforming from deep early relative to its overall shot quality, while Utah’s offensive profile was more dependent on unsustainably hot perimeter accuracy.

## Second-Half / Full-Game Flip
The game completely inverted after halftime:
- New Orleans scored **95 second-half points**
- Final shooting: **61-106 FG (57.5%)**, **14-34 3PT (41.2%)**, **20-23 FT (87.0%)**
- Utah still scored well overall, but New Orleans overwhelmed them with pace, paint scoring, and live-ball chaos
- Final margin: **NOP by 19**, easily clearing +3.5

## Final Team Drivers
### Pelicans
- Jeremiah Fears: **40 PTS, 5 REB, 6 AST**
- Jordan Poole: **34 PTS**
- Derik Queen: **17 PTS, 12 REB, 7 AST**
- Kevon Looney: **12 REB**
- Jordan Hawkins: **25 PTS off bench**

### Jazz
- Keyonte Chandler: **31 PTS, 8 AST**
- Ben Mbeng: **26 PTS**
- John Konchar: **12 PTS, 10 REB, 10 AST**

## Diagnostic Tags
- `LIVEFLOW_EDGE_ACTIVE`
- `HALFTIME_COMEBACK_SIGNAL`
- `THREE_POINT_REGRESSION_TRIGGER`
- `PAINT_PRESSURE_CONFIRMATION`
- `TRANSITION_EDGE_CONFIRMED`
- `GHOST_PICK_WIN`

## Model Relevance Summary
This was a strong example of a live spread position where the trailing side still had the more scalable offensive environment. The halftime deficit overstated Utah’s control because:
- Utah’s perimeter accuracy was overheated
- New Orleans owned the more repeatable rim and transition pathways
- The Pelicans had obvious room for positive shooting regression

This entry should be retained as a clean **LiveFlow comeback template** for future second-half spread scans where:
- trailing team is still generating paint offense
- opponent is running hot from three
- game state suggests efficiency regression rather than structural dominance
