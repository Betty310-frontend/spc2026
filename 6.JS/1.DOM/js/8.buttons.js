const result = document.getElementById("result");
const initValue = parseInt(result.textContent);
const counter = { value: initValue };

const incBtn = document.getElementById("inc_btn");
const decBtn = document.getElementById("dec_btn");

function updateResult(value) {
  counter.value += value;
  result.innerText = counter.value;
}

incBtn.addEventListener("click", () => updateResult(1));
decBtn.addEventListener("click", () => updateResult(-1));
