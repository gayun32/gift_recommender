const giftForm = document.getElementById("gift-form");
const resultArea = document.getElementById("result-area");
const resultContent = document.getElementById("result-content");
const loading = document.getElementById("loading");
const errorMessage = document.getElementById("error-message");
const submitBtn = giftForm.querySelector("button[type='submit']");

giftForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const relationship = document.getElementById("relationship").value.trim();
  const age = document.getElementById("age").value.trim();
  const gender = document.getElementById("gender").value;
  const budget = document.getElementById("budget").value.trim();
  const interest = document.getElementById("interest").value.trim();

  // 1) 클라이언트 단 필수값 체크 (빠른 피드백, 서버 검증과 별개)
  if (!relationship || !age || !budget) {
    showError("필수값을 입력하세요. (관계 / 나이 / 예산은 필수입니다)");
    return;
  }

  const payload = { relationship, age, gender, budget, interest };

  // 2) 타임아웃 처리용 AbortController (10초)
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 10000);

  setLoading(true);
  hideError();
  hideResult();

  try {
    const res = await fetch("/api/recommend", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });

    clearTimeout(timeoutId);
    const data = await res.json();

    if (!res.ok) {
      // 백엔드가 보낸 {error: "..."} 메시지 그대로 표시
      showError(data.error || "오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
      return;
    }

    renderRecommendations(data.recommendations);

  } catch (err) {
    clearTimeout(timeoutId);
    if (err.name === "AbortError") {
      showError("응답이 지연되고 있습니다. 잠시 후 다시 시도해주세요.");
    } else {
      showError("네트워크 오류가 발생했습니다. 잠시 후 다시 시도해주세요.");
    }
  } finally {
    setLoading(false);
  }
});

function setLoading(isLoading) {
  loading.style.display = isLoading ? "block" : "none";
  submitBtn.disabled = isLoading;
}

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.style.display = "block";
}

function hideError() {
  errorMessage.style.display = "none";
  errorMessage.textContent = "";
}

function hideResult() {
  resultArea.style.display = "none";
  resultContent.innerHTML = "";
}

function renderRecommendations(recommendations) {
  if (!Array.isArray(recommendations) || recommendations.length === 0) {
    showError("추천 결과를 받아오지 못했습니다.");
    return;
  }

  resultContent.innerHTML = recommendations
    .map(
      (item) => `
      <div class="gift-item">
        <h4>${escapeHtml(item.name)}</h4>
        <p>${escapeHtml(item.reason)}</p>
      </div>
    `
    )
    .join("");

  resultArea.style.display = "block";
}

// AI가 생성한 텍스트를 innerHTML에 그대로 넣지 않기 위한 이스케이프 (XSS 방지)
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}