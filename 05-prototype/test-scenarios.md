# Kịch bản thử prototype "Lộ trình khám trong ngày" (bản 3, 18/10/2026, sửa theo review)

> Bản 2 trước review: [test-scenarios-v2.md](test-scenarios-v2.md).
> **Tour `?tour=1` là demo do người làm bài bấm, không phải buổi thử.** Chỉ lượt người thử tự cầm máy mới được ghi vào test-log.

> Bản 1 (hướng H1 "Chuẩn bị buổi khám"): [test-scenarios-v1.md](test-scenarios-v1.md).

Người thử **đóng vai** theo thẻ, không dùng tình trạng sức khoẻ thật (ràng buộc 6.4 của đề). Mỗi người 3 thẻ, khoảng 15
phút. Người điều phối (Thái) **chỉ quan sát, không chỉ dẫn**; khi người thử hỏi "giờ đi đâu", trả lời "bạn thử tìm trong
app xem" và **đếm số lần họ hỏi mình**: đây là chỉ số chính.

## Chuẩn bị

1. Chạy `python3 app/server.py` (nên dùng chế độ LLM nếu đã có key), mở trên máy của mình ở cửa sổ hẹp hoặc chia sẻ màn
   hình cho người thử điều khiển. Server chỉ nghe ở máy local nên điện thoại người thử không vào được.
2. Xoá log thử cũ nếu cần, nhập **Mã người thử** (T1, T2, T3) ở màn "Hôm nay bạn đến viện".
3. Đọc lời mở đầu: "Đây là bản thử, không phải app thật của bệnh viện. Bạn đang đứng ở sảnh một bệnh viện bạn chưa
   đến bao giờ. Mình đang thử cái app, không thử bạn. Bạn cứ nói to điều bạn nghĩ khi bấm."
4. Đưa thẻ cho người thử đọc rồi cất đi.

## Thẻ kịch bản

| Thẻ | Tình huống trên thẻ | Người thử cần làm | Quan sát điều gì |
|---|---|---|---|
| K1 | "Bạn đến khám lần đầu, **không đặt lịch**, có thẻ BHYT. Bạn vừa bước vào sảnh." | Tìm xem phải vào quầy nào, mang gì | Có tìm ra quầy BHYT mà không hỏi mình không? Có đọc dòng "Vì sao" không? |
| K2 | "Bác sĩ vừa chỉ định **xét nghiệm máu, siêu âm bụng, xét nghiệm nước tiểu**. Bạn chưa ăn sáng và đang đói." | Nhập chỉ định (ô mô phỏng), đi theo lộ trình, hỏi xem khi nào được ăn | Có hiểu vì sao nước tiểu để sau siêu âm không? Hỏi chuyện ăn bằng cách nào (gõ hay bấm gợi ý)? |
| K3 | **Chỉ làm với người thật sự từng đưa bố mẹ lớn tuổi đi khám** (không đóng vai). Hỏi trước: "Lần gần nhất đưa bố/mẹ đi, ở đâu bạn phải hỏi đường hay hỏi nhân viên?" rồi để họ hỏi trợ lý **câu hỏi họ đã thật sự hỏi hôm đó** | Gõ câu hỏi thật của mình | Trợ lý hiểu câu nói tự nhiên không? Câu trả lời có thay được việc phải hỏi nhân viên không? |
| K4 | "Có kết quả máu, bạn thấy đường huyết 7,2 và muốn biết **có cao không**." | Hỏi trợ lý | Có hiểu vì sao trợ lý không trả lời không? Có thấy câu hỏi được lưu để hỏi bác sĩ không? Có bực không? |
| K6 | "Bạn muốn **khám sức khoẻ tổng quát** sáng mai. Bạn đặt lịch trên app rồi muốn biết tối nay và sáng mai phải làm gì." | Đặt lịch (tab Đặt lịch), mở Lịch hẹn, xem lộ trình | Có tìm ra nút "Xem lộ trình hôm khám" không? Có đọc phần chuẩn bị (nhịn ăn, nhịn tiểu) không? Thấy giờ check-in có hợp lý không? |
| K5 | "Đang ngồi chờ kết quả, **bố bạn tự nhiên méo miệng, nói khó**." | Dùng app | Có thấy ngay chỉ đường khoa Cấp cứu, gọi 115 không? Mất bao lâu? |

Mỗi người làm K1, K2 và một trong K3, K4. Người thứ ba làm thêm K5. Ít nhất một người làm K6 (luồng đã đặt lịch). Ít nhất một người từng khám ở **viện tư**, để kiểm tra
điểm đau "bỡ ngỡ quầy" có còn đúng ở bối cảnh giống Vinmec không.

## Một phiên chỉ kiểm một giả thuyết

Review chỉ ra prototype ôm nhiều thứ (quầy đầu tiên, thứ tự chỉ định, nhịn ăn, giờ chờ, đặt lịch, câu y khoa, cấp cứu)
nên một phiên không biết phản ứng đến từ đâu. Mỗi phiên thử chỉ đo **một** câu hỏi học được:

| Phiên | Câu hỏi học được | Thẻ | Chỉ số |
|---|---|---|---|
| A | Người đến lần đầu có tìm đúng quầy đầu tiên **mà không phải hỏi người khác** không? | K1 | Số lần hỏi người điều phối; có đọc dòng "Vì sao" không |
| B | Thứ tự chỉ định có giúp đi ít vòng hơn không? | K2 | Số lần hỏi; số lần quay lại màn trước |
| C | Người bệnh có gõ câu hỏi bằng lời của mình không (nếu chỉ bấm gợi ý thì không cần AI)? | K3 | Số câu tự gõ / tổng số câu; số câu trợ lý "chưa hiểu" |

K4, K5 (câu y khoa, cấp cứu) là kiểm tra an toàn, làm sau cùng, không tính vào chỉ số sản phẩm.

## Ghi lại khi quan sát

- Số lần người thử **hỏi người điều phối** (mục tiêu: 0).
- Số lần bấm "Chỉ đường", số câu hỏi trợ lý, số câu tự gõ so với bấm gợi ý.
- Chỗ người thử dừng lại, đọc lại, hoặc nói "hả?". Câu nói nguyên văn.

## Câu hỏi sau khi thử (3 phút)

1. Lần gần nhất bạn đi khám, bạn đã phải hỏi người khác (bảo vệ, nhân viên, người bệnh khác) ở những bước nào? Hỏi mấy lần? (hỏi về việc đã xảy ra; **không** hỏi "nếu có app này bạn có dùng không")
2. Có bước nào app chỉ mà bạn **không tin** không? Vì sao?
3. Thời gian dự kiến có giúp không, hay làm bạn lo hơn nếu sai?
4. Trợ lý từ chối câu hỏi về kết quả: bạn thấy hợp lý hay khó chịu?
5. Ở viện bạn hay khám, nhân viên hay biển báo đã đủ chưa? App thêm được gì?
6. Bạn muốn sửa điều gì đầu tiên?
