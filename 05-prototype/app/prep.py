"""Lõi "Chuẩn bị buổi khám": lời kể tự do -> phiếu tóm tắt cho bác sĩ + câu hỏi + checklist.

Thứ tự xử lý (không đổi được bằng prompt):
1. Che thông tin cá nhân (dùng lại triage.mask_pii).
2. Luật dấu hiệu cấp cứu (dùng lại triage.detect_red_flags). Có dấu hiệu -> dừng, hướng dẫn gọi 115, KHÔNG gọi LLM.
3. Tóm tắt vào khung phiếu cố định: dùng LLM nếu đã cấu hình, nếu không thì dùng luật tách câu.
4. Kiểm tra đầu ra: mỗi dòng phải kèm đoạn TRÍCH NGUYÊN VĂN có trong lời kể, nếu không có thì bỏ dòng đó
   (AI không được thêm điều người bệnh không nói). Dòng có chẩn đoán/khuyên thuốc, hoặc dưới 70% số từ có trong
   lời kể, thì thay bằng nguyên văn.
5. Câu hỏi gợi ý và checklist chuẩn bị là LUẬT CỐ ĐỊNH, không do LLM sinh. Câu hỏi y khoa của người bệnh không
   được trả lời, chỉ được ghi vào danh sách "hỏi bác sĩ".
"""

from __future__ import annotations

import json
import os
import re
import time
import unicodedata
import urllib.request

import triage

# Khung phiếu tóm tắt. Thứ tự là thứ tự bác sĩ đọc.
FIELDS = {
    "ly_do": "Lý do chính",
    "tu_khi_nao": "Từ khi nào",
    "da_lam": "Đã khám / đã dùng thuốc / đã thử",
    "dieu_lo": "Điều lo nhất",
    "mong_muon": "Mong bác sĩ giúp",
}

# Dịch vụ GIẢ LẬP cho prototype. Mục có source="vinmec" lấy từ trang công khai của Vinmec; mục "prototype" là đề xuất
# của bài tập, cần Vinmec xác nhận trước khi dùng thật.
VINMEC_TQ = "https://www.vinmec.com/vie/bai-viet/nhung-dieu-can-luu-y-truoc-khi-kham-suc-khoe-tong-quat-vi"
COMMON_DOCS = {"text": "Giấy tờ tuỳ thân, thẻ bảo hiểm (nếu có)", "source": "prototype"}
SERVICES = {
    "kham-chuyen-khoa": {
        "name": "Khám chuyên khoa (lần đầu)",
        "checklist": [
            COMMON_DOCS,
            {"text": "Kết quả xét nghiệm, phim chụp hoặc đơn thuốc cũ liên quan (nếu có)", "source": "prototype"},
            {"text": "Thuốc hoặc vỏ hộp thuốc đang dùng", "source": "prototype", "key": "thuoc"},
            {"text": "Chưa rõ có xét nghiệm máu không: hỏi tổng đài trước xem có cần nhịn ăn", "source": "prototype"},
            {"text": "Đến sớm 15–20 phút để làm thủ tục", "source": "prototype"},
        ],
    },
    "kham-tong-quat": {
        "name": "Khám sức khoẻ tổng quát",
        "checklist": [
            {"text": "Không ăn sáng; tránh đồ uống có đường, có gas, trà, cà phê trước khi lấy máu", "source": "vinmec", "url": VINMEC_TQ},
            {"text": "Uống nhiều nước và nhịn tiểu cho tới khi siêu âm ổ bụng xong", "source": "vinmec", "url": VINMEC_TQ},
            {"text": "Nữ: không khám phụ khoa trong kỳ kinh; đang mang thai thì báo trước (không chụp X-quang)", "source": "vinmec", "url": VINMEC_TQ, "key": "nguoi-lon"},
            COMMON_DOCS,
            {"text": "Thuốc hoặc vỏ hộp thuốc đang dùng", "source": "prototype", "key": "thuoc"},
        ],
    },
    "tai-kham": {
        "name": "Tái khám",
        "checklist": [
            COMMON_DOCS,
            {"text": "Kết quả và đơn thuốc của lần khám trước", "source": "prototype"},
            {"text": "Thuốc hoặc vỏ hộp thuốc đang dùng", "source": "prototype", "key": "thuoc"},
            {"text": "Ghi lại thay đổi từ lần khám trước (đỡ hơn, nặng hơn, có gì mới)", "source": "prototype"},
        ],
    },
}
CHILD_ITEM = {"text": "Sổ tiêm chủng và sổ khám của bé (nếu có)", "source": "prototype"}
DEFAULT_SERVICE = "kham-chuyen-khoa"

# Câu hỏi gợi ý chung (kiểu question prompt list). Không chứa thông tin y khoa, chỉ giúp người bệnh hỏi đủ.
Q_FOLLOWUP = "Tôi cần tái khám khi nào, hay chỉ quay lại khi có vấn đề?"
Q_WARNING = "Dấu hiệu nào thì tôi cần quay lại hoặc đi cấp cứu ngay?"
Q_TESTS = "Tôi cần làm xét nghiệm gì, bao lâu có kết quả, ai sẽ báo kết quả cho tôi?"
Q_MEDS = "Thuốc tôi đang dùng có cần đổi hay dừng không?"
Q_CARER = "Ở nhà tôi cần theo dõi gì cho người thân, và khi nào thì gọi bệnh viện?"
Q_RESULTS = "Chỉ số nào trong đợt khám này tôi cần theo dõi thêm?"


# ---------------------------------------------------------------------------
# Tiện ích so khớp: bỏ dấu TỪNG KÝ TỰ để giữ nguyên vị trí, cắt lại được đoạn gốc
# ---------------------------------------------------------------------------
def _fold_char(ch: str) -> str:
    base = "".join(c for c in unicodedata.normalize("NFD", ch.lower()) if unicodedata.category(c) != "Mn")
    return (base.replace("đ", "d") or ch)[:1]


def fold(text: str) -> str:
    """Bỏ dấu, viết thường, GIỮ ĐỘ DÀI: fold(text)[i] ứng với text[i]."""
    return "".join(_fold_char(c) for c in unicodedata.normalize("NFC", text))


def _squash(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", fold(text)).strip()


def quote_in_text(quote: str, text: str) -> bool:
    q = _squash(quote)
    return len(q) >= 2 and q in _squash(text)


def words_from_text(value: str, text: str) -> float:
    """Tỷ lệ từ của dòng tóm tắt có xuất hiện trong lời kể (chặn diễn giải vượt lời kể)."""
    words = _squash(value).split()
    pool = set(_squash(text).split())
    return sum(w in pool for w in words) / len(words) if words else 1.0


# ---------------------------------------------------------------------------
# 3a. Tóm tắt bằng luật (chế độ không cần API key)
# ---------------------------------------------------------------------------
_TIME = re.compile(r"(?<![a-z])(?:(?:\d+|mot|hai|ba|bon|nam|sau|bay|tam|chin|muoi|vai|may|nua)\s+"
                   r"(?:ngay|tuan|thang|nam|hom|buoi)(?:\s+(?:nay|roi|qua|truoc))?"
                   r"|ca\s+(?:ngay|tuan|thang|nam)(?:\s+(?:nay|roi|qua|truoc))?"
                   r"|tu\s+(?:hom|tuan|thang|nam|sang|toi|dau)\s*\w*|hom\s+qua|sang\s+nay|toi\s+qua"
                   r"|gan\s+day|lau\s+roi|keo\s+dai|thinh\s+thoang|lau\s+lau)(?![a-z])")
_DONE = ["da uong", "dang uong", "da dung", "dang dung", "uong thuoc", "tu mua thuoc", "da kham", "da di kham",
         "da xet nghiem", "da chup", "da sieu am", "da thu", "da boi", "da tiem", "ke don", "bac si cho"]
_WORRY = ["lo", "lo lang", "so", "ngai", "khong biet co", "co sao khong", "co nguy hiem"]
# Gõ có dấu thì so khớp có dấu: "số" (điện thoại) bỏ dấu cũng thành "so" giống "sợ".
_WORRY_ACC = ["lo", "lo lắng", "sợ", "ngại", "không biết có", "có sao không", "có nguy hiểm"]
# Mệnh đề bắt đầu bằng các từ này nối tiếp ý trước ("đã uống thuốc, không đỡ").
_CONTINUE = ["khong", "van", "chua", "cung", "roi", "nhung", "ma", "lai", "con"]
_WANT = ["muon bac si", "muon duoc", "mong bac si", "nho bac si", "can bac si", "muon kiem tra", "muon kham",
         "muon hoi", "muon biet", "can tu van", "muon tu van"]
_QUESTION = ["co can", "co phai", "co nen", "bao lau", "khi nao", "tai sao", "vi sao", "co sao khong",
             "co duoc khong", "the nao", "lam sao"]
_MED_WORDS = ["thuoc", "uong", "tiem", "boi"]


def _clauses(text: str) -> list[tuple[str, bool]]:
    """Tách lời kể thành mệnh đề; trả (mệnh đề, có dấu hỏi không)."""
    out = []
    for m in re.finditer(r"[^.!?\n;]+[.!?\n;]?", text):
        sent = m.group(0)
        is_q = sent.rstrip().endswith("?")
        parts = [p.strip(" ,") for p in sent.strip(" .!?\n;").split(",")]
        parts = [p for p in parts if len(p) >= 2]
        for i, part in enumerate(parts):
            # Dấu hỏi cuối câu chỉ thuộc về vế cuối ("Sợ bị nặng, có cần chụp phim không?").
            out.append((part, is_q and i == len(parts) - 1))
    return out


def _has(squashed: str, phrases: list[str]) -> bool:
    """Khớp nguyên từ trên chữ đã bỏ dấu ("lo" không khớp "long")."""
    padded = f" {squashed} "
    return any(f" {p.strip()} " in padded for p in phrases)


def rules_summarize(text: str) -> dict:
    fields: dict[str, list[dict]] = {k: [] for k in FIELDS}
    questions: list[dict] = []
    last = None
    for clause, is_q in _clauses(text):
        f = _squash(clause)
        if is_q or _has(f, _QUESTION):
            q = clause if clause.endswith("?") else clause + "?"
            questions.append({"value": q[0].upper() + q[1:], "quote": clause})
            last = None
            continue
        if last and f.split()[0] in _CONTINUE:
            item = fields[last][-1]
            item["value"] += ", " + clause
            continue
        worry = (_has(re.sub(r"[^\w]+", " ", unicodedata.normalize("NFC", clause.lower())).strip(), _WORRY_ACC) if triage.has_accents(clause)
                 else _has(f, _WORRY))
        if _has(f, _DONE):
            last = "da_lam"
        elif worry:
            last = "dieu_lo"
        elif _has(f, _WANT) or (" muon " in f" {f} " and " khong muon " not in f" {f} "):
            last = "mong_muon"
        else:
            last = "ly_do"
        fields[last].append({"value": clause, "quote": clause})
        m = _TIME.search(fold(clause))
        if m and not fields["tu_khi_nao"]:
            span = clause[m.start():m.end()]
            fields["tu_khi_nao"].append({"value": span, "quote": span})
    merged = {}
    for key, items in fields.items():
        if items:
            merged[key] = {"value": "; ".join(i["value"] for i in items[:3]),
                           "quote": items[0]["quote"]}
    return {"fields": merged, "questions": questions[:5]}


# ---------------------------------------------------------------------------
# 3b. Tóm tắt bằng LLM (OpenAI-compatible chat completions)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """Bạn là trợ lý GHI CHÉP trước buổi khám của một bệnh viện, không phải bác sĩ.
Nhiệm vụ duy nhất: sắp xếp lời kể của người bệnh (hoặc người thân) vào phiếu tóm tắt để bác sĩ đọc trước.

Quy tắc bắt buộc:
- Chỉ ghi điều người kể ĐÃ NÓI. Không suy luận, không thêm, không đoán bệnh, không khuyên, không nhắc thuốc nào họ không nhắc.
- Mỗi mục có "value" (viết gọn, tối đa 25 từ, giữ từ ngữ của người kể) và "quote" (đoạn TRÍCH NGUYÊN VĂN, liền mạch, từ lời kể làm căn cứ).
- Mục không có thông tin thì để null.
- Câu người kể muốn hỏi (kể cả câu hỏi y khoa) đưa vào "questions" đúng nguyên văn kèm "quote". KHÔNG trả lời các câu hỏi đó.
- Các mục: ly_do (lý do chính), tu_khi_nao (thời gian), da_lam (đã khám / đã dùng thuốc / đã thử), dieu_lo (điều lo nhất), mong_muon (mong bác sĩ giúp gì).

Chỉ trả về JSON đúng dạng:
{"fields": {"ly_do": {"value": "...", "quote": "..."}, "tu_khi_nao": null, "da_lam": null, "dieu_lo": null, "mong_muon": null},
 "questions": [{"value": "...?", "quote": "..."}]}"""

# Dấu hiệu AI tự chẩn đoán hoặc khuyên điều trị (so trên chữ đã bỏ dấu).
_ADVICE = re.compile(r"(ban bi |co the bi |co le bi |chan doan|nen uong|nen dung|ke don|lieu dung|\bmg\b|"
                     r"dieu tri bang|kha nang cao la)")


def llm_summarize(text: str, context: str, timeout: float = 25.0) -> dict:
    base = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {
        "model": os.environ["LLM_MODEL"],
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"{context}\nLời kể:\n{text}"},
        ],
    }
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {os.environ['LLM_API_KEY']}"},
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        content = json.load(resp)["choices"][0]["message"]["content"]
    match = re.search(r"\{.*\}", content, re.S)
    if not match:
        raise ValueError("LLM không trả JSON")
    return json.loads(match.group(0))


def validate_summary(raw: dict, text: str) -> tuple[dict, list[str]]:
    """Giữ dòng có căn cứ trong lời kể; trả thêm danh sách cảnh báo guardrail để ghi log."""
    issues: list[str] = []
    fields = {}
    for key, item in (raw.get("fields") or {}).items():
        if key not in FIELDS or not isinstance(item, dict):
            if item:
                issues.append(f"muc-ngoai-khung:{key}")
            continue
        value = str(item.get("value") or "").strip()[:200]
        quote = str(item.get("quote") or "").strip()
        if not value:
            continue
        if not quote_in_text(quote, text):
            issues.append(f"khong-co-trong-loi-ke:{key}")
            continue
        if _ADVICE.search(fold(value)) and not _ADVICE.search(fold(quote)):
            issues.append(f"co-loi-khuyen:{key}")
            value = quote
        elif words_from_text(value, text) < 0.7:
            issues.append(f"dien-giai-xa-loi-ke:{key}")
            value = quote
        fields[key] = {"value": value, "quote": quote}
    questions = []
    for item in (raw.get("questions") or [])[:5]:
        if not isinstance(item, dict):
            continue
        value = str(item.get("value") or "").strip()[:200]
        quote = str(item.get("quote") or "").strip()
        if value and quote_in_text(quote, text):
            questions.append({"value": value, "quote": quote})
        elif value:
            issues.append("cau-hoi-khong-co-trong-loi-ke")
    return {"fields": fields, "questions": questions}, issues


# ---------------------------------------------------------------------------
# 5. Luật cố định: câu hỏi gợi ý và checklist
# ---------------------------------------------------------------------------
def mentions_meds(summary: dict, text: str) -> bool:
    return any(w in _squash(text).split() for w in _MED_WORDS)


def suggest_questions(summary: dict, text: str, service: str, for_whom: str) -> list[str]:
    own = {_squash(q["value"]) for q in summary["questions"]}
    picks = [Q_FOLLOWUP, Q_WARNING]
    if mentions_meds(summary, text):
        picks.append(Q_MEDS)
    if for_whom == "nguoi-than":
        picks.append(Q_CARER)
    picks.append(Q_RESULTS if service == "kham-tong-quat" else Q_TESTS)
    return [q for q in picks if _squash(q) not in own][:4]


def build_checklist(service: str, age_group: str, summary: dict, text: str) -> list[dict]:
    items = [dict(i) for i in SERVICES[service]["checklist"]]
    if age_group == "tre-em":
        items = [i for i in items if i.get("key") != "nguoi-lon"] + [dict(CHILD_ITEM)]
    if mentions_meds(summary, text):
        for i in items:
            if i.get("key") == "thuoc":
                i["why"] = "vì bạn có nhắc tới thuốc"
    return items


# ---------------------------------------------------------------------------
# Điểm vào chung
# ---------------------------------------------------------------------------
def prepare(text: str, service: str = DEFAULT_SERVICE, for_whom: str = "ban-than",
            age_group: str = "nguoi-lon", use_llm: bool | None = None) -> dict:
    started = time.perf_counter()
    service = service if service in SERVICES else DEFAULT_SERVICE
    masked = triage.mask_pii(text or "")
    flags = triage.detect_red_flags(masked)
    base = {"service": service, "service_name": SERVICES[service]["name"], "input_masked": masked}
    if flags:
        return {**base, "mode": "rule-red-flag", "red_flag": True, "red_flag_reasons": flags,
                "fields": {}, "questions_own": [], "questions_suggested": [], "checklist": [],
                "guardrail_issues": [], "latency_ms": round((time.perf_counter() - started) * 1000)}

    use_llm = triage.llm_configured() if use_llm is None else use_llm
    issues: list[str] = []
    summary = None
    mode = "rules"
    if use_llm:
        context = (f"Người khám: {'người thân của người kể' if for_whom == 'nguoi-than' else 'chính người kể'}, "
                   f"{'trẻ em' if age_group == 'tre-em' else 'người lớn'}. Dịch vụ: {SERVICES[service]['name']}.")
        try:
            summary, issues = validate_summary(llm_summarize(masked, context), masked)
            mode = "llm"
        except Exception as exc:  # LLM lỗi/timeout -> dùng luật, không chặn người dùng
            issues.append(f"llm-loi:{type(exc).__name__}")
    if summary is None:
        summary = rules_summarize(masked)
        mode = "rules" if not use_llm else "rules-fallback"

    fields = [{"key": k, "label": FIELDS[k], **summary["fields"][k]} for k in FIELDS if k in summary["fields"]]
    return {**base, "mode": mode, "red_flag": False, "red_flag_reasons": [], "fields": fields,
            "questions_own": [q["value"] for q in summary["questions"]],
            "questions_suggested": suggest_questions(summary, masked, service, for_whom),
            "checklist": build_checklist(service, age_group, summary, masked),
            "guardrail_issues": issues, "latency_ms": round((time.perf_counter() - started) * 1000)}
