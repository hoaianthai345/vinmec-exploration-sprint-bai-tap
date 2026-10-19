// Bản 2 (18/10/2026): thẻ ghi chú nằm trong khung điện thoại, 17 bước. Bản hiện hành: tour.js (bản 3, thông tin cho hội đồng ở hai bên). Dùng bởi index-v5.html.
// Tour 3 phút cho người chấm: tự đi qua từng tính năng của "Lộ trình khám trong ngày", làm sáng đúng chỗ cần xem và
// ghi chú điều nên để ý. Dùng các hàm của index.html (state, go, startRoute, markDone, applyOrders, openSheet, send...).
// Mở bằng nút "Tour cho người chấm" ở Trang chủ hoặc thêm ?tour=1 vào URL. Lượt tour ghi log với mã người thử "TOUR"
// để tách khỏi lượt thử thật (summarize_log.py bỏ qua mã này).

(() => {
  const wait = ms => new Promise(r => setTimeout(r, ms));
  const $ = sel => document.querySelector(sel);
  const pick = (key, v) => document.querySelector(`.choice[data-key="${key}"] button[data-v="${v}"]`).click();
  async function advanceTo(id) {
    for (let i = 0; i < 20 && currentStep() && currentStep().id !== id; i++) { markDone(); await wait(60); }
  }
  async function ask(q) { if (!$("#sheet").classList.contains("open")) openSheet(); await send(q, "tour"); await wait(250); }
  const lastMsg = () => [...document.querySelectorAll("#msgs .msg")].pop();

  // Mỗi bước: target (hàm trả phần tử cần làm sáng, null = hộp giữa màn hình), before (thao tác tự động), title, body,
  // look (điều người chấm nên để ý).
  const STEPS = [
    { title: "Tour 3 phút cho người chấm",
      body: `<b>Vấn đề.</b> Phỏng vấn cho thấy người bệnh <b>đến thẳng viện</b> và bỡ ngỡ <b>không biết vào quầy nào</b>; sau khi bác sĩ chỉ định thì không biết đi phòng nào, theo thứ tự nào, chờ tới bao giờ. Đặt lịch và thanh toán thì các app lớn đã làm tốt.<br><br>
             <b>Tính năng.</b> "Lộ trình hôm nay": luôn trả lời được câu <i>"Bây giờ tôi đi đâu tiếp, và còn chờ bao lâu?"</i><br><br>
             Tour đi hai luồng: <b>người đến thẳng</b> (bước 1–11) và <b>người đã đặt lịch</b>, lộ trình bắt đầu từ lịch hẹn (bước 12–15). Tour tự bấm thay bạn. Bệnh viện, phòng, thời gian chờ đều là <b>giả lập</b>.`,
      look: "Mỗi bước có dòng này: điều nên để ý khi đánh giá." },
    { target: () => $(".banner-ad"), before: async () => { go("s-home"); },
      title: "1 · Điểm vào nằm trong app quen thuộc",
      body: "Tính năng là một mục mới trong MyVinmec (giao diện mô phỏng), không phải app riêng. Người bệnh đang đứng ở sảnh viện mở mục này.",
      look: "Có nhãn \"Bản mô phỏng cho bài tập\" ở đầu trang để không bị nhầm với app thật." },
    { target: () => $("#s-arrive .pad"), before: async () => { go("s-arrive"); pick("purpose", "kham-benh"); pick("booked", "0"); pick("bhyt", "1"); pick("first_time", "1"); },
      title: "2 · Bốn câu bấm chọn, không phải gõ",
      body: "Quầy đầu tiên phụ thuộc cách vận hành: đã đặt lịch, BHYT hay khám dịch vụ, lần đầu hay đã có hồ sơ. Tour chọn sẵn: <b>khám bệnh · chưa đặt lịch · có BHYT · lần đầu</b>.",
      look: "Không hỏi tên, không hỏi triệu chứng: chỉ hỏi đủ để chọn đúng quầy." },
    { target: () => $("#nowCard"), before: async () => { await startRoute(); await wait(200); },
      title: "3 · Bước tiếp theo, kèm lý do",
      body: "App chỉ đúng <b>Quầy tiếp nhận BHYT</b>, vị trí, giấy tờ cần mang. Dòng <b>\"Vì sao\"</b> giải thích lý do. Đây là điểm đau \"không biết vào quầy nào\" trong phỏng vấn.",
      look: "Phần này là luật cố định, không có AI. Bài cố ý không dùng AI ở chỗ luật làm tốt." },
    { target: () => $("#timeline"),
      title: "4 · Cả buổi khám trên một màn",
      body: "Toàn bộ lộ trình kèm giờ dự kiến. Bước đã xong được gạch đi; chạm vào bước đã xong để hoàn tác.",
      look: "Giờ dự kiến ghi rõ là ước tính giả lập. App thật phải lấy từ hệ thống gọi số (rủi ro R4)." },
    { target: () => $("#nowCard .orders"), before: async () => {
        await advanceTo("kham-1");
        ["xn-mau-nhin-an", "sieu-am-bung", "xn-nuoc-tieu", "x-quang-nguc"].forEach(t => pendingTests.add(t));
        render(); await wait(150); },
      title: "5 · Bác sĩ chỉ định xét nghiệm, chụp chiếu",
      body: "Ở app thật, chỉ định đến từ hệ thống bệnh viện. Prototype có ô <b>mô phỏng</b>; tour chọn sẵn: xét nghiệm máu, siêu âm bụng, nước tiểu, X-quang ngực.",
      look: "Bấm tiếp để xem lộ trình tự sắp lại." },
    { target: () => $("#timeline"), before: async () => { await applyOrders(); await wait(300); $("#timeline").scrollIntoView({ block: "start" }); },
      title: "6 · Lộ trình tự sắp lại theo luật",
      body: "Thứ tự: <b>xét nghiệm máu → siêu âm bụng</b> (cần nhịn ăn, làm trước để được ăn sớm) → <b>nước tiểu</b> (sau siêu âm, vì siêu âm cần nhịn tiểu) → <b>X-quang</b> → chờ đủ kết quả → quay lại bác sĩ. Mỗi bước có lý do riêng.",
      look: "Đây là chỗ người bệnh hay đi vòng hoặc làm sai thứ tự. Luật lộ trình có 16 phép kiểm tra tự động (eval)." },
    { target: () => lastMsg(), before: async () => { await ask("Tôi được ăn chưa?"); },
      title: "7 · Hỏi bằng lời thường",
      body: "Trợ lý biết lộ trình của chính người hỏi: còn hai mục cần nhịn ăn nên trả lời <b>chưa nên ăn</b>, kèm hướng dẫn và <b>nguồn</b> (hướng dẫn công khai của Vinmec).",
      look: "Câu trả lời được ghép từ dữ liệu của viện. LLM (nếu bật) chỉ phân loại câu hỏi, không viết câu trả lời, nên không bịa được." },
    { target: () => lastMsg(), before: async () => { await ask("chụp phổi ở đâu, có lâu không"); },
      title: "8 · Câu nói tự nhiên của người lớn tuổi",
      body: "Câu kép \"ở đâu, có lâu không\" được trả lời cả vị trí lẫn thời gian chờ và thời gian có kết quả.",
      look: "Hiểu câu hỏi tự do là chỗ duy nhất AI có thể hơn luật. Bộ held-out: luật hiểu đúng 14/20 câu; chế độ LLM đo bằng --heldout --llm." },
    { target: () => lastMsg(), before: async () => { await ask("đường huyết 7,2 có cao không"); },
      title: "9 · Câu y khoa: không trả lời, chuyển cho bác sĩ",
      body: "Trợ lý <b>không giải thích kết quả</b>, không tư vấn thuốc hay chế độ ăn. Câu hỏi được lưu vào \"Câu hỏi để hỏi bác sĩ\" để người bệnh hỏi khi quay lại phòng khám.",
      look: "Luật y khoa thắng mọi phân loại của LLM. Khi luật bỏ sót, người hỏi nhận \"chưa hiểu\", không bao giờ nhận lời khuyên." },
    { target: () => lastMsg(), before: async () => { await ask("bố tôi tự nhiên méo miệng, nói khó"); },
      title: "10 · Dấu hiệu cấp cứu",
      body: "Có dấu hiệu nguy hiểm thì app <b>chỉ đường khoa Cấp cứu</b> trong viện và có nút gọi 115. Luật chạy trước mọi thứ và <b>không gọi LLM</b>, nên phản hồi tức thì.",
      look: "Bài học từ dùng thử MyVinmec: cảnh báo của trợ lý MIA đi qua LLM mất khoảng 20 giây." },
    { target: () => $("#qCard"), before: async () => { closeSheet(); await wait(150); $("#qCard").scrollIntoView({ block: "center" }); },
      title: "11 · Câu hỏi mang vào phòng khám",
      body: "Câu y khoa vừa hỏi nằm ở đây, sẵn để hỏi bác sĩ ở bước \"Quay lại bác sĩ với kết quả\".",
      look: "Phần dùng lại từ hướng cũ (Chuẩn bị buổi khám), dựa trên nghiên cứu về danh sách câu hỏi (AHRQ)." },
    { target: () => $("#s-book .pad"), before: async () => {
        closeSheet(); go("s-book"); Object.assign(bk, { specialty: "tong-quat", day: 1, time: "07:30" }); renderBook();
        pick("bk_bhyt", "0"); pick("bk_first", "1"); },
      title: "12 · Nếu đã đặt lịch: bắt đầu từ lúc đặt",
      body: "Người đã đặt lịch không phải trả lời lại 4 câu. Màn đặt lịch ở đây chỉ là <b>mô phỏng</b> (app thật đã làm tốt bước này). Tour chọn sẵn: <b>khám sức khoẻ tổng quát · ngày mai · 07:30</b>.",
      look: "Bài không làm lại tính năng đặt lịch, chỉ nối lộ trình vào ngay sau nó." },
    { target: () => $("#apptBox"), before: async () => { bookAppt(); await wait(250); },
      title: "13 · Lịch hẹn có nút Xem lộ trình",
      body: "Lịch hẹn đã xác nhận có thêm nút <b>\"Xem lộ trình hôm khám\"</b>. App đã biết khoa, giờ hẹn, BHYT nên tự điền.",
      look: "Đây là chỗ nối tự nhiên vào màn Lịch hẹn mà app hiện có (hiện đang trống)." },
    { target: () => $("#nowCard"), before: async () => { await routeFromAppt(); await wait(250); },
      title: "14 · Lộ trình bắt đầu từ tối hôm trước",
      body: "Bước đầu là <b>Đã đặt lịch</b> (đã xong), bước tiếp theo là <b>Chuẩn bị trước ngày khám</b>: với khám tổng quát là nhịn ăn sáng, nhịn tiểu tới khi siêu âm xong, mang giấy tờ. Nguồn: hướng dẫn công khai của Vinmec.",
      look: "Phần này dùng lại checklist của hướng cũ (Chuẩn bị buổi khám), giờ gắn đúng vào một lịch hẹn cụ thể." },
    { target: () => $("#timeline"), before: async () => { markDone(); await wait(200); $("#timeline").scrollIntoView({ block: "start" }); },
      title: "15 · Giờ tính theo giờ hẹn, gói khám biết trước",
      body: "Check-in ở <b>kiosk</b> trước giờ hẹn 25 phút (không phải lấy số ở quầy). Khám tổng quát đã biết gói nên các mục xét nghiệm, chụp chiếu được <b>sắp sẵn từ lúc đặt</b>, bác sĩ khám và kết luận sau cùng.",
      look: "Với khám chuyên khoa có lịch hẹn, giờ gặp bác sĩ không sớm hơn giờ hẹn; 4 phép kiểm tra tự động cho luồng này nằm trong eval." },
    { title: "Tóm tắt để đánh giá",
      body: `<b>Đo ngày 18/10, chế độ luật</b> (file trong <code>05-prototype/eval/results/</code>):
             <ul><li>Lộ trình: 16/16 ràng buộc đúng (cả luồng đến thẳng và luồng đã đặt lịch)</li>
             <li>Trợ lý, bộ held-out 20 câu: hiểu đúng 14/20 · cấp cứu 2/2 · câu y khoa bị chặn <b>1/3</b> · chặn nhầm 0/15</li>
             <li>Chế độ LLM: <b>chưa đo</b>. Nếu không vượt rõ luật thì bỏ AI, giữ lộ trình bằng luật</li></ul>
             <b>Đọc tiếp trong repo:</b> <code>VERSIONS.md</code> (hai lần đổi hướng) · <code>03-need-statement/</code> · <code>05-prototype/README.md</code> · <code>06-rui-ro-dao-duc/</code>`,
      look: "Bấm \"Tự thử\" để dùng app từ đầu, hoặc \"Xem lại tour\"." },
  ];

  let idx = 0, running = false, prevTester = "";
  const root = document.createElement("div");
  root.id = "tour";
  root.innerHTML = `<div class="tour-hole" id="tourHole"></div><div class="tour-dim" id="tourDim"></div>
    <div class="tour-card" id="tourCard"><div class="tour-top"><span id="tourCount"></span><button id="tourExit">Thoát tour</button></div>
    <h4 id="tourTitle"></h4><div id="tourBody"></div><div class="tour-look" id="tourLook"></div>
    <div class="tour-btns" id="tourBtns"></div></div>`;
  const css = document.createElement("style");
  css.textContent = `
    #tour { position: absolute; inset: 0; z-index: 60; display: none; }
    #tour.on { display: block; }
    .tour-dim { position: absolute; inset: 0; background: rgba(10,25,24,.6); display: none; }
    .tour-dim.on { display: block; }
    .tour-hole { position: absolute; border-radius: 12px; box-shadow: 0 0 0 9999px rgba(10,25,24,.6), 0 0 0 3px #f5a623;
                 transition: all .25s; pointer-events: none; display: none; }
    .tour-hole.on { display: block; }
    .tour-card { position: absolute; left: 14px; right: 14px; background: #fff; border-radius: 14px; padding: 14px 14px 12px;
                 box-shadow: 0 10px 30px rgba(0,0,0,.3); font-size: 13.5px; line-height: 1.5; max-height: 62%; overflow-y: auto; }
    .tour-top { display: flex; justify-content: space-between; align-items: center; font-size: 11.5px; color: #8a8f8e; font-weight: 600; }
    .tour-top button { border: 0; background: none; color: #8a8f8e; font: inherit; cursor: pointer; text-decoration: underline; }
    .tour-card h4 { margin: 4px 0 6px; font-size: 16px; color: #2b958f; }
    .tour-card ul { margin: 6px 0; padding-left: 18px; }
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
    .tour-launch b { display: block; color: #5c3d00; font-size: 14.5px; }`;
  document.head.appendChild(css);
  const phone = document.getElementById("phone");
  phone.appendChild(root);

  function place(el) {
    const hole = $("#tourHole"), card = $("#tourCard"), dim = $("#tourDim");
    const P = phone.getBoundingClientRect();
    if (!el) {
      hole.classList.remove("on"); dim.classList.add("on");
      card.style.top = "50%"; card.style.bottom = "auto"; card.style.transform = "translateY(-50%)";
      return;
    }
    dim.classList.remove("on"); hole.classList.add("on");
    const S = document.getElementById("scroll").getBoundingClientRect(), R = el.getBoundingClientRect();
    const inSheet = el.closest("#sheet");
    const top = Math.max(R.top, inSheet ? P.top : S.top), bottom = Math.min(R.bottom, inSheet ? P.bottom : S.bottom);
    const pad = 6;
    Object.assign(hole.style, { left: R.left - P.left - pad + "px", top: top - P.top - pad + "px",
                                width: R.width + pad * 2 + "px", height: Math.max(bottom - top, 24) + pad * 2 + "px" });
    // Đo chiều cao thật của thẻ rồi chọn chỗ: dưới vùng sáng → trên vùng sáng → đáy màn hình (vùng sáng quá cao).
    // Luôn kẹp trong khung để không bị cắt mất tiêu đề như bản đầu.
    card.style.transform = "none"; card.style.bottom = "auto";
    const m = 12, h = card.offsetHeight;
    const holeTop = top - P.top - pad, holeBottom = bottom - P.top + pad;
    let y;
    if (holeBottom + m + h <= P.height - m) y = holeBottom + m;
    else if (holeTop - m - h >= m) y = holeTop - m - h;
    else y = P.height - h - m - 18;
    card.style.top = Math.max(m, Math.min(y, P.height - h - m)) + "px";
  }

  async function show(i) {
    idx = i;
    const s = STEPS[i];
    const btns = $("#tourBtns");
    btns.innerHTML = `<button class="main" disabled>Đang chạy…</button>`;
    if (s.before) await s.before();
    await wait(120);
    let el = s.target ? s.target() : null;
    if (el && !el.closest("#sheet") && !s.noScroll) { el.scrollIntoView({ block: "nearest" }); await wait(120); }
    $("#tourCount").textContent = `Bước ${i + 1}/${STEPS.length}`;
    $("#tourTitle").textContent = s.title;
    $("#tourBody").innerHTML = s.body;
    $("#tourLook").textContent = s.look || "";
    $("#tourLook").style.display = s.look ? "block" : "none";
    place(el);
    const last = i === STEPS.length - 1;
    btns.innerHTML = last
      ? `<button onclick="window.__tour.restart()">Xem lại tour</button><button class="main" onclick="window.__tour.end(true)">Tự thử</button>`
      : `<button class="main" onclick="window.__tour.next()">${i === 0 ? "Bắt đầu" : "Tiếp"}</button>`;
    document.getElementById("tourCard").scrollTop = 0;
  }

  function begin() {
    if (running) return;
    running = true;
    prevTester = document.getElementById("tester").value;
    // Bắt đầu sạch như một người thử mới; mã TOUR để log không lẫn với lượt thử thật
    state = fresh(); pendingTests = new Set();
    document.getElementById("msgs").innerHTML = "";
    document.getElementById("tester").value = "TOUR";
    root.classList.add("on");
    show(0);
  }
  function end(selfTry) {
    running = false;
    root.classList.remove("on");
    closeSheet();
    document.getElementById("tester").value = prevTester === "TOUR" ? "" : prevTester;
    if (selfTry) restart();
  }
  window.__tour = { begin, end, next: () => show(idx + 1), restart: () => { end(false); begin(); } };
  document.getElementById("tourExit").onclick = () => end(false);
  window.addEventListener("resize", () => running && place(STEPS[idx].target ? STEPS[idx].target() : null));

  // Nút mở tour ở Trang chủ
  const launch = document.createElement("button");
  launch.className = "tour-launch";
  launch.innerHTML = `<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#f5a623" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="m10 8 6 4-6 4z" fill="#f5a623"/></svg>
    <span><b>Tour 3 phút cho người chấm</b>App tự bấm qua từng tính năng và ghi chú điều nên để ý</span>`;
  launch.onclick = begin;
  const homePad = document.querySelector("#s-home .pad");
  homePad.insertBefore(launch, homePad.firstChild);

  if (new URLSearchParams(location.search).get("tour") === "1") setTimeout(begin, 400);
})();
