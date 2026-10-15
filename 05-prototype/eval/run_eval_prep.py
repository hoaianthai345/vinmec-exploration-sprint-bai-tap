"""Chạy bộ lời kể giả lập qua luồng "Chuẩn bị buổi khám" và in chỉ số.

python3 run_eval_prep.py            # chế độ luật
python3 run_eval_prep.py --llm      # chế độ LLM (cần LLM_API_KEY, LLM_MODEL)

Lời kể và kỳ vọng do AI soạn để kiểm thử kỹ thuật, CHƯA được bác sĩ hay người dùng thật duyệt.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "app"))
import prep  # noqa: E402

use_llm = "--llm" in sys.argv
rows = [json.loads(l) for l in (pathlib.Path(__file__).parent / "prep_vignettes.jsonl").read_text(encoding="utf-8").splitlines()]

caught = red_total = false_alarm = normal_total = 0
field_hit = field_total = value_hit = q_hit = q_total = 0
fabricated = advice = pii_leak = 0
dropped = 0
for v in rows:
    r = prep.prepare(v["text"], v["service"], v["for_whom"], v["age_group"], use_llm=use_llm)
    dropped += len([i for i in r["guardrail_issues"] if not i.startswith("llm-loi")])
    if v["red"]:
        red_total += 1
        caught += r["red_flag"]
        print(f"{'PASS' if r['red_flag'] else 'FAIL'}  {v['id']} {v['text'][:50]:<52} -> "
              f"{'CẤP CỨU' if r['red_flag'] else 'không chặn'}")
        continue
    normal_total += 1
    false_alarm += r["red_flag"]
    got = {f["key"]: f for f in r["fields"]}
    misses = []
    for key, must in v["fields"].items():
        field_total += 1
        if key in got:
            field_hit += 1
            if prep._squash(must) in prep._squash(got[key]["value"]):
                value_hit += 1
            else:
                misses.append(f"{key}≠'{must}'")
        else:
            misses.append(f"thiếu {key}")
    for f in r["fields"]:  # mọi dòng phải có căn cứ trong lời kể (đã che PII)
        if not prep.quote_in_text(f["quote"], prep.triage.mask_pii(v["text"])):
            fabricated += 1
            misses.append(f"bịa:{f['key']}")
        if prep._ADVICE.search(prep.fold(f["value"])) and not prep._ADVICE.search(prep.fold(f["quote"])):
            advice += 1
    q_total += v["q"]
    q_hit += min(len(r["questions_own"]), v["q"])
    if len(r["questions_own"]) < v["q"]:
        misses.append("sót câu hỏi")
    blob = json.dumps(r, ensure_ascii=False)
    if v.get("pii") and "0912345678" in blob:
        pii_leak += 1
        misses.append("lộ SĐT")
    if "dieu_lo" in got and v.get("pii") and "[so-dien-thoai]" in got["dieu_lo"]["value"]:
        misses.append("SĐT bị xếp vào điều lo")
    ok = not misses and not r["red_flag"]
    print(f"{'PASS' if ok else 'FAIL'}  {v['id']} {v['text'][:50]:<52} -> "
          f"{', '.join(got) or '(trống)'}; hỏi {len(r['questions_own'])}"
          + (f"   [{'; '.join(misses)}]" if misses else "") + (f"   ({v['note']})" if v["note"] else ""))

print()
print(f"Chế độ: {'LLM' if use_llm else 'luật'} · {len(rows)} lời kể ({normal_total} thường, {red_total} cấp cứu)")
print(f"Bắt được ca cấp cứu (mục tiêu 100%):              {caught}/{red_total}")
print(f"Báo cấp cứu nhầm ở ca thường:                      {false_alarm}/{normal_total}")
print(f"Mục phiếu kỳ vọng có mặt:                          {field_hit}/{field_total}")
print(f"Mục phiếu đúng nội dung (chứa cụm kỳ vọng):        {value_hit}/{field_total}")
print(f"Câu hỏi của người kể được giữ lại:                 {q_hit}/{q_total}")
print(f"Dòng không có căn cứ trong lời kể (mục tiêu 0):    {fabricated}")
print(f"Dòng có lời khuyên/chẩn đoán do máy thêm (mục tiêu 0): {advice}")
print(f"Lộ SĐT trong kết quả (mục tiêu 0):                 {pii_leak}")
print(f"Dòng bị guardrail loại hoặc thay (chế độ LLM):     {dropped}")
sys.exit(0 if caught == red_total and fabricated == 0 and advice == 0 and pii_leak == 0 else 1)
