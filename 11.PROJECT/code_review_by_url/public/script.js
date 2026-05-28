const form = document.getElementById("code-form");
const codeUrlInput = document.getElementById("code-url");
const sourceCodeEl = document.getElementById("source-code");
const resultEl = document.getElementById("result");
const vulnTypeInputs = document.querySelectorAll('input[name="vuln_types"]');

function toRawGithubUrl(url) {
  if (!url) {
    return null;
  }

  try {
    const parsed = new URL(url.trim());

    if (parsed.hostname === "raw.githubusercontent.com") {
      return parsed.toString();
    }

    if (parsed.hostname === "github.com") {
      const parts = parsed.pathname.split("/").filter(Boolean);

      // github.com/{owner}/{repo}/blob/{branch}/{path...}
      if (parts.length >= 5 && parts[2] === "blob") {
        const owner = parts[0];
        const repo = parts[1];
        const branch = parts[3];
        const filePath = parts.slice(4).join("/");
        return `https://raw.githubusercontent.com/${owner}/${repo}/${branch}/${filePath}`;
      }
    }
  } catch (_error) {
    return null;
  }

  return null;
}

function withLineNumbers(code) {
  const lines = code.replace(/\r\n/g, "\n").split("\n");
  const width = String(lines.length).length;

  return lines
    .map((line, index) => `${String(index + 1).padStart(width, " ")} | ${line}`)
    .join("\n");
}

async function fetchSourceCode(rawUrl) {
  const response = await fetch(rawUrl);
  if (!response.ok) {
    throw new Error(`소스코드를 읽지 못했습니다. (HTTP ${response.status})`);
  }
  return response.text();
}

async function analyzeSourceCode(sourceCode, vulnerabilityTypes) {
  const response = await fetch("/api/analyze", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      source_code: sourceCode,
      vulnerability_types: vulnerabilityTypes,
    }),
  });

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "분석 요청에 실패했습니다.");
  }

  return data;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function severityBadgeClass(severity) {
  if (severity === "높음") {
    return "bg-red-100 text-red-700 border-red-200";
  }
  if (severity === "중간") {
    return "bg-amber-100 text-amber-700 border-amber-200";
  }
  return "bg-emerald-100 text-emerald-700 border-emerald-200";
}

function renderFindings(summary, findings) {
  if (!findings.length) {
    resultEl.innerHTML = `
            <div class="rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-emerald-800">
              <p class="font-semibold">취약점이 발견되지 않았습니다.</p>
              <p class="text-sm mt-1">${escapeHtml(summary || "선택한 항목 기준으로 안전한 상태입니다.")}</p>
            </div>
          `;
    return;
  }

  const cards = findings
    .map((item, index) => {
      const lines = (item.line_numbers || []).length
        ? item.line_numbers.join(", ")
        : "라인 정보 없음";
      const vulnType = escapeHtml(item.vulnerability_type || "알 수 없음");
      const severity = escapeHtml(item.severity || "중간");
      const description = escapeHtml(item.description || "설명 없음");
      const recommendation = escapeHtml(item.recommendation || "권장사항 없음");
      const problematicCode = escapeHtml(item.problematic_code || "코드 정보 없음");

      return `
              <article class="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
                <div class="mb-3 flex flex-wrap items-center justify-between gap-2">
                  <h3 class="text-base font-semibold text-slate-900">${index + 1}. ${vulnType}</h3>
                  <span class="rounded-full border px-3 py-1 text-xs font-semibold ${severityBadgeClass(severity)}">위험 수준: ${severity}</span>
                </div>
                <p class="mb-2 text-sm text-slate-700"><span class="font-semibold">라인 번호:</span> ${escapeHtml(lines)}</p>
                <div class="mb-2 rounded-lg bg-slate-900 p-3">
                  <p class="mb-1 text-xs font-semibold text-slate-200">문제가 되는 코드</p>
                  <pre class="overflow-x-auto whitespace-pre-wrap text-xs text-slate-100">${problematicCode}</pre>
                </div>
                <p class="mb-2 text-sm text-slate-700"><span class="font-semibold">설명:</span> ${description}</p>
                <p class="text-sm text-slate-700"><span class="font-semibold">개선 권장사항:</span> ${recommendation}</p>
              </article>
            `;
    })
    .join("");

  resultEl.innerHTML = `
          <div class="mb-3 rounded-xl border border-blue-200 bg-blue-50 p-3 text-blue-900">
            <p class="text-sm"><span class="font-semibold">분석 요약:</span> ${escapeHtml(summary || "분석 결과를 확인하세요.")}</p>
          </div>
          <div class="space-y-3">${cards}</div>
        `;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const inputUrl = codeUrlInput.value.trim();
  const rawUrl = toRawGithubUrl(inputUrl);
  const selectedVulnTypes = Array.from(vulnTypeInputs)
    .filter((input) => input.checked)
    .map((input) => input.value);

  if (!rawUrl) {
    resultEl.innerHTML = '<p class="text-red-600">올바른 GitHub 파일 URL을 입력해주세요.</p>';
    sourceCodeEl.textContent = "";
    return;
  }

  if (!selectedVulnTypes.length) {
    resultEl.innerHTML = '<p class="text-red-600">최소 1개 이상의 취약점 유형을 선택해주세요.</p>';
    return;
  }

  resultEl.innerHTML =
    '<div class="rounded-xl border border-slate-200 bg-slate-50 p-3 text-slate-700">소스코드를 분석 중입니다...</div>';
  sourceCodeEl.textContent = "";

  try {
    const sourceCode = await fetchSourceCode(rawUrl);
    sourceCodeEl.textContent = withLineNumbers(sourceCode);

    const analysisResult = await analyzeSourceCode(sourceCode, selectedVulnTypes);
    renderFindings(analysisResult.summary, analysisResult.findings || []);
  } catch (error) {
    sourceCodeEl.textContent = "";
    resultEl.innerHTML = `<p class="text-red-600">${error.message}</p>`;
  }
});
