# Mình sẽ coach một nhóm làm bài này thế nào

Bối cảnh: nhóm 5–10 bạn K4 làm bài "một lần đi khám" trong 1 tuần. Mục tiêu của mình không phải để bài nhóm đẹp nhất,
mà để **mỗi bạn tự đi hết vòng quan sát → phỏng vấn → need statement → prototype → thử** và có bằng chứng thật cho từng bước.

## Lịch 1 tuần

| Ngày | Nhóm làm | Mình làm | Đầu ra phải có cuối ngày |
|---|---|---|---|
| T1 | Chọn khoảnh khắc, dùng thử MyVinmec | Buổi 45 phút: cách chọn hẹp, ví dụ một bảng so sánh lựa chọn (như `00-chon-khoanh-khac.md`) | Mỗi bạn 1 khoảnh khắc + lý do loại các khoảnh khắc khác |
| T2 | Soạn interview guide, phỏng vấn thử với nhau | Đóng vai người được phỏng vấn; sửa câu hỏi dẫn dắt | Guide đã qua 1 lần thử, có lời xin đồng ý |
| T3 | Phỏng vấn ≥ 3 người | Kiểm ngẫu nhiên 1 log/bạn: có trích dẫn nguyên văn? có tách quan sát với suy luận? | 3 log ẩn danh |
| T4 | Journey map, need statement, best practice | Review need statement theo checklist bên dưới | Need statement không chứa giải pháp |
| T5 | Prototype | Office hour 2 tiếng gỡ kỹ thuật; nhắc làm luồng an toàn trước | Prototype bấm được |
| T6 | Thử với 2–3 người, sửa | Xem log thử: có ghi "đã sửa gì" chưa? | Test log + ít nhất 1 lần sửa |
| T7 | Rủi ro, slides, nộp | Chạy checklist nộp bài cho cả nhóm | Repo đủ thư mục, slides ≤ 10 trang |

Nhịp cố định: check-in 15 phút mỗi tối trên nhóm chat (mỗi bạn 3 dòng: đã xong gì, kẹt gì, mai làm gì); thứ Sáu nộp
báo cáo tuần. Bạn nào trễ 1 mốc thì mình nhắn riêng trong ngày; trễ 2 mốc thì gọi 10 phút để tìm nguyên nhân.

## Cách gỡ khi nhóm kẹt

| Dấu hiệu kẹt | Câu hỏi gợi mở mình dùng | Không làm |
|---|---|---|
| Không tìm được người phỏng vấn | "Trong danh bạ, ai từng đưa bố mẹ đi khám năm nay?" | Không cho phép "phỏng vấn tưởng tượng" |
| Phỏng vấn ra toàn ý kiến chung | "Kể lại lần gần nhất…" thay vì "Bạn có thích…" | Không viết lại guide hộ |
| Viết giả thuyết khi chưa mở sản phẩm thật | "Bạn đã dùng thử MyVinmec tới bước đó chưa? Quay màn hình lại cho mình xem" | Không chấp nhận giả thuyết chỉ dựa trên web hay suy đoán |
| Chọn chỉ số nghe hay nhưng không đo được khác biệt | "Tỷ lệ gốc của vấn đề này là bao nhiêu? Nếu đã dưới 1% thì cải thiện thế nào?" | Không tự đưa con số hộ |
| Nhảy thẳng vào giải pháp AI | "Bỏ chữ AI đi thì vấn đề còn không? Rule có giải được không?" (Day 2) | Không chê ý tưởng, chỉ hỏi bằng chứng |
| Prototype không chạy | Chia nhỏ: luồng bấm được bằng dữ liệu giả trước, AI sau | Không code thay |
| Bất đồng trong nhóm về hướng đi | Đặt 2 hướng cạnh nhau, đối chiếu với log phỏng vấn; dữ liệu thắng ý kiến | Không để người nói to nhất quyết |
| Muốn dùng dữ liệu bệnh nhân thật | Dừng ngay, nhắc ràng buộc NDA/6.4 | Không có ngoại lệ |

## Cách kiểm tra chất lượng

Checklist mình dùng để review từng bài trước khi nộp:

- [ ] Phỏng vấn: ≥ 3 log, có lời xin đồng ý, ẩn danh, có trích dẫn nguyên văn, **không có nội dung bệnh án**
- [ ] Insight trỏ được về log cụ thể (P mấy, câu nào)
- [ ] Need statement đủ problem – population – outcome, **không chứa giải pháp**
- [ ] Best practice có link nguồn mở được
- [ ] Prototype: có log thử với người thật (ai, làm gì, gặp gì, sửa gì), và có ít nhất một lần sửa sau khi thử
- [ ] Có luồng an toàn: AI sai thì sao, cấp cứu thì sao
- [ ] README ghi rõ phần nào do AI tạo
- [ ] Không có log, trích dẫn hay số liệu nào bịa: **mình hỏi ngẫu nhiên 1 chi tiết và yêu cầu bạn chỉ ra nguồn**

Phản hồi theo mẫu: 1 điều làm tốt (cụ thể), 1 điều cần sửa nhất (cụ thể, kèm ví dụ), 1 câu hỏi để bạn tự nghĩ tiếp.

## Mình mang gì từ kinh nghiệm Lab Coach

Ở AI Thực Chiến, trước mỗi buổi mình tự làm lab như một học viên để biết chỗ dễ kẹt, rồi đặt mốc kiểm tra tiến độ để
biết ai đang chậm ở bước nào. Với nhóm K4, mình làm tương tự: tự làm bài này trước (chính là repo này), nên biết
trước các chỗ dễ sai như hỏi dẫn dắt, need statement lẫn giải pháp, hay prototype thiếu luồng an toàn.

Ngay trong bài này, mình đã phải đổi hướng sau khi quay video dùng thử app: tính năng mình định làm thì app đã có
(xem `00-qua-trinh-chon-huong.md`). Mình sẽ cho K4 xem đúng quá trình đó, để các bạn dùng thử sản phẩm trước khi viết
giả thuyết, và hiểu rằng đổi hướng trước khi phỏng vấn gần như không mất gì.

Ở dự án P-004, nhóm mình từng bị trả hồ sơ vì có trích dẫn người dùng không có thật. Vì vậy mục cuối của checklist
là mục mình kiểm kỹ nhất.
