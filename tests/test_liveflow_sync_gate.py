import unittest
from liveflow.nba.sync_gate import evaluate

SHA = "a" * 64

def fixtures():
    common = dict(game_id="NBA_20261029_A_AT_B", period="HALFTIME",
                  clock_seconds_remaining=0, home_score=60, away_score=55,
                  source="independent-feed", artifact_sha256=SHA)
    freeze = dict(common, captured_at_utc="2026-10-29T02:00:00Z",
                  ingested_at_utc="2026-10-29T02:00:01Z",
                  model_total_regulation=232.5, model_version="B.003")
    market = dict(common, captured_at_utc="2026-10-29T02:00:03Z",
                  ingested_at_utc="2026-10-29T02:00:04Z", sportsbook="William Hill Nevada",
                  market_type="FULL_GAME_TOTAL", total_line=230.5, odds_format="AMERICAN",
                  includes_overtime=False)
    return freeze, market

class GateTests(unittest.TestCase):
    def test_clean_pass(self):
        self.assertEqual(evaluate(*fixtures())["status"], "PASS")
    def test_phantom_points(self):
        f,m=fixtures();m["home_score"]+=2
        self.assertEqual(evaluate(f,m)["status"], "REJECT")
    def test_late_freeze(self):
        f,m=fixtures();f["ingested_at_utc"]=m["captured_at_utc"]
        self.assertEqual(evaluate(f,m)["status"], "REJECT")
    def test_book_includes_ot(self):
        f,m=fixtures();m["includes_overtime"]=True
        self.assertEqual(evaluate(f,m)["status"], "REJECT")
    def test_missing_timestamp(self):
        f,m=fixtures();del m["captured_at_utc"]
        self.assertEqual(evaluate(f,m)["status"], "REJECT")
    def test_wrong_clock(self):
        f,m=fixtures();m["clock_seconds_remaining"]=20
        self.assertEqual(evaluate(f,m)["status"], "REJECT")

if __name__ == "__main__":
    unittest.main()
