#!/usr/bin/env python3
"""Залить цели Метрики (JS) на krimsvet.ru. Обновлено: 2026-11-15."""
from __future__ import annotations

import ftplib
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / "credentials" / "regru-hosting.env"
SITE = Path(__file__).resolve().parents[1] / "site"

FILES = [
    "metrika-goals.js",
    "app.js",
    "index.html",
    "otzyvy/index.html",
    "kvartira/index.html",
    "dom/index.html",
    "biznes/index.html",
    "cena/index.html",
    "simferopol/index.html",
]


def load_env(path: Path) -> dict[str, str]:
    vals: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        vals[key] = value.strip().strip("'\"")
    return vals


def ensure_dirs(ftp: ftplib.FTP, path: str) -> None:
    parts = [p for p in path.strip("/").split("/") if p]
    cur = ""
    for part in parts:
        cur = f"{cur}/{part}" if cur else part
        try:
            ftp.mkd(cur)
        except ftplib.error_perm:
            pass


def main() -> None:
    vals = load_env(ENV_PATH)
    ftp = ftplib.FTP()
    ftp.connect(vals["FTP_HOST"], 21, timeout=90)
    ftp.login(vals["FTP_USER"], vals["FTP_PASS"])
    ftp.set_pasv(True)
    base = vals.get("FTP_PATH", "www/krimsvet.ru/").strip("/")
    for part in base.split("/"):
        try:
            ftp.cwd(part)
        except ftplib.error_perm:
            ftp.mkd(part)
            ftp.cwd(part)
    root = ftp.pwd()
    print("site root", root, flush=True)

    for rel in FILES:
        local = SITE / rel
        if not local.exists():
            print("MISSING", rel, flush=True)
            continue
        remote_dir = str(Path(rel).parent).replace("\\", "/")
        ftp.cwd(root)
        if remote_dir not in (".", ""):
            ensure_dirs(ftp, remote_dir)
            for part in remote_dir.split("/"):
                ftp.cwd(part)
        with open(local, "rb") as handle:
            ftp.storbinary(f"STOR {Path(rel).name}", handle)
        print("ok", rel, flush=True)
    ftp.quit()
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
