"""Vercel serverless: endpoint /api/event, dùng lại đúng Handler của server.py.

Mỗi endpoint một file để Vercel giữ nguyên đường dẫn gốc (rewrite làm function nhận đường dẫn đã bị viết lại).
Vercel chỉ ghi được vào /tmp nên log ghi vào /tmp/sessions.jsonl (mất khi function khởi động lại): bản deploy chỉ để xem
demo, log thử thật vẫn chạy local.
"""

import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
os.environ.setdefault("LOG_FILE", "/tmp/sessions.jsonl")

import server  # noqa: E402


class handler(server.Handler):
    pass
