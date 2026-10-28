import json
import tempfile
import unittest
from pathlib import Path
from liveflow.nba.strict_registry import append_checkpoint
from tests.test_liveflow_sync_gate import fixtures

class StrictRegistryTests(unittest.TestCase):
    def test_pass_writes_once_and_duplicate_rejected(self):
        f, m = fixtures()
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            fp, mp, rp = (root / x for x in ("freeze.json", "market.json", "registry.json"))
            fp.write_text(json.dumps(f))
            mp.write_text(json.dumps(m))
            self.assertEqual(append_checkpoint(fp, mp, rp)["status"], "PASS")
            self.assertEqual(len(json.loads(rp.read_text())["games"]), 1)
            with self.assertRaises(ValueError):
                append_checkpoint(fp, mp, rp)
            self.assertEqual(len(json.loads(rp.read_text())["games"]), 1)

    def test_score_mismatch_never_writes(self):
        f, m = fixtures()
        m["home_score"] += 2
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            fp, mp, rp = (root / x for x in ("freeze.json", "market.json", "registry.json"))
            fp.write_text(json.dumps(f))
            mp.write_text(json.dumps(m))
            with self.assertRaises(ValueError):
                append_checkpoint(fp, mp, rp)
            self.assertFalse(rp.exists())

if __name__ == "__main__":
    unittest.main()
