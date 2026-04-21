const seats = [
  { id: "A1", row: 1, col: 1 },
  { id: "A2", row: 1, col: 2 },
  { id: "A3", row: 2, col: 1 },
  { id: "A4", row: 2, col: 2 },
  { id: "A5", row: 3, col: 2 },
  { id: "A6", row: 4, col: 2 },
  { id: "B1", row: 1, col: 5 },
  { id: "B2", row: 1, col: 6 },
  { id: "B3", row: 1, col: 7 },
  { id: "B4", row: 2, col: 5 },
  { id: "B5", row: 2, col: 6 },
  { id: "B6", row: 2, col: 7 },
  { id: "B7", row: 3, col: 5 },
  { id: "B8", row: 3, col: 6 },
  { id: "B9", row: 3, col: 7 },
  { id: "B10", row: 4, col: 5 },
  { id: "B11", row: 4, col: 6 },
  { id: "B12", row: 4, col: 7 },
  { id: "B13", row: 5, col: 6 },
  { id: "B14", row: 5, col: 7 },
  { id: "C1", row: 1, col: 10 },
  { id: "C2", row: 1, col: 11 },
  { id: "C3", row: 2, col: 10 },
  { id: "C4", row: 2, col: 11 },
  { id: "C5", row: 3, col: 10 },
  { id: "C6", row: 3, col: 11 },
  { id: "C7", row: 4, col: 10 },
  { id: "C8", row: 4, col: 11 },
  { id: "C9", row: 5, col: 10 },
  { id: "C10", row: 5, col: 11 }
];

const students = [
  { id: "S01", number: 1, gender: "미정", name: "조윤" },
  { id: "S02", number: 2, gender: "미정", name: "조은결" },
  { id: "S03", number: 3, gender: "미정", name: "권태현" },
  { id: "S04", number: 4, gender: "미정", name: "김성호" },
  { id: "S05", number: 6, gender: "미정", name: "한혜경" },
  { id: "S06", number: 5, gender: "미정", name: "유지산" },
  { id: "S07", number: 7, gender: "미정", name: "이춘우" },
  { id: "S08", number: 8, gender: "미정", name: "최준호" },
  { id: "S09", number: 9, gender: "미정", name: "이서우" },
  { id: "S10", number: 10, gender: "미정", name: "김민정" },
  { id: "S11", number: 11, gender: "미정", name: "박지우" },
  { id: "S12", number: 12, gender: "미정", name: "박은빈" },
  { id: "S13", number: 13, gender: "미정", name: "진미경" },
  { id: "S14", number: 14, gender: "미정", name: "박상우" },
  { id: "S15", number: 15, gender: "미정", name: "조용민" },
  { id: "S16", number: 16, gender: "미정", name: "김민정" },
  { id: "S17", number: 17, gender: "미정", name: "이종혁" },
  { id: "S18", number: 18, gender: "미정", name: "김유신" },
  { id: "S19", number: 19, gender: "미정", name: "심정호" },
  { id: "S20", number: 20, gender: "미정", name: "이태경" },
  { id: "S21", number: 21, gender: "미정", name: "황동건" },
  { id: "S22", number: 22, gender: "미정", name: "이상욱" },
  { id: "S23", number: 23, gender: "미정", name: "원가희" },
  { id: "S24", number: 24, gender: "미정", name: "신혜진" },
  { id: "S25", number: 25, gender: "미정", name: "김선희" },
  { id: "S26", number: 26, gender: "미정", name: "한은태" },
  { id: "S27", number: 27, gender: "미정", name: "박초롱" },
  { id: "S28", number: 28, gender: "미정", name: "박준하" },
  { id: "S29", number: 29, gender: "미정", name: "채란" },
  { id: "S30", number: 30, gender: "미정", name: "이민지" }
];

const defaultAssignments = {
  A1: "S01",
  A2: "S02",
  A3: "S03",
  A4: "S04",
  A5: "S05",
  A6: "S06",
  B1: "S07",
  B2: "S08",
  B3: "S09",
  B4: "S10",
  B5: "S11",
  B6: "S12",
  B7: "S13",
  B8: "S14",
  B9: "S15",
  B10: "S16",
  B11: "S17",
  B12: "S18",
  B13: "S19",
  B14: "S20",
  C1: "S21",
  C2: "S22",
  C3: "S23",
  C4: "S24",
  C5: "S25",
  C6: "S26",
  C7: "S27",
  C8: "S28",
  C9: "S29",
  C10: "S30"
};

const STORAGE_KEY = "seating-manager-state";
const defaultStudents = structuredClone(students);

const state = {
  mode: "view",
  selectedSeatId: null,
  selectedStudentId: null,
  editingStudentId: null,
  assignments: structuredClone(defaultAssignments)
};

const seatGrid = document.getElementById("seatGrid");
const studentList = document.getElementById("studentList");
const statusText = document.getElementById("statusText");

const shuffleBtn = document.getElementById("shuffleBtn");
const manualModeBtn = document.getElementById("manualModeBtn");
const printBtn = document.getElementById("printBtn");
const resetBtn = document.getElementById("resetBtn");
const clearBtn = document.getElementById("clearBtn");
const editForm = document.getElementById("editForm");
const editNumberInput = document.getElementById("editNumber");
const editNameInput = document.getElementById("editName");
const editGenderSelect = document.getElementById("editGender");
const editorTitle = document.getElementById("editorTitle");
const printCaption = document.getElementById("printCaption");

shuffleBtn.addEventListener("click", randomShuffle);
manualModeBtn.addEventListener("click", () => {
  state.selectedSeatId = null;
  state.selectedStudentId = null;

  if (state.mode === "manual") {
    state.mode = "view";
    setStatus("수동 배치 모드를 해제했습니다. 좌석 카드를 클릭하면 학생 정보 편집만 가능합니다.");
  } else {
    state.mode = "manual";
    setStatus("수동 배치 모드입니다. 출발 좌석을 클릭한 뒤, 도착 좌석을 클릭하세요.");
  }

  render();
});
printBtn.addEventListener("click", handlePrint);

resetBtn.addEventListener("click", () => {
  students.splice(0, students.length, ...structuredClone(defaultStudents));
  state.assignments = structuredClone(defaultAssignments);
  state.selectedSeatId = null;
  state.selectedStudentId = null;
  state.editingStudentId = null;
  state.mode = "view";
  setStatus("기본 배치로 복원했습니다. 좌석 카드를 클릭하면 학생 정보만 편집할 수 있습니다.");
  saveAppState();
  render();
});

clearBtn.addEventListener("click", () => {
  state.selectedSeatId = null;
  state.selectedStudentId = null;
  state.editingStudentId = null;
  setStatus(
    state.mode === "manual"
      ? "선택을 해제했습니다. 학생을 다시 선택한 후 좌석을 클릭하세요."
      : "선택을 해제했습니다. 좌석 카드를 클릭하면 학생 정보를 편집할 수 있습니다."
  );
  render();
});

editForm.addEventListener("submit", (event) => {
  event.preventDefault();
  saveStudentEdits();
});

function setStatus(message) {
  statusText.textContent = message;
}

function saveAppState() {
  try {
    const payload = {
      students,
      assignments: state.assignments
    };

    localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
  } catch {
    // Ignore storage failures so the app remains usable.
  }
}

function loadAppState() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return;
    }

    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") {
      return;
    }

    if (Array.isArray(parsed.students)) {
      students.splice(0, students.length, ...parsed.students);
    }

    if (parsed.assignments && typeof parsed.assignments === "object") {
      const nextAssignments = {};
      seats.forEach((seat) => {
        nextAssignments[seat.id] = parsed.assignments[seat.id] ?? null;
      });
      state.assignments = nextAssignments;
    }
  } catch {
    // Ignore malformed saved data and fall back to defaults.
  }
}

function handlePrint() {
  const timestamp = new Date().toLocaleString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit"
  });

  printCaption.textContent = `출력 시각: ${timestamp}`;
  window.print();
}

function getStudentById(studentId) {
  return students.find((student) => student.id === studentId) || null;
}

function getSeatByStudentId(studentId) {
  for (const [seatId, currentStudentId] of Object.entries(state.assignments)) {
    if (currentStudentId === studentId) {
      return seatId;
    }
  }
  return null;
}

function getGenderClass(gender) {
  if (gender === "남") {
    return "gender-male";
  }

  if (gender === "여") {
    return "gender-female";
  }

  if (gender === "기타") {
    return "gender-other";
  }

  return "gender-unknown";
}

function removeStudentAssignments(studentId) {
  for (const [seatId, currentStudentId] of Object.entries(state.assignments)) {
    if (currentStudentId === studentId) {
      state.assignments[seatId] = null;
    }
  }
}

function deleteStudent(studentId) {
  const studentIndex = students.findIndex((student) => student.id === studentId);
  if (studentIndex === -1) {
    setStatus("삭제할 학생 정보를 찾을 수 없습니다.");
    return;
  }

  const student = students[studentIndex];
  const confirmed = window.confirm(`${student.name} 학생을 목록에서 삭제할까요?`);

  if (!confirmed) {
    return;
  }

  students.splice(studentIndex, 1);
  removeStudentAssignments(studentId);

  if (state.selectedStudentId === studentId) {
    state.selectedStudentId = null;
  }

  if (state.selectedSeatId && state.assignments[state.selectedSeatId] == null) {
    state.selectedSeatId = null;
  }

  if (state.editingStudentId === studentId) {
    state.editingStudentId = null;
  }

  setStatus(`${student.name} 학생을 목록에서 삭제했습니다.`);
  saveAppState();
  render();
}

function saveStudentEdits() {
  if (!state.editingStudentId) {
    setStatus("먼저 학생 목록에서 편집할 학생을 선택해 주세요.");
    return;
  }

  const student = getStudentById(state.editingStudentId);
  if (!student) {
    setStatus("선택된 학생 정보를 찾을 수 없습니다.");
    return;
  }

  const nextNumber = Number(editNumberInput.value);
  const nextName = editNameInput.value.trim();
  const nextGender = editGenderSelect.value || "미정";

  if (!Number.isInteger(nextNumber) || nextNumber < 1 || nextNumber > 999) {
    setStatus("번호는 1~999 사이의 정수로 입력해 주세요.");
    return;
  }

  if (!nextName) {
    setStatus("이름을 입력해 주세요.");
    return;
  }

  student.number = nextNumber;
  student.name = nextName;
  student.gender = nextGender;

  setStatus(`${student.name} 학생 정보를 저장했습니다.`);
  saveAppState();
  render();
}

function handleSeatClick(seatId) {
  const seatStudentId = state.assignments[seatId] || null;
  const isManualMode = state.mode === "manual";
  const selectedSeatBeforeClick = state.selectedSeatId;

  if (!isManualMode) {
    if (!seatStudentId) {
      setStatus("빈 자리는 편집할 학생 정보가 없습니다.");
      return;
    }

    state.editingStudentId = seatStudentId;

    const seatStudent = getStudentById(seatStudentId);
    setStatus(
      seatStudent
        ? `${seatStudent.name} 학생 정보를 편집 폼에 불러왔습니다.`
        : "학생 정보를 편집 폼에 불러왔습니다."
    );
    render();
    return;
  }

  if (!selectedSeatBeforeClick) {
    if (!seatStudentId) {
      setStatus("출발 좌석은 학생이 있는 좌석을 선택해 주세요.");
      return;
    }

    state.selectedSeatId = seatId;
    state.selectedStudentId = seatStudentId;
    state.editingStudentId = seatStudentId;
    setStatus("출발 좌석을 선택했습니다. 이제 도착 좌석을 클릭하세요.");
    render();
    return;
  }

  if (selectedSeatBeforeClick === seatId) {
    state.selectedSeatId = null;
    state.selectedStudentId = null;
    setStatus("출발 좌석 선택을 해제했습니다.");
    render();
    return;
  }

  const sourceStudentId = state.assignments[selectedSeatBeforeClick] || null;
  const targetStudentId = state.assignments[seatId] || null;

  state.assignments[selectedSeatBeforeClick] = targetStudentId;
  state.assignments[seatId] = sourceStudentId;
  state.selectedSeatId = null;
  state.selectedStudentId = null;
  state.editingStudentId = sourceStudentId;
  setStatus("좌석 배치를 변경했습니다.");
  saveAppState();
  render();
}

function randomShuffle() {
  state.mode = "random";

  const shuffled = [...students]
    .map((student) => ({ student, sort: Math.random() }))
    .sort((a, b) => a.sort - b.sort)
    .map((entry) => entry.student);

  const next = {};
  seats.forEach((seat, index) => {
    next[seat.id] = shuffled[index] ? shuffled[index].id : null;
  });

  state.assignments = next;
  state.selectedSeatId = null;
  state.selectedStudentId = null;
  state.editingStudentId = null;
  setStatus("랜덤 셔플을 완료했습니다.");
  saveAppState();
  render();
}

function renderSeats() {
  seatGrid.innerHTML = "";

  seats.forEach((seat) => {
    const studentId = state.assignments[seat.id] || null;
    const student = getStudentById(studentId);

    const seatEl = document.createElement("button");
    seatEl.type = "button";
    seatEl.className = "seat";
    seatEl.style.gridColumn = String(seat.col);
    seatEl.style.gridRow = String(seat.row);

    if (student) {
      seatEl.classList.add("filled");
      seatEl.classList.add(getGenderClass(student.gender));

      if (
        state.selectedSeatId === seat.id ||
        state.selectedStudentId === student.id ||
        (!state.selectedStudentId && state.editingStudentId === student.id)
      ) {
        seatEl.classList.add("selected");
      }

      seatEl.innerHTML = `
        <span class="num">${student.number}번</span>
        <span class="name">${student.name}</span>
        <span class="gender">${student.gender}</span>
      `;
    } else {
      seatEl.classList.add("empty");
      seatEl.innerHTML = `
        <span class="name">빈 자리</span>
      `;
    }

    seatEl.addEventListener("click", () => handleSeatClick(seat.id));
    seatGrid.appendChild(seatEl);
  });
}

function renderStudents() {
  studentList.innerHTML = "";

  students.forEach((student) => {
    const seatId = getSeatByStudentId(student.id);

    const item = document.createElement("li");
    item.className = "student-item";
    item.classList.add(getGenderClass(student.gender));

    if (state.selectedStudentId === student.id) {
      item.classList.add("active");
    }

    if (state.editingStudentId === student.id) {
      item.classList.add("editing");
    }

    item.innerHTML = `
      <div class="student-item-header">
        <strong>${student.number}번 ${student.name}</strong>
        <button class="delete-btn" type="button" data-student-id="${student.id}">✖</button>
      </div>
      <span class="meta">성별: ${student.gender} | 좌석: ${seatId || "미배정"}</span>
    `;

    const deleteBtn = item.querySelector(".delete-btn");
    deleteBtn.addEventListener("click", (event) => {
      event.stopPropagation();
      deleteStudent(student.id);
    });

    item.addEventListener("click", () => {
      if (state.mode !== "manual") {
        state.selectedStudentId = null;
        state.editingStudentId = student.id;
        setStatus(`${student.name} 학생 정보를 편집 폼에 불러왔습니다.`);
        render();
        return;
      }

      state.selectedSeatId = null;
      state.selectedStudentId = student.id;
      state.editingStudentId = student.id;
      setStatus(`${student.name} 학생 정보를 확인 중입니다. 좌석 카드로 출발/도착 좌석을 선택해 배치하세요.`);
      render();
    });

    studentList.appendChild(item);
  });
}

function renderEditor() {
  const editingStudent = state.editingStudentId
    ? getStudentById(state.editingStudentId)
    : null;

  if (!editingStudent) {
    editorTitle.textContent = "학생 정보 편집 (학생을 선택하세요)";
    editNumberInput.value = "";
    editNameInput.value = "";
    editGenderSelect.value = "미정";
    return;
  }

  editorTitle.textContent = `${editingStudent.name} 학생 정보 편집`;
  editNumberInput.value = String(editingStudent.number);
  editNameInput.value = editingStudent.name;
  editGenderSelect.value = editingStudent.gender || "미정";
}

function updateModeButton() {
  manualModeBtn.textContent =
    state.mode === "manual" ? "수동 배치 모드 (활성)" : "수동 배치 모드";
}

function render() {
  updateModeButton();
  renderSeats();
  renderStudents();
  renderEditor();
}

loadAppState();

if (students.length === 0) {
  students.splice(0, students.length, ...structuredClone(defaultStudents));
}

setStatus("현재 상태가 이 브라우저에 자동 저장됩니다.");
render();
