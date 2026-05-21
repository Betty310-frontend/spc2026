// 커스텀 confirm 모달 함수
window.customConfirm = function (message) {
  return new Promise((resolve) => {
    const modal = document.getElementById("custom-confirm-modal");
    const msgBox = document.getElementById("custom-confirm-message");
    const okBtn = document.getElementById("custom-confirm-ok");
    const cancelBtn = document.getElementById("custom-confirm-cancel");
    if (!modal || !msgBox || !okBtn || !cancelBtn) {
      resolve(window.confirm(message)); // fallback
      return;
    }
    msgBox.textContent = message;
    modal.classList.add("show");
    const cleanup = () => {
      modal.classList.remove("show");
      okBtn.removeEventListener("click", onOk);
      cancelBtn.removeEventListener("click", onCancel);
    };
    function onOk() {
      cleanup();
      resolve(true);
    }
    function onCancel() {
      cleanup();
      resolve(false);
    }
    okBtn.addEventListener("click", onOk);
    cancelBtn.addEventListener("click", onCancel);
    // ESC 키로 닫기
    modal.onkeydown = (e) => {
      if (e.key === "Escape") {
        cleanup();
        resolve(false);
      }
    };
    modal.focus();
  });
};
