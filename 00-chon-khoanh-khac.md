# Chọn khoảnh khắc (bản 2, 18/10/2026; cột nguồn sửa theo bản ghi sau review, bản trước ở [-v2](00-chon-khoanh-khac-v2.md)): Chờ, tức trong ngày khám, từ cửa viện tới lúc nhận thuốc

> Bản 1 chọn đoạn "đặt lịch xong → gặp bác sĩ" (hướng H1), giữ ở [00-chon-khoanh-khac-v1.md](00-chon-khoanh-khac-v1.md).
> Toàn bộ quá trình đổi hướng: [00-qua-trinh-chon-huong.md](00-qua-trinh-chon-huong.md).

## Quyết định

Đào sâu khoảnh khắc **chờ**, hiểu rộng là **cả ngày khám tại viện**: tìm quầy đăng ký, đi các phòng xét nghiệm và chụp
chiếu theo chỉ định, chờ kết quả, quay lại bác sĩ, nhận thuốc. Câu hỏi trung tâm của người bệnh: **"Bây giờ tôi đi đâu
tiếp, và còn phải chờ bao lâu?"**

Không đào sâu: đặt lịch (các app lớn đã làm tốt), thanh toán và kết toán BHYT (UMC Care, MyVinmec đã có), đọc kết quả
(gần lời khuyên y khoa).

## Vì sao đổi so với bản 1

| Dữ kiện mới (18/10) | Nguồn | Ảnh hưởng |
|---|---|---|
| Người bệnh **đến thẳng viện**, không đặt lịch qua app | Bản ghi P1, P2 (2/2) | Đoạn "đặt xong → gặp bác sĩ" gần như không tồn tại với họ |
| Phiếu thông tin ở viện là **trắc nghiệm**, có ô ghi thêm, không gây khó | Thái nhớ lại từ một cuộc không ghi âm; không có trong bản ghi P1, P2 | Hướng "phiếu trước khám" không có điểm đau |
| Than phiền: **bỡ ngỡ, không biết vào quầy nào** (tuỳ cách vận hành của viện) | Thái nhớ lại từ một cuộc không ghi âm; không có trong bản ghi P1, P2. P1 còn mô tả ngược lại (máy quét, tự chọn khoa). **Giả thuyết, 0/2** | Điểm đau nằm trong ngày khám |
| Người dùng trên Threads cho rằng app đặt lịch hiện **đã tốt và tiện** | Thái đọc Threads (⚠️ chờ trích nguyên văn) | Không làm thêm ở bước đặt lịch |
| UMC Care (bác sĩ được phỏng vấn giới thiệu) làm tốt đặt lịch, thanh toán, kết quả; **hướng dẫn quy trình chỉ là bài viết chung**, không theo chỉ định của từng người | Dùng thử UMC Care 18/10; [ghi chép](04-best-practice/umc-care-va-app-benh-vien-vn.md) | Khoảng trống: app biết dữ liệu nhưng không chỉ bước tiếp theo |

## So sánh lại theo tiêu chí cũ (A–F)

| Khoảnh khắc | A. Không chạm bệnh án | B. Ai cũng trải qua | C. Thử được | D. AI có lợi thế | E. Rủi ro kiểm soát được | F. App chưa giải | Kết luận |
|---|---|---|---|---|---|---|---|
| **Chờ / trong ngày khám** | ✅ hỏi đi đâu, chờ bao lâu | ✅ | ⚠️ thử bằng dữ liệu giả lập (đề cho phép) | ⚠️ **chỉ ở bước hiểu câu hỏi tự do**; lộ trình là luật | ✅ không trả lời câu y khoa, câu trả lời ghép từ dữ liệu viện | ✅ app chỉ có hướng dẫn chung | **Chọn** |
| Đặt lịch → chuẩn bị gặp bác sĩ (bản 1) | ✅ | ⚠️ người đến thẳng không qua đoạn này | ✅ | ✅ | ✅ | ✅ | Dừng: phỏng vấn không thấy điểm đau. Backlog B9 |
| Đặt lịch → chọn khoa (H0) | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ app đã có | Backlog B1 |
| Nhận kết quả | ❌ | ✅ | ✅ | ✅ | ❌ gần lời khuyên y khoa | ⚠️ | Loại |
| Sau khám (hiểu lời dặn) | ⚠️ | ⚠️ | ⚠️ | ✅ | ⚠️ cần bác sĩ duyệt | ⚠️ | Backlog B3 |

**Điểm yếu thừa nhận trước:** tiêu chí D chỉ đạt một phần. Phần lớn giá trị đến từ luật và dữ liệu vận hành; AI chỉ đáng
dùng nếu hiểu câu hỏi tự do tốt hơn rõ rệt so với luật từ khoá. Bài đo điều này trên bộ held-out (xem `05-prototype/`).
Trước đó, bản 1 đã đổi hướng khi đạt cả 6 tiêu chí trên giấy nhưng phỏng vấn không thấy điểm đau: tiêu chí trên giấy không
thay được bằng chứng người dùng.

## Câu hỏi còn phải trả lời khi thử

1. Điểm đau "bỡ ngỡ quầy, lộ trình" ở viện công có còn mạnh ở **Vinmec** (viện tư, có nhân viên chăm sóc khách hàng)?
2. Người thử có tin giờ dự kiến không, hay giờ sai làm họ lo hơn?
3. Người thử hỏi bằng lời của mình nhiều không, hay chỉ bấm câu gợi ý? (Nếu chỉ bấm gợi ý thì không cần AI.)
