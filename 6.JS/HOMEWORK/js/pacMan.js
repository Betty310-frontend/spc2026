const MAP = [
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
  [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 1, 1, 1, 0, 1, 1, 0, 1, 2, 2, 1, 0, 1, 1, 0, 1, 1, 1, 1],
  [1, 1, 1, 1, 0, 1, 1, 0, 2, 2, 2, 2, 0, 1, 1, 0, 1, 1, 1, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
  [1, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
];

const CELL_SIZE = 32;
const COLS = MAP[0].length;
const ROWS = MAP.length;
const WALL = 1;
const DOT = 0;
const EMPTY = 2;
const POWER_PELLET = 3;

const DIRECTIONS = {
  ArrowUp: { x: 0, y: -1, angle: -Math.PI / 2 },
  ArrowDown: { x: 0, y: 1, angle: Math.PI / 2 },
  ArrowLeft: { x: -1, y: 0, angle: Math.PI },
  ArrowRight: { x: 1, y: 0, angle: 0 },
};

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const score = document.getElementById("score");
const message = document.getElementById("message");
const restartBtn = document.getElementById("restartBtn");

canvas.width = COLS * CELL_SIZE;
canvas.height = ROWS * CELL_SIZE;

let map;
let scoreValue;
let animationId;
let pacman;
let isWon;

function createPacman() {
  return {
    col: 1,
    row: 1,
    offsetX: 0,
    offsetY: 0,
    dir: { x: 1, y: 0, angle: 0 },
    nextDir: { x: 1, y: 0, angle: 0 },
    speed: 2,
    mouth: 0.18,
    mouthStep: 0.02,
  };
}

function resetGame() {
  map = MAP.map((row) => [...row]);
  scoreValue = 0;
  isWon = false;
  pacman = createPacman();
  score.textContent = scoreValue;
  message.textContent = "";
  message.classList.add("hidden");
  canvas.focus();

  cancelAnimationFrame(animationId);
  gameLoop();
}

function isWall(col, row) {
  if (col < 0 || col >= COLS || row < 0 || row >= ROWS) {
    return true;
  }

  return map[row][col] === WALL;
}

function isCentered() {
  return pacman.offsetX === 0 && pacman.offsetY === 0;
}

function canMoveFromCell(direction) {
  return !isWall(pacman.col + direction.x, pacman.row + direction.y);
}

function updateDirection() {
  if (!isCentered()) {
    return;
  }

  if (canMoveFromCell(pacman.nextDir)) {
    pacman.dir = { ...pacman.nextDir };
    return;
  }

  if (!canMoveFromCell(pacman.dir)) {
    pacman.dir = { x: 0, y: 0, angle: pacman.dir.angle };
  }
}

function movePacman() {
  updateDirection();

  if (pacman.dir.x === 0 && pacman.dir.y === 0) {
    return;
  }

  pacman.offsetX += pacman.dir.x * pacman.speed;
  pacman.offsetY += pacman.dir.y * pacman.speed;

  if (pacman.offsetX <= -CELL_SIZE) {
    pacman.col -= 1;
    pacman.offsetX += CELL_SIZE;
  }
  if (pacman.offsetX >= CELL_SIZE) {
    pacman.col += 1;
    pacman.offsetX -= CELL_SIZE;
  }
  if (pacman.offsetY <= -CELL_SIZE) {
    pacman.row -= 1;
    pacman.offsetY += CELL_SIZE;
  }
  if (pacman.offsetY >= CELL_SIZE) {
    pacman.row += 1;
    pacman.offsetY -= CELL_SIZE;
  }

  pacman.mouth += pacman.mouthStep;
  if (pacman.mouth > 0.34 || pacman.mouth < 0.08) {
    pacman.mouthStep *= -1;
  }

  if (isCentered()) {
    eatCurrentCell();
  }
}

function eatCurrentCell() {
  const cell = map[pacman.row][pacman.col];

  if (cell === DOT) {
    map[pacman.row][pacman.col] = EMPTY;
    scoreValue += 10;
  }

  if (cell === POWER_PELLET) {
    map[pacman.row][pacman.col] = EMPTY;
    scoreValue += 50;
  }

  score.textContent = scoreValue;

  const remaining = map
    .flat()
    .some((value) => value === DOT || value === POWER_PELLET);
  if (!remaining) {
    isWon = true;
    message.textContent = "CLEAR";
    message.classList.remove("hidden");
  }
}

function drawBoard() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  for (let row = 0; row < ROWS; row += 1) {
    for (let col = 0; col < COLS; col += 1) {
      const x = col * CELL_SIZE;
      const y = row * CELL_SIZE;
      const cell = map[row][col];

      ctx.fillStyle = "#020617";
      ctx.fillRect(x, y, CELL_SIZE, CELL_SIZE);

      if (cell === WALL) {
        ctx.fillStyle = "#1d4ed8";
        ctx.fillRect(x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4);
        ctx.strokeStyle = "#60a5fa";
        ctx.lineWidth = 2;
        ctx.strokeRect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8);
      }

      if (cell === DOT) {
        ctx.fillStyle = "#f8fafc";
        ctx.beginPath();
        ctx.arc(x + CELL_SIZE / 2, y + CELL_SIZE / 2, 3, 0, Math.PI * 2);
        ctx.fill();
      }

      if (cell === POWER_PELLET) {
        ctx.fillStyle = "#fde047";
        ctx.beginPath();
        ctx.arc(x + CELL_SIZE / 2, y + CELL_SIZE / 2, 7, 0, Math.PI * 2);
        ctx.fill();
      }
    }
  }
}

function drawPacman() {
  const centerX = pacman.col * CELL_SIZE + CELL_SIZE / 2 + pacman.offsetX;
  const centerY = pacman.row * CELL_SIZE + CELL_SIZE / 2 + pacman.offsetY;
  const radius = CELL_SIZE / 2 - 4;

  ctx.fillStyle = "#facc15";
  ctx.beginPath();
  ctx.moveTo(centerX, centerY);
  ctx.arc(
    centerX,
    centerY,
    radius,
    pacman.dir.angle + pacman.mouth,
    pacman.dir.angle + Math.PI * 2 - pacman.mouth,
  );
  ctx.closePath();
  ctx.fill();

  let eyeOffsetX = 4;
  let eyeOffsetY = -6;

  if (pacman.dir.x === -1) {
    eyeOffsetX = -4;
    eyeOffsetY = -6;
  }

  if (pacman.dir.y === -1) {
    eyeOffsetX = -6;
    eyeOffsetY = -4;
  }

  if (pacman.dir.y === 1) {
    eyeOffsetX = -6;
    eyeOffsetY = -4;
  }

  const eyeX = centerX + eyeOffsetX;
  const eyeY = centerY + eyeOffsetY;

  ctx.fillStyle = "#111827";
  ctx.beginPath();
  ctx.arc(eyeX, eyeY, 2.5, 0, Math.PI * 2);
  ctx.fill();
}

function gameLoop() {
  drawBoard();
  movePacman();
  drawPacman();

  if (!isWon) {
    animationId = requestAnimationFrame(gameLoop);
  }
}

function handleKeydown(event) {
  const direction = DIRECTIONS[event.key];

  if (!direction) {
    return;
  }

  event.preventDefault();
  pacman.nextDir = { ...direction };
}

window.addEventListener("keydown", handleKeydown);
canvas.addEventListener("click", () => canvas.focus());
restartBtn.addEventListener("click", resetGame);

resetGame();
