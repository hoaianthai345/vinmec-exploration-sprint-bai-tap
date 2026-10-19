# Bản 2 lưu lại (19/10/2026 tối), trước khi sửa theo nhận xét dùng thử (giờ quá nửa đêm, giờ mở cửa, nước lọc). Không được import.
"""Lõi "Lộ trình khám trong ngày": người bệnh đang ở viện biết bước tiếp theo đi đâu, theo thứ tự nào, chờ bao lâu.

Hai phần, tách bạch:
A. LỘ TRÌNH (luật cố định, không có AI): từ tình trạng lượt khám (đặt lịch chưa, BHYT, lần đầu, chỉ định của bác sĩ)
   -> danh sách bước có phòng, vị trí, lý do sắp xếp và thời gian ước tính.
B. TRỢ LÝ HỎI ĐÁP: câu hỏi tự do -> câu trả lời ghép từ dữ liệu của viện. Thứ tự xử lý (không đổi được bằng prompt):
   1. Che thông tin cá nhân (triage.mask_pii).
   2. Luật dấu hiệu cấp cứu (triage.detect_red_flags). Có dấu hiệu -> chỉ đường Cấp cứu / gọi 115, KHÔNG gọi LLM.
   3. Luật câu hỏi y khoa (diễn giải kết quả, bệnh, thuốc, bệnh nền khi nhịn ăn). Khớp -> không trả lời, ghi vào
      danh sách "hỏi bác sĩ". Luật này thắng mọi phân loại của LLM.
   4. Phân loại câu hỏi vào DANH MỤC CỐ ĐỊNH (loại câu hỏi + phòng/xét nghiệm): LLM nếu đã cấu hình, nếu không thì luật.
   5. Câu trả lời được GHÉP từ dữ liệu phòng/xét nghiệm và lộ trình của chính người đó. LLM không viết câu trả lời,
      nên không thể bịa vị trí, giờ hay hướng dẫn. Mỗi câu trả lời ghi nguồn.

Toàn bộ phòng, vị trí, thời gian chờ là GIẢ LẬP (không phải sơ đồ của Vinmec). Mục có source="vinmec" lấy từ trang
hướng dẫn công khai của Vinmec; mục "gia-lap" cần bệnh viện xác nhận trước khi dùng thật.
"""

from __future__ import annotations

import json
import os
import re
import time
import urllib.request

import triage

VINMEC_TQ = "https://www.vinmec.com/vie/bai-viet/nhung-dieu-can-luu-y-truoc-khi-kham-suc-khoe-tong-quat-vi"

# ---------------------------------------------------------------------------
# Dữ liệu viện GIẢ LẬP
# ---------------------------------------------------------------------------
# wait: phút chờ ước tính; service: phút thực hiện. Cả hai là số giả lập để minh hoạ.
PLACES = {
    "kiosk-hen": {"name": "Kiosk check-in / Quầy lịch hẹn (quầy 9)", "where": "Tầng 1, sảnh A, bên phải cửa chính",
                  "how": "Quét mã QR lịch hẹn trên app tại kiosk; kiosk lỗi thì ra quầy 9", "wait": 3, "service": 2,
                  "aliases": ["kiosk", "quay 9", "check in", "checkin", "quay lich hen", "quay dat lich"]},
    "quay-bhyt": {"name": "Quầy tiếp nhận BHYT (quầy 5–8)", "where": "Tầng 1, sảnh A, giữa sảnh",
                  "how": "Lấy số ở máy bấm số màu xanh lá, chờ gọi số trên bảng", "wait": 20, "service": 5,
                  "aliases": ["quay bhyt", "bao hiem y te", "bhyt", "quay bao hiem", "quay 5", "quay 6", "quay 7", "quay 8"]},
    "quay-dich-vu": {"name": "Quầy tiếp đón khám dịch vụ (quầy 1–4)", "where": "Tầng 1, sảnh A, bên trái cửa chính",
                     "how": "Lấy số ở máy bấm số màu xanh dương; lần đầu sẽ được mở hồ sơ", "wait": 10, "service": 5,
                     "aliases": ["quay dich vu", "quay tiep don", "tiep don", "quay 1", "quay 2", "quay 3", "quay 4",
                                 "mo ho so", "dang ky kham"]},
    "sinh-hieu": {"name": "Đo sinh hiệu (huyết áp, cân nặng)", "where": "Tầng 2, khu B, đầu hành lang phòng khám",
                  "how": "Đưa phiếu khám cho điều dưỡng", "wait": 5, "service": 3,
                  "aliases": ["sinh hieu", "do huyet ap", "can nang", "do cao"]},
    "phong-kham": {"name": "Phòng khám 205 (bác sĩ của bạn)", "where": "Tầng 2, khu B, phòng 205",
                   "how": "Ngồi chờ trước phòng, nghe gọi tên hoặc xem số trên màn hình", "wait": 25, "service": 10,
                   "aliases": ["phong kham", "phong 205", "phong bac si", "gap bac si", "cho bac si", "bac si"]},
    "thu-ngan": {"name": "Thu ngân (quầy 10–12) hoặc thanh toán trên app", "where": "Tầng 1, sảnh A, cạnh nhà thuốc",
                 "how": "Có thể thanh toán phiếu chỉ định ngay trên app để khỏi xếp hàng", "wait": 8, "service": 3,
                 "aliases": ["thu ngan", "thanh toan", "dong tien", "tra tien", "quay 10", "quay 11", "quay 12"]},
    "lay-mau": {"name": "Phòng lấy mẫu xét nghiệm 105", "where": "Tầng 1, khu C, phòng 105 (đi theo vạch đỏ dưới sàn)",
                "how": "Lấy số tại cửa phòng; nộp mẫu nước tiểu ở ô bên cạnh", "wait": 10, "service": 5,
                "aliases": ["lay mau", "lay mau xet nghiem", "phong xet nghiem", "phong 105", "xet nghiem", "nop mau",
                            "lay mau mau", "rut mau", "phong lay mau"]},
    "sieu-am": {"name": "Phòng siêu âm 301–304", "where": "Tầng 3, khu B, thang máy số 2 lên tầng 3 rẽ trái",
                "how": "Đưa phiếu chỉ định ở bàn điều dưỡng trước dãy phòng", "wait": 20, "service": 10,
                "aliases": ["sieu am", "phong sieu am", "phong 301", "tang 3"]},
    "x-quang": {"name": "Phòng X-quang 110", "where": "Tầng 1, khu D, cuối hành lang (đi theo vạch vàng)",
                "how": "Đưa phiếu chỉ định ở cửa phòng", "wait": 15, "service": 5,
                "aliases": ["x quang", "xquang", "chup phim", "chup x quang", "phong 110", "chup phoi", "chup"]},
    "dien-tim": {"name": "Phòng điện tim 210", "where": "Tầng 2, khu B, phòng 210 (cùng dãy phòng khám)",
                 "how": "Đưa phiếu chỉ định cho điều dưỡng", "wait": 10, "service": 5,
                 "aliases": ["dien tim", "do dien tim", "ecg", "phong 210"]},
    "nha-thuoc": {"name": "Nhà thuốc bệnh viện", "where": "Tầng 1, sảnh A, cạnh thu ngân",
                  "how": "Đưa đơn thuốc hoặc mã QR đơn thuốc trên app", "wait": 10, "service": 5,
                  "aliases": ["nha thuoc", "lay thuoc", "mua thuoc", "quay thuoc"]},
    "wc": {"name": "Nhà vệ sinh", "where": "Mỗi tầng ở cuối hành lang, cạnh thang máy số 1", "how": "", "wait": 0,
           "service": 0, "aliases": ["nha ve sinh", "wc", "toilet", "ve sinh", "di tieu", "di ve sinh"]},
    "can-tin": {"name": "Căng tin", "where": "Tầng 1, khu E, cạnh cổng phụ", "how": "", "wait": 0, "service": 0,
                "aliases": ["can tin", "an sang", "cho an", "quan an", "do an", "an uong", "cafe", "ca phe"]},
    "gui-xe": {"name": "Bãi gửi xe", "where": "Tầng hầm B1, lối xuống bên trái cổng chính", "how": "", "wait": 0,
               "service": 0, "aliases": ["gui xe", "bai xe", "do xe", "dau xe", "giu xe"]},
    "cap-cuu": {"name": "Khoa Cấp cứu", "where": "Tầng 1, khu E, cổng riêng có biển đỏ CẤP CỨU",
                "how": "Đến thẳng, không cần lấy số; hoặc báo ngay nhân viên gần nhất", "wait": 0, "service": 0,
                "aliases": ["cap cuu", "khoa cap cuu"]},
    "quay-thong-tin": {"name": "Quầy thông tin", "where": "Tầng 1, sảnh A, đối diện cửa chính",
                       "how": "Nhân viên hỗ trợ trực tiếp", "wait": 0, "service": 0,
                       "aliases": ["quay thong tin", "hoi nhan vien", "nhan vien", "le tan"]},
}

# Chỉ định cận lâm sàng GIẢ LẬP. fasting: cần nhịn ăn trước khi làm. result: phút có kết quả sau khi làm xong.
TESTS = {
    "xn-mau-nhin-an": {"name": "Xét nghiệm máu (đường huyết, mỡ máu)", "place": "lay-mau", "fasting": True, "result": 60,
                       "prep": ["Không ăn sáng; tránh đồ uống có đường, có gas, trà, cà phê trước khi lấy máu"],
                       "source": "vinmec", "url": VINMEC_TQ,
                       "aliases": ["xet nghiem mau", "lay mau", "duong huyet", "mo mau", "thu mau", "rut mau", "mau"]},
    "xn-nuoc-tieu": {"name": "Xét nghiệm nước tiểu", "place": "lay-mau", "fasting": False, "result": 30,
                     "prep": ["Lấy lọ đựng mẫu tại phòng 105, lấy nước tiểu giữa dòng"], "source": "gia-lap",
                     "aliases": ["nuoc tieu", "xet nghiem nuoc tieu", "mau nuoc tieu"]},
    "sieu-am-bung": {"name": "Siêu âm ổ bụng", "place": "sieu-am", "fasting": True, "result": 15,
                     "prep": ["Uống nhiều nước và nhịn tiểu cho tới khi siêu âm xong"], "source": "vinmec", "url": VINMEC_TQ,
                     "aliases": ["sieu am", "sieu am bung", "sieu am o bung"]},
    "x-quang-nguc": {"name": "X-quang ngực", "place": "x-quang", "fasting": False, "result": 30,
                     "prep": ["Tháo trang sức, đồ kim loại vùng ngực",
                              "Đang mang thai hoặc nghi mang thai: báo nhân viên trước khi chụp"],
                     "source": "vinmec", "url": VINMEC_TQ,
                     "aliases": ["x quang", "xquang", "chup phoi", "chup x quang", "chup nguc", "chup phim"]},
    "dien-tim": {"name": "Điện tim", "place": "dien-tim", "fasting": False, "result": 10, "prep": [],
                 "source": "gia-lap", "aliases": ["dien tim", "ecg", "do dien tim"]},
}

PURPOSES = {
    "kham-benh": "Khám bệnh",
    "tai-kham": "Tái khám",
    "lay-ket-qua": "Lấy kết quả, gặp lại bác sĩ",
    "kham-tong-quat": "Khám sức khoẻ tổng quát",
}

# Đặt lịch GIẢ LẬP: chỉ để lộ trình bắt đầu từ lịch hẹn. Bước đặt lịch thật app bệnh viện đã làm tốt, bài không làm lại.
BOOKING = {
    "noi-tong-quat": {"name": "Khám Nội tổng quát", "doctor": "Bác sĩ Nội (giả lập)", "room": "Phòng khám 205",
                      "purpose": "kham-benh"},
    "tai-mui-hong": {"name": "Khám Tai Mũi Họng", "doctor": "Bác sĩ Tai Mũi Họng (giả lập)", "room": "Phòng khám 208",
                     "purpose": "kham-benh"},
    "tong-quat": {"name": "Khám sức khoẻ tổng quát", "doctor": "Bác sĩ khám tổng quát (giả lập)", "room": "Phòng khám 201",
                  "purpose": "kham-tong-quat"},
}
SLOTS = ["07:30", "08:30", "09:30", "10:30", "13:30", "14:30"]
# Gói khám tổng quát giả lập: biết trước chỉ định nên lộ trình có ngay từ lúc đặt lịch.
TQ_PACKAGE = ["xn-mau-nhin-an", "xn-nuoc-tieu", "sieu-am-bung", "x-quang-nguc", "dien-tim"]
PREP_BEFORE = {
    "kham-tong-quat": (["Không ăn sáng; tránh đồ uống có đường, có gas, trà, cà phê trước khi lấy máu",
                        "Uống nhiều nước và nhịn tiểu cho tới khi siêu âm ổ bụng xong",
                        "Mang giấy tờ tuỳ thân, thẻ BHYT nếu dùng"], "vinmec"),
    "default": (["Mang giấy tờ tuỳ thân, thẻ BHYT nếu dùng",
                 "Mang thuốc hoặc vỏ hộp thuốc đang dùng, kết quả và đơn thuốc cũ liên quan",
                 "Chưa rõ có xét nghiệm máu không: hỏi tổng đài trước xem có cần nhịn ăn",
                 "Đến trước giờ hẹn 15–30 phút để check-in"], "gia-lap"),
}


def _hm(text: str) -> int:
    h, m = text.split(":")
    return int(h) * 60 + int(m)


def valid_appt(appt) -> dict | None:
    if not isinstance(appt, dict) or appt.get("specialty") not in BOOKING or appt.get("time") not in SLOTS:
        return None
    return {"specialty": appt["specialty"], "time": appt["time"], "date": str(appt.get("date", ""))[:40]}


# ---------------------------------------------------------------------------
# A. Lộ trình (luật)
# ---------------------------------------------------------------------------


def _step(sid: str, place: str, title: str, why: str, kind: str = "place", **extra) -> dict:
    p = PLACES[place]
    return {"id": sid, "place": place, "title": title, "room": p["name"], "where": p["where"], "how": p["how"],
            "why": why, "kind": kind, "wait": p["wait"], "service": p["service"], **extra}


def arrival_step(visit: dict) -> dict:
    """Quầy đầu tiên phụ thuộc cách vận hành: đã đặt lịch, BHYT, lần đầu. Đây là chỗ phỏng vấn ghi nhận người bệnh bỡ ngỡ."""
    docs = ["CCCD hoặc giấy tờ tuỳ thân"]
    if visit.get("bhyt"):
        docs += ["Thẻ BHYT hoặc ứng dụng VNeID có BHYT", "Giấy chuyển tuyến (nếu có)"]
    if visit.get("booked"):
        appt = valid_appt(visit.get("appt"))
        return _step("den", "kiosk-hen", "Check-in lịch hẹn",
                     "Bạn đã đặt lịch qua app nên không cần lấy số ở quầy tiếp đón" +
                     ("; quầy 9 sẽ kiểm tra thẻ BHYT cho bạn" if visit.get("bhyt") else "") +
                     (f". Nên đến trước giờ hẹn {appt['time']} khoảng 15–30 phút" if appt else ""), docs=docs)
    if visit.get("bhyt"):
        return _step("den", "quay-bhyt", "Đăng ký khám BHYT",
                     "Khám có dùng BHYT phải đăng ký ở quầy BHYT để kiểm tra thẻ và tuyến", docs=docs)
    return _step("den", "quay-dich-vu", "Đăng ký khám" + (" và mở hồ sơ" if visit.get("first_time") else ""),
                 "Bạn chưa đặt lịch và không dùng BHYT, nên đăng ký ở quầy khám dịch vụ" +
                 ("; lần đầu đến sẽ được mở hồ sơ" if visit.get("first_time") else ""), docs=docs)


def order_tests(test_ids: list[str]) -> list[tuple[str, str]]:
    """Sắp thứ tự chỉ định, trả về (mã, lý do). Luật:
    1. Xét nghiệm cần nhịn ăn làm trước (làm xong là ăn được); lấy máu trước siêu âm vì siêu âm còn cần nhịn tiểu.
    2. Còn lại: kết quả lâu hơn làm trước để kết quả về sớm.
    3. Cùng mức: chỗ chờ ngắn hơn trước.
    4. Nước tiểu: có siêu âm ổ bụng (cần nhịn tiểu) thì làm ngay SAU siêu âm; không thì nộp luôn cùng lúc lấy máu
       (cùng phòng 105)."""
    valid = [t for t in dict.fromkeys(test_ids) if t in TESTS]
    ranked = sorted([t for t in valid if t != "xn-nuoc-tieu"],
                    key=lambda t: (not TESTS[t]["fasting"], TESTS[t]["place"] != "lay-mau",
                                   -TESTS[t]["result"], PLACES[TESTS[t]["place"]]["wait"]))
    urine_why = None
    if "xn-nuoc-tieu" in valid:
        anchor = "sieu-am-bung" if "sieu-am-bung" in ranked else "xn-mau-nhin-an" if "xn-mau-nhin-an" in ranked else None
        ranked.insert(ranked.index(anchor) + 1 if anchor else 0, "xn-nuoc-tieu")
        urine_why = {"sieu-am-bung": "Làm sau siêu âm vì siêu âm ổ bụng cần nhịn tiểu",
                     "xn-mau-nhin-an": "Nộp mẫu luôn sau khi lấy máu vì cùng phòng 105"}.get(anchor)
    out = []
    for t in ranked:
        info = TESTS[t]
        if t == "xn-nuoc-tieu" and urine_why:
            why = urine_why
        elif info["fasting"]:
            why = "Làm sớm vì cần nhịn ăn; xong các mục nhịn ăn là bạn ăn được"
        elif info["result"] >= 30:
            why = f"Làm sớm vì có kết quả lâu (khoảng {info['result']} phút)"
        else:
            why = f"Kết quả nhanh (khoảng {info['result']} phút) nên để sau"
        out.append((t, why))
    return out


def build_route(visit: dict) -> dict:
    """visit: {purpose, booked, bhyt, first_time, paid_in_app, tests: [mã], start_min: phút từ 0h (để tính giờ dự kiến),
    appt: {specialty, time, date} nếu đã đặt lịch}. Có lịch hẹn thì lộ trình bắt đầu từ lúc đặt lịch và giờ tính theo giờ hẹn."""
    purpose = visit.get("purpose") if visit.get("purpose") in PURPOSES else "kham-benh"
    appt = valid_appt(visit.get("appt")) if visit.get("booked") else None
    if appt:
        purpose = BOOKING[appt["specialty"]]["purpose"]
    steps = []
    if appt:
        # Lộ trình bắt đầu từ lúc đặt lịch: hai bước trước ngày khám, không có giờ dự kiến
        bk = BOOKING[appt["specialty"]]
        items, src = PREP_BEFORE.get(purpose, PREP_BEFORE["default"])
        steps.append({"id": "dat-lich", "place": None, "kind": "pre", "title": "Đã đặt lịch",
                      "room": f"{bk['name']} · {appt['time']}" + (f" · {appt['date']}" if appt["date"] else ""),
                      "where": f"{bk['doctor']} · {bk['room']}, tầng 2, khu B", "how": "",
                      "why": "Lộ trình bắt đầu từ lịch hẹn: app đã biết khoa, giờ hẹn, BHYT nên không hỏi lại",
                      "wait": 0, "service": 0, "eta": "Đã đặt"})
        steps.append({"id": "chuan-bi", "place": None, "kind": "pre", "title": "Chuẩn bị trước ngày khám",
                      "room": "Ở nhà, tối hôm trước và sáng hôm khám", "where": "Danh sách cần chuẩn bị ở bên dưới",
                      "how": "", "prep": items, "source": src, "url": VINMEC_TQ if src == "vinmec" else None,
                      "why": "Chuẩn bị đúng để không phải chờ thêm hoặc hẹn lại ngày khác",
                      "wait": 0, "service": 0, "eta": "Hôm trước"})
    steps.append(arrival_step(visit))
    if purpose != "lay-ket-qua":
        steps.append(_step("sinh-hieu", "sinh-hieu", "Đo sinh hiệu", "Điều dưỡng đo trước để bác sĩ có số liệu khi khám"))
    test_ids = visit.get("tests") or (TQ_PACKAGE if purpose == "kham-tong-quat" else [])
    if purpose != "kham-tong-quat":  # khám tổng quát: làm các mục trong gói trước, bác sĩ khám và kết luận sau
        steps.append(_step("kham-1", "phong-kham", "Gặp bác sĩ" if purpose != "lay-ket-qua" else "Gặp lại bác sĩ đọc kết quả",
                           "Bác sĩ khám và cho biết có cần xét nghiệm hay chụp chiếu không" if purpose != "lay-ket-qua"
                           else "Mang kết quả đã có vào phòng khám"))
    tests = order_tests(test_ids)
    if tests:
        if not visit.get("paid_in_app"):
            steps.append(_step("thanh-toan-cd", "thu-ngan", "Thanh toán phiếu chỉ định",
                               "Phải thanh toán trước khi làm xét nghiệm, chụp chiếu. Thanh toán trên app thì bỏ qua bước này"))
        for t, why in tests:
            info = TESTS[t]
            steps.append(_step(f"cd-{t}", info["place"], info["name"], why, kind="test", test=t,
                               prep=info["prep"], fasting=info["fasting"], result=info["result"],
                               source=info["source"], url=info.get("url")))
        steps.append({"id": "cho-kq", "place": "phong-kham", "title": "Chờ kết quả", "kind": "wait",
                      "room": "Có thể ngồi chờ ở bất kỳ đâu", "where": "Kết quả về sẽ có thông báo trên app (giả lập)",
                      "how": "Chưa ăn sáng thì đi ăn lúc này nếu đã xong các mục nhịn ăn",
                      "why": "Đợi đủ kết quả rồi mới quay lại bác sĩ, tránh xếp hàng hai lần", "wait": 0, "service": 0})
        steps.append(_step("kham-2", "phong-kham",
                           "Bác sĩ khám và kết luận" if purpose == "kham-tong-quat" else "Quay lại bác sĩ với kết quả",
                           "Bác sĩ đọc kết quả và kết luận. Mang theo câu hỏi bạn đã ghi lại", wait=10))
    steps.append(_step("thuoc", "nha-thuoc", "Thanh toán, nhận thuốc (nếu có đơn)",
                       "Đơn thuốc và phần chênh lệch BHYT có thể thanh toán trên app"))

    # Giờ dự kiến (giả lập): cộng dồn chờ + thực hiện; bước "chờ kết quả" kéo tới lúc kết quả cuối cùng về.
    if appt:  # phòng khám ghi đúng phòng, bác sĩ trong lịch hẹn
        bk = BOOKING[appt["specialty"]]
        for st in steps:
            if st["place"] == "phong-kham" and st["kind"] != "wait":
                st["room"] = f"{bk['room']} · {bk['doctor']}"
                st["where"] = f"Tầng 2, khu B, {bk['room'].lower()}"
    clock = _hm(appt["time"]) - 30 if appt else int(visit.get("start_min") or 8 * 60)
    ready = clock
    for s in steps:
        if s["kind"] == "pre":
            continue
        if s["kind"] == "wait":
            clock = max(clock, ready)
        elif s["id"] == "kham-1" and appt:  # có lịch hẹn: được gọi vào khoảng đúng giờ hẹn
            clock = max(clock + 5, _hm(appt["time"])) + s["service"]
        else:
            clock += s["wait"] + s["service"]
            if s["kind"] == "test":
                ready = max(ready, clock + s["result"])
        s["eta"] = f"{clock // 60:02d}:{clock % 60:02d}"
    return {"purpose": PURPOSES[purpose], "steps": steps, "finish": steps[-1]["eta"],
            "has_fasting": any(TESTS[t]["fasting"] for t, _ in tests), "appt": appt}


# ---------------------------------------------------------------------------
# B. Trợ lý hỏi đáp
# ---------------------------------------------------------------------------
INTENTS = {
    "where": "Hỏi vị trí một phòng, quầy hoặc tiện ích",
    "next": "Hỏi bước tiếp theo phải đi đâu, làm gì",
    "fasting": "Hỏi có cần nhịn ăn, nhịn uống, được ăn chưa",
    "prep": "Hỏi cần chuẩn bị gì trước một xét nghiệm hoặc chụp chiếu",
    "wait": "Hỏi chờ bao lâu, khi nào có kết quả, khi nào tới lượt",
    "pay": "Hỏi thanh toán ở đâu, bằng cách nào",
    "docs": "Hỏi cần mang giấy tờ gì",
    "counter": "Hỏi nên vào quầy nào để đăng ký",
    "medical": "Câu hỏi y khoa: ý nghĩa kết quả, bệnh, thuốc, có nặng không, nên điều trị gì",
    "other": "Không thuộc các loại trên",
}


def _n(text: str) -> str:
    return " " + re.sub(r"[^a-z0-9]+", " ", triage.strip_accents(text)).strip() + " "


def _has(s: str, phrases: list[str]) -> bool:
    return any(_n(p) in s for p in phrases)


# Câu hỏi y khoa: diễn giải kết quả, chẩn đoán, thuốc, bệnh nền ảnh hưởng tới chuẩn bị. Thắng mọi phân loại khác.
# Nói vòng (không dính cụm dưới) xử lý ở _circumlocution: thấy phát hiện bất thường, hỏi ý nghĩa kết quả,
# hoặc hỏi có nên dùng thuốc / thực phẩm chức năng. Không liệt kê từng câu của bộ đo.
_MEDICAL = ["co sao khong", "co sao ko", "co nang khong", "co nguy hiem", "binh thuong khong", "co binh thuong",
            "nghia la gi", "la benh gi", "bi benh gi", "toi bi gi", "co bi gi", "chi so", "cao qua", "thap qua",
            "co can dieu tri", "dieu tri", "uong thuoc gi", "thuoc gi", "uong thuoc nao", "lieu", "co phai mo",
            "co can mo", "ung thu", "khoi u", "co lay khong", "tieu duong", "insulin", "thuoc huyet ap",
            "dang uong thuoc", "bo thuoc", "ngung thuoc", "mang thai co", "ket qua xau", "ket qua nhu the nao",
            "doc ket qua", "giai thich ket qua", "ket qua nay", "co phai bi", "chan doan",
            # bổ sung sau lần đo 1 (18/10): hỏi chế độ ăn sau chẩn đoán, hỏi bác sĩ đã nói gì
            "nen an gi", "kieng gi", "an gi tot", "kieng an", "bac si bao", "bac si noi toi bi", "cao ha", "thap ha",
            "cao khong", "thap khong", "la cao", "la thap"]
# Con số kèm "cao/thấp/bình thường" là hỏi diễn giải chỉ số, ví dụ "đường huyết 7.2 là cao hả".
_NUMBER_JUDGE = re.compile(r"\d+(?:[.,]\d+)?.*\b(cao|thap|binh thuong|on khong|tot khong)\b")
# "thấy / ghi nhận" một phát hiện bất thường, rồi hỏi ý nghĩa. "can nang" không phải "nang".
_FINDING = re.compile(
    r"\b(?:thay|phat hien|ghi|bao|ket luan)\b.{0,48}"
    r"\b(?:mo|dom|(?<!can )nang|soi|vet|bong|bat thuong|lech|vuot|khong deu|duong tinh|am tinh)\b"
    r"|"
    r"\b(?:mo|dom|(?<!can )nang|soi|vet|bong|bat thuong|khong deu|duong tinh|am tinh|vuot|lech)\b.{0,48}"
    r"\b(?:bi|benh|sao|xu ly|nghia|van de|lo|lam sao)\b"
)
# Nhắc xét nghiệm / phim / chỉ số VÀ hỏi xử lý, bệnh, đổi ăn uống. Không gồm "có phải" trần
# (tránh nuốt "siêu âm có phải nhịn ăn không").
_RESULT_MENTION = re.compile(
    r"\b(?:ket qua|mo mau|duong huyet|chi so|xet nghiem|sieu am|x quang|xquang|dien tim|phim)\b"
)
# Không dùng "bi gi": sau khi bỏ dấu, "chuẩn bị gì" cũng là cụm "bi gi".
_RESULT_JUDGE = re.compile(
    r"\b(?:xu ly|van de|lam sao|nen an|an uong|phai doi|thay doi|kieng|bi lam sao)\b"
)
_SUBSTANCE = re.compile(
    r"\b(?:vitamin|tpcn|glucosamine|omega|collagen|men vi sinh|thuc pham chuc nang|ke don|don thuoc|thuoc)\b"
)
_COUNSEL = re.compile(r"\b(?:uong them|co nen|nen uong|moi ngay|ngung|bo sung)\b")
_THUOC_PLACE = ("nha thuoc", "lay thuoc", "mua thuoc", "quay thuoc")
_RULES = [
    ("counter", ["quay nao", "vao quay", "dang ky o dau", "dang ky kham o dau", "lay so o dau", "bat dau tu dau",
                 "moi den", "vua den", "toi nen vao dau", "lay so"]),
    ("fasting", ["nhin an", "duoc an", "an sang", "an duoc", "uong nuoc", "nhin doi", "an gi chua", "an chua",
                 "duoc uong", "nhin uong", "an truoc", "doi qua", "doi bung"]),
    ("wait", ["bao lau", "khi nao co", "may gio", "luc nao co", "toi luot", "den luot", "con lau", "cho lau",
              "bao gio co", "khi nao xong", "may phut", "lau khong", "lau ko", "chung nao", "bao gio"]),
    ("pay", ["thanh toan", "dong tien", "tra tien", "tien kham", "dong phi", "quet ma", "chuyen khoan"]),
    ("docs", ["giay to", "mang gi", "can mang", "cccd", "can cuoc", "the bhyt", "giay chuyen tuyen", "mang theo"]),
    ("prep", ["chuan bi gi", "can chuan bi", "phai lam gi truoc", "nhin tieu", "thao trang suc", "truoc khi chup",
              "truoc khi sieu am", "truoc khi lay mau", "luu y gi"]),
    ("next", ["tiep theo", "di dau tiep", "lam gi tiep", "bay gio di dau", "gio di dau", "buoc tiep", "xong roi",
              "roi lam gi", "di dau nua", "con gi nua", "tiep tuc",
              # bổ sung sau lần đo 1 (18/10)
              "ke tiep", "cho nao nua", "noi nao nua", "thi di dau", "roi di dau"]),
    ("where", ["o dau", "cho nao", "phong nao", "tang may", "duong nao", "di the nao", "di sao", "o tang", "huong nao",
               "nam o", "lam o dau", "lay o dau", "loi nao", "ngo nao"]),
]


def _find_target(s: str) -> str | None:
    """Tìm phòng/xét nghiệm được nhắc tới. Ưu tiên cụm dài nhất để "sieu am bung" thắng "sieu am"."""
    best, best_len = None, 0
    for tid, info in TESTS.items():
        for a in info["aliases"]:
            if _n(a) in s and len(a) > best_len:
                best, best_len = tid, len(a)
    for pid, info in PLACES.items():
        for a in info["aliases"]:
            if _n(a) in s and len(a) > best_len:
                best, best_len = pid, len(a)
    return best


def rules_classify(question: str) -> dict:
    s = _n(question)
    target = _find_target(s)
    for intent, phrases in _RULES:
        if _has(s, phrases):
            return {"intent": intent, "target": target}
    if target in PLACES:
        return {"intent": "where", "target": target}
    return {"intent": "other", "target": target}


def _substance_counsel(s: str) -> bool:
    """Hỏi có nên dùng thuốc hoặc thực phẩm chức năng. Bỏ tên quầy nhà thuốc để khỏi nuốt câu hỏi đường đi."""
    masked = s
    for place in _THUOC_PLACE:
        masked = masked.replace(place, " ")
    has_sub = bool(_SUBSTANCE.search(masked))
    has_counsel = bool(_COUNSEL.search(masked)) or " duoc khong " in masked
    return has_sub and has_counsel


def _circumlocution(s: str) -> bool:
    """Diễn giải kết quả / thuốc / thực phẩm chức năng khi không dính cụm _MEDICAL. Không chắc thì cũng coi là y khoa."""
    if _FINDING.search(s):
        return True
    if _RESULT_MENTION.search(s) and _RESULT_JUDGE.search(s):
        return True
    return _substance_counsel(s)


def is_medical(question: str) -> bool:
    s = _n(question)
    return _has(s, _MEDICAL) or bool(_NUMBER_JUDGE.search(s)) or _circumlocution(s)


SYSTEM_PROMPT = """Bạn là bộ PHÂN LOẠI câu hỏi của người bệnh đang ở bệnh viện. Bạn KHÔNG trả lời câu hỏi.
Nhiệm vụ: xếp câu hỏi vào đúng một loại và (nếu có) một mã phòng hoặc xét nghiệm được nhắc tới.

Loại câu hỏi (intent):
{intents}

Mã phòng/tiện ích: {places}
Mã xét nghiệm, chụp chiếu: {tests}

Quy tắc:
- Câu hỏi về ý nghĩa kết quả, bệnh, thuốc, có nặng không, nên điều trị gì, hoặc bệnh nền có ảnh hưởng tới việc nhịn ăn
  không -> intent "medical".
- "target" chỉ được là một mã trong hai danh sách trên, hoặc null. Không tự đặt mã mới.
- Người hỏi có thể gõ không dấu, viết tắt, nói trống không. Đoán theo ý chính.

Chỉ trả về JSON: {{"intent": "<loại>", "target": "<mã hoặc null>"}}"""


def llm_classify(question: str, timeout: float = 15.0) -> dict:
    base = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    prompt = SYSTEM_PROMPT.format(intents="\n".join(f"- {k}: {v}" for k, v in INTENTS.items()),
                                  places=", ".join(f"{k} ({v['name']})" for k, v in PLACES.items()),
                                  tests=", ".join(f"{k} ({v['name']})" for k, v in TESTS.items()))
    payload = {"model": os.environ["LLM_MODEL"], "temperature": 0,
               "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": question}]}
    req = urllib.request.Request(
        f"{base}/chat/completions", data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {os.environ['LLM_API_KEY']}"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        content = json.load(resp)["choices"][0]["message"]["content"]
    match = re.search(r"\{.*\}", content, re.S)
    if not match:
        raise ValueError("LLM không trả JSON")
    return json.loads(match.group(0))


def validate_classification(raw: dict) -> tuple[dict, list[str]]:
    issues = []
    intent = raw.get("intent")
    if intent not in INTENTS:
        issues.append(f"intent-ngoai-danh-muc:{intent}")
        intent = "other"
    target = raw.get("target")
    if target in ("", "null", None):
        target = None
    elif target not in PLACES and target not in TESTS:
        issues.append(f"target-ngoai-danh-muc:{target}")
        target = None
    return {"intent": intent, "target": target}, issues


def _place_text(pid: str) -> str:
    p = PLACES[pid]
    return f"{p['name']}: {p['where']}." + (f" {p['how']}." if p["how"] else "")


def _pending_tests(route: dict, done: set[str]) -> list[dict]:
    return [s for s in route["steps"] if s["kind"] == "test" and s["id"] not in done]


def compose_answer(intent: str, target: str | None, visit: dict, done: list[str]) -> dict:
    """Ghép câu trả lời từ dữ liệu. Không có văn bản nào do LLM viết."""
    route = build_route(visit)
    done_set = set(done or [])
    remaining = [s for s in route["steps"] if s["id"] not in done_set]
    src_route, src_place = "Lộ trình của bạn (giả lập)", "Sơ đồ bệnh viện (giả lập)"

    if intent == "next" or (intent == "where" and target is None):
        if not remaining:
            return {"text": "Bạn đã xong tất cả các bước hôm nay.", "source": src_route}
        s = remaining[0]
        text = f"Bước tiếp theo: {s['title']} tại {s['room']}. {s['where']}."
        if len(remaining) > 1:
            text += f" Sau đó: {remaining[1]['title']}."
        return {"text": text, "source": src_route, "step": s["id"]}

    if intent == "counter":
        s = arrival_step(visit)
        return {"text": f"Với lượt khám của bạn, vào {s['room']}. {s['where']}. Lý do: {s['why']}.",
                "source": src_route, "step": "den"}

    if intent == "where":
        pid = TESTS[target]["place"] if target in TESTS else target
        return {"text": _place_text(pid), "source": src_place}

    if intent == "fasting":
        pending = _pending_tests(route, done_set)
        tests = [s for s in pending if s.get("test") == target] if target in TESTS else pending
        need = [s for s in tests if s["fasting"]]
        if target in TESTS and not tests:
            info = TESTS[target]
            return {"text": f"{info['name']} không có trong chỉ định còn lại của bạn. "
                            + ("Mục này thường cần nhịn ăn." if info["fasting"] else "Mục này không cần nhịn ăn."),
                    "source": "Hướng dẫn chuẩn bị (giả lập)"}
        if need:
            names = ", ".join(s["title"] for s in need)
            prep = " ".join(p for s in need for p in s["prep"])
            src = "Hướng dẫn công khai của Vinmec" if any(s["source"] == "vinmec" for s in need) else "Hướng dẫn chuẩn bị (giả lập)"
            return {"text": f"Chưa nên ăn: bạn còn {names} cần nhịn ăn. {prep}", "source": src,
                    "url": next((s["url"] for s in need if s.get("url")), None)}
        if route["has_fasting"] or pending:
            return {"text": "Các mục còn lại của bạn không cần nhịn ăn, bạn có thể ăn uống bình thường.",
                    "source": "Hướng dẫn chuẩn bị (giả lập)"}
        return {"text": "Hiện bạn chưa có chỉ định nào cần nhịn ăn. Nếu bác sĩ chỉ định thêm, lộ trình sẽ báo.",
                "source": src_route}

    if intent == "prep":
        if target in TESTS:
            info = TESTS[target]
            items = info["prep"] or ["Không cần chuẩn bị gì đặc biệt"]
            return {"text": f"{info['name']}: " + "; ".join(items) + ".",
                    "source": "Hướng dẫn công khai của Vinmec" if info["source"] == "vinmec" else "Hướng dẫn chuẩn bị (giả lập)",
                    "url": info.get("url")}
        pending = [s for s in _pending_tests(route, done_set) if s["prep"]]
        if pending:
            return {"text": " ".join(f"{s['title']}: " + "; ".join(s["prep"]) + "." for s in pending),
                    "source": "Hướng dẫn chuẩn bị (giả lập, có mục theo Vinmec)"}
        return {"text": "Các bước còn lại của bạn không cần chuẩn bị gì đặc biệt.", "source": src_route}

    if intent == "wait":
        if target in TESTS:
            info = TESTS[target]
            pl = PLACES[info["place"]]
            return {"text": f"{info['name']} ở {pl['name']} ({pl['where']}): chờ khoảng {pl['wait']} phút để làm, "
                            f"có kết quả khoảng {info['result']} phút sau khi làm xong. Kết quả về sẽ có thông báo trên app.",
                    "source": "Thời gian ước tính và sơ đồ (giả lập)"}
        if target in PLACES and PLACES[target]["wait"]:
            pl = PLACES[target]
            return {"text": f"{pl['name']} ({pl['where']}): hiện chờ khoảng {pl['wait']} phút.",
                    "source": "Thời gian ước tính và sơ đồ (giả lập)"}
        tests = [s for s in route["steps"] if s["kind"] == "test"]
        wait_step = next((s for s in route["steps"] if s["id"] == "cho-kq"), None)
        if tests and wait_step and "kham-2" not in done_set:
            return {"text": f"Dự kiến đủ kết quả lúc {wait_step['eta']}, xong cả buổi khoảng {route['finish']}.",
                    "source": "Thời gian ước tính (giả lập)"}
        return {"text": f"Dự kiến xong cả buổi khoảng {route['finish']}.", "source": "Thời gian ước tính (giả lập)"}

    if intent == "pay":
        return {"text": "Thanh toán ngay trên app (mục Thanh toán viện phí) để khỏi xếp hàng, hoặc ra "
                        + _place_text("thu-ngan"), "source": src_place}

    if intent == "docs":
        s = arrival_step(visit)
        return {"text": "Bạn cần mang: " + "; ".join(s.get("docs", [])) + ".", "source": src_route}

    return {"text": "Mình chưa hiểu câu hỏi. Bạn thử chọn một câu gợi ý bên dưới, hoặc hỏi "
                    + _place_text("quay-thong-tin"), "source": src_place, "fallback": True}


EMERGENCY_TEXT = ("Đây có thể là tình huống cấp cứu. Đến ngay {room} ({where}) hoặc báo nhân viên gần nhất. "
                  "Nếu đang ở ngoài bệnh viện, gọi 115.")
MEDICAL_TEXT = ("Câu này cần hỏi bác sĩ hoặc nhân viên y tế. Trợ lý không giải thích kết quả, thuốc hay "
                "thực phẩm chức năng, và không chỉ một phòng. Mình đã ghi câu hỏi lại để bạn hỏi bác sĩ hoặc nhân viên.")


def ask(question: str, visit: dict, done: list[str] | None = None, use_llm: bool | None = None) -> dict:
    t0 = time.time()
    masked = triage.mask_pii(question)
    out = {"question_masked": masked, "red_flag": False, "red_flag_reasons": [], "medical": False,
           "intent": None, "target": None, "mode": "luat", "guardrail_issues": []}
    flags = triage.detect_red_flags(masked)
    if flags:
        cc = PLACES["cap-cuu"]
        out.update(red_flag=True, red_flag_reasons=flags, intent="emergency",
                   answer={"text": EMERGENCY_TEXT.format(room=cc["name"], where=cc["where"]), "source": "Luật an toàn"})
        out["latency_ms"] = int((time.time() - t0) * 1000)
        return out

    rule_medical = is_medical(masked)
    use_llm = triage.llm_configured() if use_llm is None else use_llm
    cls = None
    if use_llm:
        try:
            cls, issues = validate_classification(llm_classify(masked))
            out["mode"] = "llm"
            out["guardrail_issues"] = issues
        except Exception as exc:  # LLM lỗi -> luật, người dùng không bị chặn
            out["mode"] = f"llm-loi:{type(exc).__name__}"
    if cls is None:
        cls = rules_classify(masked)
    elif cls["target"] is None:  # LLM không nêu hoặc nêu mã ngoài danh mục -> dùng phòng mà luật tìm thấy trong câu
        cls["target"] = rules_classify(masked)["target"]
    if rule_medical and cls["intent"] != "medical":
        out["guardrail_issues"].append(f"luat-y-khoa-thang:{cls['intent']}")
        cls["intent"] = "medical"

    out.update(intent=cls["intent"], target=cls["target"])
    if cls["intent"] == "medical":
        out["medical"] = True
        out["answer"] = {"text": MEDICAL_TEXT, "source": "Luật an toàn", "save_question": masked}
    else:
        out["answer"] = compose_answer(cls["intent"], cls["target"], visit, done or [])
    out["latency_ms"] = int((time.time() - t0) * 1000)
    return out
