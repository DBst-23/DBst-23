"""Paper-only NBA scoreboard monitor. Public ESPN scoreboard; no paid odds requests."""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard"
def main():
    now = datetime.now(timezone.utc)
    req = urllib.request.Request(URL, headers={"User-Agent":"SharpEdge-paper-scoreboard/1.0"})
    with urllib.request.urlopen(req, timeout=18) as resp:
        raw=json.load(resp)
    games=[]
    for event in raw.get("events",[]):
        comp=(event.get("competitions") or [{}])[0]
        teams={c.get("homeAway"):c for c in comp.get("competitors",[])}
        status=event.get("status") or {}
        state=(status.get("type") or {}).get("state","unknown")
        period=status.get("period",0)
        clock=status.get("displayClock","")
        home=teams.get("home",{})
        away=teams.get("away",{})
        games.append({"event_id":event.get("id"),"start_time_utc":event.get("date"),
                      "home":home.get("team",{}).get("displayName"),"away":away.get("team",{}).get("displayName"),
                      "home_score":home.get("score"),"away_score":away.get("score"),
                      "state":state,"period":period,"clock":clock,
                      "status_detail":(status.get("type") or {}).get("detail"),
                      "halftime_candidate":state=="in" and period==2 and (clock in ("0:00","00:00","0.0") or "halftime" in str((status.get("type") or {}).get("detail","")).lower()),
                      "halftime_confirmed": "halftime" in str((status.get("type") or {}).get("detail","")).lower()})
    out={"observed_at_utc":now.isoformat(),"source":"ESPN public NBA scoreboard","source_url":URL,
         "games":games,"odds_fetched":False,"model_run":False,"betting_status":"PAPER_ONLY"}
    path=Path(os.environ.get("OUTPUT_PATH","data/nba/live_scoreboard_latest.json"))
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
if __name__=="__main__":
    main()
