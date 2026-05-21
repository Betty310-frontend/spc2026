document.addEventListener("DOMContentLoaded", () => {
  // 전역 요소 및 상태 관리
  let isPlaying = false;
  let progressTimer = null;
  let currentProgressPercent = 0;
  const mockSongDuration = 200; // 가상 곡 재생시간: 3분 20초 (200초)
  let currentSeconds = 0;

  const playPauseBtn = document.getElementById("btn-play-pause");
  const playPauseIcon = playPauseBtn ? playPauseBtn.querySelector("i") : null;
  const progressFill = document.querySelector(".timeline-progress-fill");
  const progressBg = document.querySelector(".timeline-progress-bg");
  const currentTimeLabel = document.getElementById("current-time");
  const eqContainer = document.querySelector(".eq-container");

  // ==========================================
  // 1. 가상 오디오 플레이어 (Mock Player)
  // ==========================================

  function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  }

  function startPlayback() {
    if (progressTimer) clearInterval(progressTimer);
    isPlaying = true;

    if (playPauseIcon) {
      playPauseIcon.className = "fas fa-pause";
    }
    if (eqContainer) {
      eqContainer.classList.add("active");
    }

    progressTimer = setInterval(() => {
      currentSeconds++;
      if (currentSeconds >= mockSongDuration) {
        currentSeconds = 0;
        stopPlayback();
      }

      // 프로그레스 바 비율 계산 및 라벨 갱신
      currentProgressPercent = (currentSeconds / mockSongDuration) * 100;
      if (progressFill) {
        progressFill.style.width = `${currentProgressPercent}%`;
      }
      if (currentTimeLabel) {
        currentTimeLabel.textContent = formatTime(currentSeconds);
      }
    }, 1000);
  }

  function stopPlayback() {
    isPlaying = false;
    if (playPauseIcon) {
      playPauseIcon.className = "fas fa-play";
    }
    if (eqContainer) {
      eqContainer.classList.remove("active");
    }
    if (progressTimer) {
      clearInterval(progressTimer);
    }
  }

  // 플레이어 바 재생/일시정지 클릭 토글
  if (playPauseBtn) {
    playPauseBtn.addEventListener("click", () => {
      if (isPlaying) {
        stopPlayback();
      } else {
        startPlayback();
      }
    });
  }

  // 재생 프로그레스 클릭 이동 (Scrubbing)
  if (progressBg) {
    progressBg.addEventListener("click", (e) => {
      const bgWidth = progressBg.clientWidth;
      const clickX = e.offsetX;
      const clickPercent = clickX / bgWidth;

      currentSeconds = Math.floor(clickPercent * mockSongDuration);
      currentProgressPercent = clickPercent * 100;

      if (progressFill) {
        progressFill.style.width = `${currentProgressPercent}%`;
      }
      if (currentTimeLabel) {
        currentTimeLabel.textContent = formatTime(currentSeconds);
      }

      if (isPlaying) {
        startPlayback();
      }
    });
  }

  // 볼륨 조절 모방
  const volumeBg = document.querySelector(".volume-progress-bg");
  const volumeFill = document.querySelector(".volume-progress-fill");
  if (volumeBg && volumeFill) {
    volumeBg.addEventListener("click", (e) => {
      const bgWidth = volumeBg.clientWidth;
      const clickPercent = e.offsetX / bgWidth;
      volumeFill.style.width = `${clickPercent * 100}%`;
    });
  }

  // 카드 재생 버튼 또는 상세 재생 버튼 클릭 시 트랙 로드
  window.loadAndPlayTrack = function (title, artist, imageClass) {
    // 플레이어 바 정보 업데이트
    const playerCover = document.querySelector(".player-cover");
    const playerTitle = document.querySelector(".player-song-title");
    const playerArtist = document.querySelector(".player-song-artist");

    if (playerCover) {
      playerCover.className = `player-cover ${imageClass}`;
      playerCover.textContent = title.charAt(0);
    }
    if (playerTitle) playerTitle.textContent = title;
    if (playerArtist) playerArtist.textContent = artist;

    // 시간 초기화 및 재생 시작
    currentSeconds = 0;
    if (progressFill) progressFill.style.width = "0%";
    if (currentTimeLabel) currentTimeLabel.textContent = "0:00";

    startPlayback();

    // 플래시 효과 알림
    showToast(`'${title}' 재생을 시작합니다.`);
  };

  // ==========================================
  // 2. 통합 실시간 검색 (검색어 대조)
  // ==========================================

  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const query = e.target.value.toLowerCase().trim();
      filterSongs(query);
    });
  }

  function filterSongs(query) {
    const cards = document.querySelectorAll(".music-card");

    cards.forEach((card) => {
      const title = card.getAttribute("data-title").toLowerCase();
      const artist = card.getAttribute("data-artist").toLowerCase();
      const tags = card.getAttribute("data-tags").toLowerCase(); // 예: "#kpop #pop"

      if (!query) {
        card.style.display = "flex";
        return;
      }

      if (query.startsWith("#")) {
        // 해시태그 전용 검색
        if (tags.includes(query)) {
          card.style.display = "flex";
        } else {
          card.style.display = "none";
        }
      } else {
        // 타이틀, 가수명, 해시태그 통합 검색
        if (title.includes(query) || artist.includes(query) || tags.includes(query)) {
          card.style.display = "flex";
        } else {
          card.style.display = "none";
        }
      }
    });
  }

  // 카드 내 해시태그 클릭 시 검색창 자동입력 및 필터링
  document.querySelectorAll(".tag-badge").forEach((tag) => {
    tag.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      const tagText = tag.textContent.trim();
      if (searchInput) {
        searchInput.value = tagText;
        searchInput.focus();
        filterSongs(tagText);
      }
    });
  });

  // ==========================================
  // 3. 로그인 요구 팝업 모달 관리
  // ==========================================

  const loginModal = document.getElementById("login-modal");
  window.showLoginModal = function () {
    if (loginModal) {
      loginModal.classList.add("show");
    }
  };

  window.closeLoginModal = function () {
    if (loginModal) {
      loginModal.classList.remove("show");
    }
  };

  // 비로그인 상태에서 댓글창 포커스 시 로그인 팝업 유도
  const guestCommentArea = document.getElementById("comment-guest-textarea");
  if (guestCommentArea) {
    guestCommentArea.addEventListener("focus", (e) => {
      e.preventDefault();
      guestCommentArea.blur();
      showLoginModal();
    });
  }

  // ==========================================
  // 4. AJAX 좋아요 제어 (곡 / 댓글)
  // ==========================================

  window.toggleLike = function (songId, element) {
    // 비로그인 시 예외 처리
    if (element.getAttribute("data-logged-in") === "false") {
      showLoginModal();
      return;
    }

    fetch(`/like/${songId}`, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => {
        if (response.status === 401) {
          showLoginModal();
          throw new Error("Unauthorized");
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          const heartIcon = element.querySelector("i");
          const countSpan = element.querySelector(".like-count");

          if (data.liked) {
            element.classList.add("liked");
            heartIcon.className = "fas fa-heart";
            showToast("곡을 좋아합니다!");
          } else {
            element.classList.remove("liked");
            heartIcon.className = "far fa-heart";
          }

          if (countSpan) {
            countSpan.textContent = data.likes_count;
          }
        }
      })
      .catch((err) => console.error(err));
  };

  // 댓글 좋아요 토글
  window.toggleCommentLike = function (commentId, element) {
    if (element.getAttribute("data-logged-in") === "false") {
      showLoginModal();
      return;
    }

    fetch(`/comment/${commentId}/like`, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => {
        if (response.status === 401) {
          showLoginModal();
          throw new Error("Unauthorized");
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          const thumbsIcon = element.querySelector("i");
          const countSpan = element.querySelector(".comment-like-count");

          if (data.liked) {
            element.classList.add("liked");
            thumbsIcon.className = "fas fa-thumbs-up";
          } else {
            element.classList.remove("liked");
            thumbsIcon.className = "far fa-thumbs-up";
          }

          if (countSpan) {
            countSpan.textContent = data.likes_count;
          }
        }
      })
      .catch((err) => console.error(err));
  };

  // ==========================================
  // 5. 해시태그 실시간 추가 / 삭제 (상세페이지)
  // ==========================================

  const addTagForm = document.getElementById("add-tag-form");
  if (addTagForm) {
    addTagForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const songId = addTagForm.getAttribute("data-song-id");
      const input = addTagForm.querySelector("input");
      const tagVal = input.value.trim();

      if (!tagVal) return;

      const formData = new FormData();
      formData.append("tag", tagVal);

      fetch(`/song/${songId}/tag/add`, {
        method: "POST",
        body: formData,
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.success) {
            // 태그 뱃지 실시간 화면 주입
            const container = document.getElementById("tag-list-container");
            const newBadge = document.createElement("span");
            newBadge.className = "tag-badge-editable";
            newBadge.id = `tag-badge-${data.tag.replace("#", "hash-")}`;
            newBadge.innerHTML = `
                        ${data.tag}
                        <button class="tag-delete-btn" onclick="deleteTag('${songId}', '${data.tag}')">
                            <i class="fas fa-times"></i>
                        </button>
                    `;
            container.appendChild(newBadge);
            input.value = "";
            showToast("해시태그가 추가되었습니다.");
          } else {
            showToast(data.error, "danger");
          }
        })
        .catch((err) => console.error(err));
    });
  }

  window.deleteTag = function (songId, tag) {
    const formData = new FormData();
    formData.append("tag", tag);

    fetch(`/song/${songId}/tag/delete`, {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          // DOM 엘리먼트 제거
          const tagElId = `tag-badge-${tag.replace("#", "hash-")}`;
          const badge = document.getElementById(tagElId);
          if (badge) {
            badge.remove();
          }
          showToast("해시태그가 삭제되었습니다.");
        } else {
          showToast(data.error, "danger");
        }
      })
      .catch((err) => console.error(err));
  };

  // ==========================================
  // 6. 댓글 수정 / 삭제 CUD AJAX 제어
  // ==========================================

  // 댓글 삭제
  window.deleteComment = async function (commentId) {
    const confirmed = await window.customConfirm("정말 이 댓글을 삭제하시겠습니까?");
    if (!confirmed) return;

    fetch(`/comment/${commentId}/delete`, {
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          const card = document.getElementById(`comment-card-${commentId}`);
          if (card) {
            card.style.opacity = "0";
            setTimeout(() => card.remove(), 300);
          }
          showToast(data.message);
        } else {
          showToast(data.error, "danger");
        }
      })
      .catch((err) => console.error(err));
  };

  // 댓글 수정 활성화 (인라인 수정 인풋 토글)
  window.enableEditComment = function (commentId) {
    const contentDiv = document.getElementById(`comment-content-${commentId}`);
    const actionsDiv = document.getElementById(`comment-actions-${commentId}`);
    if (!contentDiv) return;

    const currentText = contentDiv.textContent.trim();

    // 임시 폼 생성
    contentDiv.innerHTML = `
            <div class="comment-edit-container">
                <textarea class="comment-edit-input" id="edit-area-${commentId}">${currentText}</textarea>
                <div class="comment-edit-actions">
                    <button class="btn-secondary" style="padding: 0.3rem 0.8rem; font-size: 0.8rem;" onclick="cancelEditComment('${commentId}', '${currentText.replace(/'/g, "\\'")}')">취소</button>
                    <button class="btn-primary" style="padding: 0.3rem 0.8rem; font-size: 0.8rem;" onclick="saveEditComment('${commentId}')">저장</button>
                </div>
            </div>
        `;

    if (actionsDiv) {
      actionsDiv.style.display = "none";
    }
  };

  window.cancelEditComment = function (commentId, originalText) {
    const contentDiv = document.getElementById(`comment-content-${commentId}`);
    const actionsDiv = document.getElementById(`comment-actions-${commentId}`);
    if (contentDiv) {
      contentDiv.textContent = originalText;
    }
    if (actionsDiv) {
      actionsDiv.style.display = "flex";
    }
  };

  window.saveEditComment = function (commentId) {
    const textarea = document.getElementById(`edit-area-${commentId}`);
    if (!textarea) return;

    const newText = textarea.value.trim();
    if (!newText) {
      showToast("댓글 내용을 입력해주세요.", "warning");
      return;
    }

    const formData = new FormData();
    formData.append("content", newText);

    fetch(`/comment/${commentId}/edit`, {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          const contentDiv = document.getElementById(`comment-content-${commentId}`);
          const actionsDiv = document.getElementById(`comment-actions-${commentId}`);
          if (contentDiv) {
            contentDiv.textContent = data.content;
          }
          if (actionsDiv) {
            actionsDiv.style.display = "flex";
          }
          showToast(data.message);
        } else {
          showToast(data.error, "danger");
        }
      })
      .catch((err) => console.error(err));
  };

  // ==========================================
  // 7. 프로필 탭 전환 (Comments vs Liked Music)
  // ==========================================

  const tabs = document.querySelectorAll(".profile-tab");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");

      const targetId = tab.getAttribute("data-tab");
      document.querySelectorAll(".tab-content").forEach((content) => {
        content.classList.remove("active");
      });

      const activeContent = document.getElementById(targetId);
      if (activeContent) {
        activeContent.classList.add("active");
      }
    });
  });

  // ==========================================
  // 8. 토스트 메세지 (Toast Notifications)
  // ==========================================

  function showToast(message, type = "success") {
    const container = document.getElementById("toast-container");
    if (!container) {
      const newContainer = document.createElement("div");
      newContainer.id = "toast-container";
      newContainer.className = "flash-messages";
      document.body.appendChild(newContainer);
    }

    const toast = document.createElement("div");
    toast.className = `alert alert-${type}`;

    let icon = "fa-check-circle";
    if (type === "danger") icon = "fa-exclamation-circle";
    if (type === "warning") icon = "fa-exclamation-triangle";

    toast.innerHTML = `
            <i class="fas ${icon}"></i>
            <span>${message}</span>
        `;

    document.getElementById("toast-container").appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = "0";
      setTimeout(() => toast.remove(), 400);
    }, 3000);
  }
});
