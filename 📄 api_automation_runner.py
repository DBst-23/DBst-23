import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = "comprehensive_api_automation_v1.1_config.json"

def fetch_and_store(feed):
    source = feed["source"]
    method = feed.get("method", "GET")
    auth_type = feed.get("auth")
    headers = {}

    if auth_type == "api_key":
        headers["Authorization"] = f"Bearer {os.getenv('API_KEY')}"

    print(f"📡 Fetching data from: {source}")
    response = requests.request(method, source, headers=headers)

    if response.status_code == 200:
        data = response.json()
        out_path = feed["storage_path"]
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✅ Saved to: {out_path}")
    else:
        print(f"❌ Failed with status {response.status_code}: {response.text}")

def main():
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    if not config.get("enabled", False):
        print("⚠️ Protocol is disabled in config.")
        return

    for feed_name, feed_config in config.get("data_feeds", {}).items():
        print(f"\n🔄 Starting fetch: {feed_name}")
        fetch_and_store(feed_config)

if __name__ == "__main__":
    main()