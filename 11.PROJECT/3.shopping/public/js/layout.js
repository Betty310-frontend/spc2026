// 공통 레이아웃 컴포넌트(header, footer)를 fetch해서 플레이스홀더에 주입합니다.
async function loadComponent(selector, url) {
  const el = document.querySelector(selector);
  if (!el) return;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error(`Failed to load ${url}`);
    el.innerHTML = await res.text();
  } catch (e) {
    console.error(e);
  }
}

document.addEventListener("DOMContentLoaded", async () => {
  await loadComponent("#layout-header", "/components/header.html");
  document.dispatchEvent(new CustomEvent("headerLoaded"));
  await loadComponent("#layout-footer", "/components/footer.html");
  document.dispatchEvent(new CustomEvent("layoutLoaded"));
});
