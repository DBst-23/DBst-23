import requests
from datetime import datetime
from typing import Dict, Any


class TelegramAlerts:

    @staticmethod
    def send_alert(bot_token: str, chat_id: str, message: str) -> Dict[str, Any]:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload, timeout=10)
            return {"status": "sent", "response": response.json()}
        except Exception as e:
            return {"status": "failed", "error": str(e)}


class ExecutionLogger:

    @staticmethod
    def build_message(execution_result: Dict[str, Any]) -> str:
        return (
            f"\n📊 SharpEdge Execution Log\n"
            f"Time: {datetime.utcnow().isoformat()}\n"
            f"Status: {execution_result.get('status')}\n"
            f"Confidence: {execution_result.get('confidence')}\n"
            f"Units: {execution_result.get('units')}\n"
            f"Message: {execution_result.get('message')}\n"
        )


if __name__ == "__main__":
    msg = ExecutionLogger.build_message({"status": "EXECUTED", "confidence": 82, "units": 1.5, "message": "Simulated"})
    print(msg)
