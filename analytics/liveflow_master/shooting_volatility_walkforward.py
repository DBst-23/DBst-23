#!/usr/bin/env python3
"""SharpEdge halftime shooting study: validate season-scale CSV and run expanding-window OOS tests.
No sportsbook odds or possessions are fabricated. Input is one row per team-game.
"""
import argparse,csv,json,math,statistics
from collections import defaultdict
from datetime import date
FIELDS=["game_id","game_date","team","opponent","h1_3pm","h1_3pa","h2_3pm","h2_3pa","h1_points","h2_points","h1_fga","h1_fta","h1_orb","h1_tov","h2_fga","h2_fta","h2_orb","h2_tov","halftime_total","final_total","market_book","market_captured_utc","market_total_line","market_under_american","market_over_american","source_url"]
REQUIRED=["game_id","game_date","team","opponent","h1_3pm","h1_3pa","h2_3pm","h2_3pa","h1_points","h2_points","source_url"]
def number(r,k):
    v=r.get(k,"")
    return None if v is None or str(v).strip()=="" else float(v)
def validate(rows):
    out=[];errors=[];seen=set()
    for i,r in enumerate(rows,2):
        try:
            date.fromisoformat(r["game_date"])
            key=(r["game_id"],r["team"])
            if key in seen: raise ValueError("duplicate game/team")
            seen.add(key)
            if any(not r.get(k) for k in REQUIRED): raise ValueError("missing required field")
            for half in ("h1","h2"):
                m,a=number(r,half+"_3pm"),number(r,half+"_3pa")
                if not (0<=m<=a and a>0 and m.is_integer() and a.is_integer()):raise ValueError("invalid 3PT makes/attempts")
            for k in ("h1_points","h2_points"):
                if number(r,k)<0:raise ValueError("negative points")
            for half in ("h1","h2"):
                vals=[number(r,half+"_"+x) for x in ("fga","fta","orb","tov")]
                if all(x is not None for x in vals):
                    if min(vals)<0:raise ValueError("negative possession component")
                    r[half+"_estimated_possessions"]=vals[0]+.44*vals[1]-vals[2]+vals[3]
                else:r[half+"_estimated_possessions"]=None
            if any(r.get(k) for k in ("market_book","market_captured_utc","market_total_line","market_under_american","market_over_american")):
                if not all(r.get(k) for k in ("market_book","market_captured_utc","market_total_line","market_under_american","market_over_american")):raise ValueError("partial market snapshot")
                if not r["market_captured_utc"].endswith("Z"):raise ValueError("market timestamp must be UTC Z")
            out.append(r)
        except Exception as e:errors.append({"csv_line":i,"error":str(e)})
    return out,errors
def american_decimal(v):
    v=float(v)
    if v==0:raise ValueError("zero American odds")
    return 1+ (v/100 if v>0 else 100/abs(v))
def main():
    p=argparse.ArgumentParser();p.add_argument("--input",required=True);p.add_argument("--output",required=True);p.add_argument("--min-train-games",type=int,default=200);a=p.parse_args()
    with open(a.input,newline="") as f:rows=list(csv.DictReader(f))
    good,errors=validate(rows)
    good.sort(key=lambda r:(r["game_date"],r["game_id"],r["team"]))
    # Model only uses first-half shooting + historical pregame team rates; no second-half features at prediction time.
    # Baseline: expanding-window league-average second-half 3PT% and 2H points.
    # Regression predictor: shrink first-half percentage toward historical second-half rate with n0=50 pseudo-attempts.
    # Scoring predictor: historical 2H points baseline plus fitted slope of historical shooting deviation vs 2H scoring.
    predictions=[];prior=[];dates=sorted({r["game_date"] for r in good})
    for d in dates:
        day=[r for r in good if r["game_date"]==d]
        distinct_games=len({r["game_id"] for r in prior})
        if distinct_games>=a.min_train_games:
            mu3=sum(number(r,"h2_3pm") for r in prior)/sum(number(r,"h2_3pa") for r in prior)
            mu_pts=statistics.mean(number(r,"h2_points") for r in prior)
            xs=[number(r,"h1_3pm")/number(r,"h1_3pa")-mu3 for r in prior]
            ys=[number(r,"h2_points")-mu_pts for r in prior]
            denom=sum(x*x for x in xs)
            slope=sum(x*y for x,y in zip(xs,ys))/denom if denom else 0
            for r in day:
                a3=number(r,"h1_3pa");m3=number(r,"h1_3pm")
                pred3=(m3+50*mu3)/(a3+50)
                actual3=number(r,"h2_3pm")/number(r,"h2_3pa")
                base_pts=mu_pts
                model_pts=mu_pts+slope*(m3/a3-mu3)
                record={"game_id":r["game_id"],"date":d,"team":r["team"],"actual_h2_3pt_pct":actual3,"baseline_h2_3pt_pct":mu3,"model_h2_3pt_pct":pred3,"actual_h2_points":number(r,"h2_points"),"baseline_h2_points":base_pts,"model_h2_points":model_pts,"market_comparison":"NOT_AVAILABLE"}
                # Market total is a game-level target; a team-row 2H points model cannot be compared to it.
                predictions.append(record)
        prior.extend(day)
    def mae(target,pred):return sum(abs(x[target]-x[pred]) for x in predictions)/len(predictions) if predictions else None
    result={"status":"RESEARCH_ONLY_NO_BETTING_PROBABILITIES","input_rows":len(rows),"valid_rows":len(good),"errors":errors,"independent_games":len({r["game_id"] for r in good}),"oos_team_rows":len(predictions),"oos_distinct_games":len({r["game_id"] for r in predictions}),"walk_forward_by_date":True,"min_prior_distinct_games":a.min_train_games,"mae_2h_points_baseline":mae("actual_h2_points","baseline_h2_points"),"mae_2h_points_shooting_model":mae("actual_h2_points","model_h2_points"),"mae_h2_3pt_pct_baseline":mae("actual_h2_3pt_pct","baseline_h2_3pt_pct"),"mae_h2_3pt_pct_shrunk_model":mae("actual_h2_3pt_pct","model_h2_3pt_pct"),"market_comparison":"NOT_IMPLEMENTED: needs synchronized game-level halftime total distribution and both-side odds","calibrated_probability":None,"edge":None,"predictions":predictions}
    with open(a.output,"w") as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!="predictions"},indent=2))
if __name__=="__main__":main()
