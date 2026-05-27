// 다국어 지원 스크립트
// - /locales/{lang}.json 파일을 로드해 DOM의 data-i18n 속성에 적용합니다.
// - t(key) 함수를 전역으로 제공하여 JS 파일에서도 번역 텍스트를 사용할 수 있습니다.

let _translations = {};

/** 번역 키로 텍스트를 반환합니다. 로드 전이면 키를 그대로 반환합니다. */
function t(key) {
  return _translations[key] ?? key;
}

/** 현재 선택된 언어 코드를 반환합니다. */
function getCurrentLang() {
  return localStorage.getItem("lang") || "ko";
}

async function loadTranslations(lang) {
  try {
    const res = await fetch(`/locales/${lang}.json`);
    if (!res.ok) throw new Error(`locale not found: ${lang}`);
    _translations = await res.json();
  } catch {
    // 대상 언어 파일이 없으면 한국어로 폴백
    if (lang !== "ko") {
      const fallback = await fetch("/locales/ko.json");
      _translations = await fallback.json();
    }
  }
}

/** data-i18n / data-i18n-placeholder 속성을 가진 요소에 번역을 적용합니다. */
function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });
  // <html lang> 속성 갱신
  const langMap = { ko: "ko", en: "en", ja: "ja", zh: "zh" };
  const lang = localStorage.getItem("lang") || "ko";
  document.documentElement.lang = langMap[lang] || "ko";
}

function initLanguageSelect() {
  const sel = document.getElementById("language-select");
  if (!sel) return;

  const saved = localStorage.getItem("lang") || "ko";
  sel.value = saved;

  sel.addEventListener("change", async (e) => {
    const lang = e.target.value;
    localStorage.setItem("lang", lang);
    await loadTranslations(lang);
    applyTranslations();
    document.dispatchEvent(new CustomEvent("translationsReady"));
    document.dispatchEvent(new CustomEvent("languageChange", { detail: { lang } }));
  });
}

// 헤더 로드 완료 → 번역 파일 로드 + 언어 셀렉터 초기화 + translationsReady 발행
document.addEventListener("headerLoaded", async () => {
  const lang = localStorage.getItem("lang") || "ko";
  await loadTranslations(lang);
  initLanguageSelect();
  document.dispatchEvent(new CustomEvent("translationsReady"));
});

// 헤더+푸터 모두 로드 완료 → DOM 전체에 번역 적용
document.addEventListener("layoutLoaded", () => {
  applyTranslations();
});
