from datetime import datetime
from typing import List, Dict, Any


class LiveOddsScraperSim:

    @staticmethod
    def fetch_live_lines() -> List[Dict[str, Any]]:
        """Simulated odds feed"""
        return [
            {"player": "Evan Mobley", "market": "Rebounds", "line": 10.5, "odds": -110},
            {"player": "Bobby Portis", "market": "Rebounds", "line": 8.5, "odds": -105},
        ]


class AutoTriggerEngine:

    @staticmethod
    def detect_edges(lines: List[Dict[str, Any]], model_outputs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        triggered = []

        for line in lines:
            for model in model_outputs:
                if line["player"] == model["player"]:
                    edge = model.get("projection", 0) - line["line"]

                    if abs(edge) >= 1.0 and model.get("confidence_score", 0) >= 72:
                        triggered.append({
                            "player": line["player"],
                            "market": line["market"],
                            "edge": round(edge,2),
                            "confidence": model.get("confidence_score"),
                            "timestamp": datetime.utcnow().isoformat()
                        })

        return triggered


if __name__ == "__main__":
    lines = LiveOddsScraperSim.fetch_live_lines()
    model = [
        {"player": "Evan Mobley", "projection": 12.0, "confidence_score": 86},
        {"player": "Bobby Portis", "projection": 7.0, "confidence_score": 52},
    ]
    print(AutoTriggerEngine.detect_edges(lines, model))
