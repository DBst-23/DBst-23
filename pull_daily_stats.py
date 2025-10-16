import pandas as pd
from datetime import date
import requests

TODAY = date.today().strftime("%Y-%m-%d")

# --- Baseball-Reference ---
def pull_baseball_reference():
    print("⏳ Pulling Baseball-Reference standings …")
    url = "https://www.baseball-reference.com/leagues/majors/{}.shtml".format(date.today().year)
    tables = pd.read_html(url)
    tables[0].to_csv(f"data/raw/mlb/br_standings_{TODAY}.csv", index=False)
    print("✅ Saved Baseball-Reference standings")

# --- FanGraphs ---
def pull_fangraphs():
    print("⏳ Pulling FanGraphs team stats …")
    url = (
        "https://www.fangraphs.com/leaders.aspx?"
        f"pos=all&stats=bat&lg=all&qual=0&type=8&season={date.today().year}&month=0&team=0,ts"
    )
    dfs = pd.read_html(url)
    dfs[0].to_csv(f"data/raw/mlb/fangraphs_team_{TODAY}.csv", index=False)
    print("✅ Saved FanGraphs team stats")

if __name__ == "__main__":
    pull_baseball_reference()
    pull_fangraphs()
