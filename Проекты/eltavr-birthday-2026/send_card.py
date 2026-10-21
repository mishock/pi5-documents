#!/usr/bin/env python3
"""Отправка открытки на почту через msmtp: python3 send_card.py [получатель]"""
import subprocess
import sys
from email.message import EmailMessage
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TO = sys.argv[1] if len(sys.argv) > 1 else "mishock24@gmail.com"

msg = EmailMessage()
msg["To"] = TO
msg["Subject"] = "🎉 ООО «Эльтавр» — 12 лет! Открытка и поздравление для общего чата"
msg.set_content((ROOT / "pozdravlenie.txt").read_text(encoding="utf-8"))
for name in ("eltavr_12_let_otkrytka.jpg",):
    msg.add_attachment((ROOT / "generated" / name).read_bytes(), maintype="image", subtype="jpeg", filename=name)
subprocess.run(["msmtp", TO], input=msg.as_bytes(), check=True)
print("Отправлено на", TO)
