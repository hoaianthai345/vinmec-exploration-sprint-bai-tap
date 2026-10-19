# Log thử nghiệm với người dùng: Lộ trình khám trong ngày

> Thẻ kịch bản: [test-scenarios.md](test-scenarios.md). Bản trước: [test-log-v2.md](test-log-v2.md) (khi chưa có buổi thử).
> Tour `?tour=1` là demo do người làm bài bấm, không tính là buổi thử.

**Trạng thái (19/10/2026): 1 buổi thử với người thật (T1).** Chưa đủ 2–3 người như đề gợi ý; chưa có vòng 2 để thử lại phần đã sửa.

## Vòng 1 (19/10/2026, khoảng 22:20, bản deploy, chế độ luật)

> **Nguồn ghi chép:** T1 tự cầm máy thử. Thái ghi lại nhận xét của T1 rồi nhờ AI viết lại thành văn bản
> ([nhan-xet-dung-thu-19-10.md](nhan-xet-dung-thu-19-10.md)). Vì vậy câu chữ trong đó **là bản AI viết lại, không phải lời
> nguyên văn của T1**. Không có ghi âm. Số lần T1 phải hỏi người điều phối **không được ghi lại**.

| Người thử | Hồ sơ (ẩn danh) | Làm gì | Gặp gì | Sửa gì sau đó |
|---|---|---|---|---|
| T1 | 22 tuổi, đã đồng ý; không tham gia làm bài này | Luồng đến thẳng có BHYT (giống K1); nhập chỉ định máu, siêu âm bụng, nước tiểu (giống K2); hỏi trợ lý vị trí phòng, giờ mở cửa, nước lọc, đường huyết 7,2, dấu hiệu méo miệng nói khó (giống K3–K5); đặt lịch khám tổng quát rồi xem lộ trình (giống K6) | **Làm được:** tìm đúng quầy BHYT kèm giấy tờ; hiểu thứ tự sau chỉ định; câu hỏi phòng siêu âm, câu cấp cứu, câu y khoa được xử lý đúng; đặt lịch xong không phải trả lời lại. **Vướng:** giờ dự kiến vượt 24:00 khi thử buổi tối; hỏi giờ mở cửa thì nhận chỉ đường; hỏi nước lọc nhận cả đoạn nhịn ăn; đáp án BHYT chọn sẵn "Không" suýt làm chỉ sai quầy; câu hỏi lượt trước dính sang lịch hẹn mới; tải lại trang mất lộ trình; nút Hỏi đè bước cuối; banner tour đứng trước thẻ tính năng | 10 sửa, xem bảng dưới |

## Số liệu từ log máy

Bản deploy trên Vercel chỉ ghi log vào `/tmp` (mất khi function khởi động lại), nên **không có log máy cho buổi T1**.
Lượt thử sau nên chạy bản local để có log (`python3 app/server.py`, rồi `python3 eval/summarize_log.py`).

## Thay đổi sau vòng 1

| # | Vấn đề T1 gặp | Sửa gì | Commit |
|---|---|---|---|
| 1 | Giờ dự kiến "25:44" khi thử lúc 22:20 | Giờ khám ngoại trú giả lập 07:00–16:30; ngoài giờ thì báo rõ, tính từ 07:00, chỉ đường Cấp cứu 24/7 | `14c855e` |
| 2 | Hỏi "khoa xét nghiệm đóng cửa chưa" nhận chỉ đường | Thêm loại câu hỏi giờ mở cửa | `14c855e` |
| 3 | Hỏi nước lọc nhận cả đoạn nhịn ăn | Trả lời thẳng: nước lọc được uống (theo hướng dẫn Vinmec) | `14c855e` |
| 4 | Thẻ chuẩn bị nhắc thẻ BHYT dù không dùng BHYT | Chỉ nhắc khi có BHYT | `14c855e` |
| 5 | Câu hỏi lượt trước dính sang lịch hẹn mới | Mỗi lộ trình mới bắt đầu trống | `14c855e` |
| 6 | Đáp án quyết định quầy được chọn sẵn | Bỏ chọn sẵn; chưa chọn đủ thì không cho xem lộ trình | `14c855e` |
| 7 | Nút Hỏi đè bước cuối | Chừa khoảng trống | `14c855e` |
| 8 | "Phòng khám 205 (bác sĩ của bạn)" cho người chưa chọn khoa | "Phòng khám ghi trên phiếu đăng ký" | `14c855e` |
| 9 | Giờ hẹn không thành một mốc | Bước check-in ghi giờ hẹn | `14c855e` |
| 10 | Banner tour đứng trước thẻ tính năng | Chuyển xuống cuối trang chủ | `14c855e` |
| — | Tải lại trang mất lộ trình; "Chỉ đường" chưa có sơ đồ | Chưa sửa (hết thời gian) | — |

Kiểm chứng các sửa bằng Playwright và bộ đo, xem [nhan-xet-dung-thu-19-10.md](nhan-xet-dung-thu-19-10.md). **Chưa có vòng 2**
với người thật để xác nhận các sửa giải được đúng chỗ T1 vướng.

## Vòng 2: chưa có

| Người thử | Kết quả sau sửa |
|---|---|
| (chưa có) | |
