# Ghi chép dùng thử MyVinmec: luồng đặt lịch

> Bản có khung mẫu ban đầu: [myvinmec-trial-notes-v1.md](myvinmec-trial-notes-v1.md). Chi tiết theo mốc thời gian video và
> 10 khoảng trống T1–T10: [myvinmec-gap-analysis.md](myvinmec-gap-analysis.md).

- Ngày thử: 15/10/2026 · iOS · tài khoản chưa kết nối hồ sơ y tế
- Nguồn: 18 ảnh chụp màn hình và 2 video quay màn hình (3:30 và 4:44). Ảnh, video gốc **ngoài repo** vì có họ tên, SĐT;
  7 ảnh trong `anh-myvinmec/` đã cắt phần thông tin cá nhân.
- Không tạo lịch hẹn thật; dừng trước bước xác nhận.

## Bước đã làm

| # | Màn hình | Làm gì | Thấy gì | Vướng | Nguồn |
|---|---|---|---|---|---|
| 1 | Trang chủ | Mở app | Lưới dịch vụ, nút trợ lý AI MIA nổi ở góc | Nút MIA che nội dung ở nhiều màn (T7) | ảnh 03, 05 |
| 2 | Tab Đặt lịch | Chọn "Khám chuyên khoa tại bệnh viện" | Chọn khách hàng (Tôi / + Thêm), hai ô tick CBNV và người nước ngoài | Nhiều lối vào đặt lịch khác nhau (T10) | V1 0:20–1:45 |
| 3 | Chọn cơ sở | Chọn một trong khoảng 15 cơ sở | — | — | V1 |
| 4 | Chọn phương thức | Theo bác sĩ, theo chuyên khoa, **theo triệu chứng** | Danh sách triệu chứng xếp ABC, lẫn tên bệnh và thủ thuật; gõ tìm thì ra mục dễ hiểu | Danh sách mặc định khó hiểu (T5); gợi ý theo tuổi có ngõ cụt (T4) | ảnh 01, 02 |
| 5 | Chọn ngày | Chọn ngày khám mong muốn | Không chọn giờ cụ thể | — | V1 1:20–1:31 |
| 6 | Lý do khám, đặt hẹn | Gõ lý do (tối đa 120 ký tự) | Phải mô tả lại vấn đề lần thứ ba (danh sách, MIA, ô lý do) | Kể lại 3 lần (T3) | V2 1:07–1:47 |
| 7 | Trợ lý MIA | "Kiểm tra triệu chứng", đóng vai câu đau ngực và "bạn tôi bị méo miệng nói khó" | Modal cảnh báo cấp cứu có nút gọi 115 | Cảnh báo đến sau khoảng 20 giây (T2); form đặt lịch lại cho chọn "Cơn đau thắt ngực" như triệu chứng thường (T1) | ảnh 06, 07; V2 3:08–4:10 |

## Câu hỏi khi thử và câu trả lời

- App có giúp khi **không biết** nên chọn khoa nào không? → **Có**: đặt theo triệu chứng và MIA.
- Đặt cho **người thân** thì sao? → Có "+ Thêm" hồ sơ; MIA hỏi giới tính, tuổi của người đang có triệu chứng.
- App đã có AI chưa? → Có trợ lý MIA (chat tự do, thẻ trắc nghiệm, cảnh báo cấp cứu).
- Có ô "lý do khám" không? → Có, nằm **sau** bước chọn khoa hoặc triệu chứng.
- Sau khi đặt có hướng dẫn chuẩn bị không? → **Chưa quan sát được** (màn Lịch hẹn của tài khoản này trống).

## Tóm tắt 3 phát hiện chính

1. Bài toán "không biết khám khoa nào" app **đã giải phần lớn** (đặt theo triệu chứng, MIA) → bỏ hướng gợi ý khoa.
2. **Cảnh báo cấp cứu không nhất quán và chậm** (T1, T2) → nguyên tắc "luật cấp cứu chạy trước AI" trong prototype.
3. Người dùng **mô tả cùng một vấn đề 3 lần** (T3).

## Quan sát từ ảnh chụp app (15/10/2026, lượt 1: 18 ảnh, IMG_2221–2238)

> Ảnh gốc nằm ở `../myvinmec/` (ngoài repo). **Không đưa ảnh gốc vào repo**: các ảnh 2225, 2227, 2229, 2237, 2238 có họ tên,
> ngày sinh, SĐT. Khi cần đưa vào slide thì cắt hoặc che phần thông tin cá nhân trước.

- **App đã có trợ lý AI "MIA"** (nút nổi góc phải ở hầu hết màn hình). Màn hình chính có 4 thẻ: *Kiểm tra triệu chứng*
  ("Nhập triệu chứng, nhận phân tích và gợi ý phù hợp"), *Phân tích dinh dưỡng*, *Đặt lịch khám* ("với bác sĩ và cơ sở
  phù hợp"), *Liên kết ứng dụng*. Có ô chat tự do "Hỏi về sức khỏe & y tế…" và phần "Quá trình suy nghĩ".
- **Đặt lịch qua MIA hỏi *lý do khám* ở bước 1/3**, cùng hồ sơ khám (bản thân hoặc người thân) và cơ sở. Đây là luồng
  ngược với form web, nơi phải chọn chuyên khoa trước. Chưa thấy bước 2/3 và 3/3.
- Màn hình chính có mục "Sàng lọc đột quỵ" và "Sàng lọc sức khỏe sinh sản" (bộ câu hỏi sàng lọc).
- "Dịch vụ y tế" liệt kê theo chuyên khoa, có mô tả ngắn từng khoa và nút "Nhận tư vấn".
- "Liên hệ" có "Đặt lịch chủ động: chọn ngày, giờ, xác nhận lịch tự động", cổng CSKH 24/7 và số gọi từng bệnh viện.
- Trang "Lịch hẹn" của tài khoản chưa kết nối hồ sơ y tế đang trống.

**Hệ quả:** giả thuyết "không có gì giúp người dùng chọn khoa" **không còn đúng với app** (chỉ còn đúng với form web).
Lượt 2 (video quay màn hình) cho thấy form đặt khám còn có sẵn "Đặt lịch theo triệu chứng". Phân tích đầy đủ và những
chỗ còn thiếu: [myvinmec-gap-analysis.md](myvinmec-gap-analysis.md). Phát hiện này dẫn tới việc đổi hướng bài sang
"Chuẩn bị buổi khám" (xem [../00-qua-trinh-chon-huong.md](../00-qua-trinh-chon-huong.md)).

## Desk research từ nguồn công khai (15/10/2026, trước khi dùng thử)

Phần này lấy từ trang công khai, **không phải** trải nghiệm trong app. Khi dùng thử, ghi lại chỗ app khác với web.

- **Form đặt khám trên web** ([vinmec.com/dat-kham](https://vinmec.com/dat-kham)): chọn cơ sở → **chuyên khoa (bắt buộc)** →
  bác sĩ (không bắt buộc) → thời gian → thông tin cá nhân → **lý do khám (bắt buộc, gõ tự do)** → OTP → xác nhận. Sau đó
  tổng đài gọi lại để xác nhận lịch hẹn. Không có lựa chọn "chưa rõ chuyên khoa" hay gợi ý theo triệu chứng.
- **Mô tả trên App Store** ([MyVinmec](https://apps.apple.com/vn/app/myvinmec/id1494832536)): 4,9/5 với khoảng 16 nghìn
  lượt đánh giá; tính năng gồm đặt lịch cho bản thân và người thân, khám từ xa, hồ sơ sức khoẻ, hỏi chuyên gia, check-in QR.
  Không nhắc tới gợi ý chuyên khoa hay chatbot AI. Ghi chú phát hành chỉ ghi chung chung "tối ưu trải nghiệm".
- **Hệ quả cho giả thuyết H1:** người dùng phải chọn khoa *trước* khi được mô tả triệu chứng. Tuy vậy, cuộc gọi xác nhận
  của tổng đài có thể đã là một lớp sửa sai do con người làm. Phỏng vấn cần hỏi: "Tổng đài có từng đổi khoa giúp bạn
  không?" Nếu có, pain có thể nằm ở **thời gian chờ gọi lại** chứ không phải ở việc chọn sai khoa.

## Tóm tắt 3 phát hiện chính

1. …
2. …
3. …
