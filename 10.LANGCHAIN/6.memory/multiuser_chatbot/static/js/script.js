// ── 자동 스크롤 ───────────────────────────────────────────────
function scrollToBottom() {
  const box = document.getElementById("chat-box");
  box.scrollTop = box.scrollHeight;
}
scrollToBottom();

// ── 메시지 버블 추가 ──────────────────────────────────────────
function appendMessage(role, content) {
  const empty = document.getElementById("empty-state");
  if (empty) empty.remove();

  const box = document.getElementById("chat-box");
  const row = document.createElement("div");
  row.className = `msg-row ${role}`;
  row.innerHTML = `
        <div class="avatar">${role === "user" ? "👤" : "🤖"}</div>
        <div class="bubble">${escapeHtml(content)}</div>
    `;
  box.appendChild(row);
  scrollToBottom();
  return row;
}

// ── 타이핑 인디케이터 ─────────────────────────────────────────
function showTyping() {
  const box = document.getElementById("chat-box");
  const row = document.createElement("div");
  row.className = "msg-row ai";
  row.id = "typing-indicator";
  row.innerHTML = `
        <div class="avatar">🤖</div>
        <div class="bubble typing-dots">
        <span></span><span></span><span></span>
        </div>
    `;
  box.appendChild(row);
  scrollToBottom();
}

function hideTyping() {
  const el = document.getElementById("typing-indicator");
  if (el) el.remove();
}

// ── XSS 방지 ─────────────────────────────────────────────────
function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;")
    .replace(/\n/g, "<br>");
}

// ── 메시지 전송 ───────────────────────────────────────────────
let isSending = false;

async function sendMessage() {
  if (isSending) return;

  const input = document.getElementById("user-input");
  const btn = document.getElementById("send-btn");
  const message = input.value.trim();
  if (!message) return;

  isSending = true;
  input.value = "";
  input.style.height = "auto";
  btn.disabled = true;

  appendMessage("user", message);
  showTyping();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await res.json();
    hideTyping();

    if (res.ok) {
      appendMessage("ai", data.answer);
      msgCount = Math.min(msgCount + 2, MAX_HISTORY);
      updateCounter();
    } else {
      appendMessage("ai", `⚠️ 오류: ${data.error}`);
    }
  } catch (err) {
    hideTyping();
    appendMessage("ai", "⚠️ 서버 연결에 실패했습니다.");
  } finally {
    btn.disabled = false;
    isSending = false;
    input.focus();
  }
}

// ── 대화 초기화 ───────────────────────────────────────────────
async function clearHistory() {
  if (!confirm("대화 기록을 모두 삭제할까요?")) return;

  await fetch("/api/history/clear", { method: "POST" });
  document.getElementById("chat-box").innerHTML = `
        <div class="empty-state" id="empty-state">
        <div class="icon">💬</div>
        <p>무엇이든 물어보세요!</p>
        </div>`;
  msgCount = 0;
  updateCounter();
}

// ── Enter 키 처리 ─────────────────────────────────────────────
document.getElementById("user-input").addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// ── textarea 자동 높이 조절 ───────────────────────────────────
document.getElementById("user-input").addEventListener("input", function () {
  this.style.height = "auto";
  this.style.height = Math.min(this.scrollHeight, 120) + "px";
});
