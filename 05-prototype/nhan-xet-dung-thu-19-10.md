# Nhận xét dùng thử prototype (19/10/2026, khoảng 22:20) và cách xử lý

> **Nguồn:** buổi thử của **T1** (người thật, 22 tuổi, đã đồng ý), ghi ở [test-log.md](test-log.md). Thái ghi lại nhận xét
> của T1 rồi nhờ AI viết lại thành văn bản; câu trong ngoặc kép là chữ của **bản viết lại**, không phải nguyên văn T1.

## Điều người dùng thử làm được ngay

Chọn 4 câu → thấy quầy BHYT, giấy tờ và dòng "vì sao"; lộ trình tự xếp lại sau chỉ định; hỏi phòng siêu âm ra câu dùng được;
câu cấp cứu hiện ngay khung đỏ và nút 115; câu "đường huyết 7,2" không được giải thích mà được ghi vào câu hỏi cho bác sĩ;
đặt lịch xong không phải trả lời lại 4 câu.

## Lỗi và cách xử lý

| # | Lỗi (theo nhận xét) | Mức | Đã làm |
|---|---|---|---|
| 1 | Mở lúc 22:20, giờ dự kiến hiện "25:44", "24:24"… | Cao, đụng lời hứa "chờ bao lâu" | ✅ Có giờ khám ngoại trú giả lập 07:00–16:30; ngoài giờ thì báo rõ và tính lộ trình từ 07:00, kèm chỉ đường Cấp cứu 24/7; giờ không còn vượt 24:00 |
| 2 | "khoa xét nghiệm đóng cửa chưa?" được trả lời bằng chỉ đường | Cao | ✅ Thêm loại câu hỏi giờ mở cửa: trả giờ làm việc giả lập của phòng và đang mở hay đã đóng |
| 3 | "Được uống nước lọc không?" nhận lại cả đoạn nhịn ăn, hai ý dính nhau | Cao | ✅ Trả lời thẳng: nước lọc được uống (hướng dẫn Vinmec chỉ yêu cầu không ăn sáng, tránh đồ uống có đường, có gas, trà, cà phê); siêu âm ổ bụng còn cần uống nhiều nước, nhịn tiểu; các ý tách bằng dấu câu |
| 4 | Thẻ chuẩn bị khám tổng quát có "mang thẻ BHYT nếu dùng" dù chọn không BHYT | Trung bình | ✅ Chỉ nhắc thẻ BHYT khi có dùng BHYT |
| 5 | Câu hỏi của lượt trước dính sang lịch hẹn mới | Trung bình | ✅ Mỗi lộ trình mới bắt đầu với danh sách câu hỏi và trợ lý trống |
| 6 | "Không" BHYT và "Chưa, đến thẳng" được chọn sẵn: dễ bị chỉ sai quầy | Cao | ✅ Bỏ chọn sẵn ở 3 câu quyết định quầy; chưa chọn đủ thì không cho xem lộ trình |
| 7 | Nút Hỏi đè bước cuối | Thấp | ✅ Chừa khoảng trống dưới danh sách |
| 8 | Người đến thẳng thấy "Phòng khám 205 (bác sĩ của bạn)" dù chưa chọn khoa | Trung bình | ✅ Ghi "Phòng khám ghi trên phiếu đăng ký (giả lập: phòng 205)" |
| 9 | Giờ hẹn 07:30 không thành một mốc trên danh sách | Trung bình | ✅ Bước check-in ghi "(giờ hẹn 07:30)" |
| 10 | Banner tour nằm trên thẻ "Lộ trình hôm nay": người bệnh sẽ bấm tour trước | Thấp | ✅ Chuyển banner tour xuống dưới cùng trang chủ |
| 11 | Tải lại trang là mất lộ trình | Trung bình | ⏳ Chưa sửa (hết thời gian); app thật phải lưu lộ trình theo tài khoản |
| 12 | "Chỉ đường" chỉ có một câu, không có sơ đồ | Trung bình | ⏳ Chưa làm; cần sơ đồ tầng thật của viện |

Kiểm chứng sau khi sửa (19/10, khoảng 22:30): bộ đo trợ lý không đổi (bộ chính 44/44, held-out 16/20, held-out2 20/20, chặn nhầm 0);
16/16 ràng buộc lộ trình; Playwright: mở lúc 22:xx hiện ghi chú ngoài giờ, không có giờ ≥ 24:00; bấm "Xem lộ trình" khi chưa
chọn đủ bị chặn; nút Hỏi không đè bước cuối; lịch hẹn mới không còn câu hỏi cũ; tour 17 bước chạy hết, không lỗi JavaScript.
