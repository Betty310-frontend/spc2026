const pathParts = window.location.pathname.split("/");
const productId = Number(pathParts[pathParts.length - 1]);

const productNameEl = document.getElementById("product-name");
const productDescriptionEl = document.getElementById("product-description");
const productImageEl = document.getElementById("product-image");
const reviewSummaryEl = document.getElementById("review-summary");
const aiSummaryTextEl = document.getElementById("ai-summary-text");
const averageRatingValueEl = document.getElementById("average-rating-value");
const reviewListEl = document.getElementById("review-list");
const reviewFormEl = document.getElementById("review-form");
const sendBtnEl = document.getElementById("send-btn");
const sortSelectEl = document.getElementById("sort-select");
const ratingStarsEl = document.getElementById("rating-stars");
const ratingTextEl = document.getElementById("rating-text");
let currentReviews = [];

const SKELETON_LINE_FULL = '<span class="skeleton h-4 w-full mb-2"></span>';
const SKELETON_LINE_80 = '<span class="skeleton h-4 mb-2" style="width:80%"></span>';
const SKELETON_LINE_60 = '<span class="skeleton h-4" style="width:60%"></span>';

function showProductSkeleton() {
  productNameEl.innerHTML = '<span class="skeleton h-8 mb-3" style="width:60%"></span>';
  productDescriptionEl.innerHTML = SKELETON_LINE_FULL + SKELETON_LINE_80 + SKELETON_LINE_60;
}

function showReviewSkeleton() {
  aiSummaryTextEl.innerHTML = SKELETON_LINE_FULL + SKELETON_LINE_80 + SKELETON_LINE_60;
  averageRatingValueEl.innerHTML = '<span class="skeleton h-6" style="width:140px"></span>';

  const skeletonReview = `
    <div class="border border-gray-200 rounded-lg p-4">
      <div class="flex items-center justify-between mb-3">
        <span class="skeleton h-4" style="width:120px"></span>
        <span class="skeleton h-4" style="width:90px"></span>
      </div>
      <span class="skeleton h-4 w-full mb-2"></span>
      <span class="skeleton h-4" style="width:70%"></span>
    </div>
  `;
  reviewListEl.innerHTML = Array(3).fill(skeletonReview).join("");
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function loadProduct() {
  const response = await fetch(`/api/products/${productId}?lang=${getCurrentLang()}`);
  if (!response.ok) {
    throw new Error("상품 정보를 불러오지 못했습니다.");
  }

  const data = await response.json();
  const product = data.product;

  document.title = `${product.name} | ${t("site_name")}`;
  productNameEl.textContent = product.name;
  productDescriptionEl.textContent = product.description;
  productImageEl.src = product.image;
  productImageEl.alt = product.name;
  productImageEl.className = "w-full h-72 object-cover rounded-lg bg-gray-100";
}

function renderReviewSummary(aiSummary, averageRating) {
  const stars = Number.isFinite(averageRating)
    ? `${"★".repeat(Math.round(averageRating))}${"☆".repeat(5 - Math.round(averageRating))}`
    : "N/A";

  aiSummaryTextEl.textContent = aiSummary || t("no_reviews");
  averageRatingValueEl.textContent = stars !== "N/A" ? `${averageRating} (${stars})` : "N/A";
}

function updateRatingStars(selectedValue) {
  const starEls = ratingStarsEl.querySelectorAll("[data-star]");
  const score = Number(selectedValue || 0);

  starEls.forEach((starEl) => {
    const value = Number(starEl.dataset.star);
    if (value <= score) {
      starEl.classList.remove("text-gray-300");
      starEl.classList.add("text-amber-500");
    } else {
      starEl.classList.remove("text-amber-500");
      starEl.classList.add("text-gray-300");
    }
  });

  ratingTextEl.textContent =
    score > 0 ? t("rating_selected").replace("{score}", score) : t("rating_placeholder");
}

function formatCreatedAt(createdAt) {
  if (!createdAt) {
    return t("no_time_info");
  }

  const date = new Date(createdAt);
  if (Number.isNaN(date.getTime())) {
    return t("no_time_info");
  }

  const langLocaleMap = { ko: "ko-KR", en: "en-US", ja: "ja-JP", zh: "zh-CN" };
  const currentLang = localStorage.getItem("lang") || "ko";
  return date.toLocaleString(langLocaleMap[currentLang] || "ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function sortReviews(reviews) {
  const sortType = sortSelectEl.value;
  const copied = [...reviews];

  if (sortType === "rating") {
    return copied.sort((a, b) => {
      if (b.rating !== a.rating) {
        return b.rating - a.rating;
      }

      return new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime();
    });
  }

  return copied.sort(
    (a, b) => new Date(b.created_at || 0).getTime() - new Date(a.created_at || 0).getTime(),
  );
}

function renderReviews(reviews) {
  if (!Array.isArray(reviews) || reviews.length === 0) {
    reviewListEl.innerHTML = `<p class="text-gray-500">${t("no_reviews")}</p>`;
    return;
  }

  const sorted = sortReviews(reviews);

  reviewListEl.innerHTML = sorted
    .map(
      (review) => `
              <article class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-center justify-between gap-3 mb-2">
                  <p class="font-semibold">${t("review_rating_label").replace("{rating}", review.rating)} <span class="text-amber-500">${"★".repeat(review.rating)}${"☆".repeat(5 - review.rating)}</span></p>
                  <p class="text-xs text-gray-500">${formatCreatedAt(review.created_at)}</p>
                </div>
                <p class="text-gray-700 whitespace-pre-wrap">${escapeHtml(review.comment || t("no_content"))}</p>
              </article>
            `,
    )
    .join("");
}

async function loadReviews() {
  const lang = getCurrentLang();
  const [reviewsResponse, summaryResponse] = await Promise.all([
    fetch(`/api/products/${productId}/reviews?lang=${lang}`),
    fetch(`/api/products/${productId}/ai-summary?lang=${lang}`),
  ]);

  if (!reviewsResponse.ok || !summaryResponse.ok) {
    throw new Error("리뷰 정보를 불러오지 못했습니다.");
  }

  const reviewsData = await reviewsResponse.json();
  const summaryData = await summaryResponse.json();
  currentReviews = reviewsData.reviews || [];
  renderReviewSummary(summaryData.ai_summary, summaryData.average_rating);
  renderReviews(currentReviews);
}

sortSelectEl.addEventListener("change", () => {
  renderReviews(currentReviews);
});

reviewFormEl.querySelectorAll('input[name="rating"]').forEach((inputEl) => {
  inputEl.addEventListener("change", (event) => {
    updateRatingStars(event.target.value);
  });
});

reviewFormEl.addEventListener("submit", async (event) => {
  event.preventDefault();

  const selectedRating = reviewFormEl.querySelector('input[name="rating"]:checked');
  const comment = document.getElementById("comment").value.trim();

  if (!selectedRating) {
    alert(t("select_rating_alert"));
    return;
  }

  sendBtnEl.disabled = true;
  sendBtnEl.textContent = t("submitting");

  const response = await fetch(`/api/products/${productId}/reviews`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      rating: Number(selectedRating.value),
      comment,
    }),
  });

  if (!response.ok) {
    alert(t("review_submit_failed"));
    sendBtnEl.disabled = false;
    sendBtnEl.textContent = t("submit_review_short");
    return;
  }

  reviewFormEl.reset();
  updateRatingStars(0);
  await loadReviews();
  sendBtnEl.disabled = false;
  sendBtnEl.textContent = t("submit_review_short");
});

async function initPage() {
  if (!Number.isInteger(productId) || productId <= 0) {
    productNameEl.textContent = t("invalid_product");
    productDescriptionEl.textContent = t("check_product_id");
    return;
  }

  showProductSkeleton();
  showReviewSkeleton();

  try {
    await loadProduct();
    await loadReviews();
  } catch (error) {
    productNameEl.textContent = t("product_load_failed");
    productDescriptionEl.textContent = t("retry_later");
    reviewSummaryEl.innerHTML = `<p class="text-red-500">${t("reviews_load_failed")}</p>`;
    reviewListEl.innerHTML = "";
  }
}

updateRatingStars(0);
initPage();

document.addEventListener("languageChange", async () => {
  showProductSkeleton();
  showReviewSkeleton();
  await loadProduct();
  await loadReviews();
});
