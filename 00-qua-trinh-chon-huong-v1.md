# Quá trình research và chọn hướng (14–15/10/2026)

> **Bản 1 (15/10/2026), dừng ở bước 7; bản hiện hành [00-qua-trinh-chon-huong.md](00-qua-trinh-chon-huong.md) có thêm lần đổi hướng 18/10.**

Báo cáo này ghi lại hướng ban đầu, dữ kiện nào làm mình đổi hướng, các hướng đã cân nhắc và lý do không chọn. Các hướng
chưa làm được đưa vào [BACKLOG.md](BACKLOG.md).

**Quyết định cuối (15/10/2026):** làm **H1, "Chuẩn bị buổi khám"**, thuộc khoảnh khắc *Đặt lịch*. Lát cắt cụ thể là
đoạn từ lúc đặt hẹn xong tới lúc gặp bác sĩ.

## Dòng thời gian

| Bước | Ngày | Làm gì | Kết luận lúc đó | Điều gì làm đổi hướng |
|---|---|---|---|---|
| 1 | 14/10 | Desk research form đặt khám trên vinmec.com; so sánh 5 khoảnh khắc | Chọn *Đặt lịch, lúc không biết khám khoa nào*. Form web bắt chọn chuyên khoa trước, không có gợi ý | — |
| 2 | 14/10 | Làm prototype gợi ý khoa: luật cấp cứu chạy trước, LLM chỉ chọn trong 15 mã khoa, 32 vignette | 10/10 ca cấp cứu bị chặn, 21/22 đúng khoa trong top-2 (chế độ luật) | — |
| 3 | 15/10 sáng | Dùng thử app MyVinmec, 18 ảnh chụp màn hình | App **đã có** trợ lý AI "MIA" với "Kiểm tra triệu chứng" | Giả thuyết "không có gì giúp chọn khoa" **sai với app**, chỉ đúng với form web |
| 4 | 15/10 chiều | Quay 2 video (3:30 và 4:44), đi hết các luồng đặt lịch | Form đặt lịch còn có sẵn **"Đặt lịch theo triệu chứng"**. Tìm được 10 khoảng trống T1–T10 ([gap analysis](01-phong-van/myvinmec-gap-analysis.md)) | Bài toán gợi ý khoa đã được app giải phần lớn. Phần còn lại là lỗi và chỗ chưa nhất quán |
| 5 | 15/10 chiều | So sánh 12 app/hệ thống trong và ngoài nước ([bảng](04-best-practice/app-dat-lich-trong-ngoai-nuoc.md)) | Gợi ý khoa là xu hướng chung và có người dùng thật. Nhưng **tỷ lệ đặt sai khoa vốn rất thấp** (0,68% ở một bệnh viện Quảng Châu) | Nếu tiếp tục hướng cũ, chỉ số "chọn đúng khoa" khó cho thấy khác biệt |
| 6 | 15/10 chiều | Thái nhận xét: đề cần **tính năng mới theo luồng nghiệp vụ từ góc nhìn người bệnh**, không phải chỉ sửa lỗi app | Vẽ luồng 9 bước, đối chiếu với tính năng app đang có, đưa ra 7 hướng ([so sánh](00-huong-tinh-nang-moi.md)) | Đoạn **đặt xong → gặp bác sĩ** gần như trống trong app, lại có bằng chứng nghiên cứu mạnh |
| 7 | 15/10 | Thái chốt H1 | — | — |

## Các hướng đã cân nhắc và lý do

| Hướng | Quyết định | Lý do chính | Xem backlog |
|---|---|---|---|
| **H0. Gợi ý chuyên khoa theo triệu chứng** (hướng ban đầu) | Dừng làm trọng tâm, giữ làm module | App đã có form triệu chứng và MIA; tỷ lệ đặt sai gốc thấp; phần còn lại là sửa lỗi app, không phải tính năng mới | B1, B2 |
| **H1. Chuẩn bị buổi khám** | **Chọn** | Đoạn trống trong app; có bằng chứng về điểm đau (người bệnh không nói hết điều lo, bác sĩ ít hỏi và hay ngắt lời, danh sách câu hỏi giúp người bệnh hỏi nhiều hơn); không đụng lời khuyên y khoa; phỏng vấn được mà không hỏi bệnh; dùng lại được luật cấp cứu; giúp cả bác sĩ | — |
| H2. Hiểu lời dặn sau khám | Backlog, ưu tiên cao nhất | Nhu cầu mạnh nhất (quên 40–80% thông tin), nhưng cần ghi chú bác sĩ làm đầu vào, gần lời khuyên y khoa, và bản viết lại bằng LLM phải được bác sĩ duyệt. Hợp với sprint 6 tuần có bác sĩ hơn bài 1 tuần | B3 |
| H3. Đặt hộ bố mẹ bằng giọng nói | Backlog | Nhóm người lớn tuổi đáng phục vụ, nhưng làm và thử giọng nói trong 1 tuần thì rủi ro kỹ thuật cao; tổng đài người hiện đã làm việc này | B4 |
| H4. Tư vấn chọn gói khám sức khoẻ | Không làm nếu chưa có điều kiện | **Xung đột lợi ích**: AI dễ thành công cụ bán gói. App đã có tiền lệ nhãn "sàng lọc" dẫn tới trang bán IVF (T9) | B5 |
| H5. Ước tính chi phí và bảo hiểm | Backlog | Cần bảng giá và hợp đồng bảo hiểm thật; sai về tiền làm mất niềm tin nhanh | B6 |
| H6. Trợ lý trong ngày khám | Backlog | Cần dữ liệu hàng đợi thật, không kiểm chứng được trong 1 tuần | B7 |
| H7. Lấy chỗ sớm hơn khi có người huỷ | Backlog, không thuộc bài AI | Giải bằng rule; chỉ 11% lời mời được nhận và người lớn tuổi nhận ít hơn (UCSF) | B8 |

## Những gì giữ lại từ hướng cũ

- **Luật cấp cứu chạy trước LLM** (`05-prototype/app/triage.py`): H1 vẫn cho người bệnh kể bằng lời thường, nên vẫn cần
  lớp an toàn này. Phát hiện T1/T2 (app cảnh báo cấp cứu không nhất quán và chậm) càng cho thấy lớp này đáng giữ.
- **Nguyên tắc "AI chỉ dịch vào danh mục, không tự sinh"**: áp sang H1 thành "AI chỉ ghi lại lời người bệnh, không thêm
  điều người bệnh không nói; hướng dẫn chuẩn bị chỉ lấy từ tài liệu Vinmec".
- **Ghi chép dùng thử app và gap analysis**: vẫn là bằng chứng của bước "dùng thử MyVinmec". T3 (kể lại 3 lần) là một
  điểm đau dẫn trực tiếp tới H1.

## Bài học về cách làm (để coach K4)

1. **Dùng thử sản phẩm thật trước khi viết giả thuyết.** Hướng ban đầu dựa trên form web, và hai video app đã bác bỏ nó
   trong một buổi chiều.
2. **Tìm tỷ lệ gốc trước khi chọn chỉ số.** "Giảm đặt sai khoa" nghe hợp lý, nhưng tỷ lệ sai vốn đã dưới 1%.
3. **Đặt các bước của luồng cạnh tính năng app đang có** để thấy chỗ trống, thay vì chỉ soi một màn hình.
4. Đổi hướng **trước khi phỏng vấn** thì gần như không mất gì; đổi sau phỏng vấn thì phải phỏng vấn lại.
