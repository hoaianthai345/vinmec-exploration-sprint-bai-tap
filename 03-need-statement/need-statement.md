# Need statement (bản 2, 18/10/2026; cập nhật bằng chứng sau review)

> ⚠️ **Trạng thái: GIẢ THUYẾT, chưa được phỏng vấn xác nhận.** Hai buổi có bản ghi (P1, P2) không nhắc tới điểm đau "không
> biết vào quầy, phòng nào" (0/2). Bản trước khi cập nhật bằng chứng: [need-statement-v2.md](need-statement-v2.md).

> Bản 1 (hướng "Chuẩn bị buổi khám", H1) giữ ở [need-statement-v1.md](need-statement-v1.md). Lý do đổi: phỏng vấn cho thấy
> người bệnh đến thẳng viện (bản ghi P1, P2), phiếu tại viện không gây khó, còn điều họ than phiền là **bỡ ngỡ không biết vào
> quầy nào** (hai ý sau: Thái nhớ lại từ một cuộc không ghi âm; không có trong bản ghi P1, P2).
> Xem [../VERSIONS.md](../VERSIONS.md).

## Câu need statement

> Cách để **người bệnh khám ngoại trú, và người thân đi cùng, nhất là người đến lần đầu hoặc đến thẳng không đặt lịch**,
> gặp tình huống **không biết bước tiếp theo phải đến quầy hay phòng nào, theo thứ tự nào và phải chờ tới khi nào**, có
> thể **đi hết các bước của buổi khám đúng chỗ, đúng thứ tự, biết trước thời gian chờ, mà không phải hỏi nhiều người hay
> quay lại chỗ cũ**.

Theo mẫu Biodesign:

| Thành phần | Nội dung | Bằng chứng |
|---|---|---|
| Problem (vấn đề) | **Không biết** bước tiếp theo: vào quầy nào; sau chỉ định thì đi phòng nào, theo thứ tự nào; khi nào có kết quả | **Phỏng vấn có bản ghi: chưa có (0/2)**; P1 mô tả khâu đăng ký đã nhanh nhờ máy quét. Thái nhớ lại từ một cuộc không ghi. Desk research gián tiếp: số thứ tự "nhảy cóc" (VnReview) |
| Population (nhóm người dùng) | Người bệnh ngoại trú và người đi cùng; ưu tiên người đến lần đầu, đến thẳng, người lớn tuổi | 2/2 người được ghi âm đến thẳng viện (P1, P2). Tuổi Trẻ (8/2024): "chưa mấy ai biết đến App đặt khám và cách sử dụng chúng" |
| Outcome (kết quả mong muốn) | Đi đúng chỗ, đúng thứ tự; biết trước thời gian chờ; không phải hỏi nhiều người, không quay lại chỗ cũ | ⚠️ đo khi thử: số lần phải hỏi người khác, số lần đi nhầm hoặc quay lại |

**Hai vấn đề không được trộn:** "chờ lâu" (khảo sát hài lòng ngoại trú nêu chờ ở khâu xét nghiệm, chiếu chụp, trả kết quả) và
"không biết giờ, không biết bước tiếp". Need statement này chỉ nói vấn đề thứ hai. Giờ dự kiến **không làm hàng đợi ngắn lại**,
và giờ sai có hại (rủi ro R4), nên không được trình bày như giải pháp cho "chờ lâu".

Kiểm tra theo đề: câu need statement **không chứa giải pháp**. Không có chữ "app", "AI", "lộ trình số" hay "trợ lý".

## Problem statement đầy đủ (khung 9 yếu tố của Day 2)

| Yếu tố | Nội dung |
|---|---|
| Actor | Người bệnh ngoại trú (hoặc người thân đi cùng) đang ở trong viện |
| Workflow hiện tại | Đến viện → tìm quầy (dịch vụ, BHYT hay lịch hẹn) → lấy số → đo sinh hiệu → gặp bác sĩ → thanh toán chỉ định → đi từng phòng xét nghiệm, chụp chiếu → chờ kết quả → quay lại bác sĩ → thanh toán, nhận thuốc |
| Bottleneck | Người bệnh tự đoán bước tiếp theo từ biển báo và hỏi người xung quanh. App bệnh viện **biết** chỉ định và phòng của từng người nhưng chỉ đưa hướng dẫn chung (quan sát UMC Care, MyVinmec) |
| Impact | **Chưa đo được.** Bản ghi P1, P2 không có lần nào đi nhầm quầy hoặc phòng. Cần một lần khám cụ thể: đi nhầm mấy lần, hỏi mấy người, mất thêm bao lâu |
| Success metric | Product: số lần người thử phải hỏi người điều phối; số bước bấm "chỉ đường"; thời gian đi hết thẻ kịch bản; tỷ lệ thấy "có giúp". AI: tỷ lệ hiểu đúng câu hỏi tự do (luật so với LLM, trên bộ held-out); **100% câu y khoa bị chuyển cho bác sĩ; 100% cấp cứu bị chặn; 0 câu trả lời có nội dung ngoài dữ liệu viện** |
| Boundary | Không giải thích kết quả, không chẩn đoán, không tư vấn thuốc hay chế độ ăn sau chẩn đoán. Chỉ chỉ đường, thời gian chờ, chuẩn bị theo hướng dẫn của viện. Không thay biển báo và nhân viên, chỉ bổ sung |
| Điểm AI can thiệp | Hiểu câu hỏi bằng lời thường (không dấu, nói trống không, người lớn tuổi) và xếp vào danh mục cố định: loại câu hỏi + phòng hoặc xét nghiệm |
| Mức chọn | **Workflow, AI ở đúng một bước.** Lộ trình là luật (không cần AI). Trợ lý: luật cấp cứu → luật y khoa → LLM phân loại vào danh mục → câu trả lời ghép từ dữ liệu viện. Không phải agent |
| Rủi ro & HITL | Chỉ sai đường (dữ liệu phòng cũ); thời gian ước tính sai; câu y khoa lọt (chặn bằng luật + câu trả lời không bao giờ chứa nội dung y khoa); cấp cứu (luật trước LLM). Xem `06-rui-ro-dao-duc/` |

**Thành thật về phần AI (Day 2: "bỏ chữ AI đi thì vấn đề còn không?"):** phần lớn giá trị (quầy nào, thứ tự phòng, giờ
dự kiến) đến từ **luật và dữ liệu vận hành**, không cần AI. AI chỉ đáng dùng ở bước hiểu câu hỏi tự do: trên bộ 20 câu
held-out (đo một lần, trước khi vá luật y khoa ngày 19/10), luật từ khoá chỉ hiểu đúng 14/20 và chặn được 1/3 câu y khoa (xem `05-prototype/README.md`). Nếu chế độ LLM
không vượt rõ con số này thì nên bỏ AI, giữ lộ trình bằng luật.

## Quyết định Go / Not Yet / No-Go

**Conditional go cho prototype**, **Not Yet cho triển khai thật**:

- Go để thử với người dùng: dữ liệu giả lập, không chạm dữ liệu người bệnh, câu trả lời không thể chứa lời khuyên y khoa.
- Not Yet cho production: cần dữ liệu phòng và hàng đợi thật của viện; cần kiểm tra điểm đau này có còn mạnh ở **Vinmec**
  (viện tư, có nhân viên chăm sóc khách hàng) hay chủ yếu ở viện công; danh sách dấu hiệu cấp cứu chưa được bác sĩ duyệt.

## Bản cuối (sau khi thử với người dùng)

> **Chưa có bản cuối**: chưa có buổi thử với người thật. Khi có, viết lại nếu người thử cho thấy vấn đề khác, ghi rõ đã đổi gì
> và vì sao, và lưu bản trước thành `-vN`.
