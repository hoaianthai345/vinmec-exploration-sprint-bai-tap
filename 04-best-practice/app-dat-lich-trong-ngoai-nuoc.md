# App đặt lịch khám trong và ngoài nước: có luồng gì, người dùng có cần không

Desk research ngày 15/10/2026. Phục vụ quyết định chọn hướng; bộ best practice của hướng ban đầu (Zocdoc, NHS 111, Ada) ở [huong-cu-dieu-huong.md](huong-cu-dieu-huong.md).

**Cách đọc:** "Điều nguồn nói" chỉ ghi điều nguồn công bố. Số của nhà cung cấp (Ubie, Doctolib, Zocdoc, Epic) là số tự
báo cáo. App Việt Nam mình chỉ đọc mô tả trên store và web, **chưa dùng thử**. Phần "người dùng có cần không" là suy
luận từ bằng chứng, phải kiểm lại bằng phỏng vấn.

## Kết luận ngắn

1. **Luồng đặt lịch cốt lõi ở đâu cũng giống nhau:** cơ sở → khoa/bác sĩ → giờ → xác nhận. Các app khác nhau ở phần
   *trước* bước đặt (điều hướng theo triệu chứng) và phần *sau* bước đặt (nhắc lịch, đổi lịch, danh sách chờ, hàng đợi).
2. **Điều hướng theo triệu chứng là xu hướng chung:** Ubie (Nhật), bệnh viện Trung Quốc, Buoy và Ada đều làm. Trong
   các app Việt Nam mình xem được (Medpro, YouMed, Tâm Anh), mô tả công khai **không** nhắc tới tính năng này. Theo các
   nguồn này, MyVinmec (form triệu chứng + MIA) đang đi trước trong nước.
3. **Người dùng có dùng tính năng này:** ở một bệnh viện Quảng Châu, số lượt tra cứu mỗi ngày bằng 16–29% số lượt khám.
   Với Buoy, tỷ lệ người "không chắc nên đi đâu" giảm từ 34% xuống 21%. **Nhưng tỷ lệ đặt sai khoa vốn đã thấp**
   (0,68% ở Quảng Châu). Vì vậy giá trị chính có lẽ là **giảm phân vân, giảm thời gian và an toàn**, ít nằm ở việc sửa
   chuyện đặt sai khoa. Điều này buộc bài phải đổi chỉ số chính (xem mục 4).
4. **Người lớn tuổi được lợi ít hơn.** Với Ada, 93% người 18–24 tuổi thấy lời khuyên hữu ích, ở người từ 70 tuổi chỉ
   59%. Với Fast Pass, người từ 65 tuổi ít nhận lịch sớm hơn. Vì vậy vẫn phải giữ kênh tổng đài và đặt hộ.

## 1. Mỗi bên có luồng gì

| Bên | Nước | Luồng / tính năng nổi bật | Điều nguồn nói |
|---|---|---|---|
| **Ubie** | Nhật (có bản Mỹ) | Trả lời khoảng 20 câu hỏi → bệnh có thể liên quan + **khoa nên khám** + cơ sở gần. Bản cho bệnh viện là **hỏi bệnh trước khám** (AI 問診): câu trả lời chuyển sẵn cho bác sĩ. | Báo chí 3/2025: khoảng 12 triệu người dùng/tháng; bản cho bệnh viện có ở hơn 1.800 cơ sở [1][2] |
| **BV Phụ sản – Nhi Quảng Châu** (Tencent) | Trung Quốc | Chọn triệu chứng → hỏi tiếp → gợi ý khoa → đặt lịch → **chỉ đường trong viện**. Có chẩn đoán sẵn thì đi thẳng tới khoa. | Đặt sai giảm từ 0,68% xuống 0,12%; 56–61% lượt tra cứu dẫn tới đặt lịch thành công [3] |
| **BV Tân Hoa, Thượng Hải** | Trung Quốc | **Gõ lời tự do** → trích triệu chứng → chuẩn hoá ICD-10 → gợi ý trong **79 khoa phụ**, có xét tuổi và giới. Chạy trên WeChat mini program. | Huỷ đăng ký giảm từ 3,83% xuống 3,53%; mất 10 giây so với 14 giây của điều dưỡng; điều dưỡng vẫn đúng hơn (98% so với 92%) [4] |
| **Zocdoc** | Mỹ | **Lý do khám** là bắt buộc và quyết định thời lượng slot; guided search; từ 5/2025 có **Zo**, trợ lý AI đặt lịch qua điện thoại 24/7, ca phức tạp chuyển cho nhân viên. | Zocdoc tự công bố Zo xử lý được tới 70% cuộc gọi [5][6] |
| **Doctolib** | Pháp, Đức, Ý | Chọn **motif** (lý do khám, danh sách do phòng khám đặt) → bệnh nhân mới hay cũ → khám tại chỗ hay video → giờ. Sau khi đặt: nhắc lịch SMS/email/thông báo, đổi/huỷ tới 4 giờ trước, danh sách chờ, chặn đặt trùng chuyên khoa trong 6 ngày. | Khoảng 93 triệu lời nhắc/tháng; no-show của bác sĩ chuyên khoa giảm từ 4,5% xuống 3,1% (số Doctolib tự báo cáo) [7][8] |
| **Epic MyChart** | Mỹ | Tự đặt lịch theo cây câu hỏi; **Fast Pass**: có người huỷ thì tự mời bệnh nhân lấy chỗ sớm hơn. | UCSF: 11% lời mời được nhận, khám sớm hơn trung vị 14 ngày; người từ 65 tuổi và người nói tiếng Trung ít nhận hơn [9] |
| **NHS: Patchs, eConsult** | Anh | **Mô tả vấn đề trước**, phòng khám phân loại rồi mới cấp lịch ("total triage"). | Truy cập rộng hơn nhưng phòng khám quá tải, có báo cáo kiệt sức; một số người bệnh thấy mất quan hệ với bác sĩ [10][11] |
| **Buoy** | Mỹ | Chatbot hỏi triệu chứng → tối đa 3 khả năng kèm **mức chăm sóc** (tự theo dõi, bác sĩ gia đình, cấp cứu). | 158.083 lượt: "không chắc" giảm từ 34% xuống 21%; 32% hạ mức khẩn, 4% tăng mức khẩn (một tác giả có cổ phần Buoy) [12] |
| **Ada** | Đức / Anh | Symptom checker dùng trong phòng chờ phòng khám. | 523 người: 97,8% thấy dễ dùng, 88,1% sẽ dùng lại; 86% nói không đổi cách đi khám [13] |
| **Medpro** | Việt Nam | Chọn bệnh viện → chuyên khoa → bác sĩ → giờ → **thanh toán trong app**; lấy số thứ tự; tư vấn video; tổng đài 1900 2115. | Mô tả không nhắc gợi ý theo triệu chứng [14] |
| **YouMed** | Việt Nam | Lấy số và đặt khám ở phòng khám/bác sĩ; tư vấn video hoặc chat, có gọi bác sĩ ngay. | Mô tả store không nhắc AI hay kiểm tra triệu chứng [15] |
| **BVĐK Tâm Anh** | Việt Nam | Đặt hẹn, **theo dõi hàng đợi**, tra lịch sử khám, nhắc tái khám. | Mô tả store không nhắc AI [16] |

## 2. Gom theo nhóm tính năng: người dùng có cần không

| Nhóm | Ai làm | Bằng chứng về nhu cầu | MyVinmec | Liên quan khoảnh khắc "đặt lịch khi chưa biết khoa"? |
|---|---|---|---|---|
| **A. Điều hướng theo triệu chứng** (khoa hoặc mức chăm sóc) | Ubie, BV Trung Quốc, Buoy, Ada, Zocdoc | **Có người dùng thật:** số lượt tra cứu bằng 16–29% lượt khám [3]; giảm "không chắc" từ 34% xuống 21% [12]; 88% sẽ dùng lại [13]. **Nhưng** tỷ lệ đặt sai gốc thấp (0,68%) và mức giảm huỷ đăng ký nhỏ (0,3 điểm %) [3][4]. | **Đã có:** form triệu chứng + MIA | **Trực tiếp.** Đây là phần cần cải tiến, không làm mới. |
| **B. Kiểm tra cấp cứu trước khi đặt** | NHS 111, Buoy, Ada (mức khẩn) | Buoy: 4% lượt được nâng mức khẩn [12]. Các app tốt về an toàn tiệm cận bác sĩ (97%) [huong-cu-dieu-huong.md] | MIA có; **form đặt lịch chưa** (T1) | **Trực tiếp.** Đây là khoảng trống rõ nhất. |
| **C. Lý do khám có cấu trúc / hỏi bệnh trước khám** | Zocdoc, Doctolib, Ubie AI 問診 | Bên bệnh viện được lợi (thời lượng slot, chuẩn bị trước) [5]; bên người dùng được lợi là **không phải kể lại** | Ô tự do ≤ 120 ký tự, không lấy từ MIA (T3) | Có, ở bước cuối: dùng lại mô tả. |
| **D. Danh sách chờ / lịch sớm hơn** | Epic Fast Pass, Doctolib | Có giá trị (khám sớm 14 ngày) nhưng chỉ 11% lời mời được nhận; người lớn tuổi nhận ít hơn [9] | Chưa thấy | Không. Ghi nhận cho sau. |
| **E. Nhắc lịch, tự đổi hoặc huỷ** | Doctolib, Tâm Anh | Doctolib và AP-HP báo no-show giảm sau khi có đặt online và nhắc lịch (số tự báo cáo, không có nhóm đối chứng) [7][8] | Chưa quan sát; Vinmec có tổng đài gọi xác nhận | Không. |
| **F. Hàng đợi, lấy số tại viện** | Medpro, Tâm Anh | Bối cảnh Việt Nam: khảo sát 53 quầy ở bệnh viện công TP.HCM (2018) thấy **khâu đăng ký** là khâu người bệnh ít hài lòng nhất [17]; ở BV 108 (2024), thời gian chờ cận lâm sàng chỉ được khoảng 61–63% hài lòng [18] | Có check-in QR | Không. Phù hợp hơn với khoảnh khắc "chờ tại viện". |
| **G. Đặt lịch qua giọng nói AI** | Zocdoc Zo | Phục vụ người không dùng app; số 70% là số Zocdoc tự công bố [6] | Tổng đài người | Gián tiếp: kênh cho người lớn tuổi. |
| **H. Bắt buộc mô tả trước, triage rồi mới cấp lịch** | NHS total triage | Truy cập rộng hơn nhưng quá tải, mất quan hệ với bác sĩ [10][11] | Không bắt buộc (đúng) | **Bài học ngược:** đừng biến AI thành cổng chặn bắt buộc. |

## 3. Bài học áp vào hướng cải tiến MyVinmec

1. **Giữ điều hướng ở dạng tuỳ chọn**, đúng như MyVinmec đang làm (bài học từ NHS total triage). Người biết khoa thì đặt
   thẳng.
2. **Dùng một danh sách luật cấp cứu chung cho mọi lối vào** (nhóm B). Đây là khoảng trống mà các app nước ngoài coi là
   phần lõi của triage. Ở MyVinmec, phần này mới chỉ nằm trong MIA.
3. **Cho gõ lời tự do rồi ánh xạ vào danh mục khoa có xét tuổi và giới**, như BV Tân Hoa. Đây chính là hướng prototype
   đang làm. Lưu ý bằng chứng ở đó: AI nhanh hơn điều dưỡng nhưng vẫn kém chính xác hơn. Vì vậy chỉ nên **gợi ý**, không
   tự đặt.
4. **Một lần mô tả, dùng cho cả đường đi** (nhóm C): mô tả ban đầu → MIA → ô "Lý do khám" → chuyển cho bác sĩ, giống
   cách Ubie chuyển câu trả lời hỏi bệnh cho bác sĩ.
5. **Thiết kế cho người lớn tuổi và người đặt hộ** (Ada, Fast Pass): giữ tổng đài; hỏi tuổi và giới *của người bệnh*,
   không phải của chủ tài khoản. MIA đã làm điểm này.

## 4. Hệ quả cho chỉ số của bài

Bằng chứng từ Trung Quốc cho thấy tỷ lệ "đặt sai khoa" có thể **rất thấp sẵn** (0,68%), nhất là khi có tổng đài gọi lại
như Vinmec. Nếu need statement chỉ đo "đổi khoa khi đến viện", rất có thể không thấy khác biệt. Đề xuất đo thêm:

- **An toàn:** 100% ca có dấu hiệu cấp cứu được cảnh báo, **ở mọi lối vào**, kèm thời gian từ lúc nhập tới lúc cảnh báo.
- **Phân vân:** tỷ lệ người còn "không chắc khoa nào" sau bước gợi ý (cách đo giống Buoy).
- **Công sức:** số lần người dùng phải mô tả lại và thời gian tới lúc đặt xong.

Phỏng vấn nên hỏi thêm: *"Lần gần nhất bạn có phân vân giữa hai khoa không? Bạn đã làm gì?"* và *"Tổng đài gọi lại có
đổi khoa giúp bạn không?"* (`interview-guide.md` bản 2 hỏi ở chặng C1 và C2). Nếu hầu hết người được hỏi đều chọn đúng khoa
mà không mất công, trọng tâm nên nghiêng hẳn về **an toàn cấp cứu và giảm phải kể lại**, không nghiêng về "chọn đúng khoa".

## Nguồn

1. BioSpectrum Asia, *Ubie launches AI-powered symptom checker in the US* (4/2022).
   https://www.biospectrumasia.com/news/50/20161/ubie-japanese-healthtech-startup-launches-ai-powered-symptom-checker-in-the-us-.html
2. THE BRIDGE, *Healthtech company Ubie… secures funding from Japan Post Capital* (3/2025).
   https://thebridge.jp/2025/03/healthtech-company-ubie-tackling-the-challenge-of-maximizing-healthy-life-expectancy-secures-funding-from-japan-post-capital
3. Xie W. et al. *The Use of Smartphone-Based Triage to Reduce the Rate of Outpatient Error Registration: Cross-Sectional
   Study.* JMIR mHealth uHealth 2019;7(11):e15313. doi:10.2196/15313. Một bệnh viện, so trước/sau, không có nhóm đối chứng.
4. Yang L. et al. *Evolution of the "Internet Plus Health Care" Mode Enabled by Artificial Intelligence: Development and Application of
   an Outpatient Triage System.* J Med Internet Res 2024;26:e51711. doi:10.2196/51711. Theo tác giả, so sánh với điều
   dưỡng bị lệch vì điều dưỡng nói chuyện trực tiếp với người bệnh.
5. Zocdoc, *Why Visit Reasons Matter*. https://www.zocdoc.com/resources/blog/article/why-visit-reasons-matter-get-discovered-in-the-right-patient-searches/
6. Zocdoc, *Zocdoc launches Zo by Zocdoc, an AI phone assistant* (5/2025).
   https://www.zocdoc.com/about/news/zocdoc-launches-zo-by-zocdoc-an-ai-phone-assistant-that-vanquishes-hold-times-and-maximizes-appointment-scheduling/
   · Fierce Healthcare: https://www.fiercehealthcare.com/health-tech/zocdoc-launches-voice-ai-tool-zo-streamline-phone-visit-bookings
7. Doctolib, *Doctolib actualise ses statistiques annuelles rendez-vous non honorés*.
   https://media.doctolib.com/image/upload/mkg/file/doctolib__actualise_ses_statistiques_annuelles_rendez_vous_non_honores.pdf
8. Le Quotidien du Médecin, *Hôpitaux de Paris : moins de lapins grâce à la prise de rendez-vous en ligne*.
   https://www.lequotidiendumedecin.fr/hopital/hopitaux-de-paris-moins-de-lapins-grace-la-prise-de-rendez-vous-en-ligne-se-felicite-lap-hp
   · Siècle Digital (2020) về danh sách motif do phòng khám đặt: https://siecledigital.fr/2020/02/29/doctolib-donnees-limite-patients-mon-docteur/
9. *An Electronic Health Record–Based Automated Self-Rescheduling Tool to Improve Patient Access: Retrospective Cohort
   Study.* J Med Internet Res 2024;26:e52071. doi:10.2196/52071.
10. *Patient experiences of an online consultation system: a qualitative study in English primary care post-COVID-19.*
    Br J Gen Pract 2024;74(744):e489. https://bjgp.org/content/74/744/e489
11. BMJ Open Quality, nghiên cứu mô hình total triage eConsult (vol. 14, số 3; mình chưa mở toàn văn). https://bmjopenquality.bmj.com/content/14/3/e002741
12. Winn A.N. et al. *Association of Use of Online Symptom Checkers With Patients' Plans for Seeking Care.* JAMA Netw Open
    2019;2(12):e1918561. doi:10.1001/jamanetworkopen.2019.18561. Đo *dự định*, không đo hành vi thật.
13. Miller S. et al. *Patients' Utilization and Perception of an AI-Based Symptom Assessment and Advice Technology in a
    British Primary Care Waiting Room: Exploratory Pilot Study.* JMIR Hum Factors 2020;7(3):e19713. Có tác giả của Ada.
14. Medpro, *Ứng dụng Medpro: đặt khám online với bác sĩ*. https://medpro.vn/tin-tuc/ung-dung-medpro-dat-kham-online-voi-bac-si
15. YouMed trên App Store. https://apps.apple.com/app/id1466077723
16. BVĐK Tâm Anh trên App Store. https://apps.apple.com/vn/app/id6451921508
17. Tuổi Trẻ, mục *Đăng ký khám bệnh* (có bài 4/5/2018 về khảo sát 53 quầy và bài 15/5/2025 *Giảm thời gian chờ khám
    bệnh, sao không đặt lịch khám trực tuyến?*). https://tuoitre.vn/dang-ky-kham-benh.html
18. *Khảo sát sự hài lòng người bệnh ngoại trú tại khu khám bệnh A, B, Bệnh viện TWQĐ 108* (2024). https://vnras.com/?p=127770
