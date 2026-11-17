"""Step 2K: out-of-sample halftime lead-reversal probability audit.

2022 train, 2023 residual calibration, 2024 evaluation. No odds or bets.
"""
from __future__ import annotations
import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import mean
from liveflow_halftime_baseline import fit, predict, probability_home_win

def wilson(k, n, z=1.96):
    if not n:
        return None
    p = k / n
    d = 1 + z*z/n
    c = (p + z*z/(2*n))/d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return [round(c-h,4), round(c+h,4)]

def score(records):
    if not records:
        return None
    n=len(records)
    return {"n":n,"actual_reversals":sum(y for p,y in records),
            "expected_reversals":round(sum(p for p,y in records),3),
            "predicted_rate":round(mean(p for p,y in records),4),
            "observed_rate":round(mean(y for p,y in records),4),
            "observed_rate_wilson_95":wilson(sum(y for p,y in records),n),
            "observed_minus_predicted":round(mean(y-p for p,y in records),4),
            "brier":round(mean((p-y)**2 for p,y in records),5),
            "log_loss":round(mean(-y*math.log(p)-(1-y)*math.log1p(-p) for p,y in records),5)}

def audit(rows):
    seasons=defaultdict(list)
    ids=set()
    for r in rows:
        required={"game_id","season","halftime_margin_home","second_half_margin_home","final_home","final_away"}
        if not required.issubset(r):
            raise ValueError("Missing required columns")
        if r["game_id"] in ids:
            raise ValueError("Duplicate game ID")
        ids.add(r["game_id"])
        seasons[int(r["season"])].append(r)
    if any(len(seasons[y])<100 for y in (2022,2023,2024)):
        raise ValueError("Need >=100 games in each of 2022, 2023, 2024")
    model=fit(seasons[2022],"second_half_margin_home")
    residuals=[float(r["second_half_margin_home"])-predict(model,r) for r in seasons[2023]]
    naive_residuals=[float(r["second_half_margin_home"]) for r in seasons[2023]]
    groups=defaultdict(list)
    naive_groups=defaultdict(list)
    reliability=defaultdict(list)
    for r in seasons[2024]:
        h=float(r["halftime_margin_home"])
        if h==0:
            continue
        actual_final=float(r["final_home"])-float(r["final_away"])
        # Exact zero final margin should not occur in regulation; guard against invalid rows.
        if actual_final==0:
            raise ValueError("Tied final score in regulation")
        y=int(h*actual_final<0)
        projected=h+predict(model,r)
        home_p=probability_home_win(projected,residuals)
        naive_home_p=probability_home_win(h,naive_residuals)
        p=(1-home_p) if h>0 else home_p
        np=(1-naive_home_p) if h>0 else naive_home_p
        lead=abs(h)
        band="1-9" if lead<10 else ("10-14" if lead<15 else "15+")
        for key in ("all_non_tied",band,"10+" if lead>=10 else "under_10"):
            groups[key].append((p,y))
            naive_groups[key].append((np,y))
        reliability[min(int(p*10),9)].append((p,y))
    return {"split":{str(y):len(seasons[y]) for y in (2022,2023,2024)},
            "excluded_tied_halftime":sum(float(r["halftime_margin_home"])==0 for r in seasons[2024]),
            "bands":{k:{"model":score(v),"halftime_only_baseline":score(naive_groups[k])}
                     for k,v in sorted(groups.items())},
            "reliability_by_predicted_probability":
                [{"range":f"{i/10:.1f}-{(i+1)/10:.1f}",**score(v)}
                 for i,v in sorted(reliability.items())],
            "method":"2022 ridge point estimate + empirical 2023 residual CDF; 2024 untouched in fitting/calibration; 0.5-point win threshold and +0.5 smoothing inherited from baseline",
            "interpretation":"Compare observed-minus-predicted and proper scores against halftime-only baseline; nonzero discrepancy alone is not proof of systematic underestimation.",
            "limitations":["2024 holdout previously inspected: exploratory only",
                           "Overtime games excluded after outcomes: selection/lookahead bias",
                           "Residuals pooled across lead sizes and teams",
                           "No confidence interval for calibration gap; Wilson interval covers observed rate only",
                           "No sportsbook odds, no EV, no bet authorization"],
            "betting_deployment":"LOCKED"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--dataset",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    rows=[json.loads(x) for x in a.dataset.read_text().splitlines() if x.strip()]
    result=audit(rows)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"split":result["split"],"bands":result["bands"],"betting_deployment":"LOCKED"}))

if __name__=="__main__":
    main()
