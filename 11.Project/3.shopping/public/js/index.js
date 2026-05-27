const productListEl = document.getElementById("product-list");

const SKELETON_CARD = `
  <div class="block border border-gray-200 rounded-lg overflow-hidden">
    <span class="skeleton w-full h-48"></span>
    <div class="p-4">
      <span class="skeleton h-5 mb-3" style="width:70%"></span>
      <span class="skeleton h-4 mb-2 w-full"></span>
      <span class="skeleton h-4" style="width:55%"></span>
    </div>
  </div>
`;

function showProductListSkeleton() {
  productListEl.innerHTML = Array(6).fill(SKELETON_CARD).join("");
}

function renderProducts(products) {
  if (!Array.isArray(products) || products.length === 0) {
    productListEl.innerHTML = `<p class="text-gray-500">${t("no_products")}</p>`;
    return;
  }

  productListEl.innerHTML = products
    .map(
      (product) => `
              <a
                href="/product/${product.id}"
                class="block border border-gray-200 rounded-lg overflow-hidden hover:shadow-lg transition"
              >
                <img
                  src="${product.image}"
                  alt="${product.name}"
                  class="w-full h-48 object-cover"
                />
                <div class="p-4">
                  <h3 class="text-lg font-semibold mb-2">${product.name}</h3>
                  <p class="text-sm text-gray-600">${product.description}</p>
                </div>
              </a>
            `,
    )
    .join("");
}

async function loadProducts() {
  showProductListSkeleton();
  try {
    const response = await fetch(`/api/products?lang=${getCurrentLang()}`);
    if (!response.ok) {
      throw new Error("제품 목록을 불러오지 못했습니다.");
    }

    const data = await response.json();
    renderProducts(data.products || []);
  } catch (error) {
    productListEl.innerHTML = '<p class="text-red-500">제품 목록 로드 중 오류가 발생했습니다.</p>';
  }
}

loadProducts();

document.addEventListener("languageChange", () => {
  loadProducts();
});
