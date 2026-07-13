import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API_KEY = os.getenv("SPORTRADAR_API_KEY")
if not API_KEY:
    print("ERROR: SPORTRADAR_API_KEY is not available to this workflow.")
    sys.exit(1)

# Sportradar product versions can vary by account. Start with the current WNBA
# trial hierarchy endpoint and allow easy override from GitHub Actions later.
BASE_URL = os.getenv(
    "SPORTRADAR_WNBA_TEST_URL",
    "https://api.sportradar.com/wnba/trial/v8/en/league/hierarchy.json",
)

url = f"{BASE_URL}?{urllib.parse.urlencode({'api_key': API_KEY})}"
request = urllib.request.Request(
    url,
    headers={
        "Accept": "application/json",
        "User-Agent": "SharpEdge-WNBA-Monitor/1.0",
    },
)

try:
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
        print(f"SUCCESS: Sportradar responded with HTTP {response.status}.")
        print(f"Endpoint: {BASE_URL}")
        print("Top-level response fields:", ", ".join(payload.keys()))
except urllib.error.HTTPError as exc:
    body = exc.read().decode("utf-8", errors="replace")
    print(f"HTTP ERROR {exc.code}: {exc.reason}")
    print(body[:1000])
    sys.exit(1)
except urllib.error.URLError as exc:
    print(f"NETWORK ERROR: {exc.reason}")
    sys.exit(1)
except json.JSONDecodeError:
    print("ERROR: Sportradar returned a response that was not valid JSON.")
    sys.exit(1)
