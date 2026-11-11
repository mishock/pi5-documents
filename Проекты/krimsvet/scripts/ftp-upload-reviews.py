#!/usr/bin/env python3
"""Загрузка отзывов и связанных страниц krimsvet.ru по FTP. Обновлено: 2026-11-11."""
from __future__ import annotations

import ftplib
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / "credentials" / "regru-hosting.env"
SITE = Path(__file__).resolve().parents[1] / "site"

FILES = [
    "index.html",
    "styles.css",
    "sitemap.xml",
    ".htaccess",
    "otzyvy/index.html",
    "kvartira/index.html",
    "dom/index.html",
    "biznes/index.html",
    "cena/index.html",
    "simferopol/index.html",
    "media/reviews/review-01.mp4",
    "media/reviews/review-01-poster.jpg",
    "media/reviews/review-01-gear.jpg",
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
    host = vals["FTP_HOST"]
    user = vals["FTP_USER"]
    passwd = vals["FTP_PASS"]
    base = vals.get("FTP_PATH", "www/krimsvet.ru/").strip("/") 

    ftp = ftplib.FTP()
    ftp.connect(host, 21, timeout=90)
    ftp.login(user, passwd)
    ftp.set_pasv(True)
    print("login ok", ftp.pwd(), flush=True)

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
        name = Path(rel).name
        size = local.stat().st_size
        print(f"upload {rel} ({size / 1024 / 1024:.2f} MB) ...", flush=True)
        with open(local, "rb") as handle:
            ftp.storbinary(f"STOR {name}", handle, blocksize=1024 * 256)
        print("  ok", flush=True)

    ftp.quit()
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
