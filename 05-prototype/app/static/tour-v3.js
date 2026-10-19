// Bản 3 lưu lại (18/10/2026): chưa có nút "Thoát tour, tự dùng thử" ở mọi bước và nút quay lại tour. Không trang nào nạp file này; bản hiện hành là tour.js.
// Bản 3 (18/10/2026): tour cho hội đồng. Màn điện thoại giữ đúng giao diện người dùng (chỉ một viền sáng nhẹ); hai bên
// màn hình là "Nghiên cứu & bằng chứng" (trái) và "Vì sao làm vậy" (phải), có nút Trước/Tiếp. Màn hẹp (< 1080px) thì
// dùng thẻ ghi chú trong khung như bản 2 (tour-v2.js).
// Dùng các hàm của index.html (state, go, startRoute, markDone, applyOrders, openSheet, send, bookAppt, routeFromAppt...).
// Mở bằng nút "Tour cho người chấm" ở Trang chủ hoặc ?tour=1. Lượt tour ghi log với mã người thử "TOUR" để tách khỏi
// lượt thử thật (summarize_log.py bỏ qua mã này).

(() => {
  let fast = false;  // khi bấm "Trước": chạy lại nhanh từ đầu tới bước cần xem
  const wait = ms => new Promise(r => setTimeout(r, fast ? 0 : ms));
  const $ = sel => document.querySelector(sel);
  const pick = (key, v) => document.querySelector(`.choice[data-key="${key}"] button[data-v="${v}"]`).click();
  async function advanceTo(id) {
    for (let i = 0; i < 20 && currentStep() && currentStep().id !== id; i++) { markDone(); await wait(60); }
  }
  async function ask(q) { if (!$("#sheet").classList.contains("open")) openSheet(); await send(q, "tour"); await wait(250); }
  const lastMsg = () => [...document.querySelectorAll("#msgs .msg")].pop();
  // Chỉ cuộn bên trong màn điện thoại (không cuộn cả cửa sổ, nếu không điện thoại sẽ lệch so với hai bảng cố định)
  function reveal(el, block = "nearest") {
    const sc = document.getElementById("scroll");
    if (!el || !sc.contains(el)) return;
    const r = el.getBoundingClientRect(), b = sc.getBoundingClientRect();
    if (block === "start") sc.scrollTop += r.top - b.top - 8;
    else if (block === "center") sc.scrollTop += (r.top + r.bottom) / 2 - (b.top + b.bottom) / 2;
    else if (r.top < b.top) sc.scrollTop += r.top - b.top - 8;
    else if (r.bottom > b.bottom) sc.scrollTop += Math.min(r.bottom - b.bottom + 8, r.top - b.top - 8);
  }
  // Một mục bằng chứng: loại nguồn, nội dung, nơi đọc thêm trong repo
  const R = (tag, text, src) => ({ tag, text, src });

  // Mỗi bước: target, before (thao tác tự động), title, body (tính năng), research (bằng chứng), why (vì sao),
  // look (hội đồng nên để ý), limit (giới hạn, nếu có).
  const STEPS = [
    { title: "Lộ trình khám trong ngày",
      body: `Một mục mới trong MyVinmec (giao diện mô phỏng) luôn trả lời được câu <i>"Bây giờ tôi đi đâu tiếp, và còn chờ bao lâu?"</i>. Tour đi hai luồng: <b>người đến thẳng</b> (bước 1–11) và <b>người đã đặt lịch</b> (bước 12–15).`,
      research: [
        R("Đổi hướng 1 · 15/10", "Dùng thử MyVinmec (2 video, 18 ảnh): app đã có đặt lịch theo triệu chứng và trợ lý MIA, nên bỏ hướng \"gợi ý chuyên khoa\".", "00-qua-trinh-chon-huong.md"),
        R("Đổi hướng 2 · 18/10", "Phỏng vấn: người bệnh đến thẳng viện; phiếu tại viện là trắc nghiệm, không gây khó; điều họ than là bỡ ngỡ không biết vào quầy nào. Bỏ hướng \"Chuẩn bị buổi khám\".", "VERSIONS.md"),
        R("Desk research", "UMC Care (bác sĩ được phỏng vấn giới thiệu) và MyVinmec đã làm tốt đặt lịch, thanh toán, xem kết quả. Ý kiến người dùng trên Threads (Thái tổng hợp) cũng cho rằng app đặt lịch hiện đã tiện.", "04-best-practice/umc-care-va-app-benh-vien-vn.md"),
      ],
      why: "Khoảng trống còn lại nằm <b>trong ngày khám</b>: app bệnh viện biết phiếu khám, chỉ định, phòng của từng người nhưng chỉ đưa hướng dẫn chung.",
      look: "Bài đổi hướng hai lần, mỗi lần do một bằng chứng cụ thể. Mọi bản cũ được giữ lại để đối chiếu.",
      limit: "Bệnh viện, phòng, thời gian chờ trong prototype đều là giả lập." },
    { target: () => $(".banner-ad"), before: async () => { go("s-home"); },
      title: "1 · Điểm vào nằm trong app quen thuộc",
      body: "Người bệnh đang đứng ở sảnh viện mở mục \"Lộ trình hôm nay\" ngay trên Trang chủ.",
      research: [
        R("Báo chí", "Tuổi Trẻ (8/2024): hầu hết bệnh viện đã có app đặt khám, nhưng \"chưa mấy ai biết đến App đặt khám và cách sử dụng chúng\".", "04-best-practice/umc-care-va-app-benh-vien-vn.md"),
        R("Đánh giá app", "MyVinmec 4,9/5 với khoảng 16 nghìn lượt; UMC Care 3,6/5 với 807 lượt (App Store, xem 18/10).", "04-best-practice/umc-care-va-app-benh-vien-vn.md"),
      ],
      why: "Làm thêm một mục trong app có sẵn rẻ hơn và dễ được dùng hơn một app riêng. Người bệnh không phải cài gì mới.",
      look: "Có nhãn \"Bản mô phỏng cho bài tập\" ở đầu trang để không bị nhầm với app thật (rủi ro R10)." },
    { target: () => $("#s-arrive .pad"), before: async () => { go("s-arrive"); pick("purpose", "kham-benh"); pick("booked", "0"); pick("bhyt", "1"); pick("first_time", "1"); },
      title: "2 · Bốn câu bấm chọn, không phải gõ",
      body: "Đến để làm gì · đã đặt lịch chưa · có BHYT không · lần đầu hay đã từng khám. Tour chọn sẵn: <b>khám bệnh, chưa đặt lịch, có BHYT, lần đầu</b>.",
      research: [
        R("Phỏng vấn", "Người được hỏi bỡ ngỡ không biết nên vào quầy nào; theo họ, điều này tuỳ cách vận hành của từng bệnh viện. (Thái ghi lại 18/10, log P đang hoàn thiện.)", "01-phong-van/"),
        R("Quan sát", "Quầy đầu tiên khác nhau theo 3 yếu tố: đặt lịch (kiosk/quầy lịch hẹn), BHYT (quầy BHYT), khám dịch vụ (quầy tiếp đón, mở hồ sơ nếu lần đầu).", "05-prototype/app/lotrinh.py"),
        R("Nghiên cứu", "Epic MyChart: chỉ 26,4% người từ 65 tuổi điền phiếu trước khám, trung vị 14 phút (Naimark 2024).", "04-best-practice/best-practice.md"),
      ],
      why: "Chỉ hỏi đủ để chọn đúng quầy, bằng nút bấm. Không hỏi tên, không hỏi triệu chứng: ngắn để người lớn tuổi cũng dùng được.",
      look: "Hướng cũ thất bại vì hỏi nhiều mà người dùng không thấy cần. Bản này hỏi đúng 4 câu quyết định quầy." },
    { target: () => $("#nowCard"), before: async () => { await startRoute(); await wait(200); },
      title: "3 · Bước tiếp theo, kèm lý do",
      body: "App chỉ đúng <b>Quầy tiếp nhận BHYT</b>, vị trí, giấy tờ cần mang, và dòng <b>\"Vì sao\"</b>.",
      research: [
        R("Phỏng vấn", "Điểm đau số 1: không biết vào quầy nào.", "02-journey-map/journey-map.md"),
        R("Quan sát UMC Care", "Phiếu khám ghi rõ phòng và tầng (\"Phòng 95, Tầng trệt khu B\"), nhưng mục \"Hướng dẫn quy trình khám bệnh\" là bài viết chung, không theo lượt khám của từng người.", "04-best-practice/umc-care-va-app-benh-vien-vn.md"),
      ],
      why: "Đây là <b>luật cố định</b>, không dùng AI. Day 2 (PAIR): bỏ chữ AI đi mà vấn đề vẫn giải được bằng luật thì dùng luật. Dòng \"Vì sao\" giúp người bệnh hiểu và tin bước được chỉ.",
      look: "Bài cố ý không gắn AI vào chỗ luật làm tốt." },
    { target: () => $("#timeline"),
      title: "4 · Cả buổi khám trên một màn",
      body: "Toàn bộ lộ trình kèm giờ dự kiến. Bước đã xong được gạch đi; chạm vào bước đã xong để hoàn tác.",
      research: [
        R("Diễn đàn", "VnReview: số thứ tự trên bảng gọi \"nhảy cóc\" vì được cấp cho cả lộ trình khám; người bệnh không biết cơ chế nên tưởng bị chen ngang.", "04-best-practice/umc-care-va-app-benh-vien-vn.md"),
        R("Khảo sát", "Báo cáo hài lòng người bệnh ngoại trú (BV Đa khoa tỉnh Phú Thọ, 2021) nêu cần rút ngắn chờ ở khâu xét nghiệm, chiếu chụp, trả kết quả.", "04-best-practice/umc-care-va-app-benh-vien-vn.md"),
        R("App khác", "BVĐK Tâm Anh có theo dõi hàng đợi; BV Phụ sản – Nhi Quảng Châu (Tencent) có chỉ đường trong viện sau khi đặt lịch.", "04-best-practice/app-dat-lich-trong-ngoai-nuoc.md"),
      ],
      why: "Thấy cả buổi giúp người bệnh biết còn bao lâu, có kịp ăn hay đi việc khác không.",
      look: "Giờ dự kiến ghi rõ là ước tính giả lập.",
      limit: "App thật phải lấy giờ từ hệ thống gọi số (HIS/LIS); giờ sai làm người bệnh bỏ lượt (rủi ro R4)." },
    { target: () => $("#nowCard .orders"), before: async () => {
        await advanceTo("kham-1");
        ["xn-mau-nhin-an", "sieu-am-bung", "xn-nuoc-tieu", "x-quang-nguc"].forEach(t => pendingTests.add(t));
        render(); await wait(150); },
      title: "5 · Bác sĩ chỉ định xét nghiệm, chụp chiếu",
      body: "Prototype có ô <b>mô phỏng chỉ định</b>; tour chọn sẵn: xét nghiệm máu, siêu âm bụng, nước tiểu, X-quang ngực.",
      research: [
        R("Journey map", "Sau khi bác sĩ chỉ định là đoạn người bệnh phải tự tìm nhiều phòng ở nhiều tầng, khu khác nhau (điểm đau Đ4).", "02-journey-map/journey-map.md"),
      ],
      why: "Ở app thật, chỉ định đến từ hệ thống bệnh viện; người bệnh không phải nhập gì.",
      look: "Bấm Tiếp để xem lộ trình tự sắp lại." },
    { target: () => $("#timeline"), before: async () => { await applyOrders(); await wait(300); reveal($("#timeline"), "start"); },
      title: "6 · Lộ trình tự sắp lại theo luật",
      body: "Xét nghiệm máu → siêu âm bụng (cần nhịn ăn, làm trước) → nước tiểu (sau siêu âm, vì siêu âm cần nhịn tiểu) → X-quang → chờ đủ kết quả → quay lại bác sĩ.",
      research: [
        R("Hướng dẫn Vinmec", "Khám tổng quát: không ăn sáng trước khi lấy máu; uống nhiều nước và nhịn tiểu cho tới khi siêu âm ổ bụng xong.", "vinmec.com · nhung-dieu-can-luu-y-truoc-khi-kham-suc-khoe-tong-quat"),
        R("Đo tự động", "16/16 ràng buộc lộ trình đúng, gồm: mục nhịn ăn trước, nước tiểu sau siêu âm, thanh toán trước khi làm, chờ đủ kết quả.", "05-prototype/eval/run_eval_lotrinh.py"),
      ],
      why: "Thứ tự sai là lý do người bệnh đi vòng hoặc phải làm lại (nộp nước tiểu trước khi siêu âm). Luật cố định thì kiểm thử được, mỗi bước có lý do riêng.",
      look: "Mỗi bước có dòng \"Vì sao\" khác nhau, không phải câu chung." },
    { target: () => lastMsg(), before: async () => { await ask("Tôi được ăn chưa?"); },
      title: "7 · Hỏi bằng lời thường",
      body: "Trợ lý biết lộ trình của chính người hỏi: còn hai mục cần nhịn ăn nên trả lời <b>chưa nên ăn</b>, kèm hướng dẫn và nguồn.",
      research: [
        R("Thiết kế", "Câu trả lời được ghép từ dữ liệu của viện và lộ trình của người đó. LLM (nếu bật) chỉ xếp câu hỏi vào danh mục cố định, không viết câu trả lời.", "05-prototype/README.md"),
        R("Đo guardrail", "Thử bằng LLM giả cài lỗi: mã phòng bịa bị bỏ; loại câu hỏi bịa bị bỏ; LLM timeout thì chuyển sang luật.", "05-prototype/README.md"),
      ],
      why: "Người bệnh hỏi bằng câu của mình, không phải tìm trong menu. Vì câu trả lời không do LLM viết, trợ lý không thể bịa phòng, giờ hay hướng dẫn.",
      look: "Mỗi câu trả lời có dòng \"Nguồn\"." },
    { target: () => lastMsg(), before: async () => { await ask("chụp phổi ở đâu, có lâu không"); },
      title: "8 · Câu nói tự nhiên của người lớn tuổi",
      body: "Câu kép \"ở đâu, có lâu không\" được trả lời cả vị trí, thời gian chờ và lúc có kết quả.",
      research: [
        R("Đo · bộ chính", "Lần đo đầu: luật từ khoá hiểu đúng 36/44 câu. Sau khi bổ sung luật: 44/44, nhưng đã chỉnh theo chính bộ này nên không khách quan.", "05-prototype/eval/results/"),
        R("Đo · held-out", "20 câu viết sau khi chỉnh luật: luật hiểu đúng 14/20. Đây là con số đáng tin.", "05-prototype/eval/results/"),
      ],
      why: "Hiểu câu hỏi tự do là <b>chỗ duy nhất AI có thể hơn luật</b>. Luật hụt ở chính chỗ này (14/20), nên đây là nơi đo xem có đáng dùng LLM không.",
      look: "Bài báo cả con số xấu và nói rõ con số nào không có ý nghĩa.",
      limit: "Chế độ LLM chưa đo (chưa có API key). Cam kết: nếu LLM không vượt rõ luật thì bỏ AI." },
    { target: () => lastMsg(), before: async () => { await ask("đường huyết 7,2 có cao không"); },
      title: "9 · Câu y khoa: không trả lời, chuyển cho bác sĩ",
      body: "Trợ lý không giải thích kết quả, không tư vấn thuốc hay chế độ ăn. Câu hỏi được lưu vào \"Câu hỏi để hỏi bác sĩ\".",
      research: [
        R("Ràng buộc đề", "Mục 6.4: không đưa ra lời khuyên y khoa.", "Bài tập ứng tuyển, mục 6.4"),
        R("Đo", "Bộ held-out: luật chặn được 1/3 câu y khoa nói vòng (\"x quang thấy phổi mờ là bị gì\" lọt). Câu bị lọt nhận \"chưa hiểu\", không nhận lời khuyên.", "05-prototype/README.md"),
      ],
      why: "Luật y khoa thắng mọi phân loại của LLM. Kể cả khi luật bỏ sót, câu trả lời vẫn chỉ ghép từ dữ liệu phòng, nên không thể chứa lời khuyên y khoa: an toàn nhờ cách dựng.",
      look: "Từ chối nhưng không bỏ rơi: câu hỏi được giữ lại để hỏi bác sĩ." },
    { target: () => lastMsg(), before: async () => { await ask("bố tôi tự nhiên méo miệng, nói khó"); },
      title: "10 · Dấu hiệu cấp cứu",
      body: "Chỉ đường <b>khoa Cấp cứu</b> trong viện, có nút gọi 115. Luật chạy trước mọi thứ và <b>không gọi LLM</b>.",
      research: [
        R("Dùng thử MyVinmec", "Trợ lý MIA cảnh báo \"méo miệng, nói khó\" sau khoảng 20 giây vì đi qua LLM (video V2, 3:48 → 4:10).", "01-phong-van/myvinmec-gap-analysis.md"),
        R("Dùng thử MyVinmec", "Form đặt lịch cho chọn \"Cơn đau thắt ngực\" như triệu chứng thường, trong khi MIA cảnh báo cấp cứu với cùng mô tả (T1).", "01-phong-van/myvinmec-gap-analysis.md"),
        R("Đo", "Bắt được 6/6 câu cấp cứu (bộ chính và held-out).", "05-prototype/eval/results/"),
      ],
      why: "Với đột quỵ, từng phút đều quan trọng. Luật cố định phản hồi tức thì, nhất quán ở mọi lối vào và kiểm thử được.",
      look: "Ở trong viện, đường đúng là khoa Cấp cứu hoặc nhân viên gần nhất; 115 dành cho người ở ngoài.",
      limit: "Danh sách dấu hiệu cấp cứu chưa được bác sĩ duyệt." },
    { target: () => $("#qCard"), before: async () => { closeSheet(); await wait(150); reveal($("#qCard"), "center"); },
      title: "11 · Câu hỏi mang vào phòng khám",
      body: "Câu y khoa vừa hỏi nằm ở đây, sẵn để hỏi khi quay lại bác sĩ với kết quả.",
      research: [
        R("Nghiên cứu", "Tổng quan 42 nghiên cứu: danh sách câu hỏi giúp người bệnh hỏi nhiều hơn, rõ nhất khi bác sĩ đồng thuận (Sansoni 2015). Nguồn mẫu: AHRQ QuestionBuilder.", "04-best-practice/best-practice.md"),
        R("Nghiên cứu", "Chỉ 4/35 người bệnh nói ra đủ điều họ định nói (Barry, BMJ 2000).", "04-best-practice/best-practice.md"),
      ],
      why: "Phần dùng lại từ hướng cũ (Chuẩn bị buổi khám). Không bắt người bệnh chuẩn bị trước, chỉ giữ lại câu họ đã tự hỏi trong ngày.",
      look: "Hướng cũ bị dừng nhưng phần có bằng chứng vẫn được giữ." },
    { target: () => $("#s-book .pad"), before: async () => {
        resetApp(); go("s-book"); Object.assign(bk, { specialty: "tong-quat", day: 1, time: "07:30" }); renderBook();  // người bệnh khác
        pick("bk_bhyt", "0"); pick("bk_first", "1"); },
      title: "12 · Nếu đã đặt lịch: bắt đầu từ lúc đặt",
      body: "Một người bệnh khác, đã đặt lịch trước. Màn đặt lịch chỉ là <b>mô phỏng tối giản</b>. Tour chọn sẵn: khám sức khoẻ tổng quát, ngày mai, 07:30.",
      research: [
        R("Desk research", "Đặt lịch đã được giải tốt: UMC Care có 3 cách đặt (chuyên khoa, ngày, bác sĩ), khung giờ 1 tiếng; MyVinmec có đặt theo triệu chứng.", "04-best-practice/umc-care-va-app-benh-vien-vn.md"),
      ],
      why: "Người đã đặt lịch không phải trả lời lại 4 câu. Bài không làm lại tính năng đặt lịch, chỉ nối lộ trình vào ngay sau nó.",
      look: "Ranh giới phạm vi rõ: chỗ app đã tốt thì không đụng." },
    { target: () => $("#apptBox"), before: async () => { bookAppt(); await wait(250); },
      title: "13 · Lịch hẹn có nút Xem lộ trình",
      body: "Lịch hẹn đã xác nhận có thêm nút <b>\"Xem lộ trình hôm khám\"</b>. App đã biết khoa, giờ hẹn, BHYT nên tự điền.",
      research: [
        R("Dùng thử MyVinmec", "Màn \"Lịch hẹn\" của tài khoản chưa kết nối hồ sơ đang trống; chưa thấy hướng dẫn chuẩn bị gắn với lịch hẹn.", "01-phong-van/myvinmec-trial-notes.md"),
      ],
      why: "Nối vào màn Lịch hẹn mà app hiện có là điểm vào tự nhiên nhất cho người đã đặt.",
      look: "Chưa kiểm chứng app gửi gì sau khi đặt (SMS, cuộc gọi); cần hỏi thêm khi phỏng vấn." },
    { target: () => $("#nowCard"), before: async () => { await routeFromAppt(); await wait(250); },
      title: "14 · Lộ trình bắt đầu từ tối hôm trước",
      body: "Bước đầu là <b>Đã đặt lịch</b> (đã xong), tiếp theo là <b>Chuẩn bị trước ngày khám</b>: nhịn ăn sáng, nhịn tiểu tới khi siêu âm xong, mang giấy tờ.",
      research: [
        R("Hướng dẫn Vinmec", "Các mục chuẩn bị khám tổng quát lấy nguyên từ trang hướng dẫn công khai của Vinmec; mục khác ghi rõ \"giả lập, cần viện xác nhận\".", "05-prototype/app/lotrinh.py"),
      ],
      why: "Chuẩn bị đúng để không phải chờ thêm hoặc hẹn lại. Checklist của hướng cũ giờ gắn vào đúng một lịch hẹn cụ thể.",
      look: "Mỗi hướng dẫn có nguồn, không có nội dung y khoa do máy tự sinh." },
    { target: () => $("#timeline"), before: async () => { markDone(); await wait(200); reveal($("#timeline"), "start"); },
      title: "15 · Giờ theo giờ hẹn, gói khám biết trước",
      body: "Check-in ở <b>kiosk</b> trước giờ hẹn 25 phút. Khám tổng quát biết trước gói nên các mục được sắp sẵn từ lúc đặt; bác sĩ kết luận sau cùng.",
      research: [
        R("Quan sát UMC Care", "Mục \"Quy trình đặt khám\" của app: người bệnh không dùng BHYT đến phòng khám trước giờ hẹn 15–30 phút để xác nhận thông tin.", "04-best-practice/umc-care-va-app-benh-vien-vn.md"),
        R("Đo tự động", "4 phép kiểm tra cho luồng này: thứ tự Đã đặt lịch → Chuẩn bị → Check-in; check-in trước giờ hẹn; gặp bác sĩ không sớm hơn giờ hẹn; gói tổng quát.", "05-prototype/eval/run_eval_lotrinh.py"),
      ],
      why: "Người đã đặt lịch cần biết <b>mấy giờ phải có mặt</b> và cả buổi xong lúc nào, không chỉ giờ hẹn.",
      look: "Khám chuyên khoa có lịch hẹn: giờ gặp bác sĩ tính từ giờ hẹn, không phải từ lúc mở app." },
    { title: "Tóm tắt để đánh giá",
      body: `<ul><li>Lộ trình: <b>16/16</b> ràng buộc đúng (cả hai luồng)</li>
             <li>Trợ lý, held-out 20 câu: hiểu đúng <b>14/20</b> · cấp cứu 2/2 · câu y khoa bị chặn <b>1/3</b> · chặn nhầm 0/15</li>
             <li>Chế độ LLM: <b>chưa đo</b></li></ul>`,
      research: [
        R("Kết quả đo", "Đo ngày 18/10, chế độ luật. Ba lần đo đều giữ nguyên.", "05-prototype/eval/results/"),
        R("Đọc tiếp", "Câu chuyện đổi hướng: VERSIONS.md, 00-qua-trinh-chon-huong.md · Need statement: 03-need-statement/ · Rủi ro: 06-rui-ro-dao-duc/", "README.md"),
      ],
      why: "Phần lớn giá trị đến từ <b>luật và dữ liệu vận hành</b>; AI chỉ ở bước hiểu câu hỏi. Nếu LLM không vượt rõ luật trên held-out thì bỏ AI, giữ lộ trình bằng luật.",
      look: "Ba điều cần làm tiếp: đo chế độ LLM; thử với 2–3 người thật theo thẻ K1–K6; kiểm tra điểm đau có còn mạnh ở Vinmec (viện tư).",
      limit: "Chưa thử với người dùng thật; dữ liệu phòng và hàng đợi là giả lập." },
  ];

  let idx = 0, running = false, prevTester = "";
  const phone = document.getElementById("phone");
  const root = document.createElement("div");
  root.id = "tour";
  root.innerHTML = `<div class="tour-hole" id="tourHole"></div><div class="tour-dim" id="tourDim"></div>
    <div class="tour-card" id="tourCard"><div class="tour-top"><span id="tourCount"></span><button class="tour-exit">Thoát tour</button></div>
    <h4 id="tourTitle"></h4><div id="tourBody"></div><div class="tour-look" id="tourLook"></div>
    <div class="tour-btns" id="tourBtns"></div></div>`;
  phone.appendChild(root);
  const left = document.createElement("aside"), right = document.createElement("aside");
  left.id = "tourLeft"; right.id = "tourRight"; left.className = right.className = "tour-side";
  document.body.append(left, right);

  const css = document.createElement("style");
  css.textContent = `
    #tour { position: absolute; inset: 0; z-index: 60; display: none; }
    #tour.on { display: block; }
    .tour-dim { position: absolute; inset: 0; background: rgba(10,25,24,.6); display: none; }
    .tour-dim.on { display: block; }
    .tour-hole { position: absolute; border-radius: 12px; box-shadow: 0 0 0 9999px rgba(10,25,24,.6), 0 0 0 3px #f5a623;
                 transition: all .25s; pointer-events: none; display: none; }
    .tour-hole.on { display: block; }
    body.tour-wide .tour-hole { box-shadow: 0 0 0 3px #f5a623, 0 0 0 9px rgba(245,166,35,.22); }
    body.tour-wide .tour-card, body.tour-wide .tour-dim { display: none !important; }
    .tour-card { position: absolute; left: 14px; right: 14px; background: #fff; border-radius: 14px; padding: 14px 14px 12px;
                 box-shadow: 0 10px 30px rgba(0,0,0,.3); font-size: 13.5px; line-height: 1.5; max-height: 62%; overflow-y: auto; }
    .tour-top { display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: #8a8f8e; font-weight: 600; }
    .tour-exit { border: 0; background: none; color: #8a8f8e; font: inherit; cursor: pointer; text-decoration: underline; }
    .tour-card h4 { margin: 4px 0 6px; font-size: 16px; color: #2b958f; }
    .tour-card ul, .tour-side ul { margin: 6px 0; padding-left: 18px; }
    .tour-card code { font-size: 12px; background: #f1f4f4; padding: 0 4px; border-radius: 4px; }
    .tour-look { margin-top: 8px; font-size: 12.5px; background: #fff4e5; color: #7a5200; border-radius: 8px; padding: 7px 10px; }
    .tour-look::before { content: "Người chấm nên để ý: "; font-weight: 700; }
    .tour-btns { display: flex; gap: 8px; margin-top: 10px; }
    .tour-btns button { flex: 1; padding: 10px; border-radius: 8px; border: 1.5px solid #37aea7; background: #fff; color: #37aea7;
                        font: inherit; font-weight: 600; cursor: pointer; }
    .tour-btns button.main { background: #37aea7; color: #fff; }
    .tour-btns button:disabled { opacity: .6; cursor: default; }
    .tour-launch { display: flex; align-items: center; gap: 10px; width: 100%; margin-bottom: 12px; padding: 12px 14px; border-radius: 12px;
                   border: 1.5px dashed #f5a623; background: #fff4e5; color: #7a5200; font: inherit; font-size: 13.5px; cursor: pointer; text-align: left; }
    .tour-launch b { display: block; color: #5c3d00; font-size: 14.5px; }

    /* Hai bên màn hình: chỉ hiện ở màn rộng */
    .tour-side { position: fixed; top: 24px; bottom: 24px; width: min(460px, calc(50vw - 195px - 52px)); overflow-y: auto;
                 background: #fff; border-radius: 18px; padding: 20px 22px 18px; box-shadow: 0 10px 40px rgba(0,0,0,.12);
                 font-size: 14px; line-height: 1.55; color: #1f1f1f; display: none; z-index: 10; }
    body.tour-wide .tour-side { display: flex; flex-direction: column; }
    #tourLeft { right: calc(50% + 195px + 26px); }
    #tourRight { left: calc(50% + 195px + 26px); }
    .side-kicker { font-size: 11px; font-weight: 700; letter-spacing: .6px; color: #8a8f8e; text-transform: uppercase; display: flex; justify-content: space-between; }
    .tour-side h2 { margin: 6px 0 12px; font-size: 21px; line-height: 1.3; color: #1f1f1f; }
    .tour-side h3 { margin: 16px 0 6px; font-size: 12px; letter-spacing: .5px; text-transform: uppercase; color: #2b958f; }
    .ev { border: 1px solid #e6ecec; border-radius: 12px; padding: 10px 12px; margin-bottom: 10px; }
    .ev .tag { display: inline-block; font-size: 11px; font-weight: 700; color: #2b958f; background: #e8f6f5; border-radius: 99px; padding: 1px 9px; margin-bottom: 4px; }
    .ev .src { display: block; font-size: 11.5px; color: #8a8f8e; margin-top: 4px; word-break: break-word; }
    .ev .src::before { content: "Nguồn: "; }
    .side-feature { background: #f6f8f8; border-radius: 12px; padding: 10px 12px; }
    .side-look { background: #fff4e5; color: #6b4800; border-radius: 12px; padding: 10px 12px; }
    .side-limit { background: #fdeeee; color: #8a1c1f; border-radius: 12px; padding: 10px 12px; }
    .side-nav { margin-top: auto; padding-top: 14px; }
    .dots { display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 10px; }
    .dots span { width: 18px; height: 5px; border-radius: 3px; background: #e3e8e7; cursor: pointer; }
    .dots span.on { background: #37aea7; }
    .dots span.cur { background: #f5a623; }
    .side-nav .row2 { display: flex; gap: 8px; }
    .side-nav button { flex: 1; padding: 11px; border-radius: 10px; border: 1.5px solid #37aea7; background: #fff; color: #37aea7;
                       font: inherit; font-weight: 600; cursor: pointer; }
    .side-nav button.main { background: #37aea7; color: #fff; flex: 2; }
    .side-nav button:disabled { opacity: .55; cursor: default; }
    .side-nav .keys { font-size: 11.5px; color: #8a8f8e; margin-top: 8px; text-align: center; }`;
  document.head.appendChild(css);

  const wide = () => window.innerWidth >= 1080;

  function place(el) {
    const hole = $("#tourHole"), card = $("#tourCard"), dim = $("#tourDim");
    const P = phone.getBoundingClientRect();
    if (!el) {
      hole.classList.remove("on"); dim.classList.add("on");
      card.style.top = "50%"; card.style.bottom = "auto"; card.style.transform = "translateY(-50%)";
      return;
    }
    dim.classList.remove("on"); hole.classList.add("on");
    const S = document.getElementById("scroll").getBoundingClientRect(), Rr = el.getBoundingClientRect();
    const inSheet = el.closest("#sheet");
    const top = Math.max(Rr.top, inSheet ? P.top : S.top), bottom = Math.min(Rr.bottom, inSheet ? P.bottom : S.bottom);
    const pad = 6;
    Object.assign(hole.style, { left: Rr.left - P.left - pad + "px", top: top - P.top - pad + "px",
                                width: Rr.width + pad * 2 + "px", height: Math.max(bottom - top, 24) + pad * 2 + "px" });
    // Thẻ trong khung (màn hẹp): đo chiều cao thật rồi chọn chỗ dưới → trên → đáy, luôn kẹp trong khung
    card.style.transform = "none"; card.style.bottom = "auto";
    const m = 12, h = card.offsetHeight;
    const holeTop = top - P.top - pad, holeBottom = bottom - P.top + pad;
    let y;
    if (holeBottom + m + h <= P.height - m) y = holeBottom + m;
    else if (holeTop - m - h >= m) y = holeTop - m - h;
    else y = P.height - h - m - 18;
    card.style.top = Math.max(m, Math.min(y, P.height - h - m)) + "px";
  }

  function navHtml(i) {
    const last = i === STEPS.length - 1;
    const dots = STEPS.map((_, k) => `<span class="${k < i ? "on" : k === i ? "cur" : ""}" title="Bước ${k + 1}" onclick="window.__tour.goTo(${k})"></span>`).join("");
    const main = last ? `<button class="main" onclick="window.__tour.end(true)">Tự thử</button>`
                      : `<button class="main" onclick="window.__tour.next()">${i === 0 ? "Bắt đầu" : "Tiếp"}</button>`;
    const prev = last ? `<button onclick="window.__tour.goTo(0)">Xem lại</button>`
                      : `<button onclick="window.__tour.prev()" ${i === 0 ? "disabled" : ""}>Trước</button>`;
    return `<div class="dots">${dots}</div><div class="row2">${prev}${main}</div>
      <div class="keys">Phím ← → để chuyển bước · Esc để thoát · <button class="tour-exit" style="flex:none;border:0;padding:0">Thoát tour</button></div>`;
  }

  function renderSides(i) {
    const s = STEPS[i], n = `Bước ${i + 1}/${STEPS.length}`;
    left.innerHTML = `<div class="side-kicker"><span>Nghiên cứu &amp; bằng chứng</span><span>${n}</span></div>
      <h2>${s.title}</h2>
      ${(s.research || []).map(e => `<div class="ev"><span class="tag">${e.tag}</span><div>${e.text}</div>${e.src ? `<span class="src">${e.src}</span>` : ""}</div>`).join("")}`;
    right.innerHTML = `<div class="side-kicker"><span>Vì sao làm vậy</span><span>${n}</span></div>
      <h3>Tính năng ở bước này</h3><div class="side-feature">${s.body}</div>
      ${s.why ? `<h3>Vì sao thiết kế như vậy</h3><div>${s.why}</div>` : ""}
      ${s.look ? `<h3>Hội đồng nên để ý</h3><div class="side-look">${s.look}</div>` : ""}
      ${s.limit ? `<h3>Giới hạn</h3><div class="side-limit">${s.limit}</div>` : ""}
      <div class="side-nav" id="sideNav">${navHtml(i)}</div>`;
    right.querySelectorAll(".tour-exit").forEach(b => b.onclick = () => end(false));
  }

  function busy(on) {
    document.querySelectorAll("#tourBtns button, #sideNav button").forEach(b => { if (!b.classList.contains("tour-exit")) b.disabled = on; });
    if (on) { const m = document.querySelector("#sideNav .main, #tourBtns .main"); if (m) m.textContent = "Đang chạy…"; }
  }

  async function show(i, skipBefore = false) {
    idx = i;
    const s = STEPS[i];
    busy(true);
    if (s.before && !skipBefore) await s.before();
    await wait(120);
    const el = s.target ? s.target() : null;
    if (el && !el.closest("#sheet")) { reveal(el); await wait(120); }
    document.body.classList.toggle("tour-wide", wide());
    renderSides(i);
    $("#tourCount").textContent = `Bước ${i + 1}/${STEPS.length}`;
    $("#tourTitle").textContent = s.title;
    $("#tourBody").innerHTML = s.body + (s.why ? `<div style="margin-top:6px;color:#5d6b66">${s.why}</div>` : "");
    $("#tourLook").textContent = s.look || "";
    $("#tourLook").style.display = s.look ? "block" : "none";
    const last = i === STEPS.length - 1;
    $("#tourBtns").innerHTML = last
      ? `<button onclick="window.__tour.goTo(0)">Xem lại tour</button><button class="main" onclick="window.__tour.end(true)">Tự thử</button>`
      : `<button onclick="window.__tour.prev()" ${i === 0 ? "disabled" : ""}>Trước</button><button class="main" onclick="window.__tour.next()">${i === 0 ? "Bắt đầu" : "Tiếp"}</button>`;
    place(el);
    $("#tourCard").scrollTop = 0; left.scrollTop = 0; right.scrollTop = 0;
  }

  function resetApp() {
    state = fresh(); pendingTests = new Set();
    document.getElementById("msgs").innerHTML = "";
    closeSheet();
  }
  // Chuyển tới bước bất kỳ: tiến thì chạy tiếp; lùi thì dựng lại nhanh từ đầu (các thao tác tự động đều chạy được từ trạng thái mới)
  async function goTo(k) {
    if (!running || k < 0 || k >= STEPS.length || k === idx) return;
    if (k === idx + 1) return show(k);
    busy(true);
    const from = k > idx ? idx + 1 : 1;
    if (k < idx) resetApp();
    fast = true;
    try { for (let j = from; j <= k; j++) if (STEPS[j].before) await STEPS[j].before(); } finally { fast = false; }
    return show(k, true);
  }

  function begin() {
    if (running) return;
    running = true;
    prevTester = document.getElementById("tester").value;
    resetApp();
    document.getElementById("tester").value = "TOUR";
    root.classList.add("on");
    show(0);
  }
  function end(selfTry) {
    running = false;
    root.classList.remove("on");
    document.body.classList.remove("tour-wide");
    closeSheet();
    document.getElementById("tester").value = prevTester === "TOUR" ? "" : prevTester;
    if (selfTry) restart();
  }
  window.__tour = { begin, end, goTo, next: () => goTo(idx + 1), prev: () => goTo(idx - 1) };
  root.querySelector(".tour-exit").onclick = () => end(false);
  window.addEventListener("resize", () => {
    if (!running) return;
    document.body.classList.toggle("tour-wide", wide());
    place(STEPS[idx].target ? STEPS[idx].target() : null);
  });
  window.addEventListener("keydown", e => {
    if (!running || document.activeElement?.tagName === "INPUT") return;
    if (document.querySelector("#sideNav .main, #tourBtns .main")?.disabled) return;
    if (e.key === "ArrowRight") goTo(idx + 1);
    else if (e.key === "ArrowLeft") goTo(idx - 1);
    else if (e.key === "Escape") end(false);
  });

  // Nút mở tour ở Trang chủ
  const launch = document.createElement("button");
  launch.className = "tour-launch";
  launch.innerHTML = `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#f5a623" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="m10 8 6 4-6 4z" fill="#f5a623"/></svg>
    <span><b>Tour cho người chấm</b>App tự bấm qua từng tính năng; hai bên màn hình là nghiên cứu và lý do thiết kế</span>`;
  launch.onclick = begin;
  const homePad = document.querySelector("#s-home .pad");
  homePad.insertBefore(launch, homePad.firstChild);

  if (new URLSearchParams(location.search).get("tour") === "1") setTimeout(begin, 400);
})();
