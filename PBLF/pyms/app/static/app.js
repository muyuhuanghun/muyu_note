/* 前端控制台逻辑 */
const state = {
  selectedTaskId: null,
  eventSource: null,
  resultsPage: 1,
  resultsView: "clean",
  resultsQuery: "",
  resultsTotal: 0,
};

// DOM 元素
const $ = (id) => document.getElementById(id);

function init() {
  $("submit-form").addEventListener("submit", onSubmitTask);
  $("refresh-tasks").addEventListener("click", loadTasks);
  $("command-form").addEventListener("submit", onCommand);
  $("delete-task").addEventListener("click", onDeleteTask);
  $("export-json").addEventListener("click", () => onExport("json"));
  $("export-csv").addEventListener("click", () => onExport("csv"));
  $("results-search").addEventListener("click", onResultsSearch);
  $("results-query").addEventListener("keydown", (e) => { if (e.key === "Enter") onResultsSearch(); });
  $("results-view").addEventListener("change", (e) => { state.resultsView = e.target.value; state.resultsPage = 1; refreshResults(); });
  $("results-prev").addEventListener("click", () => { if (state.resultsPage > 1) { state.resultsPage--; refreshResults(); } });
  $("results-next").addEventListener("click", () => { if (state.resultsPage < totalPages(state.resultsTotal)) { state.resultsPage++; refreshResults(); } });
  document.querySelectorAll("[data-cmd]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (!state.selectedTaskId) { showOutput("command-output", { message: "请先选择任务", code: 1001 }); return; }
      $("command-input").value = `${btn.dataset.cmd} task_id=${state.selectedTaskId}`;
    });
  });
  // 词云图按钮 — 直接调用 API，不走命令表单
  $("btn-wordcloud").addEventListener("click", runWordcloud);
  loadTasks();
}

// 提交任务
async function onSubmitTask(e) {
  e.preventDefault();
  const payload = {
    url: $("submit-url").value.trim(),
    limit: Number($("submit-limit").value) || 50,
    depth: Number($("submit-depth").value) || 1,
  };
  const keyword = $("submit-keyword").value.trim();
  if (keyword) payload.keyword = keyword;
  const name = $("submit-task-name").value.trim();
  if (name) payload.task_name = name;
  const res = await api("/v1/crawl/submit", { method: "POST", body: JSON.stringify(payload) });
  showOutput("submit-output", res);
  if (res.code === 0 && res.data?.task_id) {
    selectTask(res.data.task_id);
    await loadTasks();
  }
}

// 执行命令
async function onCommand(e) {
  e.preventDefault();
  const cmd = $("command-input").value.trim();
  if (!cmd) return;
  try {
    const res = await api("/v1/command", { method: "POST", body: JSON.stringify({ command: cmd }) });
    console.log("command response:", JSON.stringify(res).substring(0, 200));
    if (res.code === 0 && res.data && res.data.wordcloud) {
      showOutput("command-output", { message: "词云图已生成，请查看页面底部", task_id: res.data.task_id });
      showWordcloudImage(res.data.wordcloud, res.data.task_id, res.data.sentiment);
    } else {
      showOutput("command-output", res);
    }
    if (res.code === 0 && res.data && res.data.task_id) {
      selectTask(res.data.task_id);
      await loadTasks();
    }
  } catch (err) {
    console.error("command error:", err);
    showOutput("command-output", { error: String(err) });
  }
}

// 删除任务
async function onDeleteTask() {
  if (!state.selectedTaskId) return;
  if (!confirm(`确认删除任务 ${state.selectedTaskId}？`)) return;
  const res = await api(`/v1/tasks/${state.selectedTaskId}`, { method: "DELETE" });
  showOutput("command-output", res);
  if (res.code === 0) {
    closeStream();
    state.selectedTaskId = null;
    $("task-detail").innerHTML = '<div class="empty">选择任务后显示详情</div>';
    $("events-log").innerHTML = "";
    $("stream-status").textContent = "未连接";
    await loadTasks();
  }
}

// 导出
async function onExport(format) {
  if (!state.selectedTaskId) return;
  const resp = await fetch(`/v1/tasks/${state.selectedTaskId}/export`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ format }),
  });
  if (!resp.ok) { showOutput("command-output", await resp.json()); return; }
  const blob = await resp.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `${state.selectedTaskId}.${format}`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

// 显示词云图图片
function showWordcloudImage(base64Data, taskId, sentimentData) {
  const container = $("wordcloud-display");
  if (!container) return;
  const imgSrc = `data:image/png;base64,${base64Data}`;

  let sentimentHtml = "";
  if (sentimentData) {
    const { positive, neutral, negative, total } = sentimentData;
    const maxVal = Math.max(positive, neutral, negative, 1);
    const pct = (v) => Math.round((v / total) * 100);
    sentimentHtml = `
      <div class="sentiment-section">
        <h3 class="sentiment-title">📊 评论倾向分析</h3>
        <div class="sentiment-summary">
          <span class="sentiment-total">共 <strong>${total}</strong> 条评论</span>
        </div>
        <div class="sentiment-bars">
          <div class="sentiment-bar-row">
            <span class="sentiment-label positive">😊 正面</span>
            <div class="sentiment-bar-track">
              <div class="sentiment-bar-fill positive" style="width:${(positive / maxVal) * 100}%"></div>
            </div>
            <span class="sentiment-count">${positive} <small>(${pct(positive)}%)</small></span>
          </div>
          <div class="sentiment-bar-row">
            <span class="sentiment-label neutral">😐 中立</span>
            <div class="sentiment-bar-track">
              <div class="sentiment-bar-fill neutral" style="width:${(neutral / maxVal) * 100}%"></div>
            </div>
            <span class="sentiment-count">${neutral} <small>(${pct(neutral)}%)</small></span>
          </div>
          <div class="sentiment-bar-row">
            <span class="sentiment-label negative">😟 负面</span>
            <div class="sentiment-bar-track">
              <div class="sentiment-bar-fill negative" style="width:${(negative / maxVal) * 100}%"></div>
            </div>
            <span class="sentiment-count">${negative} <small>(${pct(negative)}%)</small></span>
          </div>
        </div>
      </div>
    `;
  }

  container.innerHTML = `
    <div class="wordcloud-card">
      <h3>词云图 — ${esc(taskId)}</h3>
      <img src="${imgSrc}" alt="词云图" class="wordcloud-img">
      <br>
      <a href="${imgSrc}" download="${taskId}_wordcloud.png" class="wordcloud-download">点击下载词云图</a>
    </div>
    ${sentimentHtml}
  `;
  container.scrollIntoView({ behavior: "smooth" });
}

// 词云图按钮 — 直接调用 API
async function runWordcloud() {
  if (!state.selectedTaskId) {
    showOutput("command-output", { message: "请先选择一个任务", code: 1001 });
    return;
  }
  showOutput("command-output", { message: "正在生成词云图..." });
  try {
    const res = await api("/v1/command", {
      method: "POST",
      body: JSON.stringify({ command: `wordcloud run task_id=${state.selectedTaskId}` }),
    });
    if (res.code === 0 && res.data && res.data.wordcloud) {
      showOutput("command-output", { message: "词云图已生成，请查看页面下方", task_id: res.data.task_id });
      showWordcloudImage(res.data.wordcloud, res.data.task_id, res.data.sentiment);
    } else {
      showOutput("command-output", res);
    }
    if (res.code === 0 && res.data && res.data.task_id) {
      await loadTasks();
    }
  } catch (err) {
    showOutput("command-output", { error: String(err) });
  }
}

// 搜索结果
function onResultsSearch() {
  state.resultsQuery = $("results-query").value.trim();
  state.resultsPage = 1;
  refreshResults();
}

// 加载任务列表
async function loadTasks() {
  const res = await api("/v1/tasks");
  if (res.code !== 0 || !Array.isArray(res.data)) { renderTaskList([]); return; }
  renderTaskList(res.data);
  if (!state.selectedTaskId && res.data.length > 0) {
    selectTask(res.data[0].task_id);
    await refreshSelectedTask();
  }
}

// 渲染任务列表
function renderTaskList(tasks) {
  if (!tasks.length) {
    $("task-list").innerHTML = '<div class="empty">当前没有任务</div>';
    return;
  }
  $("task-list").innerHTML = tasks.map((t) => `
    <button class="task-item ${t.task_id === state.selectedTaskId ? "active" : ""}" data-id="${t.task_id}">
      <div class="name">${esc(t.task_name || t.task_id)}</div>
      <div class="meta">${esc(t.task_id)} · <span class="tag tag-${esc(t.status)}">${esc(t.status)}</span> · progress=${esc(String(t.progress))}%</div>
    </button>
  `).join("");
  $("task-list").querySelectorAll("[data-id]").forEach((btn) => {
    btn.addEventListener("click", () => { selectTask(btn.dataset.id); refreshSelectedTask(); });
  });
}

// 选择任务
function selectTask(taskId) {
  state.selectedTaskId = taskId;
  state.resultsPage = 1;
  closeStream();
  startEventStream(taskId);
}

// 刷新选中任务
async function refreshSelectedTask() {
  if (!state.selectedTaskId) return;
  const res = await api(`/v1/tasks/${state.selectedTaskId}`);
  if (res.code !== 0 || !res.data) return;
  const t = res.data;
  $("task-detail").innerHTML = [
    detailItem("task_id", t.task_id),
    detailItem("status", t.status),
    detailItem("root_url", t.root_url),
    detailItem("keyword", t.keyword || "-"),
    detailItem("progress", `${t.progress}%`),
    detailItem("done", String(t.done_count)),
    detailItem("failed", String(t.failed_count)),
    detailItem("total", String(t.total_count)),
    detailItem("clean_done", String(t.clean_done_count)),
  ].join("");
  await refreshResults();
}

// 刷新结果
async function refreshResults() {
  if (!state.selectedTaskId) return;
  const url = `/v1/tasks/${state.selectedTaskId}/results?view=${state.resultsView}&page=${state.resultsPage}&page_size=15&q=${encodeURIComponent(state.resultsQuery)}`;
  const res = await api(url);
  if (res.code !== 0 || !res.data) return;
  state.resultsTotal = res.data.total;
  $("results-page-label").textContent = `${res.data.page} / ${totalPages(res.data.total)}`;
  if (!res.data.items.length) {
    $("results-table-wrap").innerHTML = '<div class="empty">当前页没有结果</div>';
    return;
  }
  const isRaw = res.data.view === "raw";
  $("results-table-wrap").innerHTML = `
    <table>
      <thead><tr><th>ID</th><th>日期</th><th>标题</th><th>内容</th><th>${isRaw ? "来源URL" : "去重键"}</th></tr></thead>
      <tbody>${res.data.items.map((item) => {
        const title = isRaw ? item.news_title : item.clean_news_title;
        const date = isRaw ? item.news_date : item.clean_news_date;
        const content = isRaw ? item.news_content : item.clean_news_content;
        const extra = isRaw ? (item.source_url || "-") : (item.dedup_key || "-");
        return `<tr><td>${esc(String(item.id))}</td><td>${esc(date || "-")}</td><td>${esc(title || "-")}</td><td>${esc(content || "-")}</td><td>${esc(extra)}</td></tr>`;
      }).join("")}</tbody>
    </table>
  `;
}

// 事件流
function startEventStream(taskId) {
  if (!taskId) return;
  $("stream-status").textContent = "连接中";
  state.eventSource = new EventSource(`/v1/events/stream?task_id=${taskId}`);
  state.eventSource.onopen = () => { $("stream-status").textContent = "已连接"; };
  state.eventSource.onerror = () => { $("stream-status").textContent = "连接结束"; };
  state.eventSource.onmessage = (e) => {
    const data = JSON.parse(e.data);
    const line = document.createElement("div");
    line.className = "log-line";
    line.textContent = `[${data.timestamp}] ${data.event_type} ${JSON.stringify(data.payload)}`;
    $("events-log").prepend(line);
    while ($("events-log").children.length > 100) $("events-log").removeChild($("events-log").lastChild);
    // 刷新任务状态
    if (state.selectedTaskId) {
      refreshSelectedTask();
    }
  };
}

function closeStream() {
  if (state.eventSource) { state.eventSource.close(); state.eventSource = null; }
}

// API 请求
async function api(url, opts = {}) {
  const resp = await fetch(url, { headers: { "Content-Type": "application/json", ...opts.headers }, ...opts });
  if (!resp.ok) {
    const text = await resp.text();
    try { return JSON.parse(text); } catch(e) { return { code: resp.status, message: text, data: null }; }
  }
  return resp.json();
}

// 辅助函数
function showOutput(id, data) { $(id).textContent = JSON.stringify(data, null, 2); }
function detailItem(label, value) { return `<dl class="detail-item"><dt>${esc(label)}</dt><dd>${esc(value)}</dd></dl>`; }
function totalPages(total) { return Math.max(1, Math.ceil(Number(total || 0) / 15)); }
function esc(s) { return String(s).replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;"); }

init();
