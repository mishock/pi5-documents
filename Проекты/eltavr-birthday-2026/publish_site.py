#!/usr/bin/env python3
"""Публикация открытки и поздравления на сайт ЭЛЬТАВР (Payload CMS на Pi 5)."""
import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("cms", Path.home() / "bin/eltavr-cms-core.py")
cms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cms)

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1"
TITLE = "«Эльтавру» — 12 лет! С днём рождения, команда!"

cfg = cms.load_config()
token = cms.login({**cfg, "ELTAVR_API_URL": BASE})

existing = cms.api_json("GET", f"{BASE}/api/news?where[title][equals]={cms.urllib.parse.quote(TITLE)}&depth=0", token)
if existing.get("docs"):
    print("Уже опубликовано, id", existing["docs"][0]["id"])
    sys.exit(0)

media_id = cms.upload_media(BASE, token, str(ROOT / "generated/eltavr_12_let_otkrytka.jpg"),
                            "ООО «Эльтавр» — 12 лет, 21.10.2014 — 21.10.2026", "image/jpeg")
summary = (ROOT / "site_text.txt").read_text(encoding="utf-8").strip()
doc = cms.api_json("POST", f"{BASE}/api/news", token, {
    "title": TITLE,
    "summary": summary,
    "coverImage": media_id,
    "publishedAt": datetime.now(timezone(timedelta(hours=3))).isoformat(),
    "isPublished": True,
})
print("Опубликовано, id", doc["doc"]["id"], "media", media_id)
