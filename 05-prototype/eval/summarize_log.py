"""Tóm tắt log thử nghiệm (logs/sessions.jsonl) theo từng người thử.

python3 eval/summarize_log.py [đường-dẫn-log]

Bảng 1 là luồng chính "Chuẩn bị buổi khám". Bảng 2 là module chọn khoa cũ (backlog B1), chỉ in khi có dữ liệu.
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
by_tester = collections.defaultdict(list)
for e in events:
    by_tester[e.get("tester_id") or "(không mã)"].append(e)


def count(evts, name, **match):
    return sum(1 for e in evts if e["event"] == name and all(e.get(k) == v for k, v in match.items()))


def total(evts, name, key):
    return sum(len(e.get(key) or []) if isinstance(e.get(key), list) else (e.get(key) or 0)
               for e in evts if e["event"] == name)


print(f"Log: {path} · {len(events)} sự kiện · {len(by_tester)} người thử\n")
print("Chuẩn bị buổi khám")
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
