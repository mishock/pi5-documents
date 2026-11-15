#!/usr/bin/env python3
"""Создать JS-цели Метрики для krimsvet.ru. Обновлено: 2026-11-15.

Нужен OAuth-токен Яндекса с правом metrika:write:
  export YANDEX_OAUTH_TOKEN='...'
  python3 scripts/metrika-create-goals.py
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

COUNTER_ID = 114159186
API = f"https://api-metrika.yandex.net/management/v1/counter/{COUNTER_ID}/goals"

GOALS = [
    {"name": "Подбор комплекта", "id": "calc_complete"},
    {"name": "Заявка отправлена", "id": "lead_submit"},
    {"name": "Клик по телефону", "id": "phone_click"},
]


def api(method: str, token: str, path: str = "", body: dict | None = None) -> dict:
    url = API + path
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"OAuth {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> int:
    token = os.environ.get("YANDEX_OAUTH_TOKEN", "").strip()
    if not token:
        print("Нет YANDEX_OAUTH_TOKEN", file=sys.stderr)
        return 2

    existing = api("GET", token).get("goals") or []
    by_cond = set()
    for g in existing:
        for c in g.get("conditions") or []:
            if c.get("url"):
                by_cond.add(c["url"])
        if g.get("type") == "action" and g.get("conditions"):
            pass
    print("existing goals:", len(existing))
    for g in existing:
        print(" -", g.get("id"), g.get("name"), g.get("type"), g.get("conditions"))

    for item in GOALS:
        if item["id"] in by_cond:
            print("skip exists", item["id"])
            continue
        payload = {
            "goal": {
                "name": item["name"],
                "type": "action",
                "conditions": [{"type": "exact", "url": item["id"]}],
            }
        }
        try:
            created = api("POST", token, body=payload)
            print("created", item["id"], "->", created.get("goal", {}).get("id"))
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", errors="replace")
            print("FAIL", item["id"], err.code, detail, file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
