# Best practice của hướng ban đầu: điều hướng chọn khoa (backlog B1)

> Đây là bộ best practice cho hướng ban đầu (gợi ý chuyên khoa). Hướng chính hiện tại là **Chuẩn bị buổi khám**, xem
> [best-practice.md](best-practice.md). Phần an toàn ở đây (luật cấp cứu, đo bằng vignette) vẫn áp dụng cho hướng mới.

Tiêu chí chọn: mỗi ví dụ giải đúng bài toán "người dùng chưa biết cần loại chăm sóc nào" và có nguồn đọc được.
Mình chỉ ghi điều nguồn nói; phần "bài học" là suy luận của mình.


## 1. Zocdoc (Mỹ): đặt lịch theo "lý do khám", có tìm kiếm có hướng dẫn

**Điều nguồn nói**
- Mỗi lịch hẹn gắn với một **visit reason** (lý do khám). Visit reason quyết định thời lượng cuộc hẹn và cách tính
  lịch trống, và bắt buộc phải có khi lấy lịch trống [1].
- Zocdoc thừa nhận "nhiều bệnh nhân cần giúp để diễn đạt nhu cầu thành thuật ngữ y khoa", và đã ra mắt **guided
  search** để giúp họ chuyển điều mình tìm thành visit reason cụ thể [2].

**Bài học cho Vinmec**
- Lõi của việc đặt đúng là một **danh mục lý do khám do bệnh viện sở hữu**. AI chỉ nên làm nhiệm vụ dịch lời người
  dùng vào danh mục đó, không tự sinh ra khoa hay dịch vụ mới. Prototype của mình áp dụng đúng nguyên tắc này: LLM chỉ
  được chọn trong danh sách mã khoa, mọi mã ngoài danh sách bị loại.
- Lý do khám cũng giúp vận hành (thời lượng slot, chuẩn bị trước). Đây là giá trị cho bệnh viện, không chỉ cho người bệnh.

## 2. NHS 111 online (Anh): điều hướng tới đúng dịch vụ, và bằng chứng nói gì

**Điều nguồn nói** (tổng quan hệ thống của Chambers và cộng sự, 2019 [3], [4])
- Bằng chứng tổng thể còn yếu, phần lớn là nghiên cứu quan sát và tài liệu chưa bình duyệt.
- Độ chính xác chẩn đoán của các symptom checker biến thiên mạnh và **nói chung thấp**. Triage theo thuật toán có xu
  hướng **thận trọng hơn** (risk averse) so với nhân viên y tế.
- **Người trẻ và học vấn cao dùng nhiều hơn**. Mức hài lòng cao nhưng đo trong nghiên cứu không có nhóm đối chứng.

**Bài học cho Vinmec**
- Không bán giải pháp như "AI chẩn đoán". Chỉ nhận vai **điều hướng**, chấp nhận thận trọng hơn (thà báo cấp cứu nhầm
  còn hơn bỏ sót) và nói rõ điều đó với người dùng. Prototype hiện báo nhầm 1/22 ca thường, đây là cái giá đã chọn.
- **Công bằng tiếp cận**: người lớn tuổi, ít dùng app là nhóm dễ bị bỏ lại. Vì vậy phải giữ kênh tổng đài và cho phép
  đặt hộ người thân, và trong phỏng vấn cố ý hỏi một người lớn tuổi.
- Hài lòng không chứng minh hiệu quả: phải đo kết quả thật (tỷ lệ chuyển khoa, tỷ lệ đặt xong), không chỉ đo rating.

## 3. Ada Health (Đức): đánh giá bằng bộ ca mẫu trước khi tin vào AI

**Điều nguồn nói** (Gilbert và cộng sự, BMJ Open 2020 [5])
- So sánh 8 app đánh giá triệu chứng với 7 bác sĩ đa khoa trên **200 ca mẫu (vignette)**.
- Độ chính xác top-3 của bác sĩ trung bình **82,1%**; app tốt nhất (Ada) đạt **70,5%**.
- Tỷ lệ lời khuyên mức khẩn cấp an toàn: bác sĩ **97,0%**; chỉ Ada (97,0%), Babylon (95,1%) và Symptomate (97,8%) ở
  gần mức này.
- Lưu ý xung đột lợi ích: nghiên cứu do Ada dẫn dắt, có tác giả là nhân viên Ada.

**Bài học cho Vinmec**
- **Đo an toàn và đo độ chính xác như hai chỉ số riêng.** Ngay cả app tốt nhất vẫn kém bác sĩ về độ chính xác, nhưng có
  thể ngang bác sĩ về an toàn. Với bài toán chọn khoa, chỉ số phải đạt 100% là "không bỏ sót cấp cứu".
- Trước khi cho người thật dùng, cần **bộ vignette có nhãn do bác sĩ duyệt**. Prototype của mình đã có bộ 32 vignette
  và script đo (`05-prototype/eval/`), nhưng nhãn do AI soạn. Bước đầu tiên khi có bác sĩ đồng hành là nhờ bác sĩ duyệt bộ này.
- Đọc nghiên cứu của nhà cung cấp phải để ý ai tài trợ.

## Tổng hợp: áp dụng vào bối cảnh Việt Nam / Vinmec

| Nguyên tắc | Từ | Đã áp dụng trong prototype |
|---|---|---|
| AI dịch vào danh mục do bệnh viện sở hữu | Zocdoc | ✅ chỉ chọn trong danh sách mã khoa |
| Điều hướng, không chẩn đoán; thận trọng có chủ đích | NHS 111 | ✅ luật cấp cứu chạy trước AI; câu chẩn đoán/thuốc bị chặn |
| Giữ kênh cho người không dùng app | NHS 111 | ✅ nút gọi tổng đài, tự chọn khoa, đặt cho người thân |
| Đánh giá bằng vignette, tách an toàn và độ đúng | Ada | ✅ `run_eval.py` (nhãn chưa được bác sĩ duyệt) |

## Nguồn

1. Zocdoc API Docs, *Glossary* (Visit Reason, Default Visit Reason). https://api-docs.zocdoc.com/guides/glossary
2. Zocdoc, *Why Visit Reasons Matter: Get Discovered in the Right Patient Searches*.
   https://www.zocdoc.com/resources/blog/article/why-visit-reasons-matter-get-discovered-in-the-right-patient-searches/
3. Chambers D. et al. *Digital and online symptom checkers and health assessment/triage services for urgent health
   problems: systematic review.* BMJ Open 2019;9:e027743. doi:10.1136/bmjopen-2018-027743.
   https://eprints.whiterose.ac.uk/138885/
4. NIHR Evidence. *Impact of online or app-based assessment for urgent health problems largely unclear.*
   https://evidence.nihr.ac.uk/alert/impact-of-online-or-app-based-assessment-for-urgent-health-problems-largely-unclear
5. Gilbert S. et al. *How accurate are digital symptom assessment apps for suggesting conditions and urgency advice? A
   clinical vignettes comparison to GPs.* BMJ Open 2020;10(12):e040269. doi:10.1136/bmjopen-2020-040269.
   https://pubmed.ncbi.nlm.nih.gov/33328258/
