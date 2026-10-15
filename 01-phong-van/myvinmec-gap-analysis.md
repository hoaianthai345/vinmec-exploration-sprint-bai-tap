# MyVinmec: luồng đặt lịch thực tế và chỗ còn thiếu

**Nguồn**, đều quay ngày 15/10/2026 trên iOS, tài khoản chưa kết nối hồ sơ y tế:

- **V1**: video 3 phút 30 giây, đi lướt các luồng.
- **V2**: video 4 phút 44 giây, gồm đặt theo triệu chứng, MIA "Kiểm tra triệu chứng" và một câu đóng vai cấp cứu.
- 18 ảnh chụp màn hình.

Mốc thời gian ghi `V1 m:ss` hoặc `V2 m:ss`. Video và ảnh gốc **không** đưa vào repo vì có họ tên, SĐT và thông báo tin nhắn
của người khác. Ảnh trong `anh-myvinmec/` đã cắt bỏ những phần này.

> Đây là **quan sát trên một tài khoản, vài lần thử**. Đây chưa phải số liệu người dùng, nên cần đối chiếu với phỏng vấn. Mọi
> câu mô tả triệu chứng trong video là đóng vai, không phải tình trạng sức khoẻ thật.

## 1. App hiện có gì

```
Tab "Đặt lịch" ─┬─ Tham vấn tâm lý từ xa
                └─ Khám chuyên khoa tại bệnh viện
                     → Chọn khách hàng (Tôi / + Thêm) → CBNV Vingroup? → người nước ngoài?
                     → Chọn địa điểm (≈ 15 cơ sở)
                     → Chọn phương thức: theo bác sĩ | theo chuyên khoa | theo TRIỆU CHỨNG
                          └─ Chọn triệu chứng (danh sách, tìm kiếm, "+ Thêm triệu chứng", chọn nhiều)
                               → "Chọn chuyên khoa gợi ý" (có xét tuổi)  hoặc  → mở MIA
                     → Ngày khám mong muốn → Lý do khám (≤ 120 ký tự) → ĐẶT HẸN
MIA (nút nổi) ──┬─ Kiểm tra triệu chứng: chat + thẻ câu hỏi trắc nghiệm → cảnh báo cấp cứu (modal, nút "Gọi cấp cứu 115")
                └─ Đặt lịch khám → form 3 bước: hồ sơ, cơ sở, lý do (≤ 100 ký tự) …
```

### Điểm app đang làm tốt (giữ lại, đừng làm lại)

- **Đặt theo triệu chứng đã có**, tìm được bằng lời thường: gõ "Đau bụng" hoặc "Ho" ra các mục dễ hiểu như "Ho dai
  dẳng (trên 3 tuần)" (V2 0:34–0:58). Màn gợi ý ghi rõ *"chỉ mang tính chất tham khảo"* và *"gợi ý theo độ tuổi của hồ
  sơ"* (V1 1:22, [ảnh 02](anh-myvinmec/02-goi-y-chuyen-khoa.jpg)).
- **MIA hỏi có cấu trúc:** hỏi giới tính và tuổi của *người đang gặp triệu chứng*, nên đặt hộ người khác được. Sau đó là
  các thẻ trắc nghiệm về diễn biến, tính chất, vị trí, triệu chứng kèm theo, đều có nút "Bỏ qua" (V2 1:47–3:03).
- **MIA có cảnh báo cấp cứu tốt:** modal "Dấu hiệu cần hỗ trợ y tế khẩn cấp!" nêu lý do, có nút **"Gọi cấp cứu 115"** và
  "Liên hệ Vinmec", ghi chú "không thay thế chẩn đoán y tế", tự đính kèm vị trí hiện tại. Đã bật với câu đau ngực (V2
  3:08) và câu "Bạn tôi bị méo miệng nói khó" (V2 4:10), xem [ảnh 07](anh-myvinmec/07-mia-canh-bao-cap-cuu.jpg).
- Đặt cho người thân bằng "+ Thêm"; chọn ngày nhanh; danh sách bác sĩ có phí khám dự kiến.

## 2. Chỗ còn thiếu, theo bằng chứng

| # | Quan sát | Bằng chứng | Vì sao quan trọng |
|---|---|---|---|
| **T1** | **Hai hệ thống không thống nhất về dấu hiệu cấp cứu.** Trong form đặt lịch, tìm "Đau bụng" ra ngay các mục *"Phình động mạch chủ… lóc tách động mạch chủ… đau bụng dữ dội"* và *"Cơn đau thắt ngực (đau như bóp nghẹt sau xương ức, lan lên cằm, vai trái…)"*, chọn được như triệu chứng thường để đặt hẹn. Cũng mô tả đau ngực đó, MIA lại bật modal cấp cứu kèm nút gọi 115. | V2 0:36, [ảnh 06](anh-myvinmec/06-tim-dau-bung.jpg) đặt cạnh [ảnh 07](anh-myvinmec/07-mia-canh-bao-cap-cuu.jpg) | Người đi đường đặt lịch, tức đường chính, không được cảnh báo. *Chưa thử bấm chọn mục đó xem có cảnh báo không.* |
| **T2** | **Cảnh báo cấp cứu đến chậm vì đi qua LLM.** Với câu "Bạn tôi bị méo miệng nói khó", từ lúc gửi tới khi modal hiện mất khoảng 20 giây, gồm "Quá trình suy nghĩ" và "Đang ghi nhận các triệu chứng". Với đau ngực, cảnh báo chỉ hiện sau khi người dùng trả lời khoảng 8 thẻ câu hỏi. | V2 3:48 → 4:10; 1:47 → 3:08 | Với đột quỵ, từng phút đều quan trọng. Một danh sách luật cố định sẽ phản hồi tức thì và nhất quán ở mọi lối vào. |
| **T3** | **Chuyển sang MIA nhưng mất ngữ cảnh.** Chọn 2 triệu chứng ("Đau bụng hố chậu phải", "Ho dai dẳng") rồi bấm Tiếp tục, app mở thẳng màn chào chung của MIA. Người dùng phải tự bấm "Kiểm tra triệu chứng", gõ lại khoảng 30 giây ("Tôi chưa rõ chuyên khoa phù hợp với triệu chứng đau bụng ho chóng mặt"), rồi MIA hỏi lại giới tính và tuổi. | V2 1:07–1:47 | Người dùng mô tả cùng một vấn đề tới 3 lần (danh sách, MIA, ô "Lý do khám"). |
| **T4** | **Gợi ý dẫn vào ngõ cụt theo tuổi.** Hồ sơ người lớn chọn một mục dành cho trẻ em, app chỉ gợi ý *Nhi*, kèm dòng đỏ "Chỉ khám cho khách hàng dưới 16 tuổi", không có khoa thay thế. Danh sách không lọc theo tuổi, dù bước gợi ý có xét tuổi. | V1 1:21–1:22, [ảnh 02](anh-myvinmec/02-goi-y-chuyen-khoa.jpg) | Người dùng nhận một gợi ý không đặt được. |
| **T5** | **Danh sách mặc định xếp theo ABC, lẫn tên bệnh và thủ thuật:** *Alzheimer, Bạch tạng, Bệnh lý mạch vành – can thiệp mạch vành, đặt stent…* Phải gõ tìm mới ra mục dễ hiểu. | V1 1:20, [ảnh 01](anh-myvinmec/01-chon-trieu-chung.jpg) | Người không biết gõ gì sẽ gặp danh sách khó hiểu đầu tiên. |
| **T6** | **Chưa thấy MIA kết thúc bằng gợi ý khoa hoặc nút đặt lịch.** Lượt thử duy nhất đi tới cảnh báo cấp cứu, vì người thử chọn "đau tức ngực". | V2 1:47–3:21 | *Cần thử thêm một ca không cấp cứu.* |
| **T7** | **Nút MIA nổi che nội dung:** nút "Ngày khác", nút "Xem chi tiết", khung quét mã, ô "Lý do khám". | V1 0:46, 1:15, 1:43, 2:04; [ảnh 03](anh-myvinmec/03-chon-phuong-thuc.jpg), [ảnh 05](anh-myvinmec/05-bong-mia-che-nut.jpg) | Lỗi giao diện rõ ràng, sửa rẻ. |
| **T8** | **Sheet "Liên hệ" không có số cấp cứu:** khoảng 20 số (bệnh viện, phòng khám, ngân hàng mô, tư vấn gói ưu đãi), không có "Cấp cứu / 115". | V1 1:38–1:41, [ảnh 04](anh-myvinmec/04-lien-he-cuoi-danh-sach.jpg) | Nút 115 hiện chỉ có trong modal của MIA. |
| T9 | "Câu hỏi sàng lọc sức khỏe → Sàng lọc sức khỏe sinh sản" mở trang web giới thiệu gói IVF và trữ noãn, có nút "Mua gói online ngay". Không có câu hỏi sàng lọc nào. | V2 4:40–4:43 | Nhãn không khớp nội dung. Ngoài phạm vi đặt lịch. |
| T10 | Nhiều lối vào đặt lịch: tab Đặt lịch, Lịch hẹn, Liên hệ, "Đặt lịch nhanh", banner, MIA, Dịch vụ y tế → "Nhận tư vấn". Form có hai ô tick CBNV và người nước ngoài đứng trước thông tin đặt hẹn. | V1 0:20–1:45 | Ghi nhận để tham khảo. |

## 3. Chưa quan sát được

1. Bấm chọn "Cơn đau thắt ngực…" trong form đặt lịch thì có cảnh báo không (để khẳng định T1).
2. MIA "Kiểm tra triệu chứng" với một ca **không** cấp cứu: kết thúc bằng gì, có gợi ý khoa hay nút đặt lịch không (T6).
3. MIA "Đặt lịch khám" bước 2/3 và 3/3. "Sàng lọc đột quỵ". Toàn bộ danh sách khoa khi đặt theo chuyên khoa.

## 4. Cơ hội cải thiện (đề xuất, chờ phỏng vấn xác nhận)

> **Cập nhật 15/10/2026:** bài đã chọn làm tính năng mới **Chuẩn bị buổi khám** (H1), dựa một phần vào T3 (kể lại 3 lần).
> Các đề xuất sửa app dưới đây được chuyển vào [BACKLOG.md](../BACKLOG.md), mục B2.

Trọng tâm: **bước "Đặt lịch theo triệu chứng"**. Bước này đã có trong app, nên đây là cải tiến chứ không phải tính năng mới.
Mục tiêu là đưa sự an toàn và khả năng hiểu lời thường mà MIA đang có vào đúng đường người dùng đi đặt lịch:

1. **Kiểm tra dấu hiệu cấp cứu bằng luật cố định ngay khi chọn hoặc gõ triệu chứng** (T1, T2). Phản hồi tức thì, cùng
   một danh sách cho cả form lẫn MIA. Có dấu hiệu thì dừng đặt lịch, hiện nút gọi 115.
2. **Cho gõ mô tả bằng lời thường ngay trong bước này** (T3, T5). AI chỉ được ánh xạ mô tả vào danh mục chuyên khoa có
   sẵn, rồi hiện 1–2 khoa kèm lý do. Khi cần chuyển sang MIA thì **mang theo** triệu chứng đã chọn, tuổi và giới của hồ sơ.
3. **Luôn gợi ý được một khoa hợp tuổi** (T4).
4. **Dùng lại mô tả cho ô "Lý do khám"**, để người dùng không phải gõ lại (T3).
5. Sửa nhanh: nút MIA nổi không được che nút bấm hay ô nhập (T7); thêm "Cấp cứu 115" vào sheet Liên hệ (T8).
