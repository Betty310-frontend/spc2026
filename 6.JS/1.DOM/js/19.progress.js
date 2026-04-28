let timeId;

const timeInput = document.getElementById("time-input");
const progressText = document.getElementById("progress-text");
const startBtn = document.getElementById("start-btn");
const resetBtn = document.getElementById("reset-btn");
const errorMsg = document.getElementById("error-message");

function startProgress() {
  const duration = parseInt(timeInput.value);
  const progressElem = document.getElementById("progress");

  let elapsed = 0;

  if (isNaN(duration) || duration <= 0) {
    errorMsg.classList.remove("hidden");
    return;
  } else {
    errorMsg.classList.add("hidden");
  }

  startBtn.disabled = true;

  timeId = setInterval(() => {
    elapsed++;
    //  NOTE: 진행률 계산
    const ratio = (elapsed / duration) * 100;
    progressText.textContent = `${Math.floor(ratio)}%`;

    progressElem.style.width = `${ratio}%`;
    if (elapsed >= duration) {
      clearInterval(timeId);
      startBtn.disabled = false;
    }
  }, 1000);
}

function clearProgress() {
  clearInterval(timeId);
  const progressElem = document.getElementById("progress");
  progressElem.style.width = "2px";
  progressText.textContent = "0%";
  timeInput.value = "";
  startBtn.disabled = false;
}

startBtn.addEventListener("click", startProgress);
resetBtn.addEventListener("click", clearProgress);
