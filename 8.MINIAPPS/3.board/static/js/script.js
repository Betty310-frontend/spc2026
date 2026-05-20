const inputTitle = document.getElementById("input-title");
const inputMessage = document.getElementById("input-message");
const saveBtn = document.getElementById("save-button");
const cardContainer = document.getElementById("card-container");
const alertContainer = document.getElementById("alert-container");

function getCardViewHtml(id, title, message) {
  return `
    <div>
        <h3 class="mt-0.5 text-lg font-medium text-gray-900">
        ${title}
        </h3>
        <p class="max-h-32 mt-2 whitespace-pre-wrap text-sm/relaxed text-gray-500 overflow-y-auto">
        ${message}
        </p>
    </div>
    <div class="mt-4 flex justify-end items-center gap-2">
      <button id="edit-${id}" class="rounded-lg bg-gray-100 px-2 py-1 text-sm font-medium text-gray-600 transition hover:bg-gray-200">수정</button>
      <button id="delete-${id}" class="rounded-lg bg-red-100 px-2 py-1 text-sm font-medium text-red-600 transition hover:bg-red-200">삭제</button>
    </div>
  `;
}

function showAlert(message) {
    
}

function renderBoards(data) {
  cardContainer.innerHTML = "";

  data.forEach((item) => {
    const id = item.id ?? item[0];
    const title = item.title ?? item[1];
    const message = item.message ?? item[2];

    const card = `
      <article id="board-${id}" class="flex flex-col justify-between rounded-lg border border-gray-100 bg-white p-4 shadow-xs transition hover:shadow-lg sm:p-6">
        ${getCardViewHtml(id, title, message)}
      </article>
    `;
    cardContainer.insertAdjacentHTML("beforeend", card);
  });
}

function restoreBoardCard(id, title, message) {
  const card = document.getElementById(`board-${id}`);
  if (!card) return;
  card.innerHTML = getCardViewHtml(id, title, message);
}

async function refreshBoards() {
  const response = await fetch("/api/board");
  const data = await response.json();
  renderBoards(data);
}

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await refreshBoards();
  } catch (error) {
    console.error("게시글을 불러오는 중 오류가 발생했습니다:", error);
  }
});

saveBtn.addEventListener("click", async () => {
  try {
    const title = inputTitle.value.trim();
    const message = inputMessage.value.trim();

    if (title && message) {
      const response = await fetch("/api/board", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, message }),
      });

      if (response.status === 201) {
        const alertMessage = await response.json();
        alert(alertMessage.message);
        inputTitle.value = "";
        inputMessage.value = "";
        await refreshBoards();
      }
    }
  } catch (error) {
    console.error("게시글을 저장하는 중 오류가 발생했습니다:", error);
  }
});

function modifyBoard(id) {
  const card = document.getElementById(`board-${id}`);
  if (!card) return;

  const originalTitle = card.querySelector("h3")?.textContent.trim() ?? "";
  const originalMessage = card.querySelector("p")?.textContent.trim() ?? "";
  card.dataset.originalTitle = originalTitle;
  card.dataset.originalMessage = originalMessage;

  const modifyElem = `
    <input type="text" class="border border-gray-300 rounded p-1 w-full mb-2 text-left text-sm" value="${originalTitle}"/>
    <textarea class="border border-gray-300 rounded p-1 w-full mb-2 resize-none h-20 text-sm">${originalMessage}</textarea>
    <div class="mt-4 flex justify-end items-center gap-2">
        <button id="edit-${id}" class="rounded-lg bg-blue-100 px-2 py-1 text-sm font-medium text-blue-600 transition hover:bg-blue-200">저장</button>
        <button id="cancel-${id}" class="rounded-lg bg-gray-100 px-2 py-1 text-sm font-medium text-gray-600 transition hover:bg-gray-200">취소</button>
    </div>
  `;

  card.innerHTML = modifyElem;
}

cardContainer.addEventListener("click", async (event) => {
  const target = event.target;
  if (target.tagName !== "BUTTON") return;

  const [action, id] = target.id.split("-");

  if (action === "edit") {
    const card = document.getElementById(`board-${id}`);
    if (!card) return;

    const editTitleInput = card.querySelector("input");
    const editMessageInput = card.querySelector("textarea");

    if (editTitleInput && editMessageInput) {
      const title = editTitleInput.value.trim();
      const message = editMessageInput.value.trim();

      if (!title || !message) {
        alert("제목과 메시지를 모두 입력해주세요.");
        return;
      }

      try {
        const response = await fetch(`/api/board/${id}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ title, message }),
        });

        if (!response.ok) {
          throw new Error("수정 요청 실패");
        }

        alert("게시글이 성공적으로 수정되었습니다.");
        restoreBoardCard(id, title, message);
      } catch (error) {
        console.error("게시글을 수정하는 중 오류가 발생했습니다:", error);
      }
    } else {
      modifyBoard(id);
    }
  } else if (action === "delete") {
    const confirmed = confirm("정말 삭제하시겠습니까?");
    if (confirmed) {
      try {
        const response = await fetch(`/api/board/${id}`, {
          method: "DELETE",
        });

        if (!response.ok) {
          throw new Error("삭제 요청 실패");
        }

        alert("게시글이 성공적으로 삭제되었습니다.");
        document.getElementById(`board-${id}`)?.remove();
      } catch (error) {
        console.error("게시글을 삭제하는 중 오류가 발생했습니다:", error);
      }
    }
  } else if (action === "cancel") {
    const card = document.getElementById(`board-${id}`);
    if (!card) return;

    const originalTitle = card.dataset.originalTitle ?? "";
    const originalMessage = card.dataset.originalMessage ?? "";
    restoreBoardCard(id, originalTitle, originalMessage);
  }
});
