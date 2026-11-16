import unittest

from modules.api_basketball_game_dates import (
    GameDateVerificationError, enrich_verified_dates, verified_game_date,
)


def record(game_id):
    return {"source": "api_basketball_v1", "game_id": game_id,
            "player_id": 7, "minutes": 20.0, "total_rebounds": 5}


class GameDateTests(unittest.TestCase):
    def test_verified_date_and_cached_join(self):
        calls = []
        def fetch(game_id):
            calls.append(game_id)
            return {"response": [{"id": game_id, "date": "2025-01-05T19:30:00+00:00"}]}
        result = enrich_verified_dates([record(12), record(12), record(13)], schedule_fetcher=fetch)
        self.assertEqual(calls, [12, 13])
        self.assertEqual([r["game_date"] for r in result], ["2025-01-05"] * 3)

    def test_reject_mismatch_missing_and_bad_date(self):
        for payload in ({"response": []}, {"response": [{"id": 99, "date": "2025-01-05"}]},
                        {"response": [{"id": 12, "date": "2025-02-30"}]},
                        {"errors": {"token": "invalid"}, "response": []}):
            with self.subTest(payload=payload), self.assertRaises(GameDateVerificationError):
                verified_game_date(payload, 12)

    def test_reject_conflicting_existing_date(self):
        row = {**record(12), "game_date": "2025-01-04"}
        with self.assertRaises(GameDateVerificationError):
            enrich_verified_dates([row], schedule_fetcher=lambda _: {
                "response": [{"id": 12, "date": "2025-01-05"}]})

    def test_input_unchanged_and_no_guessing(self):
        row = record(12)
        enriched = enrich_verified_dates([row], schedule_fetcher=lambda _: {
            "response": [{"id": 12, "date": "2025-01-05"}]})
        self.assertNotIn("game_date", row)
        self.assertEqual(enriched[0]["game_date"], "2025-01-05")
        with self.assertRaises(GameDateVerificationError):
            enrich_verified_dates([{"source": "api_basketball_v1", "game_id": None}])


if __name__ == "__main__":
    unittest.main()
