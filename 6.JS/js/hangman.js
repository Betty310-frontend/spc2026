document.addEventListener("DOMContentLoaded", () => {
  const WORDS = {
    4: [
      { word: "STAR", hint: "밤하늘에 빛나는 것" },
      { word: "FIRE", hint: "뜨겁고 빛나는 것" },
      { word: "MOON", hint: "밤에 뜨는 위성" },
      { word: "RAIN", hint: "하늘에서 내리는 것" },
      { word: "TREE", hint: "숲을 이루는 식물" },
      { word: "BOOK", hint: "읽고 배우는 것" },
      { word: "CAKE", hint: "생일에 먹는 것" },
      { word: "BIRD", hint: "하늘을 나는 동물" },
      { word: "DOOR", hint: "열고 닫는 것" },
      { word: "FISH", hint: "물속에 사는 동물" },
      { word: "WAVE", hint: "바다에서 일렁이는 것" },
      { word: "LEAF", hint: "나무에 달린 것" },
      { word: "FROG", hint: "개구리" },
      { word: "WOLF", hint: "숲속의 야생 동물" },
      { word: "GOLD", hint: "귀한 금속" },
    ],
    5: [
      { word: "APPLE", hint: "빨갛거나 초록색 과일" },
      { word: "OCEAN", hint: "광활한 바다" },
      { word: "MUSIC", hint: "귀로 듣는 예술" },
      { word: "LIGHT", hint: "어둠을 밝히는 것" },
      { word: "BREAD", hint: "밀로 만든 식품" },
      { word: "CLOUD", hint: "하늘에 떠다니는 것" },
      { word: "DANCE", hint: "음악에 맞춰 몸을 움직이는 것" },
      { word: "EARTH", hint: "우리가 사는 행성" },
      { word: "FLAME", hint: "불꽃" },
      { word: "GLASS", hint: "투명한 재질" },
      { word: "HEART", hint: "사랑의 상징" },
      { word: "JUICE", hint: "과일로 만든 음료" },
      { word: "KNIFE", hint: "주방 도구" },
      { word: "LEMON", hint: "신 노란색 과일" },
      { word: "MOUSE", hint: "작은 설치류" },
      { word: "NIGHT", hint: "해가 진 후" },
      { word: "PIANO", hint: "건반 악기" },
      { word: "RIVER", hint: "흐르는 물" },
      { word: "SNAKE", hint: "기어다니는 파충류" },
      { word: "TIGER", hint: "줄무늬 고양이과 동물" },
    ],
    6: [
      { word: "BUTTER", hint: "빵에 바르는 것" },
      { word: "CASTLE", hint: "왕이 사는 곳" },
      { word: "DESERT", hint: "모래로 뒤덮인 건조한 곳" },
      { word: "FLOWER", hint: "아름다운 식물" },
      { word: "GARDEN", hint: "식물을 가꾸는 공간" },
      { word: "HARBOR", hint: "배가 정박하는 곳" },
      { word: "ISLAND", hint: "물로 둘러싸인 땅" },
      { word: "JUNGLE", hint: "열대 밀림" },
      { word: "KNIGHT", hint: "중세 전사" },
      { word: "LEGEND", hint: "전설" },
      { word: "MIRROR", hint: "얼굴을 비추는 것" },
      { word: "NATURE", hint: "자연" },
      { word: "ORANGE", hint: "주황색 과일" },
      { word: "PLANET", hint: "태양 주위를 도는 천체" },
      { word: "RABBIT", hint: "귀가 긴 동물" },
      { word: "ROCKET", hint: "우주로 향하는 것" },
      { word: "SILVER", hint: "은빛 금속" },
      { word: "SPRING", hint: "꽃이 피는 계절" },
      { word: "SUNSET", hint: "해가 지는 순간" },
      { word: "WINTER", hint: "눈이 내리는 계절" },
    ],
  };

  const HM_PARTS = [
    "hm-head",
    "hm-body",
    "hm-arm-l",
    "hm-arm-r",
    "hm-leg-l",
    "hm-leg-r",
  ];
  const MAX_WRONG = 6;
  const KB_ROWS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"];

  let currentWord = "";
  let currentHint = "";
  let guessed = new Set();
  let wrongCount = 0;
  let currentLength = 4;
  let gameOver = false;

  // Screens
  function showScreen(id) {
    document
      .querySelectorAll(".screen")
      .forEach((s) => s.classList.remove("active"));
    document.getElementById(id).classList.add("active");
  }

  const newGameBtn = document.getElementById("new-game-btn");
  const goMenuBtn = document.getElementById("go-menu-btn");

  function goMenu() {
    document.getElementById("result-overlay").classList.remove("show");
    showScreen("screen-menu");
  }

  newGameBtn.addEventListener("click", goMenu);
  goMenuBtn.addEventListener("click", goMenu);

  const replayBtn = document.getElementById("replay-btn");

  function replayGame() {
    document.getElementById("result-overlay").classList.remove("show");
    startGame(currentLength);
  }

  replayBtn.addEventListener("click", replayGame);

  // Start Game
  const lenBtn4 = document.getElementById("len-btn-4");
  const lenBtn5 = document.getElementById("len-btn-5");
  const lenBtn6 = document.getElementById("len-btn-6");

  function startGame(len) {
    currentLength = len;
    const pool = WORDS[len];
    const picked = pool[Math.floor(Math.random() * pool.length)];
    currentWord = picked.word;
    currentHint = picked.hint;
    guessed = new Set();
    wrongCount = 0;
    gameOver = false;

    showScreen("screen-game");
    renderHangman();
    renderChanceDots();
    renderWordBlanks();
    renderUsedLetters();
    renderKeyboard();
    document.getElementById("lives-num").textContent = MAX_WRONG - wrongCount;
    document.getElementById("status-msg").textContent =
      "글자를 선택해 단어를 맞춰보세요";
    document.getElementById("hint-area").textContent = `힌트: ${currentHint}`;
  }

  lenBtn4.addEventListener("click", () => startGame(4));
  lenBtn5.addEventListener("click", () => startGame(5));
  lenBtn6.addEventListener("click", () => startGame(6));

  // Hangman
  function renderHangman() {
    HM_PARTS.forEach((id, i) => {
      const el = document.getElementById(id);
      el.classList.remove("visible", "error");
      if (i < wrongCount) el.classList.add("visible");
    });
  }

  function renderChanceDots() {
    const container = document.getElementById("chance-dots");
    container.innerHTML = "";
    for (let i = 0; i < MAX_WRONG; i++) {
      const dot = document.createElement("div");
      dot.className = "dot" + (i < wrongCount ? " used" : "");
      container.appendChild(dot);
    }
  }

  // Word blanks
  function renderWordBlanks() {
    const container = document.getElementById("word-blanks");
    container.innerHTML = "";
    for (let i = 0; i < currentWord.length; i++) {
      const slot = document.createElement("div");
      slot.className = "letter-slot";

      const char = document.createElement("div");
      char.className = "letter-char";
      char.id = `slot-${i}`;
      if (guessed.has(currentWord[i])) {
        char.textContent = currentWord[i];
        char.classList.add("revealed");
      }

      const line = document.createElement("div");
      line.className =
        "letter-line" + (guessed.has(currentWord[i]) ? " active" : "");

      slot.appendChild(char);
      slot.appendChild(line);
      container.appendChild(slot);
    }
  }

  // Used letters
  function renderUsedLetters() {
    const container = document.getElementById("used-letters");
    container.innerHTML = "";
    guessed.forEach((l) => {
      const span = document.createElement("span");
      span.className =
        "used-letter " + (currentWord.includes(l) ? "correct" : "wrong");
      span.textContent = l;
      container.appendChild(span);
    });
  }

  // Keyboard
  function renderKeyboard() {
    const container = document.getElementById("keyboard");
    container.innerHTML = "";
    KB_ROWS.forEach((row) => {
      const rowDiv = document.createElement("div");
      rowDiv.className = "kb-row";
      [...row].forEach((letter) => {
        const btn = document.createElement("button");
        btn.className = "kb-key";
        btn.textContent = letter;
        btn.id = `kb-${letter}`;
        if (guessed.has(letter)) {
          btn.disabled = true;
          btn.classList.add(
            currentWord.includes(letter) ? "correct-key" : "wrong-key",
          );
        }
        btn.addEventListener("click", () => guess(letter));
        rowDiv.appendChild(btn);
      });
      container.appendChild(rowDiv);
    });
  }

  // Guess
  function guess(letter) {
    if (gameOver || guessed.has(letter)) return;
    guessed.add(letter);

    const isCorrect = currentWord.includes(letter);

    // Update key style
    const keyBtn = document.getElementById(`kb-${letter}`);
    if (keyBtn) {
      keyBtn.disabled = true;
      keyBtn.classList.add(isCorrect ? "correct-key" : "wrong-key");
    }

    if (!isCorrect) {
      wrongCount++;
      // Animate new part with error flash
      const partEl = document.getElementById(HM_PARTS[wrongCount - 1]);
      if (partEl) {
        partEl.classList.add("visible");
        partEl.classList.add("error");
        setTimeout(() => partEl.classList.remove("error"), 400);
      }
      renderChanceDots();
      document.getElementById("lives-num").textContent = MAX_WRONG - wrongCount;

      if (wrongCount >= MAX_WRONG) {
        endGame(false);
        return;
      }

      document.getElementById("status-msg").textContent =
        "틀렸어요! 다시 시도해보세요";
    } else {
      // Reveal letters
      for (let i = 0; i < currentWord.length; i++) {
        if (currentWord[i] === letter) {
          const charEl = document.getElementById(`slot-${i}`);
          if (charEl) {
            charEl.textContent = letter;
            charEl.classList.add("revealed");
            charEl.parentElement
              .querySelector(".letter-line")
              .classList.add("active");
          }
        }
      }

      // Check win
      const won = [...currentWord].every((l) => guessed.has(l));
      if (won) {
        endGame(true);
        return;
      }
      document.getElementById("status-msg").textContent = "정답! 계속하세요 🎯";
    }

    renderUsedLetters();
  }

  // End Game
  function endGame(won) {
    gameOver = true;
    setTimeout(() => {
      const overlay = document.getElementById("result-overlay");
      overlay.classList.add("show");
      document.getElementById("result-emoji").textContent = won ? "🎉" : "💀";
      document.getElementById("result-title").textContent = won
        ? "EXCELLENT!"
        : "GAME OVER";
      document.getElementById("result-title").style.color = won
        ? "var(--accent)"
        : "var(--accent2)";
      document.getElementById("result-word").textContent = currentWord;
      document.getElementById("result-sub").textContent = won
        ? `${currentWord.length}글자 단어를 맞췄습니다! 대단해요 🌟`
        : `정답은 "${currentWord}" 였습니다`;

      if (won) spawnConfetti();
    }, 300);
  }

  // Confetti
  function spawnConfetti() {
    const colors = [
      "#e8ff47",
      "#ff4757",
      "#4ecdc4",
      "#ffffff",
      "#ff6b6b",
      "#ffd93d",
    ];
    for (let i = 0; i < 80; i++) {
      setTimeout(() => {
        const piece = document.createElement("div");
        piece.className = "confetti-piece";
        piece.style.left = Math.random() * 100 + "vw";
        piece.style.top = "-10px";
        piece.style.background =
          colors[Math.floor(Math.random() * colors.length)];
        piece.style.width = Math.random() * 10 + 5 + "px";
        piece.style.height = Math.random() * 10 + 5 + "px";
        piece.style.borderRadius = Math.random() > 0.5 ? "50%" : "2px";
        const dur = (Math.random() * 2 + 2).toFixed(2);
        piece.style.animationDuration = dur + "s";
        document.body.appendChild(piece);
        setTimeout(() => piece.remove(), parseFloat(dur) * 1000);
      }, i * 30);
    }
  }

  // Keyboard input
  document.addEventListener("keydown", (e) => {
    const letter = e.key.toUpperCase();
    if (
      /^[A-Z]$/.test(letter) &&
      document.getElementById("screen-game").classList.contains("active")
    ) {
      guess(letter);
    }
  });
});
