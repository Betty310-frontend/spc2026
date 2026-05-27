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

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

async function loadProduct() {
  const response = await fetch(`/api/products/${productId}`);
  if (!response.ok) {
    throw new Error("상품 정보를 불러오지 못했습니다.");
  }

  const data = await response.json();
  const product = data.product;

  document.title = `${product.name} | SPC 쇼핑몰`;
  productNameEl.textContent = product.name;
  productDescriptionEl.textContent = product.description;
  productImageEl.src = product.image;
  productImageEl.alt = product.name;
}

function renderReviewSummary(aiSummary, averageRating) {
  const stars = Number.isFinite(averageRating)
    ? `${"★".repeat(Math.round(averageRating))}${"☆".repeat(5 - Math.round(averageRating))}`
    : "N/A";

  aiSummaryTextEl.textContent = aiSummary || "아직 등록된 리뷰가 없습니다.";
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

  ratingTextEl.textContent = score > 0 ? `${score}점 선택` : "선택하세요.";
}

function formatCreatedAt(createdAt) {
  if (!createdAt) {
    return "시간 정보 없음";
  }

  const date = new Date(createdAt);
  if (Number.isNaN(date.getTime())) {
    return "시간 정보 없음";
  }

  return date.toLocaleString("ko-KR", {
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
    reviewListEl.innerHTML = '<p class="text-gray-500">아직 등록된 리뷰가 없습니다.</p>';
    return;
  }

  const sorted = sortReviews(reviews);

  reviewListEl.innerHTML = sorted
    .map(
      (review) => `
              <article class="border border-gray-200 rounded-lg p-4">
                <div class="flex items-center justify-between gap-3 mb-2">
                  <p class="font-semibold">평점: ${review.rating} / 5 <span class="text-amber-500">${"★".repeat(review.rating)}${"☆".repeat(5 - review.rating)}</span></p>
                  <p class="text-xs text-gray-500">${formatCreatedAt(review.created_at)}</p>
                </div>
                <p class="text-gray-700 whitespace-pre-wrap">${escapeHtml(review.comment || "내용 없음")}</p>
              </article>
            `,
    )
    .join("");
}

async function loadReviews() {
  const [reviewsResponse, summaryResponse] = await Promise.all([
    fetch(`/api/products/${productId}/reviews`),
    fetch(`/api/products/${productId}/ai-summary`),
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
    alert("평점을 선택해주세요.");
    return;
  }

  sendBtnEl.disabled = true;
  sendBtnEl.textContent = "등록 중...";

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
    alert("리뷰 등록에 실패했습니다. 잠시 후 다시 시도해주세요.");
    sendBtnEl.disabled = false;
    sendBtnEl.textContent = "등록";
    return;
  }

  reviewFormEl.reset();
  updateRatingStars(0);
  await loadReviews();
  sendBtnEl.disabled = false;
  sendBtnEl.textContent = "등록";
});

async function initPage() {
  if (!Number.isInteger(productId) || productId <= 0) {
    productNameEl.textContent = "유효하지 않은 상품입니다.";
    productDescriptionEl.textContent = "상품 ID를 확인해주세요.";
    return;
  }

  try {
    await loadProduct();
    await loadReviews();
  } catch (error) {
    productNameEl.textContent = "상품 정보를 불러오지 못했습니다.";
    productDescriptionEl.textContent = "잠시 후 다시 시도해주세요.";
    reviewSummaryEl.innerHTML = '<p class="text-red-500">리뷰 정보를 불러오지 못했습니다.</p>';
    reviewListEl.innerHTML = "";
  }
}

updateRatingStars(0);
initPage();
