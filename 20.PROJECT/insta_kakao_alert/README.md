# Instagram -> Kakao Alert (1-month MVP)

특정 인스타 계정의 새 게시물을 감시하고, 캡션에 키워드가 포함된 경우 카카오톡 `나에게 보내기`로 알림을 전송합니다.

## Why this approach

- 카카오 오픈채팅 자동 발송은 공식 API가 없어 운영 리스크가 큽니다.
- 카카오 공식 API로 안정적으로 가능한 경로는 `나에게 보내기`입니다.
- 1개월 MVP 목적에 적합한 최소 구현입니다.

## 1) Install

```bash
pip install -r requirements.txt
```

## 2) Configure

`.env.example`를 참고해 `.env`를 만드세요.

필수 값:
- `INSTAGRAM_USERNAME`
- `KEYWORDS`
- `KAKAO_REST_API_KEY`
- `KAKAO_REFRESH_TOKEN`

## 3) Kakao token preparation (one-time)

Kakao Developers 앱에서 아래를 준비하세요.

1. 카카오 로그인 활성화
2. Redirect URI 등록
3. 동의항목에서 `talk_message` 권한 설정
4. 사용자 인증 후 Authorization Code 발급
5. Code로 Refresh Token 발급

참고: 이 프로젝트는 Refresh Token으로 Access Token을 매 알림 시점에 갱신합니다.

빠른 발급 방법:

1. `kakao_token_helper.py` 파일에 `REST_API_KEY`, `REDIRECT_URI` 입력
2. 파일 상단 URL에서 `code` 발급
3. `AUTHORIZATION_CODE` 입력 후 실행
4. 출력된 `refresh_token`을 `.env`의 `KAKAO_REFRESH_TOKEN`에 저장

## 4) Run

```bash
python app.py
```

## Behavior

- 첫 실행에서 `SEED_WITH_LATEST=true`이면 현재 최신 게시물들은 "이미 처리됨"으로 저장하고 알림을 보내지 않습니다.
- 이후 새 게시물만 감지합니다.
- 키워드 매칭 시 카카오톡으로 게시물 링크와 캡션 요약을 전송합니다.

## Notes

- 인스타 계정이 비공개거나 접근 제한 시 수집이 실패할 수 있습니다.
- 인스타 구조 변경/차단 정책에 따라 크롤링 로직이 깨질 수 있습니다.
- 오픈채팅 자동전송이 꼭 필요하면, 기술적으로는 브라우저 자동화 같은 비공식 우회가 가능하지만 안정성과 정책 측면에서 권장하지 않습니다.
