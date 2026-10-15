# Ghi chép dùng thử MyVinmec: luồng đặt lịch

> ⚠️ THÁI ĐIỀN: tự cài app, làm thử, chụp màn hình **của chính app** (không chụp thông tin cá nhân).
> Đặt thử tới bước cuối rồi huỷ, hoặc dừng trước bước xác nhận. Đừng tạo lịch hẹn thật chiếm chỗ người khác.

- Ngày thử: …/10/2026 · Thiết bị: iOS/Android · Phiên bản app: …
- Tài khoản: đã có / tạo mới

## Bước tôi đã làm

| # | Màn hình | Tôi làm gì | Thấy gì | Vướng/cảm xúc (😀 😐 😟) | Ảnh |
|---|---|---|---|---|---|
| 1 | Mở app | | | | |
| 2 | Vào mục đặt lịch | | | | |
| 3 | Chọn cơ sở | | | | |
| 4 | **Chọn chuyên khoa / bác sĩ** | | | | |
| 5 | Chọn ngày giờ | | | | |
| 6 | Xác nhận | | | | |

## Câu hỏi cần trả lời khi thử (để nối với khoảnh khắc đã chọn)

- [ ] App có giúp gì khi tôi **không biết** nên chọn khoa nào không? (mô tả khoa, tìm theo triệu chứng, chatbot…)
- [ ] Danh sách chuyên khoa có bao nhiêu mục? Tên khoa có dễ hiểu với người không làm y tế không?
- [ ] Đặt cho **người thân** (trẻ em, bố mẹ) thì luồng khác gì?
- [ ] Nếu chọn sai khoa thì app có nói gì không? Có đường gọi tổng đài không?
- [ ] App đã có tính năng AI/chatbot nào chưa? Nếu có thì làm gì?
- [ ] Có ô "lý do khám" không? Ô này nằm **trước hay sau** bước chọn khoa?
- [ ] Sau khi đặt, tổng đài có gọi lại xác nhận không? Nếu có, họ có hỏi lại triệu chứng để đổi khoa không?
- [ ] Nếu chọn theo **bác sĩ** thay vì theo khoa, hồ sơ bác sĩ có ghi bệnh/triệu chứng mà bác sĩ đó khám không?

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
