# React Shop

Flask + Next.js 쇼핑몰 프로젝트

---

## Backend (Flask)

### 요구사항

- Python 3.x

### 설치 및 실행

```bash
cd backend

# 패키지 설치
pip install -r requirements.txt

# 서버 실행
python app.py
```

### 접속 링크

| 항목         | URL                        |
| ------------ | -------------------------- |
| REST API     | http://127.0.0.1:5001/api  |
| Swagger 문서 | http://127.0.0.1:5001/docs |

---

## Frontend (Next.js)

### 요구사항

- Node.js 20.12.2 (nvm 사용 권장)

### 설치 및 실행

```bash
cd frontend

# Node.js 버전 설정 (nvm 사용 시)
nvm use

# 패키지 설치
npm install

# 개발 서버 실행
npm run dev
```

### 접속 링크

| 항목 | URL                   |
| ---- | --------------------- |
| 앱   | http://localhost:3000 |

---

## 환경 변수

**backend/.env**

```
SECRET_KEY=your_secret_key
DB_NAME=your_db_name
```

**frontend/.env.local**

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:5001
```
