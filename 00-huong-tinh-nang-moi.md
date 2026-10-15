# Các hướng tính năng mới dọc hành trình đi khám (bản nháp để chọn hướng)

Soạn ngày 15/10/2026, sau khi xem 2 video dùng thử MyVinmec và làm desk research. **Đây là đề xuất của AI, chưa
được phỏng vấn kiểm chứng.** Thái chọn hướng; phỏng vấn có thể bác bỏ hướng đã chọn.

## 0. Đề bài yêu cầu gì

- Đề yêu cầu *"thiết kế lại trải nghiệm người bệnh với AI trên MyVinmec"*, nhưng phải **chọn MỘT khoảnh khắc** trong số:
  đặt lịch, check-in, chờ, nhận kết quả, tái khám ("chọn hẹp để làm sâu"). Vì vậy, dù là tính năng mới, bài vẫn phải
  neo vào một khoảnh khắc.
- Tiêu chí: điểm đau có bằng chứng phỏng vấn; need statement không chứa giải pháp; prototype có AI thử được với người
  thật; không hỏi bệnh và không đưa lời khuyên y khoa.
- Sprint thật diễn ra **trong khoa, cạnh bác sĩ và điều dưỡng**. Một tính năng giúp được cả người bệnh lẫn bác sĩ sẽ
  dễ được chọn đi tiếp hơn.

## 1. Luồng nghiệp vụ thật từ góc nhìn người bệnh, và MyVinmec đang có gì

Nguồn: 2 video dùng thử (V1, V2), form web vinmec.com/dat-kham và màn hình chính của app (V1 2:16–2:21).

| # | Bước | Người bệnh làm gì | MyVinmec hiện có | Khoảng trống |
|---|---|---|---|---|
| 1 | Quyết định đi khám, chọn nơi và khoa | Hỏi người quen, tra mạng | Đặt theo triệu chứng, MIA, Cộng đồng hỏi đáp bác sĩ | Đã phân tích ở T1–T10 |
| 2 | Gửi yêu cầu đặt hẹn | Chọn cơ sở, khoa, **ngày mong muốn** (không chọn giờ), gõ lý do ≤ 120 ký tự | Form đặt hẹn | Lý do khám chỉ là một ô gõ ngắn |
| 3 | Chờ xác nhận | Tổng đài gọi lại để chốt giờ | "Đặt lịch nhanh – xác nhận lịch tự động" (chưa thử) | Chưa rõ thời gian chờ |
| 4 | **Từ lúc xác nhận tới ngày khám** | Tự lo: nhịn ăn chưa, mang gì, hỏi bác sĩ gì | Mục Lịch hẹn; hướng dẫn chuẩn bị nằm trên **web**, dạng bài viết chung | **Chưa thấy gì cá nhân hoá theo lịch hẹn** |
| 5 | Check-in | Quét QR hoặc ra quầy | Check-in QR, Tạm ứng viện phí | — |
| 6 | Chờ, làm cận lâm sàng | Đi giữa các phòng | Chưa quan sát | Cần dữ liệu hàng đợi thật |
| 7 | **Gặp bác sĩ** | Kể bệnh trong vài phút, nghe dặn | — | Quên kể, quên hỏi, quên lời dặn |
| 8 | Nhận kết quả, đơn thuốc | Đọc kết quả, mua thuốc | Đơn thuốc, kết quả (cần mã y tế) | Gần lời khuyên y khoa |
| 9 | Sau khám, tái khám | Uống thuốc, theo dõi, quay lại | Nhắc lịch uống thuốc, Sổ tiêm | Lời dặn ngoài đơn thuốc không được lưu |

**Nhận xét:** MyVinmec dày tính năng ở bước 1–2 và 8–9. Bước 4 → 7 (chuẩn bị và gặp bác sĩ) gần như trống, mà đây lại
là nơi có bằng chứng nghiên cứu mạnh nhất về điểm đau (mục 3).

## 2. Bảy hướng và đánh giá

Thang điểm: ✅ tốt, ⚠️ được nhưng có điều kiện, ❌ khó trong 1 tuần.

| Hướng | Khoảnh khắc | Tính năng | AI làm gì | Có bằng chứng nhu cầu? | App đã có? | Phỏng vấn không chạm bệnh | Prototype với dữ liệu giả lập + thử người thật | An toàn |
|---|---|---|---|---|---|---|---|---|
| **H1. Chuẩn bị buổi khám** | Đặt lịch → trước ngày khám | Sau khi đặt: (a) kể vấn đề bằng lời thường → **phiếu tóm tắt** cho bác sĩ; (b) **danh sách câu hỏi muốn hỏi bác sĩ**; (c) **checklist chuẩn bị** theo dịch vụ (nhịn ăn, giấy tờ, thuốc đang dùng) | Hiểu lời thường → điền phiếu có cấu trúc; gợi ý câu hỏi *chung*; trả lời "cần chuẩn bị gì" chỉ từ tài liệu Vinmec | ✅ mạnh (mục 3) | ❌ chưa thấy | ✅ "Lần trước bạn có quên hỏi gì, quên mang gì không?" | ✅ người thử đóng vai theo thẻ | ✅ không chẩn đoán; dùng lại luật cấp cứu đã có |
| H2. Hiểu lời dặn sau khám | Tái khám / sau khám | Bản tóm tắt dễ hiểu sau khám: làm gì, uống gì, khi nào quay lại, dấu hiệu cần đi viện ngay | Viết lại ghi chú bác sĩ bằng lời thường | ✅ mạnh: 40–80% thông tin bị quên [5] | ⚠️ có Đơn thuốc, Nhắc thuốc | ⚠️ hỏi về "nhớ lời dặn" dễ trượt sang bệnh | ⚠️ cần ghi chú bác sĩ giả lập | ⚠️ LLM viết lại có thể sót hoặc sai: 18/100 lượt duyệt có lo ngại an toàn [6] → **bác sĩ phải duyệt** |
| H3. Đặt hộ bố mẹ bằng giọng nói | Đặt lịch | Gọi hoặc nói chuyện tự nhiên để đặt, AI điền form, người thân xác nhận | Hiểu giọng nói → điền form | ⚠️ người lớn tuổi được lợi ít hơn từ app [best practice] | ❌ (có tổng đài người) | ✅ | ⚠️ cần làm voice; khó thử trong 1 tuần | ✅ |
| H4. Chọn gói khám sức khoẻ | Đặt lịch | Hỏi tuổi, giới, mục đích → so sánh gói | Gợi ý gói | ⚠️ Vinmec có nhiều nhóm gói, chính Vinmec khuyên "nên tham khảo nhân viên y tế" [7] | ⚠️ có Danh mục giá | ✅ | ✅ | ❌ **xung đột lợi ích**: AI bán hàng (giống T9: sàng lọc dẫn tới trang bán IVF) |
| H5. Ước tính chi phí và bảo hiểm trước khám | Đặt lịch | "Lần khám này khoảng bao nhiêu, bảo hiểm trả bao nhiêu" | Đọc điều khoản bảo hiểm | ⚠️ chưa có bằng chứng | ⚠️ Danh mục giá, Tạm ứng | ✅ | ❌ cần bảng giá và hợp đồng bảo hiểm thật | ⚠️ sai tiền = mất niềm tin |
| H6. Trợ lý trong ngày khám | Chờ | Bước tiếp theo ở đâu, còn bao lâu | Trả lời theo trạng thái | ✅ (VN: khâu đăng ký và chờ ít hài lòng nhất) | ⚠️ | ✅ | ❌ cần dữ liệu hàng đợi thật | ✅ |
| H7. Lấy chỗ sớm hơn (giống Fast Pass) | Đặt lịch | Có người huỷ thì báo để lấy chỗ | Gần như không cần AI | ⚠️ 11% lời mời được nhận | ❌ | ✅ | ✅ | ✅ nhưng **là rule, không có AI** |

## 3. Vì sao khuyên chọn H1: Chuẩn bị buổi khám

**Bằng chứng về điểm đau (đã đối chiếu tóm tắt gốc trên PubMed/Europe PMC):**

- **Người bệnh không nói hết điều mình lo.** Trong 35 lượt khám, chỉ **4/35** người nói ra đủ các điều họ định nói. Ở cả
  **14/14** ca có hậu quả xấu (hiểu lầm lớn, đơn thuốc không dùng, không tuân thủ), ít nhất một vấn đề liên quan tới điều
  người bệnh không nói ra [1].
- **Bác sĩ ít khi hỏi người bệnh muốn nói gì, và hay ngắt lời.** Chỉ **36%** (40/112) lượt khám bác sĩ hỏi người bệnh
  muốn bàn gì; ở khám chuyên khoa chỉ **20%**. Khi có hỏi, 67% lượt bị ngắt lời sau trung vị **11 giây** [2].
- **Danh sách câu hỏi chuẩn bị trước giúp người bệnh hỏi nhiều hơn**, nhất là khi đưa ngay trước buổi khám và được bác sĩ
  đồng thuận. Tổng quan 42 nghiên cứu cho thấy vậy, nhưng chưa thấy nhất quán về giảm lo âu hay thời gian khám [3].
- **Hỏi bệnh trước khám đã thành sản phẩm:** Ubie AI 問診 có ở hơn 1.800 cơ sở tại Nhật [best practice].
- **Cảnh báo về tỷ lệ dùng:** phiếu hỏi trước khám qua Epic ở người từ 65 tuổi chỉ có **26,4%** điền; người điền trẻ hơn,
  và người bệnh nặng nhất không điền. Trong số người trả lời khảo sát, 68,7% thấy phiếu giúp được [4]. Vì vậy, phiếu
  phải ngắn, đặt hộ được, và **không bắt buộc**.

**Vì sao khả thi hơn các hướng khác trong 4 ngày còn lại:**

1. **Không đụng lời khuyên y khoa:** AI chỉ *ghi lại* lời người bệnh và gợi ý *câu hỏi*, không trả lời câu hỏi y khoa.
   Hướng dẫn chuẩn bị chỉ lấy từ tài liệu Vinmec đã công bố (ví dụ trang "Những lưu ý trước khi khám sức khỏe tổng
   quát": không ăn sáng, uống nhiều nước và nhịn tiểu trước siêu âm bụng…) [8].
2. **Phỏng vấn dễ, đúng ràng buộc 6.4:** hỏi về trải nghiệm dịch vụ ("lần gần nhất ra khỏi phòng khám bạn có quên hỏi gì
   không? có phải quay lại vì chưa nhịn ăn hay thiếu giấy tờ không?"), không hỏi bệnh gì.
3. **Dùng lại được prototype hiện có:** luật cấp cứu (`triage.py`) vẫn chạy trước khi người bệnh kể; server, giao diện,
   log và eval giữ nguyên khung. Phần mới: màn "Chuẩn bị buổi khám", prompt tóm tắt thành phiếu, danh sách câu hỏi,
   checklist theo dịch vụ.
4. **Nối được với những gì đã thấy ở MyVinmec:** giải quyết T3 (kể đi kể lại 3 lần) bằng cách *kể một lần, dùng cho cả
   bác sĩ*. Ô "Lý do khám ≤ 120 ký tự" được thay bằng phiếu tóm tắt.
5. **Có giá trị cho cả hai phía:** người bệnh không quên điều cần nói và cần hỏi; bác sĩ đọc phiếu 5 dòng trước khi gọi
   tên. Đây là chuyện sprint thật có thể đo trong khoa.

**Phác thảo luồng H1:**

```
Đặt hẹn thành công → thông báo "Chuẩn bị cho buổi khám ngày 18/10 (2 phút)"
  1. Kể bằng lời thường (gõ hoặc nói): "Bạn muốn bác sĩ giúp gì lần này?"
       └─ luật cấp cứu chạy trước → có dấu hiệu nguy hiểm: dừng, hiện nút gọi 115
  2. AI điền phiếu: lý do chính · từ khi nào · đã khám hoặc dùng thuốc gì · điều lo nhất · điều muốn bác sĩ làm
       └─ người bệnh xem và sửa từng dòng (AI không thêm điều người bệnh không nói)
  3. "Bạn có muốn hỏi bác sĩ những điều này không?" (gợi ý câu hỏi chung, người bệnh chọn hoặc tự thêm)
  4. Checklist theo dịch vụ đã đặt: nhịn ăn? mang gì? (chỉ từ tài liệu Vinmec, có link nguồn)
  → Bác sĩ nhận phiếu trước giờ khám; người bệnh mở lại checklist và danh sách câu hỏi trong phòng khám
```

**Chỉ số đề xuất (đo trong lần thử với người thật):** tỷ lệ điền xong phiếu; thời gian điền; người thử có sửa phiếu
không và sửa gì (phát hiện AI ghi sai); số câu hỏi người thử muốn mang vào phòng khám; với vai bác sĩ (nếu nhờ được một
người làm y tế đọc): phiếu có giúp hiểu nhanh hơn không. **An toàn:** 100% thẻ kịch bản cấp cứu bị chặn.

**Rủi ro chính và cách giảm:** AI tóm tắt sai hoặc thêm thông tin → người bệnh xác nhận từng dòng, giữ nguyên văn bên
cạnh; người lớn tuổi không điền → không bắt buộc, cho người thân điền hộ, tổng đài vẫn hỏi như cũ; người bệnh hỏi câu y
khoa trong ô kể → không trả lời, ghi vào "câu hỏi cho bác sĩ".

## 4. Hướng dự phòng: H2 (Hiểu lời dặn sau khám)

Bằng chứng nhu cầu mạnh nhất (người bệnh quên 40–80% thông tin ngay sau khám [5]). Tuy vậy, H2 cần ghi chú của bác sĩ
làm đầu vào, gần lời khuyên y khoa, và bản viết lại bằng LLM phải được bác sĩ duyệt [6]. Hướng này hợp với sprint 6
tuần có bác sĩ đồng hành hơn là bài 1 tuần. Nên nêu H2 như **bước tiếp theo** ở slide cuối.

## 5. Nếu chọn H1, repo phải đổi gì

| Phần | Việc | Ước lượng |
|---|---|---|
| 00, README | Khoảnh khắc: "Đặt lịch, từ lúc đặt xong tới lúc gặp bác sĩ"; giải thích vì sao đổi (bằng chứng từ dùng thử app) | 1h |
| 01 Phỏng vấn | Sửa interview guide: hỏi về chuẩn bị, quên hỏi, quên mang, kể lại nhiều lần. **Chưa phỏng vấn ai, nên đổi lúc này không mất gì** | 30' |
| 02, 03 | Journey map bước 2→7; need statement mới | 1–2h sau phỏng vấn |
| 04 | Giữ 3 best practice; thêm Ubie AI 問診, tổng quan về danh sách câu hỏi | 30' |
| 05 Prototype | Thêm màn Chuẩn bị buổi khám + prompt phiếu tóm tắt + checklist; giữ luật cấp cứu; viết vignette mới | 1 ngày |
| 06, 07, slides | Cập nhật rủi ro (tóm tắt sai, quyền riêng tư của phiếu) | 1–2h |

Hạn nộp còn 4 ngày (hết 19/10). Phỏng vấn ≥ 3 người vẫn là việc chặn mọi bước sau.

## Nguồn

1. Barry C.A. et al. *Patients' unvoiced agendas in general practice consultations: qualitative study.* BMJ
   2000;320:1246. doi:10.1136/bmj.320.7244.1246
2. Singh Ospina N. et al. *Eliciting the Patient's Agenda: Secondary Analysis of Recorded Clinical Encounters.* J Gen
   Intern Med 2019;34(1):36–40. doi:10.1007/s11606-018-4540-5
3. Sansoni J.E., Grootemaat P., Duncan C. *Question Prompt Lists in health consultations: A review.* Patient Educ Couns
   2015;98:1454–64. doi:10.1016/j.pec.2015.05.015
4. Naimark J. et al. *Leveraging an EHR Patient Portal to Help Patients Formulate Their Health Care Goals.* JMIR Form Res
   2024;8:e56332. doi:10.2196/56332
5. Kessels R.P. *Patients' memory for medical information.* J R Soc Med 2003;96(5):219–22. doi:10.1258/jrsm.96.5.219
   (con số 40–80% là tổng hợp từ các nghiên cứu trước).
6. Zaretsky J. et al. *Generative AI to Transform Inpatient Discharge Summaries to Patient-Friendly Language and Format.*
   JAMA Netw Open 2024;7(3):e240357. Tóm tắt kết luận "cần bác sĩ duyệt"; con số 18/100 lấy từ bản tóm tắt thứ cấp, cần
   đối chiếu toàn văn trước khi đưa lên slide.
7. Vinmec, *Khám sức khỏe tổng quát Vinmec 2026*. https://www.vinmec.com/vie/bai-viet/kham-suc-khoe-tong-quat-vinmec-2026-chu-dong-bao-ve-suc-khoe-tu-hom-nay
8. Vinmec, *Những lưu ý quan trọng trước khi khám sức khỏe tổng quát*.
   https://www.vinmec.com/vie/bai-viet/nhung-dieu-can-luu-y-truoc-khi-kham-suc-khoe-tong-quat-vi
- [best practice]: `04-best-practice/app-dat-lich-trong-ngoai-nuoc.md` (Ubie, Ada, Fast Pass).
