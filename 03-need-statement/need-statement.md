# Need statement

## Bản nháp (giả thuyết, trước phỏng vấn)

> Cách để **người bệnh, hoặc người thân đi khám cùng, đã đặt lịch khám chuyên khoa** gặp tình huống **chỉ có vài phút
> với bác sĩ, dễ quên nói hoặc quên hỏi điều quan trọng và không chắc cần chuẩn bị gì**, có thể **đến buổi khám đã
> chuẩn bị đúng, nói được hết điều cần nói và hỏi được hết điều cần hỏi, mà không phải kể lại cùng một chuyện nhiều
> lần**.

Theo mẫu Biodesign:

| Thành phần | Nội dung | Bằng chứng (⚠️ THÁI ĐIỀN sau phỏng vấn) |
|---|---|---|
| Problem (vấn đề) | Thời gian với bác sĩ ngắn; người bệnh quên nói hoặc quên hỏi, chuẩn bị thiếu, phải kể lại nhiều lần | Nghiên cứu (Barry 2000; Singh Ospina 2019); dùng thử app (T3); P?, "trích dẫn" |
| Population (nhóm người dùng) | Người đã đặt lịch khám chuyên khoa qua app, gồm cả người **đi cùng hoặc thay** bố mẹ, con nhỏ | P? |
| Outcome (kết quả mong muốn) | Chuẩn bị đúng; nói và hỏi được hết; kể một lần | P? |

Kiểm tra theo đề: need statement **không chứa giải pháp**. Không có chữ "AI", "phiếu", "chatbot" hay "app gợi ý" trong câu.

## Problem statement đầy đủ (khung 9 yếu tố của Day 2)

| Yếu tố | Nội dung |
|---|---|
| Actor | Người bệnh đã đặt lịch qua MyVinmec, hoặc người thân đi cùng |
| Workflow hiện tại | Đặt hẹn (ngày mong muốn + lý do ≤ 120 ký tự) → tổng đài xác nhận → tự chuẩn bị → check-in → kể lại cho điều dưỡng → gặp bác sĩ vài phút → ra về |
| Bottleneck | Khoảng thời gian ngắn với bác sĩ, và người bệnh đến mà chưa sắp xếp điều cần nói và cần hỏi |
| Impact | ⚠️ THÁI ĐIỀN từ phỏng vấn: số người từng quên hỏi (…/3), số lần kể lại (…), số người từng chuẩn bị sai (…/3) |
| Success metric | Product: % người điền xong phần chuẩn bị; số câu hỏi mang vào phòng khám; số lần phải kể lại. AI: phiếu tóm tắt **không thêm** điều người bệnh không nói (người thử xác nhận từng dòng); 100% ca cấp cứu bị chặn |
| Boundary | Không chẩn đoán, không nêu tên bệnh, không tư vấn thuốc, **không trả lời câu hỏi y khoa** (chỉ ghi lại để hỏi bác sĩ). Hướng dẫn chuẩn bị chỉ lấy từ tài liệu Vinmec. Không bắt buộc; tổng đài và bác sĩ vẫn hỏi như cũ |
| Điểm AI can thiệp | (1) Lời kể tự do → phiếu tóm tắt có cấu trúc; (2) gợi ý câu hỏi chung để người bệnh chọn |
| Mức chọn | **Workflow có một bước AI**: luật cấp cứu → LLM tóm tắt vào khung cố định → kiểm tra đầu ra → người bệnh xác nhận. Không phải agent |
| Rủi ro & HITL | AI tóm tắt sai hoặc thêm thông tin (người bệnh xem và sửa từng dòng, giữ nguyên văn bên cạnh); quyền riêng tư của phiếu; bỏ sót cấp cứu (luật chạy trước AI); xem `06-rui-ro-dao-duc/` |

## Quyết định Go / Not Yet / No-Go

**Conditional go cho prototype**, **Not Yet cho triển khai thật**:

- Go để thử với người dùng: không bắt buộc, chỉ ghi lại và gợi ý câu hỏi, có lưới an toàn (người bệnh duyệt phiếu,
  luật cấp cứu, tổng đài).
- Not Yet cho production: chưa có bác sĩ xác nhận phiếu có giúp được họ không; danh sách dấu hiệu cấp cứu chưa được
  bác sĩ duyệt; chưa có quy định ai được đọc phiếu và lưu bao lâu.

## Bản cuối (sau phỏng vấn)

> ⚠️ THÁI VIẾT LẠI câu need statement nếu phỏng vấn cho thấy vấn đề khác với giả thuyết. Ghi rõ đã đổi gì và vì sao.
