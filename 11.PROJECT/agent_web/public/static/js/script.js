const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const input = document.getElementById("question");
const sendBtn = document.getElementById("send-btn");

// marked 설정: 링크를 새 탭에서 열기
const renderer = new marked.Renderer();
renderer.link = ({ href, title, text }) => {
  const titleAttr = title ? ` title="${title}"` : "";
  return `<a href="${href}"${titleAttr} target="_blank" rel="noopener noreferrer">${text}</a>`;
};
marked.setOptions({ renderer, breaks: true });

let isStreaming = false;
let controller = null;

// 스트리밍 중 버튼 클릭 → 취소
sendBtn.addEventListener("click", (e) => {
  if (isStreaming) {
    e.preventDefault();
    controller?.abort();
  }
});

function setStreamingMode(streaming) {
  isStreaming = streaming;
  if (streaming) {
    sendBtn.innerHTML = `<i class="bi bi-stop-circle-fill"></i>`;
    sendBtn.title = "취소";
    sendBtn.type = "button"; // form submit 방지
    sendBtn.classList.replace("btn-primary", "btn-danger");
    input.disabled = true;
  } else {
    sendBtn.innerHTML = `<i class="bi bi-send-fill"></i>`;
    sendBtn.title = "전송";
    sendBtn.type = "submit";
    sendBtn.classList.replace("btn-danger", "btn-primary");
    input.disabled = false;
    input.focus();
    controller = null;
  }
}

function addBubble(text, role) {
  const row = document.createElement("div");
  row.className = `d-flex mb-3 ${role === "user" ? "justify-content-end" : "justify-content-start"}`;
  const bubble = document.createElement("div");
  bubble.className = `bubble bubble-${role}`;
  if (role === "user") {
    bubble.textContent = text;
  } else {
    bubble.innerHTML = marked.parse(text || "");
  }
  row.appendChild(bubble);
  chatBox.appendChild(row);
  chatBox.scrollTop = chatBox.scrollHeight;
  return bubble;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (isStreaming) return;

  const question = input.value.trim();
  if (!question) return;

  addBubble(question, "user");
  input.value = "";
  setStreamingMode(true);

  // 봇 버블 — 첫 토큰 전까지 로딩 표시
  const botBubble = addBubble("", "bot");
  botBubble.innerHTML = `<span class="spinner-grow spinner-grow-sm me-1" role="status"></span>검색 중...`;
  botBubble.classList.add("cursor");

  let rawText = "";
  let firstToken = true;
  controller = new AbortController();

  try {
    const res = await fetch("/api/ask-stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
      signal: controller.signal,
    });

    if (!res.ok) throw new Error(`서버 오류: ${res.status}`);

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();

      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const raw = line.slice(6).trim();
        if (raw === "[DONE]") {
          botBubble.classList.remove("cursor");
          break;
        }
        try {
          const parsed = JSON.parse(raw);
          if (parsed.token) {
            if (firstToken) {
              botBubble.innerHTML = ""; // 로딩 표시 제거
              firstToken = false;
            }
            rawText += parsed.token;
            botBubble.innerHTML = marked.parse(rawText);
            chatBox.scrollTop = chatBox.scrollHeight;
          } else if (parsed.error) {
            botBubble.innerHTML = `<span class="text-danger">오류: ${parsed.error}</span>`;
            botBubble.classList.remove("cursor");
          }
        } catch (_) {
          /* 파싱 실패 무시 */
        }
      }
    }
  } catch (err) {
    if (err.name === "AbortError") {
      // 사용자가 취소한 경우
      if (rawText) {
        botBubble.innerHTML =
          marked.parse(rawText) +
          `<br><span class="text-muted small fst-italic">(응답이 중단되었습니다.)</span>`;
      } else {
        botBubble.innerHTML = `<span class="text-muted fst-italic">응답이 취소되었습니다.</span>`;
      }
    } else {
      botBubble.innerHTML = `<span class="text-danger">오류가 발생했습니다: ${err.message}</span>`;
    }
  } finally {
    botBubble.classList.remove("cursor");
    setStreamingMode(false);
  }
});
