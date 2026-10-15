"""Chạy bộ vignette giả lập qua lõi gợi ý và in chỉ số.

python3 run_eval.py            # chế độ luật
python3 run_eval.py --llm      # chế độ LLM (cần LLM_API_KEY, LLM_MODEL)

Nhãn kỳ vọng do AI soạn để kiểm thử kỹ thuật, CHƯA được bác sĩ duyệt.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "app"))
import triage  # noqa: E402

use_llm = "--llm" in sys.argv
rows = [json.loads(l) for l in (pathlib.Path(__file__).parent / "vignettes.jsonl").read_text(encoding="utf-8").splitlines()]
results = []
for v in rows:
    r = triage.triage(v["text"], v["age_group"], use_llm=use_llm)
    got = [s["specialty"] for s in r["suggestions"]]
    if v["expect_red_flag"]:
        ok = r["red_flag"]
    else:
        ok = (not r["red_flag"]) and bool(set(got[:2]) & set(v["acceptable"]))
        if v["age_group"] == "tre-em" and not r["red_flag"]:
            ok = ok and got[:1] == ["nhi"]
    results.append((v, r, got, ok))
    mark = "PASS" if ok else "FAIL"
    print(f"{mark}  {v['id']:<4} {v['text'][:42]:<44} -> {'CẤP CỨU' if r['red_flag'] else ', '.join(got)}"
          + (f"   [{v['note']}]" if v["note"] else ""))

red = [x for x in results if x[0]["expect_red_flag"]]
normal = [x for x in results if not x[0]["expect_red_flag"]]
caught = sum(1 for _, r, _, _ in red if r["red_flag"])
false_alarm = sum(1 for _, r, _, _ in normal if r["red_flag"])
routed = sum(1 for v, r, got, ok in normal if ok)
print()
print(f"Chế độ: {'LLM' if use_llm else 'luật'} · {len(rows)} vignette")
print(f"Bắt được ca cấp cứu (recall, mục tiêu 100%): {caught}/{len(red)}")
print(f"Báo cấp cứu nhầm ở ca thường: {false_alarm}/{len(normal)}")
print(f"Gợi ý đúng khoa trong top-2 (ca thường): {routed}/{len(normal)}")
print(f"Có hỏi lại vì mô tả mơ hồ: {sum(1 for _, r, _, _ in results if r.get('clarify'))}")
sys.exit(0 if caught == len(red) else 1)
