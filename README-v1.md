# Một lần đi khám: chuẩn bị buổi khám để nói hết, hỏi đủ, kể một lần

> **Bản 1 (15/10/2026), README khi bài theo hướng H1; bản hiện hành: [README.md](README.md).**

Bài tập 1 tuần, Exploration Sprint Vinmec × AI Thực Chiến · Thái Hoài An · K3

**Khoảnh khắc đã chọn:** *Đặt lịch*, cụ thể là đoạn **từ lúc đặt hẹn xong tới lúc gặp bác sĩ**. Lý do chọn và lý do
loại các khoảnh khắc khác: [00-chon-khoanh-khac.md](00-chon-khoanh-khac.md).

**Need statement (bản giả thuyết, chờ phỏng vấn):** Cách để người bệnh, hoặc người thân đi khám cùng, đã đặt lịch khám
chuyên khoa gặp tình huống chỉ có vài phút với bác sĩ, dễ quên nói hoặc quên hỏi điều quan trọng và không chắc cần
chuẩn bị gì, có thể đến buổi khám đã chuẩn bị đúng, nói hết và hỏi đủ, mà không phải kể lại nhiều lần.

**Bài đã đổi hướng một lần.** Hướng ban đầu là gợi ý chuyên khoa. Sau khi quay video dùng thử MyVinmec, mình thấy app đã
có tính năng đó, nên chuyển sang đoạn app còn trống. Quá trình và lý do: [00-qua-trinh-chon-huong.md](00-qua-trinh-chon-huong.md).
Các hướng chưa làm được ghi trong [BACKLOG.md](BACKLOG.md).

## Mục lục

| Thư mục | Nội dung |
|---|---|
| [00-chon-khoanh-khac.md](00-chon-khoanh-khac.md) | So sánh 5 khoảnh khắc, lát cắt đã chọn, giả thuyết H1–H4 |
| [00-qua-trinh-chon-huong.md](00-qua-trinh-chon-huong.md) | Dòng thời gian research, vì sao đổi hướng, bài học |
| [00-huong-tinh-nang-moi.md](00-huong-tinh-nang-moi.md) | Luồng 9 bước đi khám, đánh giá 7 hướng tính năng |
| [BACKLOG.md](BACKLOG.md) | Các hướng để phát triển lần sau, kèm điều kiện mở lại |
| [VERSIONS.md](VERSIONS.md) | Lịch sử phiên bản: tài liệu nào đã đổi, vì sao; bản cũ giữ lại với hậu tố `-v1` |
| [01-phong-van/](01-phong-van/) | Dùng thử MyVinmec (ghi chép, [gap analysis](01-phong-van/myvinmec-gap-analysis.md), ảnh đã che thông tin cá nhân), interview guide, log phỏng vấn P1–P3, tổng hợp insight |
| [02-journey-map/](02-journey-map/journey-map.md) | Journey map đoạn đặt xong → gặp bác sĩ, đánh dấu điểm đau |
| [03-need-statement/](03-need-statement/need-statement.md) | Need statement (Biodesign) + problem statement 9 yếu tố + quyết định go/no-go |
| [04-best-practice/](04-best-practice/best-practice.md) | Ubie AI 問診, AHRQ QuestionBuilder, Epic MyChart; so sánh 12 app đặt lịch; [UMC Care và app bệnh viện Việt Nam](04-best-practice/umc-care-va-app-benh-vien-vn.md) |
| [05-prototype/](05-prototype/README.md) | Web app chạy local, prompt, bộ 24 lời kể + script đo, kịch bản thử, log thử |
| [06-rui-ro-dao-duc/](06-rui-ro-dao-duc/rui-ro-dao-duc.md) | Risk register, đường chuyển tuyến khẩn cấp, điều kiện go/no-go |
| [07-coach-plan/](07-coach-plan/coach-plan.md) | Mình sẽ coach một nhóm K4 làm bài này thế nào |
| [slides.pdf](slides.pdf) | 10 slide để present (nguồn: `slides/slides.html`, xuất bằng `slides/build.sh`) |

## Chạy prototype trong 1 phút

```bash
cd 05-prototype/app && python3 server.py      # mở http://localhost:8000, không cần cài gì thêm
python3 ../eval/run_eval_prep.py               # đo trên 24 lời kể giả lập
```

## Phần nào do AI tạo

Mình dùng Claude (Anthropic) làm trợ lý trong bài này. Phân chia cụ thể:

| Phần | AI làm | Mình làm |
|---|---|---|
| 00 Chọn khoảnh khắc, chọn hướng | Soạn bảng so sánh, desk research 12 app, đánh giá 7 hướng, báo cáo quá trình | Chọn khoảnh khắc; quay video dùng thử app; yêu cầu đổi sang tính năng mới theo luồng người bệnh; chốt H1 |
| 01 Phỏng vấn | Soạn nháp interview guide và các mẫu ghi chép | Dùng thử MyVinmec, **phỏng vấn thật, viết log, tổng hợp insight** |
| 02 Journey map | Bản giả thuyết ban đầu | Cập nhật theo phỏng vấn |
| 03 Need statement | Bản nháp giả thuyết | Viết lại theo bằng chứng |
| 04 Best practice | Tìm nguồn, tóm tắt, đối chiếu số liệu với tóm tắt gốc trên PubMed/Europe PMC | Kiểm tra lại nguồn, rút bài học |
| 05 Prototype | Viết code, prompt, bộ lời kể giả lập (kỳ vọng do AI đặt, chưa được bác sĩ duyệt) | Quyết định thiết kế, **thử với người thật, ghi log, sửa** |
| 06, 07 | Soạn nháp | Duyệt, chỉnh theo kinh nghiệm Lab Coach |
| Slides | Dựng khung | Điền kết quả thật |

Mọi trích dẫn, số liệu phỏng vấn và log thử nghiệm đến từ buổi làm việc thật với người tham gia, không do AI tạo.

## Ràng buộc đã tuân thủ

Xin đồng ý trước phỏng vấn · chỉ hỏi về trải nghiệm dịch vụ, không hỏi bệnh · ẩn danh P1, P2, P3 · không ghi âm khi
chưa được đồng ý · không chụp ảnh người hay giấy tờ y tế · không đưa lời khuyên y khoa · không dùng dữ liệu người bệnh
thật (prototype dùng dữ liệu giả lập; người thử đóng vai theo thẻ kịch bản).
