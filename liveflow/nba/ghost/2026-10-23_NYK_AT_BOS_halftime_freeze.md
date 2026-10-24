# NBA LiveFlow Ghost #002 — NYK @ BOS — 2026-10-23 HALFTIME FROZEN BEFORE BOOK
Status: PAPER-ONLY, PRE-BOOKMARKET, forecast is NOT historically calibrated.
Time-context: User provides Friday October 23 2026 official first half only, score NYK 49 BOS 50 (99).
Venue TD Garden. Source: user-supplied NBA first half and play by play; no external scores used.

## First-half inputs
NYK 17/40 FG, 6/20 3PT, 9/12 FT, 5 OREB, 9 team turnovers, 49 points.
BOS 20/45 FG, 7/20 3PT, 3/4 FT, 7 OREB, 7 team turnovers, 50 points.
Quarter scoring NYK 27-22; BOS 26-24.
NYK Towns 12pts, 8reb, 3 fouls and 5/5 FGM; Brunson 7pts 2/6; Bridges 0pts 0/4; Hart 7; OG 8 and 5 rebounds.
BOS Tatum 11pts 6reb; Paul George 5pts 2/7; Derrick White 6pts 3/3; Mitchell Robinson 2 fouls in 9:12, Queta 2 fouls in 11:18; Garza 8pts, 3/3 FG.
Possession estimate NYK 40-5+9+0.44*12=49.28; BOS 45-7+7+0.44*4=46.76 (rough counts from reported turnovers, estimate sensitive to team reb/FT rules). Baseline ~48 possessions per team per half.

## Model v0.2, exploratory
100000 random draws, fixed xorshift32 seed 20261023, Box-Muller standard normals, correlation rho=0.10; NYK 2H Normal(mean=53.5,sd=9.2), BOS 2H Normal(mean=55.0,sd=9.5), round to integer & clip at zero. These parameters are judgmental, not trained/calibrated. Raw percentages shouldn't be presented as verified edges.
Rationale: modest upward scoring from 99-point first half, regression expectations for Bridges/Brunson vs Towns perfect first-half FG and Boston bench efficiencies; NYK Towns 3 fouls, Celtics center foul management and uncertain rotations. No sharp books viewed.
Calculated simulation:
- NYK 2H mean 53.483, median 54; BOS mean 54.977, median 55.
- 2H total mean 108.460, median 109. Implied final total 207.460, median 208.
- full final implied NYK 102.48, BOS 104.98, BOS winning margin 2.49.
- NYK 2H win 43.54%; BOS 2H win 53.32%; tie 3.14%; NYK full outright win 40.48%.
- Over probability table (2H): 102.5:66.6%, 104.5:61.3%, 106.5:55.6%, 108.5:50%, 110.5:44.2%, 112.5:38.6%, 114.5:33.3%
No book price, no EV or probability edge yet. Never amend this frozen file after game finishes.

## Status and patches
KEEP frozen-premarket timestamp and team player foul/rebound split.
MODIFY monitoring: Towns 3PF risk, uncertain NYK rim rotation, BOS Queta/Mitchell Robinson 2PF each, league opening tiny samples.
Foul, free-throw and regulation overtime risks are not explicitly simulated here.
Next step capture book screenshot with full-game or **second-half-only** market tags and exact odds; compare on matching settlement horizon.
