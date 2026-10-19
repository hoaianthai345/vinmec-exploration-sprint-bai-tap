# 3 best practice quốc tế cho "Chuẩn bị buổi khám" và bài học cho Vinmec

Tiêu chí chọn: mỗi ví dụ giải đúng bài toán "giúp người bệnh chuẩn bị trước khi gặp bác sĩ" và có nguồn đọc được. Mình
chỉ ghi điều nguồn nói; phần "bài học" là suy luận của mình.

Tài liệu liên quan trong thư mục này:
- [app-dat-lich-trong-ngoai-nuoc.md](app-dat-lich-trong-ngoai-nuoc.md): so sánh 12 app/hệ thống đặt lịch, dùng để chọn hướng.
- [huong-cu-dieu-huong.md](huong-cu-dieu-huong.md): Zocdoc, NHS 111, Ada cho hướng ban đầu (backlog B1). Phần an toàn
  (luật cấp cứu chạy trước AI, đo bằng vignette) vẫn được dùng cho hướng mới.

## 1. Ubie AI 問診 (Nhật Bản): hỏi bệnh trước khám, kết quả chuyển thẳng cho bác sĩ

**Điều nguồn nói**
- Thay phiếu hỏi bệnh giấy bằng hỏi bệnh trên máy tính bảng hoặc điện thoại. Người bệnh nhập triệu chứng lúc chờ hoặc
  trước khi đến; kết quả chuyển vào bệnh án điện tử, giảm việc ghi chép của bác sĩ [1].
- Có ở hơn 1.800 cơ sở y tế (báo chí 3/2025) [2].
- Bệnh viện Urasoe báo thời gian từ lúc hỏi bệnh tới lúc vào khám giảm từ trung bình 40 phút xuống 20 phút. Đây là số
  liệu trong thông cáo của nhà cung cấp [1].
- Bản cho bác sĩ còn gợi ý các bệnh có thể nghĩ tới [1].

**Bài học cho Vinmec**
- Giá trị lớn nằm ở chỗ **phiếu đi thẳng vào workflow của bác sĩ**, không phải một màn hình riêng của người bệnh. Trong
  prototype, phiếu hiển thị đúng như bác sĩ sẽ đọc (5 dòng cố định).
- Mình **không** làm phần gợi ý bệnh: đề bài cấm chẩn đoán, và phần đó cần bác sĩ thẩm định. Phiếu chỉ ghi lại lời
  người bệnh, có trích dẫn nguyên văn cho từng dòng.
- Số liệu hiệu quả là của nhà cung cấp. Khi vào khoa, cần đo lại trên chính quy trình của Vinmec.

## 2. AHRQ QuestionBuilder (Mỹ) và bằng chứng về danh sách câu hỏi

**Điều nguồn nói**
- Cơ quan AHRQ (Bộ Y tế Mỹ) phát hành app miễn phí QuestionBuilder trong chiến dịch "Questions Are the Answer". Người
  dùng nhập lịch hẹn và lý do khám, chọn câu hỏi từ danh sách có sẵn theo loại buổi khám hoặc tự viết, rồi lưu vào lịch
  hẹn. Dữ liệu chỉ nằm trên máy người dùng [3].
- Tổng quan 42 nghiên cứu cho thấy danh sách câu hỏi giúp người bệnh hỏi nhiều hơn và bác sĩ cung cấp nhiều thông tin
  hơn, rõ nhất khi danh sách **được bác sĩ đồng thuận** và **đưa ngay trước buổi khám**. Chưa thấy hiệu quả nhất quán về
  lo âu, mức hài lòng hay thời gian khám [4].
- Lý do cần làm: chỉ 4/35 người bệnh nói ra đủ những gì họ định nói [5]; bác sĩ hỏi người bệnh muốn bàn gì ở 36% lượt
  khám và thường ngắt lời sau trung vị 11 giây [6].

**Bài học cho Vinmec**
- Câu hỏi gợi ý lấy từ **danh sách cố định, chung chung**, không do LLM sinh. Như vậy không trượt sang nội dung y khoa,
  và bác sĩ có thể duyệt danh sách một lần. Prototype mặc định **không chọn sẵn** câu gợi ý, để người bệnh tự chọn.
- Câu hỏi người bệnh tự kể được giữ nguyên văn và **không được trả lời**; chỉ chuyển cho bác sĩ.
- Khi triển khai thật, cần bác sĩ "đồng thuận" danh sách (ví dụ một dòng "Bác sĩ … mời bạn chuẩn bị câu hỏi"), vì
  nghiên cứu cho thấy đây là điều kiện để danh sách câu hỏi có hiệu quả.

## 3. Phiếu trước khám trên cổng bệnh nhân Epic MyChart (Mỹ): bài học về tỷ lệ dùng

**Điều nguồn nói** (Naimark và cộng sự, 2024 [7], người bệnh từ 65 tuổi ở 2 phòng khám gia đình)
- Chỉ **26,4%** (198/750) điền phiếu trước ít nhất một lượt khám; thời gian điền trung vị **14 phút**.
- Người điền trẻ hơn người không điền (72,3 so với 76,1 tuổi). Bác sĩ nhận xét **người bệnh nặng nhất không điền**.
- Trong số người trả lời khảo sát và nhớ đã điền, 90,7% không thấy khó; 68,7% đồng ý phiếu giúp họ và bác sĩ hiểu
  điều họ ưu tiên.

**Bài học cho Vinmec**
- Phiếu phải **ngắn** (mục tiêu khoảng 2 phút, không phải 14), **không bắt buộc**, và **người thân điền hộ được**.
  Prototype có nút "Để sau" và lựa chọn "Người thân".
- Không được coi phiếu là kênh duy nhất: người không điền thường là người cần nhất. Tổng đài và bác sĩ vẫn hỏi như cũ.
- Chỉ số cần đo khi thử: tỷ lệ điền xong, thời gian điền, chia theo nhóm tuổi.

## Tổng hợp: áp dụng vào prototype

| Nguyên tắc | Từ | Trong prototype |
|---|---|---|
| Phiếu đi thẳng vào workflow bác sĩ, khung cố định | Ubie | ✅ 5 dòng cố định; màn hình "bác sĩ thấy phiếu này" |
| AI chỉ ghi lại, không chẩn đoán | Ubie (làm ngược lại có chủ đích) | ✅ mỗi dòng phải có trích dẫn nguyên văn; dòng không có căn cứ bị bỏ |
| Câu hỏi từ danh sách cố định, đưa ngay trước khám | AHRQ, tổng quan QPL | ✅ danh sách luật cố định; câu của người bệnh không được trả lời |
| Ngắn, không bắt buộc, cho điền hộ | Epic MyChart | ✅ nút "Để sau", chọn "Người thân"; ⏳ đo thời gian điền với người thật |
| An toàn: luật cấp cứu chạy trước AI | NHS 111, Ada (hướng cũ) | ✅ 10/10 lời kể có dấu hiệu nguy hiểm bị chặn |

## Nguồn

1. ASCII.jp và PR TIMES về Ubie AI 問診 (thông cáo của nhà cung cấp, có số liệu Bệnh viện Urasoe).
   https://ascii.jp/elem/000/004/187/4187468/ · https://prtimes.jp/main/html/rd/p/000000216.000048083.html
2. THE BRIDGE (3/2025). https://thebridge.jp/2025/03/healthtech-company-ubie-tackling-the-challenge-of-maximizing-healthy-life-expectancy-secures-funding-from-japan-post-capital
3. AHRQ, *QuestionBuilder App*. https://www.ahrq.gov/questions/question-builder/index.html
4. Sansoni J.E., Grootemaat P., Duncan C. *Question Prompt Lists in health consultations: A review.* Patient Educ Couns
   2015;98:1454–64. doi:10.1016/j.pec.2015.05.015
5. Barry C.A. et al. *Patients' unvoiced agendas in general practice consultations: qualitative study.* BMJ
   2000;320:1246. doi:10.1136/bmj.320.7244.1246
6. Singh Ospina N. et al. *Eliciting the Patient's Agenda: Secondary Analysis of Recorded Clinical Encounters.* J Gen
   Intern Med 2019;34(1):36–40. doi:10.1007/s11606-018-4540-5
7. Naimark J. et al. *Leveraging an Electronic Health Record Patient Portal to Help Patients Formulate Their Health Care
   Goals: Mixed Methods Evaluation of Pilot Interventions.* JMIR Form Res 2024;8:e56332. doi:10.2196/56332
