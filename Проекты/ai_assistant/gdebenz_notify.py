"""Дублирование уведомлений ГдеБЕНЗ: Telegram + email."""

from __future__ import annotations

import logging
import os
import subprocess
from typing import Any, Callable


def alert_email(cfg: dict[str, Any], chat: dict[str, Any] | None = None) -> str:
    if chat and str(chat.get("alert_email", "")).strip():
        return str(chat["alert_email"]).strip()
    if str(cfg.get("alert_email", "")).strip():
        return str(cfg["alert_email"]).strip()
    return (
        os.environ.get("GDEBENZ_ALERT_EMAIL", "")
        or os.environ.get("ELTAVR_CMS_EMAIL", "")
    ).strip()


def send_email(to: str, subject: str, body: str) -> bool:
    if not to:
        return False
    payload = (
        f"Subject: {subject}\n"
        "Content-Type: text/plain; charset=UTF-8\n\n"
        f"{body.rstrip()}\n"
    ).encode("utf-8")
    try:
        proc = subprocess.run(
            ["msmtp", "-a", "default", to],
            input=payload,
            timeout=30,
            capture_output=True,
        )
    except OSError as exc:
        logging.error("email send failed to=%s: %s", to, exc)
        return False
    if proc.returncode != 0:
        err = proc.stderr.decode("utf-8", errors="replace")[:300]
        logging.error("email send failed to=%s rc=%s err=%s", to, proc.returncode, err)
        return False
    return True


def notify_fuel_alert(
    cfg: dict[str, Any],
    chat: dict[str, Any],
    chat_id: int,
    text: str,
    send_telegram: Callable[[int, str], bool],
) -> bool:
    if cfg.get("monitoring_disabled"):
        logging.info("notify skipped: monitoring_disabled chat=%s", chat_id)
        return False
    tg_ok = send_telegram(chat_id, text)
    email_to = alert_email(cfg, chat)
    if email_to:
        first = (text.splitlines() or ["ГдеБЕНЗ"])[0].strip() or "ГдеБЕНЗ"
        if not send_email(email_to, first[:120], text):
            logging.warning("email duplicate failed chat=%s to=%s", chat_id, email_to)
    return tg_ok
