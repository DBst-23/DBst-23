import os, json, sys, time
from datetime import datetime
from dateutil import tz
import requests
import yaml

TODAY = datetime.now(tz.gettz("UTC")).strftime("%Y-%m-%d")

def render(value):
    if isinstance(value, str):
        return (value
                .replace("{{today}}", TODAY)
                .replace("{{utc_now}}", datetime.utcnow().isoformat()))
    return value

def render_env(val):
    if isinstance(val, str) and "{{env." in val:
        out = val
        while "{{env." in out:
            start = out.index("{{env.") + 6
            end = out.index("}}", start)
            key = out[start:end]
            out = out.replace(f"{{{{env.{key}}}}}", os.getenv(key, ""))
        return out
    if isinstance(val, dict):
        return {k: render_env(v) for k,v in val.items()}
    if isinstance(val, list):
        return [render_env(x) for x in val]
    return val

def save_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def run_job(job):
    if not job.get("enabled", True):
        return {"id": job["id"], "status": "skipped"}
    method = job.get("method", "GET").upper()
    url = render(job["url"])
    headers = render_env(job.get("headers", {}))
    params  = render_env(job.get("params", {}))
    body    = render_env(job.get("body_json", None))
    out_path = render(job["out_path"])
    t0 = time.time()
    try:
        resp = requests.request(method, url, headers=headers, params=params,
                                json=body, timeout=60)
        resp.raise_for_status()
        text = resp.text
        if out_path.endswith(".json"):
            try:
                obj = resp.json()
                text = json.dumps(obj, indent=2, ensure_ascii=False)
            except Exception:
                pass
        save_text(out_path, text)
        dur = round(time.time()-t0, 2)
        return {"id": job["id"], "status": "ok", "ms": int(dur*1000), "bytes": len(text), "out_path": out_path}
    except Exception as e:
        return {"id": job["id"], "status": "error", "error": str(e)}

def main():
    with open("jobs/api_jobs.yaml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    results = [run_job(j) for j in cfg["jobs"]]
    log = {"run_at_utc": datetime.utcnow().isoformat(), "results": results}
    os.makedirs("data/logs", exist_ok=True)
    stamp = datetime.utcnow().strftime("%Y%m%dT%H%M%S")
    save_text(f"data/logs/api_run_{stamp}.json", json.dumps(log, indent=2))
    ok = sum(1 for r in results if r["status"]=="ok")
    err = sum(1 for r in results if r["status"]=="error")
    print(f"[API-RUN] OK={ok} ERRORS={err}")
    if err>0:
        sys.exit(1)

if __name__ == "__main__":
    main()
