# Backlog: các hướng để phát triển lần sau

Lý do chưa làm và quá trình chọn hướng: [00-qua-trinh-chon-huong.md](00-qua-trinh-chon-huong.md). Mỗi mục ghi rõ
**khi nào nên mở lại** và **bước đầu tiên**, để người làm sau (hoặc nhóm K4) bắt đầu được ngay.

Thứ tự ưu tiên: B3 → B2 → B9 → B1 → B4 → B6 → B8 → B5. B7 đang được làm (từ 18/10/2026, "Lộ trình khám trong ngày").

| Mã | Hướng | Khoảnh khắc | Vì sao chưa làm | Mở lại khi | Bước đầu tiên |
|---|---|---|---|---|---|
| **B1** | Gợi ý chuyên khoa theo triệu chứng (hướng ban đầu H0) | Đặt lịch | App đã có form triệu chứng và MIA; tỷ lệ đặt sai gốc thấp | Có số liệu Vinmec cho thấy tỷ lệ đổi khoa hoặc tải tổng đài đáng kể | Hỏi tổng đài: mỗi ngày bao nhiêu cuộc gọi hỏi "khám khoa nào", bao nhiêu ca phải đổi khoa. Prototype cũ vẫn chạy được (luật + LLM chọn trong danh mục, 32 vignette) |
| **B2** | Báo cáo và sửa các khoảng trống T1–T8 của MyVinmec | Đặt lịch | Là sửa lỗi app, không phải tính năng mới | Ngay khi có kênh báo cho đội sản phẩm MyVinmec | Xác nhận T1 trước: chọn "Cơn đau thắt ngực" trong form đặt lịch xem có cảnh báo không. Ưu tiên: T1, T2 (an toàn) → T3 (kể lại) → T7, T8 (sửa rẻ). Chi tiết: [gap analysis](01-phong-van/myvinmec-gap-analysis.md) |
| **B3** | Hiểu lời dặn sau khám (H2) | Sau khám / tái khám | Cần ghi chú bác sĩ làm đầu vào; LLM viết lại có thể sót hoặc sai, phải có bác sĩ duyệt | Sprint 6 tuần có bác sĩ đồng hành và sandbox dữ liệu đã khử định danh | Nhờ bác sĩ viết 10 ghi chú giả lập; đo bản viết lại theo 2 trục: dễ hiểu và **không sót, không sai** (bác sĩ chấm). Nối với H1: câu hỏi người bệnh chuẩn bị → câu trả lời của bác sĩ |
| **B4** | Đặt hộ bố mẹ bằng giọng nói hoặc qua Zalo (H3) | Đặt lịch | Rủi ro kỹ thuật giọng nói trong 1 tuần; tổng đài đang làm việc này | Phỏng vấn cho thấy đặt hộ người lớn tuổi là pain lớn | Quan sát 5 cuộc gọi tổng đài (nếu được phép): người gọi nói gì, tổng đài hỏi gì. Tham khảo Zocdoc Zo (AI nhận đặt lịch qua điện thoại, ca khó chuyển cho người) |
| **B5** | Tư vấn chọn gói khám sức khoẻ (H4) | Đặt lịch | Xung đột lợi ích: AI dễ thành công cụ bán gói | Có quy tắc rõ do bác sĩ đặt (gói theo tuổi, giới, yếu tố nguy cơ) và cách giải thích minh bạch | Chỉ làm khi gợi ý **kèm lý do y khoa đã được duyệt** và luôn có phương án rẻ nhất phù hợp |
| **B6** | Ước tính chi phí và quyền lợi bảo hiểm (H5) | Đặt lịch | Cần bảng giá và hợp đồng thật; sai về tiền mất niềm tin | Có API bảng giá và danh mục bảo lãnh | Bắt đầu bằng rule (bảng giá công khai), AI chỉ đọc điều khoản và **trích nguyên văn** |
| **B7** | Trợ lý trong ngày khám (H6) · **đang làm từ 18/10** | Chờ | Cần dữ liệu hàng đợi thật (prototype dùng dữ liệu giả lập) | Được vào khoa và có dữ liệu trạng thái lượt khám | Ghi lại luồng di chuyển thật của 5 người bệnh trong một buổi sáng |
| **B8** | Lấy chỗ sớm hơn khi có người huỷ (H7) | Đặt lịch | Giải bằng rule, không cần AI; người lớn tuổi dùng ít hơn | Vinmec có vấn đề lịch trống do huỷ hẹn | Đo tỷ lệ huỷ hoặc không đến theo khoa |
| **B9** | Chuẩn bị buổi khám (H1): kể trước cho bác sĩ, câu hỏi mang vào phòng, checklist | Đặt lịch → gặp bác sĩ | Phỏng vấn 18/10: người bệnh đến thẳng viện, phiếu tại viện trắc nghiệm không gây khó, không thấy cần chuẩn bị trước | Có bằng chứng người bệnh **đặt lịch trước** chiếm phần lớn (ví dụ ở Vinmec) và bác sĩ muốn đọc phiếu trước | Prototype vẫn chạy: `/index-v2.html`, đo bằng `eval/run_eval_prep.py`. Phần "câu hỏi để hỏi bác sĩ" đã dùng lại trong hướng mới |

## Nguồn tham khảo cho backlog

- Bằng chứng và so sánh app: [04-best-practice/app-dat-lich-trong-ngoai-nuoc.md](04-best-practice/app-dat-lich-trong-ngoai-nuoc.md).
- Đánh giá 7 hướng: [00-huong-tinh-nang-moi.md](00-huong-tinh-nang-moi.md).
