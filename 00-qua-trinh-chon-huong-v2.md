# Quá trình research và chọn hướng (14–18/10/2026)

Báo cáo này ghi lại hướng ban đầu, dữ kiện nào làm mình đổi hướng, các hướng đã cân nhắc và lý do không chọn. Các hướng
chưa làm được đưa vào [BACKLOG.md](BACKLOG.md).

**Quyết định hiện hành (18/10/2026):** làm **"Lộ trình khám trong ngày"**, thuộc khoảnh khắc *Chờ* (trong ngày khám tại
viện). Đây là lần đổi hướng thứ hai: lần 1 (15/10) do dùng thử app, lần 2 (18/10) do phỏng vấn. Bản trước của file này:
[00-qua-trinh-chon-huong-v1.md](00-qua-trinh-chon-huong-v1.md).

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
| 8 | 18/10 | Phỏng vấn những người đầu tiên | Người bệnh **đến thẳng viện**; phiếu ở viện là trắc nghiệm, không gây khó; than phiền chính là **bỡ ngỡ không biết vào quầy nào** | H1 không có điểm đau: theo Thái, việc hỏi bác sĩ và chuẩn bị thông tin trước khi gặp không quan trọng lắm với người được hỏi; mình phản biện bằng nghiên cứu nhưng không đủ, vì nhu cầu người dùng không tự thấy thì tỷ lệ dùng thấp (Epic: 26%) |
| 9 | 18/10 | Viết [interview guide bản 2](01-phong-van/interview-guide.md) khảo sát cả hành trình C1–C10 | Không kiểm chứng ý tưởng có sẵn, tìm chặng tệ nhất | — |
| 10 | 18/10 | Phỏng vấn một bác sĩ; bác sĩ gợi ý xem **UMC Care**. Thái dùng thử UMC Care (video 8 phút) và đọc ý kiến trên Threads | Đặt lịch, thanh toán, kết quả **đã được giải tốt**; hướng dẫn quy trình của app chỉ là bài viết chung ([ghi chép](04-best-practice/umc-care-va-app-benh-vien-vn.md)) | Khoảng trống còn lại nằm **trong ngày khám**, sau bước bác sĩ chỉ định |
| 11 | 18/10 | So 3 hướng: lộ trình trong ngày, hiểu lời dặn sau khám, giữ H1 dạng phiếu tại viện | Thái chốt **lộ trình trong ngày** | — |

## Các hướng đã cân nhắc và lý do

| Hướng | Quyết định | Lý do chính | Xem backlog |
|---|---|---|---|
| **H0. Gợi ý chuyên khoa theo triệu chứng** (hướng ban đầu) | Dừng làm trọng tâm, giữ làm module | App đã có form triệu chứng và MIA; tỷ lệ đặt sai gốc thấp; phần còn lại là sửa lỗi app, không phải tính năng mới | B1, B2 |
| **H1. Chuẩn bị buổi khám** | Chọn 15/10, **dừng 18/10** sau phỏng vấn (backlog B9) | Đoạn trống trong app; có bằng chứng về điểm đau (người bệnh không nói hết điều lo, bác sĩ ít hỏi và hay ngắt lời, danh sách câu hỏi giúp người bệnh hỏi nhiều hơn); không đụng lời khuyên y khoa; phỏng vấn được mà không hỏi bệnh; dùng lại được luật cấp cứu; giúp cả bác sĩ | — |
| H2. Hiểu lời dặn sau khám | Backlog, ưu tiên cao nhất | Nhu cầu mạnh nhất (quên 40–80% thông tin), nhưng cần ghi chú bác sĩ làm đầu vào, gần lời khuyên y khoa, và bản viết lại bằng LLM phải được bác sĩ duyệt. Hợp với sprint 6 tuần có bác sĩ hơn bài 1 tuần | B3 |
| H3. Đặt hộ bố mẹ bằng giọng nói | Backlog | Nhóm người lớn tuổi đáng phục vụ, nhưng làm và thử giọng nói trong 1 tuần thì rủi ro kỹ thuật cao; tổng đài người hiện đã làm việc này | B4 |
| H4. Tư vấn chọn gói khám sức khoẻ | Không làm nếu chưa có điều kiện | **Xung đột lợi ích**: AI dễ thành công cụ bán gói. App đã có tiền lệ nhãn "sàng lọc" dẫn tới trang bán IVF (T9) | B5 |
| H5. Ước tính chi phí và bảo hiểm | Backlog | Cần bảng giá và hợp đồng bảo hiểm thật; sai về tiền làm mất niềm tin nhanh | B6 |
| **H6. Trợ lý trong ngày khám** | **Chọn 18/10** (dạng "Lộ trình khám trong ngày") | Trước đó để backlog vì cần dữ liệu hàng đợi thật. Đổi đánh giá: đề cho phép dữ liệu giả lập ở Tuần 3; phỏng vấn cho thấy điểm đau thật; prototype chứng minh được luồng và giới hạn, còn hàng đợi thật là điều kiện triển khai | — |
| H7. Lấy chỗ sớm hơn khi có người huỷ | Backlog, không thuộc bài AI | Giải bằng rule; chỉ 11% lời mời được nhận và người lớn tuổi nhận ít hơn (UCSF) | B8 |

## Những gì giữ lại từ hướng cũ

- **Luật cấp cứu chạy trước LLM** (`05-prototype/app/triage.py`): H1 vẫn cho người bệnh kể bằng lời thường, nên vẫn cần
  lớp an toàn này. Phát hiện T1/T2 (app cảnh báo cấp cứu không nhất quán và chậm) càng cho thấy lớp này đáng giữ.
- **Nguyên tắc "AI chỉ dịch vào danh mục, không tự sinh"**: áp sang H1 thành "AI chỉ ghi lại lời người bệnh, không thêm
  điều người bệnh không nói; hướng dẫn chuẩn bị chỉ lấy từ tài liệu Vinmec".
- **Ghi chép dùng thử app và gap analysis**: vẫn là bằng chứng của bước "dùng thử MyVinmec". T3 (kể lại 3 lần) là một
  điểm đau dẫn trực tiếp tới H1.

## Bài học về cách làm (để coach K4)

0. **Tiêu chí trên giấy không thay được phỏng vấn.** H1 đạt cả 6 tiêu chí A–F nhưng người dùng không thấy đau. Nếu
   phỏng vấn trước khi làm prototype H1 thì đỡ được một lượt code; bù lại, lõi an toàn (luật cấp cứu, AI chỉ xếp vào danh
   mục, câu trả lời có nguồn) dùng lại được cho hướng mới.

1. **Dùng thử sản phẩm thật trước khi viết giả thuyết.** Hướng ban đầu dựa trên form web, và hai video app đã bác bỏ nó
   trong một buổi chiều.
2. **Tìm tỷ lệ gốc trước khi chọn chỉ số.** "Giảm đặt sai khoa" nghe hợp lý, nhưng tỷ lệ sai vốn đã dưới 1%.
3. **Đặt các bước của luồng cạnh tính năng app đang có** để thấy chỗ trống, thay vì chỉ soi một màn hình.
4. Đổi hướng **trước khi phỏng vấn** thì gần như không mất gì; đổi sau phỏng vấn thì phải phỏng vấn lại.
