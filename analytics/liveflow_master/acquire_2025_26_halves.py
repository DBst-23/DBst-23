#!/usr/bin/env python3
"""2025-26 NBA regular-season 1H/2H team stats ingestion; never fill missing markets.
Run with nba_api and pandas on a network-enabled runner. No odds are scraped.
"""
import argparse,csv,json,time,sys
from pathlib import Path
from datetime import datetime,timezone
COLS="game_id,game_date,team,opponent,h1_3pm,h1_3pa,h2_3pm,h2_3pa,h1_points,h2_points,h1_fga,h1_fta,h1_orb,h1_tov,h2_fga,h2_fta,h2_orb,h2_tov,halftime_total,final_total,market_book,market_captured_utc,market_total_line,market_under_american,market_over_american,source_url".split(",")
def retry(fn):
    for i in range(5):
        try:return fn()
        except Exception:
            if i==4:raise
            time.sleep(3*(2**i))
def val(row,*names):
    for name in names:
        if name in row and row[name] is not None:return int(row[name])
    raise KeyError("missing any of "+repr(names))
def main():
    p=argparse.ArgumentParser();p.add_argument("--out",required=True);p.add_argument("--audit");p.add_argument("--sleep",type=float,default=1.0);p.add_argument("--limit",type=int,default=0);a=p.parse_args()
    from nba_api.stats.endpoints import leaguegamefinder,boxscoretraditionalv3
    try:
        finder=retry(lambda:leaguegamefinder.LeagueGameFinder(season_nullable="2025-26",season_type_nullable="Regular Season",league_id_nullable="00",timeout=30))
        df=finder.get_data_frames()[0]
    except Exception as exc:
        audit_path=Path(a.audit or a.out+".audit.json")
        audit_path.parent.mkdir(parents=True,exist_ok=True)
        audit={"status":"BLOCKED_AT_GAME_DISCOVERY","season":"2025-26","games_discovered":0,"games_validated":0,"team_rows":0,"error_type":type(exc).__name__,"error":str(exc),"endpoint":"stats.nba.com LeagueGameFinder","generated_utc":datetime.now(timezone.utc).isoformat()}
        audit_path.write_text(json.dumps(audit,indent=2))
        print(json.dumps(audit,indent=2),file=sys.stderr)
        sys.exit(3)
    df=df[df.GAME_ID.astype(str).str.zfill(10).str.startswith("002")]
    dates={str(x.GAME_ID).zfill(10):str(x.GAME_DATE)[:10] for x in df.itertuples()}
    ids=sorted(dates)
    if a.limit:ids=ids[:a.limit]
    allrows=[];fail=[];ot=[];valid_games=0
    for idx,gid in enumerate(ids,1):
        try:
            halves=[]
            for first,last in ((1,2),(3,4)):
                endpoint=retry(lambda:boxscoretraditionalv3.BoxScoreTraditionalV3(game_id=gid,start_period=first,end_period=last,range_type=0))
                teams=endpoint.team_stats.get_data_frame().to_dict("records")
                if len(teams)!=2:raise ValueError("expected exactly two team stat rows")
                halves.append({str(val(t,"teamId","TEAM_ID")):t for t in teams})
                time.sleep(a.sleep)
            if set(halves[0])!=set(halves[1]):raise ValueError("halftime team IDs mismatch")
            ids2=sorted(halves[0]);result=[]
            h1pts={t:val(halves[0][t],"points","PTS") for t in ids2}
            h2pts={t:val(halves[1][t],"points","PTS") for t in ids2}
            # LeagueGameFinder final scores are regulation + OT. Flag OT rather than silently conflate.
            match=df[df.GAME_ID.astype(str).str.zfill(10)==gid]
            official={str(int(x.TEAM_ID)):int(x.PTS) for x in match.itertuples()}
            if len(official)!=2:raise ValueError("missing official final team scores")
            if any(h1pts[t]+h2pts[t]!=official[t] for t in ids2):
                if all(h1pts[t]+h2pts[t]<=official[t] for t in ids2):
                    ot.append(gid)
                else:raise ValueError("half scores exceed official final; endpoint mismatch")
            for t in ids2:
                o=next(x for x in ids2 if x!=t)
                r=dict.fromkeys(COLS,"")
                r.update(game_id=gid,game_date=dates[gid],team=t,opponent=o,h1_points=h1pts[t],h2_points=h2pts[t],halftime_total=sum(h1pts.values()),final_total=sum(official.values()),source_url=f"https://www.nba.com/game/{gid}/box-score")
                for n,part in enumerate(("h1","h2")):
                    src=halves[n][t]
                    for dest,aliases in {"3pm":("threePointersMade","FG3M"),"3pa":("threePointersAttempted","FG3A"),"fga":("fieldGoalsAttempted","FGA"),"fta":("freeThrowsAttempted","FTA"),"orb":("reboundsOffensive","OREB"),"tov":("turnovers","TOV")}.items():
                        r[part+"_"+dest]=val(src,*aliases)
                    if r[part+"_3pm"]>r[part+"_3pa"]:raise ValueError("3PM > 3PA")
                result.append(r)
            allrows.extend(result);valid_games+=1
        except Exception as e:fail.append({"game_id":gid,"error":str(e)})
        if idx%100==0:print(f"processed {idx}/{len(ids)}, valid {valid_games}, failed {len(fail)}",flush=True)
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=COLS);w.writeheader();w.writerows(allrows)
    audit={"status":"COMPLETE" if len(ids)==1230 and not fail and valid_games==1230 else "PARTIAL_OR_NEEDS_REVIEW","season":"2025-26","games_discovered":len(ids),"games_validated":valid_games,"team_rows":len(allrows),"expected_games":1230,"failures":fail,"ot_games":ot,"generated_utc":datetime.now(timezone.utc).isoformat(),"markets":"NOT_COLLECTED","possessions":"estimated downstream; not observed"}
    Path(a.audit or str(out)+".audit.json").write_text(json.dumps(audit,indent=2))
    print(json.dumps({k:v for k,v in audit.items() if k not in ("failures","ot_games")},indent=2))
    if audit["status"]!="COMPLETE":sys.exit(2)
if __name__=="__main__":main()
