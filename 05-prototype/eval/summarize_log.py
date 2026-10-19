"""Tóm tắt log thử nghiệm (logs/sessions.jsonl) theo từng người thử.

python3 eval/summarize_log.py [đường-dẫn-log]

Bảng 1 là luồng hiện hành "Lộ trình khám trong ngày" (từ 18/10/2026), kèm danh sách mọi câu hỏi người thử gõ vào
trợ lý (đã che SĐT/email) để chấm tay: đây là bộ câu hỏi thật, chưa từng dùng để chỉnh luật.
Bảng 2 "Chuẩn bị buổi khám" (hướng H1) và bảng 3 chọn khoa (hướng H0) chỉ in khi có dữ liệu.
"""
import collections
import json
import pathlib
import statistics
import sys

path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).parent.parent / "logs" / "sessions.jsonl"
if not path.exists():
    sys.exit(f"Chưa có log ở {path}. Chạy server và thử app trước.")

events = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
tour_n = sum(1 for e in events if e.get("tester_id") == "TOUR")
events = [e for e in events if e.get("tester_id") != "TOUR"]  # lượt chạy tour cho người chấm, không phải người thử
by_tester = collections.defaultdict(list)
for e in events:
    by_tester[e.get("tester_id") or "(không mã)"].append(e)


def count(evts, name, **match):
    return sum(1 for e in evts if e["event"] == name and all(e.get(k) == v for k, v in match.items()))


def total(evts, name, key):
    return sum(len(e.get(key) or []) if isinstance(e.get(key), list) else (e.get(key) or 0)
               for e in evts if e["event"] == name)


print(f"Log: {path} · {len(events)} sự kiện · {len(by_tester)} người thử"
      + (f" · đã bỏ {tour_n} sự kiện của tour (mã TOUR)" if tour_n else "") + "\n")
if any(e["event"] in ("route", "ask") for e in events):
    print("Lộ trình khám trong ngày")
    print(" | ".join(("Người thử", "Xem lộ trình", "Bước đã xong", "Bấm chỉ đường", "Mở trợ lý", "Câu hỏi",
                      "Gõ tay", "Chưa hiểu", "Chuyển bác sĩ", "Cấp cứu", "Chế độ", "Thời gian (giây)", "Hữu ích có/không")))
    for tester, evts in sorted(by_tester.items()):
        asks = [e for e in evts if e["event"] == "ask"]
        if not asks and not count(evts, "route"):
            continue
        secs = [e["seconds"] for e in evts if e["event"] == "finish_visit" and e.get("seconds")]
        modes = sorted({e.get("mode", "") for e in asks}) or ["-"]
        print(" | ".join(str(x) for x in (
            tester, count(evts, "route"), count(evts, "step_done"), count(evts, "show_directions"),
            count(evts, "open_assistant"), len(asks), sum(1 for e in asks if e.get("via") == "go"),
            sum(1 for e in asks if e.get("fallback")), sum(1 for e in asks if e.get("medical")),
            sum(1 for e in asks if e.get("red_flag")), ",".join(modes),
            round(statistics.mean(secs)) if secs else "-",
            f"{count(evts, 'feedback', useful=True)}/{count(evts, 'feedback', useful=False)}")))
    typed = [e for e in events if e["event"] == "ask" and e.get("via") == "go"]
    if typed:
        print("\nCâu hỏi người thử tự gõ (chấm tay: loại câu hỏi máy chọn có đúng không?)")
        for e in typed:
            print(f"- {e.get('tester_id') or '?'} [{e.get('mode')}] {e.get('question_masked')!r} -> {e.get('intent')}/{e.get('target')}"
                  + (" · CHƯA HIỂU" if e.get("fallback") else ""))
    print()

if any(e["event"] == "prepare" for e in events):
    print("Chuẩn bị buổi khám (hướng H1, bản v1/v2)")
    header = ("Người thử", "Bắt đầu", "Để sau", "Cấp cứu", "Mục AI điền", "Sửa", "Xoá", "Tự thêm mục",
              "Câu hỏi của mình", "Chọn câu gợi ý", "Tự thêm câu", "Gửi phiếu", "Thời gian TB (giây)",
              "Hữu ích có/không", "Guardrail")
    print(" | ".join(header))
    for tester, evts in sorted(by_tester.items()):
        preps = [e for e in evts if e["event"] == "prepare"]
        secs = [e["seconds"] for e in evts if e["event"] == "submit" and e.get("seconds")]
        row = (tester, count(evts, "start_prep"), count(evts, "skip_prep"), sum(1 for e in preps if e["red_flag"]),
               sum(len(e.get("fields_found", [])) for e in preps),
               total(evts, "confirm_summary", "edited"), total(evts, "confirm_summary", "deleted"),
               total(evts, "confirm_summary", "added"), total(evts, "confirm_questions", "own_kept"),
               total(evts, "confirm_questions", "suggested_chosen"), total(evts, "confirm_questions", "custom_added"),
               count(evts, "submit"), round(statistics.mean(secs)) if secs else "-",
               f"{count(evts, 'feedback', useful=True)}/{count(evts, 'feedback', useful=False)}",
               sum(len(e.get("guardrail_issues", [])) for e in preps))
        print(" | ".join(str(x) for x in row))

if any(e["event"] == "triage" for e in events):
    print("\nModule chọn khoa cũ (backlog B1)")
    print(" | ".join(("Người thử", "Lượt gợi ý", "Cấp cứu", "Chọn theo gợi ý", "Tự chọn khoa", "Đặt xong")))
    for tester, evts in sorted(by_tester.items()):
        triages = [e for e in evts if e["event"] == "triage"]
        if triages:
            print(" | ".join(str(x) for x in (tester, len(triages), sum(1 for e in triages if e["red_flag"]),
                                              count(evts, "choose_specialty"), count(evts, "manual_specialty"),
                                              count(evts, "book"))))

comments = [(e.get("tester_id"), e["comment"]) for e in events if e["event"] == "feedback" and e.get("comment")]
if comments:
    print("\nNhận xét người thử để lại (đã che SĐT/email):")
    for tester, c in comments:
        print(f"- {tester}: {c}")
