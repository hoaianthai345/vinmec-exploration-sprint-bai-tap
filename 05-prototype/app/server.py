"""Server local cho prototype "Chuẩn bị buổi khám". Chỉ dùng thư viện chuẩn của Python.

Trang chính (/) là luồng Chuẩn bị buổi khám (prep.py). Trang /chon-khoa.html là module gợi ý chuyên khoa cũ
(triage.py), giữ lại cho backlog B1.

Chạy:  python3 server.py            (chế độ luật, không cần API key)
       LLM_API_KEY=... LLM_MODEL=... [LLM_BASE_URL=...] python3 server.py   (chế độ LLM)
Mở:    http://localhost:8000
"""

from __future__ import annotations

import datetime as dt
import json
import os
import pathlib
import random
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import prep
import triage

ROOT = pathlib.Path(__file__).parent
STATIC = ROOT / "static"
LOG_FILE = pathlib.Path(os.environ.get("LOG_FILE", ROOT.parent / "logs" / "sessions.jsonl"))
PORT = int(os.environ.get("PORT", "8000"))

PREPARE_COMMON = [
    "CCCD hoặc giấy tờ tuỳ thân, thẻ BHYT/bảo hiểm (nếu có)",
    "Đơn thuốc, kết quả xét nghiệm hoặc phim chụp cũ liên quan (nếu có)",
    "Ghi sẵn 2–3 câu bạn muốn hỏi bác sĩ",
    "Đến sớm 15–20 phút để làm thủ tục",
    "Nếu dự định làm xét nghiệm máu, hỏi tổng đài trước xem có cần nhịn ăn không",
]
PREPARE_CHILD = ["Sổ tiêm chủng và sổ khám của bé (nếu có)"]


def log_event(event: dict) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    event = {"ts": dt.datetime.now().isoformat(timespec="seconds"), **event}
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def mock_slots(specialty: str) -> list[dict]:
    """Lịch trống GIẢ LẬP, chỉ để bấm thử luồng đặt lịch."""
    rng = random.Random(specialty)
    today = dt.date.today()
    slots = []
    for day in range(1, 4):
        date = today + dt.timedelta(days=day)
        for hour in sorted(rng.sample([8, 9, 10, 13, 14, 15, 16], 3)):
            slots.append({"date": date.isoformat(), "time": f"{hour:02d}:{rng.choice(['00', '30'])}",
                          "site": rng.choice(["Cơ sở 1 (giả lập)", "Cơ sở 2 (giả lập)"])})
    return slots


class Handler(BaseHTTPRequestHandler):
    def _send(self, status: int, body: bytes, ctype: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, data: dict) -> None:
        self._send(status, json.dumps(data, ensure_ascii=False).encode(), "application/json; charset=utf-8")

    def log_message(self, *_args) -> None:  # giữ terminal gọn khi demo
        pass

    def do_GET(self) -> None:
        if self.path == "/api/config":
            return self._json(200, {"mode": "llm" if triage.llm_configured() else "rules",
                                    "specialties": triage.SPECIALTIES,
                                    "services": {k: v["name"] for k, v in prep.SERVICES.items()}})
        name = "index.html" if self.path in ("/", "/index.html") else self.path.lstrip("/")
        file = (STATIC / name).resolve()
        if not str(file).startswith(str(STATIC.resolve())) or not file.is_file():
            return self._send(404, b"Not found", "text/plain")
        ctype = {"html": "text/html", "css": "text/css", "js": "application/javascript"}.get(file.suffix[1:], "text/plain")
        self._send(200, file.read_bytes(), f"{ctype}; charset=utf-8")

    def do_POST(self) -> None:
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._json(400, {"error": "Dữ liệu gửi lên không hợp lệ"})

        session = str(data.get("session_id", ""))[:40]
        tester = str(data.get("tester_id", ""))[:20]

        if self.path == "/api/prepare":
            text = str(data.get("text", ""))[:1500]
            age_group = "tre-em" if data.get("age_group") == "tre-em" else "nguoi-lon"
            for_whom = "nguoi-than" if data.get("for_whom") == "nguoi-than" else "ban-than"
            result = prep.prepare(text, str(data.get("service", "")), for_whom, age_group)
            log_event({"event": "prepare", "session_id": session, "tester_id": tester, "for_whom": for_whom,
                       "age_group": age_group, "service": result["service"],
                       **{k: result[k] for k in ("mode", "input_masked", "red_flag", "red_flag_reasons",
                                                 "guardrail_issues", "latency_ms")},
                       "fields_found": [f["key"] for f in result["fields"]],
                       "own_questions": len(result["questions_own"])})
            result.pop("input_masked")
            return self._json(200, result)

        if self.path == "/api/triage":
            text = str(data.get("text", ""))[:1000]
            age_group = "tre-em" if data.get("age_group") == "tre-em" else "nguoi-lon"
            result = triage.triage(text, age_group)
            result["prepare"] = PREPARE_COMMON + (PREPARE_CHILD if age_group == "tre-em" else [])
            log_event({"event": "triage", "session_id": session, "tester_id": tester,
                       "for_whom": data.get("for_whom"), "age_group": age_group,
                       **{k: result[k] for k in ("mode", "input_masked", "red_flag", "red_flag_reasons",
                                                 "confidence", "guardrail_issues", "latency_ms")},
                       "suggested": [s["specialty"] for s in result["suggestions"]],
                       "clarify_asked": bool(result["clarify"])})
            result.pop("input_masked")
            return self._json(200, result)

        if self.path == "/api/slots":
            specialty = data.get("specialty")
            if specialty not in triage.SPECIALTIES:
                return self._json(400, {"error": "Chuyên khoa không hợp lệ"})
            child = data.get("age_group") == "tre-em"
            return self._json(200, {"slots": mock_slots(specialty),
                                    "prepare": PREPARE_COMMON + (PREPARE_CHILD if child else [])})

        if self.path == "/api/event":
            allowed = {"choose_specialty", "manual_specialty", "book", "call_hotline",
                       "emergency_ack", "feedback", "restart",
                       # Chuẩn bị buổi khám
                       "start_prep", "skip_prep", "confirm_summary", "confirm_questions", "submit"}
            if data.get("event") not in allowed:
                return self._json(400, {"error": "Sự kiện không hợp lệ"})
            detail = {k: data.get(k) for k in ("specialty", "slot", "useful", "comment", "step", "edited",
                                                "deleted", "added", "own_kept", "suggested_chosen",
                                                "custom_added", "seconds")
                      if data.get(k) is not None}
            if "comment" in detail:
                detail["comment"] = triage.mask_pii(str(detail["comment"]))[:500]
            log_event({"event": data["event"], "session_id": session, "tester_id": tester, **detail})
            return self._json(200, {"ok": True})

        self._json(404, {"error": "Không có endpoint này"})


if __name__ == "__main__":
    mode = "LLM (" + os.environ.get("LLM_MODEL", "") + ")" if triage.llm_configured() else "luật từ khoá (không cần API key)"
    print(f"Prototype chạy ở http://localhost:{PORT} · chế độ gợi ý: {mode}")
    print(f"Log thử nghiệm: {LOG_FILE}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
