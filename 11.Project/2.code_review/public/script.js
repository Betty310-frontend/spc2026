const form = document.getElementById("code-form");

function renderMarkdown(text) {
  const markdown = typeof text === "string" ? text : "";
  const unsafeHtml = marked.parse(markdown, { breaks: true });
  return DOMPurify.sanitize(unsafeHtml);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const code = document.getElementById("code-input").value;
  const result = document.getElementById("result");
  try {
    result.innerHTML = "분석 중...";
    // fetch API를 사용하여 서버로 코드 전송
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code }),
    });
    //   결과를 받아와서 result에 출력
    const data = await response.json();
    result.innerHTML = renderMarkdown(data.result);
  } catch (error) {
    result.innerHTML = renderMarkdown("### 오류\n분석 중 오류가 발생했습니다.");
  }
});
