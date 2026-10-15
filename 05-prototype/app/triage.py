"""Lõi gợi ý chuyên khoa khi đặt lịch.

Thứ tự xử lý (không đổi được bằng prompt):
1. Che thông tin cá nhân (số điện thoại, email, số giấy tờ) trước khi log hoặc gửi đi.
2. Kiểm tra dấu hiệu khẩn cấp bằng luật cố định. Có dấu hiệu -> dừng, hướng dẫn gọi 115/đến cấp cứu,
   KHÔNG gọi LLM và KHÔNG cho đặt lịch thường.
3. Gợi ý tối đa 2 chuyên khoa trong danh sách cho phép: dùng LLM nếu đã cấu hình, nếu không thì dùng luật từ khoá.
4. Kiểm tra đầu ra: chuyên khoa phải nằm trong danh sách; câu giải thích không được chứa chẩn đoán/thuốc.
"""

from __future__ import annotations

import json
import os
import re
import time
import unicodedata
import urllib.request

# Danh sách chuyên khoa MÔ PHỎNG cho prototype, không phải danh mục chính thức của bệnh viện.
SPECIALTIES = {
    "noi-tong-quat": "Nội tổng quát",
    "nhi": "Nhi",
    "san-phu-khoa": "Sản phụ khoa",
    "tai-mui-hong": "Tai Mũi Họng",
    "rang-ham-mat": "Răng Hàm Mặt",
    "mat": "Mắt",
    "da-lieu": "Da liễu",
    "tim-mach": "Tim mạch",
    "tieu-hoa": "Tiêu hoá",
    "co-xuong-khop": "Cơ xương khớp",
    "than-kinh": "Thần kinh",
    "noi-tiet": "Nội tiết",
    "tiet-nieu": "Tiết niệu – Nam khoa",
    "ho-hap": "Hô hấp",
    "tam-than": "Sức khoẻ tâm thần",
}

DEFAULT_SPECIALTY = "noi-tong-quat"


def strip_accents(text: str) -> str:
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.replace("đ", "d")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", strip_accents(text)).strip()


def has_accents(text: str) -> bool:
    return strip_accents(text) != text.lower()


def prepare(text: str) -> tuple[str, bool]:
    """Văn bản để so khớp. Người dùng gõ có dấu -> so khớp có dấu (tránh "đã" thành "da");
    gõ không dấu -> bỏ dấu cả hai phía."""
    accented = has_accents(text)
    lowered = unicodedata.normalize("NFC", text.lower())
    return (re.sub(r"\s+", " ", lowered).strip() if accented else normalize(text)), accented


def phrase_form(phrase: str, accented: bool) -> str:
    return unicodedata.normalize("NFC", phrase.lower()) if accented else strip_accents(phrase)


_LETTER = r"[a-zà-ỹđ]"


def find_phrase(prepared: str, phrase: str, accented: bool):
    form = re.escape(phrase_form(phrase, accented))
    return re.finditer(rf"(?<!{_LETTER}){form}(?!{_LETTER})", prepared)


# ---------------------------------------------------------------------------
# 1. Che thông tin cá nhân
# ---------------------------------------------------------------------------
_PII_PATTERNS = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[email]"),
    (re.compile(r"\b\d{12}\b"), "[so-giay-to]"),
    (re.compile(r"(?:\+?84|0)(?:[\s.-]?\d){8,10}\b"), "[so-dien-thoai]"),
]


def mask_pii(text: str) -> str:
    for pattern, repl in _PII_PATTERNS:
        text = pattern.sub(repl, text)
    return text


# ---------------------------------------------------------------------------
# 2. Dấu hiệu khẩn cấp (luật cố định, viết không dấu để bắt cả khi người dùng gõ không dấu)
# ---------------------------------------------------------------------------
# Mỗi mục: (nhãn hiển thị, các cụm từ). Danh sách tham khảo các nhóm dấu hiệu "cần gọi cấp cứu"
# phổ biến; CHƯA được bác sĩ duyệt (xem 06-rui-ro-dao-duc).
RED_FLAGS = [
    ("đau hoặc tức ngực", ["đau ngực", "tức ngực", "đau thắt ngực", "nặng ngực"]),
    ("khó thở", ["khó thở", "thở không nổi", "ngạt thở", "thở gấp", "hụt hơi"]),
    ("nghi đột quỵ (méo miệng, yếu hoặc tê nửa người, nói khó)", ["méo miệng", "yếu nửa người", "liệt nửa người", "tê nửa người",
                          "nói ngọng đột ngột", "nói khó đột ngột", "đột quỵ"]),
    ("ngất, co giật hoặc lơ mơ", ["ngất xỉu", "bất tỉnh", "co giật", "lơ mơ", "hôn mê", "ngất đi"]),
    ("chảy máu nhiều", ["chảy máu nhiều", "máu không cầm", "nôn ra máu", "đi ngoài ra máu",
                        "ho ra máu", "băng huyết"]),
    ("ý nghĩ tự làm hại bản thân", ["tự tử", "muốn chết", "không muốn sống", "tự làm hại",
                                     "tự hại"]),
    ("dị ứng nặng", ["sưng lưỡi", "sưng họng", "phản vệ"]),
    ("đau bụng dữ dội", ["đau bụng dữ dội", "đau bụng quằn quại", "đau bụng chịu không nổi"]),
    ("chấn thương nặng", ["tai nạn", "gãy xương hở", "đập đầu", "chấn thương đầu"]),
    ("trẻ nhỏ sốt cao hoặc li bì", ["li bì", "sốt cao co giật", "bỏ bú"]),
]

_NEGATIONS = ("khong", "ko", "k", "chua", "het")


def _negated(prepared: str, start: int) -> bool:
    """Phủ định đứng ngay trước (tối đa 2 từ), ví dụ "không khó thở"."""
    before = strip_accents(prepared[:start]).split()[-2:]
    return any(word in _NEGATIONS for word in before)


def detect_red_flags(text: str) -> list[str]:
    prepared, accented = prepare(text)
    hits = []
    for label, phrases in RED_FLAGS:
        if any(not _negated(prepared, m.start())
               for phrase in phrases for m in find_phrase(prepared, phrase, accented)):
            hits.append(label)
    return hits


# ---------------------------------------------------------------------------
# 3a. Gợi ý bằng luật từ khoá (chế độ không cần API key)
# ---------------------------------------------------------------------------
KEYWORD_RULES = [
    ("rang-ham-mat", ["răng", "nướu", "lợi", "nhổ răng", "sâu răng", "hàm", "niềng", "đau răng", "ê buốt răng", "chảy máu chân răng"],
     "Vấn đề ở răng, nướu hoặc hàm thường được khám ở khoa Răng Hàm Mặt."),
    ("mat", ["mắt", "nhìn mờ", "mờ mắt", "đỏ mắt", "ngứa mắt", "cận thị", "thị lực", "kính", "đau mắt"],
     "Vấn đề về mắt và thị lực thường được khám ở khoa Mắt."),
    ("tai-mui-hong", ["tai", "ù tai", "mũi", "họng", "viêm họng", "nghẹt mũi", "ngáy", "xoang",
                      "khàn tiếng", "đau tai", "đau họng", "sổ mũi"],
     "Vấn đề ở tai, mũi, họng thường được khám ở khoa Tai Mũi Họng."),
    ("da-lieu", ["da", "nổi mẩn", "mụn", "ngứa", "rụng tóc", "nấm", "phát ban", "nốt ruồi", "ngứa da", "nổi mề đay"],
     "Vấn đề ngoài da, tóc, móng thường được khám ở khoa Da liễu."),
    ("san-phu-khoa", ["mang thai", "có thai", "bầu", "kinh nguyệt", "phụ khoa", "trễ kinh",
                      "khám thai", "hiếm muộn"],
     "Khám thai và các vấn đề phụ khoa thường thuộc khoa Sản phụ khoa."),
    ("tim-mach", ["huyết áp", "tim đập nhanh", "hồi hộp", "đánh trống ngực", "tim mạch",
                  "mỡ máu"],
     "Theo dõi huyết áp, nhịp tim, mỡ máu thường thuộc khoa Tim mạch."),
    ("tieu-hoa", ["bụng", "dạ dày", "tiêu chảy", "táo bón", "ợ chua", "trào ngược", "khó tiêu",
                  "buồn nôn", "đầy hơi", "đau bụng", "đau dạ dày"],
     "Các vấn đề về ăn uống, dạ dày, đường ruột thường thuộc khoa Tiêu hoá."),
    ("co-xuong-khop", ["khớp", "lưng", "vai gáy", "đầu gối", "vai", "cột sống", "bong gân",
                       "đau gót", "đau lưng", "đau khớp", "đau vai"],
     "Đau mỏi lưng, khớp, vai gáy thường được khám ở khoa Cơ xương khớp."),
    ("than-kinh", ["đau đầu", "chóng mặt", "mất ngủ", "tê tay", "tê chân", "đau nửa đầu"],
     "Đau đầu, chóng mặt kéo dài hoặc tê bì thường được khám ở khoa Thần kinh."),
    ("noi-tiet", ["tiểu đường", "đường huyết", "tuyến giáp", "béo phì", "nội tiết"],
     "Đường huyết, tuyến giáp thường được theo dõi ở khoa Nội tiết."),
    ("tiet-nieu", ["tiểu buốt", "tiểu rắt", "tiểu đêm", "tiết niệu", "nam khoa", "thận", "sỏi", "sỏi thận"],
     "Các vấn đề về tiểu tiện, thận thường được khám ở khoa Tiết niệu."),
    ("ho-hap", ["ho kéo dài", "ho lâu", "ho nhiều", "khò khè", "hen", "ho"],
     "Ho kéo dài thường được khám ở khoa Hô hấp."),
    ("tam-than", ["căng thẳng", "lo âu", "trầm cảm", "stress", "buồn bã", "mất hứng thú"],
     "Căng thẳng, lo âu kéo dài có thể trao đổi với khoa Sức khoẻ tâm thần."),
    ("noi-tong-quat", ["khám tổng quát", "khám sức khoẻ", "khám sức khỏe", "xét nghiệm máu",
                       "mệt mỏi", "sốt", "cảm cúm", "check up"],
     "Khám tổng quát hoặc khi chưa rõ vấn đề nằm ở đâu, bắt đầu từ Nội tổng quát là hợp lý."),
]


def rules_suggest(text: str, age_group: str) -> dict:
    prepared, accented = prepare(text)
    scored = []
    for slug, phrases, why in KEYWORD_RULES:
        # Gõ không dấu: bỏ qua từ đơn dễ nhầm ("da", "tai", "ho"...), chỉ tin cụm từ >= 2 tiếng.
        usable = phrases if accented else [p for p in phrases if " " in p]
        score = sum(1 for p in usable if next(find_phrase(prepared, p, accented), None))
        if score:
            scored.append((score, slug, why))
    scored.sort(key=lambda x: -x[0])
    suggestions = [{"specialty": slug, "why": why} for _, slug, why in scored[:2]]

    if age_group == "tre-em":
        child = {"specialty": "nhi",
                 "why": "Người khám là trẻ em nên bắt đầu từ khoa Nhi; bác sĩ Nhi sẽ chuyển khoa nếu cần."}
        suggestions = [child] + [s for s in suggestions if s["specialty"] not in ("nhi", "noi-tong-quat")][:1]

    if not suggestions:
        return {
            "suggestions": [{"specialty": DEFAULT_SPECIALTY,
                             "why": "Mô tả chưa đủ để chọn chuyên khoa riêng; khám Nội tổng quát trước là an toàn nhất."}],
            "clarify": "Bạn có thể nói rõ hơn vấn đề nằm ở bộ phận nào (ví dụ: răng, mắt, da, bụng, khớp…)?",
            "confidence": "thap",
        }
    return {"suggestions": suggestions, "clarify": None,
            "confidence": "cao" if scored and scored[0][0] >= 2 else "trung-binh"}


# ---------------------------------------------------------------------------
# 3b. Gợi ý bằng LLM (OpenAI-compatible chat completions)
# ---------------------------------------------------------------------------
SYSTEM_PROMPT = """Bạn là trợ lý ĐẶT LỊCH của một bệnh viện, không phải bác sĩ.
Nhiệm vụ duy nhất: từ mô tả lý do đi khám, gợi ý tối đa 2 chuyên khoa để người bệnh đặt lịch.

Quy tắc bắt buộc:
- Chỉ chọn chuyên khoa trong danh sách mã sau: {codes}.
- KHÔNG nêu tên bệnh, KHÔNG phỏng đoán chẩn đoán, KHÔNG nhắc thuốc hay cách điều trị.
- Câu "why" giải thích vì sao khoa đó thường tiếp nhận vấn đề này, tối đa 25 từ, tiếng Việt dễ hiểu.
- Nếu người khám là trẻ em, chuyên khoa đầu tiên là "nhi".
- Nếu mô tả quá mơ hồ, gợi ý "noi-tong-quat" và đặt một câu hỏi làm rõ (về bộ phận cơ thể hoặc mục đích khám), nếu không thì clarify = null.
- Nếu có dấu hiệu cần cấp cứu, đặt "red_flag": true.

Chỉ trả về JSON đúng dạng:
{{"red_flag": false, "suggestions": [{{"specialty": "<mã>", "why": "<câu>"}}], "clarify": null, "confidence": "cao|trung-binh|thap"}}"""

# Câu giải thích bị loại nếu có dấu hiệu chẩn đoán hoặc tư vấn điều trị.
_FORBIDDEN = re.compile(r"(ban bi |co the bi |chan doan|benh |uong thuoc|ke don|\bmg\b|dieu tri)")


def llm_configured() -> bool:
    return bool(os.environ.get("LLM_API_KEY") and os.environ.get("LLM_MODEL"))


def llm_suggest(text: str, age_group: str, timeout: float = 20.0) -> dict:
    base = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {
        "model": os.environ["LLM_MODEL"],
        "temperature": 0,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT.format(codes=", ".join(SPECIALTIES))},
            {"role": "user", "content": f"Người khám: {'trẻ em' if age_group == 'tre-em' else 'người lớn'}.\nMô tả: {text}"},
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


def validate_llm_output(raw: dict, age_group: str) -> tuple[dict, list[str]]:
    """Giữ phần hợp lệ của đầu ra LLM; trả thêm danh sách cảnh báo guardrail để ghi log."""
    issues = []
    suggestions = []
    for item in (raw.get("suggestions") or [])[:2]:
        slug = str(item.get("specialty", "")).strip()
        why = str(item.get("why", "")).strip()
        if slug not in SPECIALTIES:
            issues.append(f"chuyen-khoa-ngoai-danh-sach:{slug}")
            continue
        if _FORBIDDEN.search(normalize(why)):
            issues.append(f"cau-giai-thich-bi-chan:{slug}")
            why = f"Khoa {SPECIALTIES[slug]} thường tiếp nhận vấn đề bạn mô tả."
        suggestions.append({"specialty": slug, "why": why})
    if age_group == "tre-em" and (not suggestions or suggestions[0]["specialty"] != "nhi"):
        issues.append("tre-em-chua-uu-tien-nhi")
        suggestions = [{"specialty": "nhi", "why": "Người khám là trẻ em nên bắt đầu từ khoa Nhi."}] + \
                      [s for s in suggestions if s["specialty"] != "nhi"][:1]
    if not suggestions:
        raise ValueError("Không còn gợi ý hợp lệ sau kiểm tra")
    clarify = raw.get("clarify") or None
    confidence = raw.get("confidence") if raw.get("confidence") in ("cao", "trung-binh", "thap") else "trung-binh"
    return {"suggestions": suggestions, "clarify": clarify, "confidence": confidence,
            "llm_red_flag": bool(raw.get("red_flag"))}, issues


# ---------------------------------------------------------------------------
# Điểm vào chung
# ---------------------------------------------------------------------------
def triage(text: str, age_group: str = "nguoi-lon", use_llm: bool | None = None) -> dict:
    started = time.perf_counter()
    masked = mask_pii(text or "")
    flags = detect_red_flags(masked)
    if flags:
        return {"mode": "rule-red-flag", "red_flag": True, "red_flag_reasons": flags,
                "suggestions": [], "clarify": None, "confidence": None, "guardrail_issues": [],
                "input_masked": masked, "latency_ms": round((time.perf_counter() - started) * 1000)}

    use_llm = llm_configured() if use_llm is None else use_llm
    issues: list[str] = []
    result = None
    mode = "rules"
    if use_llm:
        try:
            result, issues = validate_llm_output(llm_suggest(masked, age_group), age_group)
            mode = "llm"
            if result.pop("llm_red_flag"):
                # LLM thấy dấu hiệu nguy hiểm mà luật bỏ sót: ưu tiên an toàn.
                return {"mode": "llm-red-flag", "red_flag": True,
                        "red_flag_reasons": ["trợ lý AI nhận thấy dấu hiệu có thể cần cấp cứu"],
                        "suggestions": [], "clarify": None, "confidence": None, "guardrail_issues": issues,
                        "input_masked": masked, "latency_ms": round((time.perf_counter() - started) * 1000)}
        except Exception as exc:  # LLM lỗi/timeout -> dùng luật, không chặn người dùng
            issues.append(f"llm-loi:{type(exc).__name__}")
            result = None
    if result is None:
        result = rules_suggest(masked, age_group)
        mode = "rules" if not use_llm else "rules-fallback"

    for s in result["suggestions"]:
        s["name"] = SPECIALTIES[s["specialty"]]
    return {"mode": mode, "red_flag": False, "red_flag_reasons": [], **result,
            "guardrail_issues": issues, "input_masked": masked,
            "latency_ms": round((time.perf_counter() - started) * 1000)}
