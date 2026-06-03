// ── state ──────────────────────────────────────────────────
const SESSION_ID = "user-" + Math.random().toString(36).slice(2, 8);
let prevPrices = {};

// ── ticker helpers ─────────────────────────────────────────
function setTickerItem(id1, id2, text, cls) {
  [id1, id2].forEach((id) => {
    const el = document.getElementById(id);
    if (!el) return;
    el.textContent = text;
    el.className = "ticker-item " + (cls || "");
  });
}

function updateTicker(data) {
  const r = data.usd_krw;
  const rCls = r.change > 0 ? "up" : r.change < 0 ? "down" : "";
  setTickerItem(
    "tk-usd",
    "tk-usd2",
    `USD/KRW ${r.rate.toFixed(2)}원 ${r.change >= 0 ? "▲" : "▼"}${Math.abs(r.change).toFixed(2)}`,
    rCls,
  );

  data.stocks.forEach((s) => {
    const cls = s.change > 0 ? "up" : s.change < 0 ? "down" : "";
    const arrow = s.change > 0 ? "▲" : s.change < 0 ? "▼" : "─";
    setTickerItem(
      `tk-${s.symbol}`,
      `tk-${s.symbol}2`,
      `${s.symbol} $${s.price.toFixed(2)} ${arrow}${Math.abs(s.change_pct).toFixed(2)}%`,
      cls,
    );
  });

  document.getElementById("marketTime").textContent = data.timestamp;
}

// ── stock grid ──────────────────────────────────────────────
function buildStockGrid(stocks) {
  const grid = document.getElementById("stockGrid");
  if (!grid.children.length) {
    stocks.forEach((s) => {
      const card = document.createElement("div");
      card.className = "stock-card";
      card.id = `card-${s.symbol}`;
      card.innerHTML = `
        <div class="stock-sym">${s.symbol}</div>
        <div class="stock-name">${s.name}</div>
        <div class="stock-price" id="price-${s.symbol}">$${s.price.toFixed(2)}</div>
        <div class="stock-change flat" id="chg-${s.symbol}">─</div>`;
      grid.appendChild(card);
    });
  } else {
    stocks.forEach((s) => {
      const priceEl = document.getElementById(`price-${s.symbol}`);
      const chgEl = document.getElementById(`chg-${s.symbol}`);
      const card = document.getElementById(`card-${s.symbol}`);
      if (!priceEl) return;
      priceEl.textContent = `$${s.price.toFixed(2)}`;
      const cls = s.change > 0 ? "up" : s.change < 0 ? "down" : "flat";
      const arrow = s.change > 0 ? "▲" : s.change < 0 ? "▼" : "─";
      chgEl.className = `stock-change ${cls}`;
      chgEl.textContent = `${arrow} $${Math.abs(s.change).toFixed(2)} (${s.change_pct >= 0 ? "+" : ""}${s.change_pct.toFixed(2)}%)`;

      if (s.symbol in prevPrices) {
        if (s.price > prevPrices[s.symbol]) {
          flashCard(card, "flash-up");
        } else if (s.price < prevPrices[s.symbol]) {
          flashCard(card, "flash-down");
        }
      }
      prevPrices[s.symbol] = s.price;
    });
  }
}

function flashCard(card, cls) {
  card.classList.add(cls);
  setTimeout(() => card.classList.remove(cls), 600);
}

// ── exchange rate ───────────────────────────────────────────
function updateRate(usd_krw) {
  document.getElementById("rateValue").textContent = `${usd_krw.rate.toFixed(2)}원`;
  const chgEl = document.getElementById("rateChange");
  const c = usd_krw.change;
  chgEl.className = "rate-change " + (c > 0 ? "up" : c < 0 ? "down" : "flat");
  chgEl.style.color = c > 0 ? "var(--green)" : c < 0 ? "var(--red)" : "var(--text2)";
  chgEl.textContent = `${c >= 0 ? "▲" : "▼"} ${Math.abs(c).toFixed(2)}`;
}

// ── portfolio ───────────────────────────────────────────────
function updatePortfolio(data) {
  document.getElementById("assetKrw").textContent = `₩${data.krw.toLocaleString()}`;
  document.getElementById("assetUsd").textContent = `$${data.usd.toFixed(2)}`;
  document.getElementById("assetTotal").textContent = `₩${Number(data.total_krw).toLocaleString()}`;

  const holdingsEl = document.getElementById("stockHoldings");
  if (!data.stocks.length) {
    holdingsEl.innerHTML = '<div class="empty-state">보유 주식 없음</div>';
    return;
  }
  holdingsEl.innerHTML = data.stocks
    .map(
      (s) => `
    <div class="stock-holdings-item">
      <span>${s.symbol} × ${s.qty}</span>
      <span>$${s.value_usd.toFixed(2)} / ₩${Number(s.value_krw).toLocaleString()}</span>
    </div>`,
    )
    .join("");
}

// ── reservations ────────────────────────────────────────────
function updateReservations(list) {
  const el = document.getElementById("rsvList");
  const countEl = document.getElementById("rsvCount");
  const active = list.filter((r) => r.status === "active" || r.status === "pending_approval");
  countEl.textContent = active.length;

  if (!list.length) {
    el.innerHTML = '<div class="empty-state">예약 없음</div>';
    return;
  }
  el.innerHTML = list
    .map(
      (r) => `
    <div class="rsv-item">
      <span class="rsv-label">${r.label}</span>
      <span class="rsv-badge ${r.status}">${statusLabel(r.status)}</span>
      ${r.status === "active" ? `<button class="rsv-delete" onclick="deleteReservation(${r.id})" title="삭제"><i class="bi bi-x"></i></button>` : ""}
    </div>`,
    )
    .join("");
}

function statusLabel(s) {
  const map = { active: "대기중", pending_approval: "승인요청", done: "완료", rejected: "거절" };
  return map[s] || s;
}

async function deleteReservation(id) {
  await fetch(`/api/reservations/${id}`, { method: "DELETE" });
}

// ── approvals ───────────────────────────────────────────────
function updateApprovals(list) {
  const el = document.getElementById("approvalList");
  const countEl = document.getElementById("approvalCount");
  countEl.textContent = list.length;

  if (!list.length) {
    el.innerHTML = '<div class="empty-state">승인 대기 없음</div>';
    return;
  }
  el.innerHTML = list
    .map(
      (a) => `
    <div class="approval-item">
      <div class="approval-label"><i class="bi bi-exclamation-triangle-fill"></i> ${a.rsv.label}</div>
      <div style="font-size:11px;color:var(--text2);margin-bottom:6px">현재가: ${a.current_value} · ${a.created_at}</div>
      <div class="approval-btns">
        <button class="btn-approve" onclick="handleApproval(${a.id},'approve')"><i class="bi bi-check-lg"></i> 승인</button>
        <button class="btn-reject"  onclick="handleApproval(${a.id},'reject')"><i class="bi bi-x-lg"></i> 거절</button>
      </div>
    </div>`,
    )
    .join("");
}

async function handleApproval(id, action) {
  await fetch(`/api/approvals/${id}/${action}`, { method: "POST" });
}

// ── logs ────────────────────────────────────────────────────
function updateLogs(logs) {
  const el = document.getElementById("logList");
  if (!logs.length) {
    el.innerHTML = '<div class="empty-state">로그 없음</div>';
    return;
  }
  el.innerHTML = logs
    .map(
      (l) => `
    <div class="log-item">
      <span class="log-time">${l.time}</span>
      <span class="log-msg">${l.message}</span>
    </div>`,
    )
    .join("");
}

// ── polling ─────────────────────────────────────────────────
async function fetchMarket() {
  try {
    const res = await fetch("/api/market");
    const data = await res.json();
    updateTicker(data);
    buildStockGrid(data.stocks);
    updateRate(data.usd_krw);
  } catch (e) {
    console.error("market error", e);
  }
}

async function fetchPortfolio() {
  try {
    const res = await fetch("/api/portfolio");
    updatePortfolio(await res.json());
  } catch (e) {}
}

async function fetchReservations() {
  try {
    const res = await fetch("/api/reservations");
    const data = await res.json();
    updateReservations(data.reservations);
  } catch (e) {}
}

async function fetchApprovals() {
  try {
    const res = await fetch("/api/approvals");
    const data = await res.json();
    updateApprovals(data.approvals);
  } catch (e) {}
}

async function fetchLogs() {
  try {
    const res = await fetch("/api/logs");
    const data = await res.json();
    updateLogs(data.logs);
  } catch (e) {}
}

async function fetchAll() {
  await Promise.all([
    fetchMarket(),
    fetchPortfolio(),
    fetchReservations(),
    fetchApprovals(),
    fetchLogs(),
  ]);
}

// ── chat ────────────────────────────────────────────────────
function appendMsg(role, text) {
  const container = document.getElementById("chatMessages");
  const div = document.createElement("div");
  div.className = `chat-msg ${role}`;
  div.innerHTML = `<div class="chat-bubble">${escHtml(text).trim()}</div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function appendTyping() {
  const container = document.getElementById("chatMessages");
  const div = document.createElement("div");
  div.className = "chat-msg bot";
  div.id = "typingIndicator";
  div.innerHTML = `<div class="chat-bubble typing-dots"><span></span><span></span><span></span></div>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById("typingIndicator");
  if (el) el.remove();
}

async function sendChat() {
  const input = document.getElementById("chatInput");
  const btn = document.getElementById("chatSendBtn");
  const msg = input.value.trim();
  if (!msg) return;
  input.value = "";
  btn.disabled = true;

  appendMsg("user", msg);
  appendTyping();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg, session_id: SESSION_ID }),
    });
    const data = await res.json();
    removeTyping();
    appendMsg("bot", data.reply || data.error || "오류가 발생했습니다.");
    // refresh data after chat action
    setTimeout(fetchAll, 500);
  } catch (e) {
    removeTyping();
    appendMsg("bot", "서버 오류가 발생했습니다.");
  } finally {
    btn.disabled = false;
    input.focus();
  }
}

function sendExample(text) {
  document.getElementById("chatInput").value = text;
  sendChat();
}

function escHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br>");
}

// ── keyboard shortcut (Enter sends) ────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("chatInput").addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendChat();
    }
  });

  // initial load + polling
  fetchAll();
  setInterval(fetchAll, 2000);
});
