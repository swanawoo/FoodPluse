import os, json, re, html, pathlib, datetime as dt
import yaml
from dotenv import load_dotenv

load_dotenv()
ROOT = pathlib.Path(__file__).resolve().parent.parent
#CFG = yaml.safe_load(open(ROOT / "config/sources.yaml", encoding="utf-8"))
with open(ROOT / "config/sources.yaml", encoding="utf-8") as f:
    CFG = yaml.safe_load(f)

def new_batch_id():
    return dt.datetime.now().strftime("%Y%m%dT%H%M%S")

def headers(prefix):  # "SHOPPING" 또는 "SEARCH"
    return {"X-NCP-APIGW-API-KEY-ID": os.environ[f"{prefix}_KEY_ID"],
            "X-NCP-APIGW-API-KEY": os.environ[f"{prefix}_KEY"]}

def save_raw(source, bid, filename, request, response):
    d = ROOT / "data/raw" / source / bid
    d.mkdir(parents=True, exist_ok=True)
    envelope = {"source": source, "batch_id": bid,
                "fetched_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                "request": request,      # 파라미터만 저장. 헤더(키)는 절대 저장하지 않음
                "response": response}
    (d / filename).write_text(json.dumps(envelope, ensure_ascii=False), encoding="utf-8")

def strip_html(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()
