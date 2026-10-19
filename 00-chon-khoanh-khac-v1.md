# Chọn khoảnh khắc: Đặt lịch, đoạn từ lúc đặt hẹn xong tới lúc gặp bác sĩ

> **Bản 1 (15/10/2026), hướng H1; đã thay bằng [bản 2](00-chon-khoanh-khac.md) ngày 18/10/2026 sau phỏng vấn.** Lưu lại để report.

## Quyết định

Đào sâu khoảnh khắc **đặt lịch**, và trong đó chỉ lấy một lát cắt: **từ lúc đặt hẹn thành công tới lúc ngồi trước bác
sĩ**. Đây là lúc người bệnh (hoặc người thân đặt hộ) phải tự chuẩn bị: cần nhịn ăn không, mang giấy tờ gì, kể gì và hỏi
bác sĩ điều gì.

Lát cắt này được chọn **sau khi dùng thử app**. Hướng ban đầu là "không biết khám khoa nào", nhưng MyVinmec đã có đặt
lịch theo triệu chứng và trợ lý MIA. Lý do đổi hướng và các hướng đã cân nhắc: [00-qua-trinh-chon-huong.md](00-qua-trinh-chon-huong.md).
So sánh 7 hướng tính năng: [00-huong-tinh-nang-moi.md](00-huong-tinh-nang-moi.md).

Không đào sâu: thanh toán, đổi hoặc huỷ lịch, chọn khoa (đã có trong app), đọc kết quả.

## Tiêu chí so sánh

| Tiêu chí | Vì sao quan trọng với bài này |
|---|---|
| A. Phỏng vấn được mà không chạm vào bệnh án | Đề cấm hỏi chẩn đoán, bệnh án, tình trạng sức khoẻ (mục 6.4) |
| B. Người phỏng vấn được đều từng trải qua | Chỉ phỏng vấn người quen, ít nhất 3 người, trong khoảng 1 tuần |
| C. Tự thử được trên MyVinmec | Đề yêu cầu ghi chép dùng thử app |
| D. AI có lợi thế thật so với rule/workflow | Day 2 (PAIR): "hỏi bài toán trước, AI sau"; AI chỉ đáng làm khi bài toán thuộc nhóm AI làm tốt hơn |
| E. Rủi ro an toàn kiểm soát được trong prototype 1 tuần | Đề cấm đưa lời khuyên y khoa; prototype phải thử được với người thật |
| F. App chưa giải | Mục tiêu là tính năng mới, không làm lại thứ app đã có |

## So sánh 5 khoảnh khắc

| Khoảnh khắc | A | B | C | D | E | F | Kết luận |
|---|---|---|---|---|---|---|---|
| **Đặt lịch → chuẩn bị gặp bác sĩ** | ✅ hỏi "lần trước bạn có quên hỏi, quên mang gì", không cần biết bệnh gì | ✅ ai đi khám cũng từng trải qua | ✅ đã thử luồng đặt lịch và mục Lịch hẹn | ✅ hiểu lời kể tự do → phiếu có cấu trúc; gợi ý câu hỏi (PAIR: *natural language*) | ✅ AI chỉ ghi lại và gợi ý câu hỏi, không trả lời câu hỏi y khoa; có luật cấp cứu | ✅ chưa thấy tính năng nào cho đoạn này | **Chọn** |
| Đặt lịch → chọn khoa (hướng ban đầu) | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ app đã có form triệu chứng và MIA | Dừng, đưa vào backlog B1 |
| Check-in | ✅ | ⚠️ nhiều người check-in tại quầy, khó nhớ chi tiết | ⚠️ khó thử nếu không thật sự đến viện | ❌ chủ yếu là thủ tục → rule/QR giải tốt hơn | ✅ | ⚠️ app có check-in QR | Loại |
| Chờ tại viện | ✅ | ✅ | ❌ không thử được khi ngồi nhà | ⚠️ cần **dữ liệu hàng đợi thật** | ✅ | ✅ | Loại: không kiểm chứng được trong 1 tuần (backlog B7) |
| Nhận kết quả | ❌ dễ trượt sang tình trạng sức khoẻ | ✅ | ✅ | ✅ | ❌ giải thích chỉ số rất gần **lời khuyên y khoa** | ⚠️ | Loại |
| Tái khám, sau khám | ⚠️ | ⚠️ | ⚠️ có Đơn thuốc, Nhắc thuốc | ✅ viết lại lời dặn dễ hiểu | ⚠️ phải đọc nội dung y khoa, cần bác sĩ duyệt | ⚠️ | Backlog B3, ưu tiên cao nhất cho sprint 6 tuần |

## Vì sao không chọn từng phương án còn lại (bản ngắn để trả lời khi phỏng vấn)

- **Chọn khoa:** app đã có. Tỷ lệ đặt sai gốc ở nơi khác cũng rất thấp (0,68% ở một bệnh viện Quảng Châu), nên khó cho
  thấy khác biệt. Mình giữ phát hiện về app (T1–T10) làm bằng chứng dùng thử.
- **Check-in:** bài toán thủ tục; rule, QR hoặc check-in online giải tốt hơn và rẻ hơn AI.
- **Chờ:** pain có thật, nhưng cần dữ liệu hàng đợi thật mà ứng viên không có.
- **Nhận kết quả:** pain lớn về cảm xúc, nhưng chỉ một bước nhỏ là thành lời khuyên y khoa.
- **Sau khám:** nhu cầu mạnh nhất, nhưng cần ghi chú bác sĩ và bác sĩ duyệt. Hợp với sprint có bác sĩ đồng hành.

## Giả thuyết cần kiểm chứng bằng phỏng vấn

Đây mới là **giả thuyết**; phỏng vấn có thể bác bỏ. Nếu 3 người đều nói "chuẩn bị không có gì khó, khó là ...", mình ghi
lại và đổi trọng tâm.

- **H1. Người bệnh không nói hết hoặc quên hỏi điều mình định hỏi** khi gặp bác sĩ (thời gian ngắn, bị ngắt lời, hồi
  hộp, hoặc người đặt hộ không đi cùng).
- **H2. Người bệnh phải kể lại cùng một chuyện nhiều lần** (form đặt lịch, tổng đài, điều dưỡng, bác sĩ).
- **H3. Người bệnh có lúc chuẩn bị sai** (chưa nhịn ăn, thiếu giấy tờ, không mang thuốc đang dùng hay kết quả cũ) và
  phải chờ thêm hoặc quay lại.
- **H4. Người bệnh sẵn sàng dành khoảng 2 phút trước buổi khám** nếu biết bác sĩ sẽ đọc, nhưng lo về việc ai đọc được
  phiếu đó.
