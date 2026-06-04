import requests, os
from dotenv import load_dotenv

load_dotenv()

# 1) 브라우저에서 아래 URL 접속 후 code 값을 복사하세요.
# https://kauth.kakao.com/oauth/authorize?response_type=code&client_id={REST_API_KEY}&redirect_uri={REDIRECT_URI}&scope=talk_message

REST_API_KEY = os.getenv("KAKAO_REST_API_KEY", "").strip()
REDIRECT_URI = os.getenv("KAKAO_REDIRECT_URI", "").strip()
AUTHORIZATION_CODE = os.getenv("KAKAO_AUTHORIZATION_CODE", "").strip()


def main() -> None:
    if not REST_API_KEY or not REDIRECT_URI or not AUTHORIZATION_CODE:
        raise ValueError("REST_API_KEY, REDIRECT_URI, AUTHORIZATION_CODE 를 채워주세요.")

    resp = requests.post(
        "https://kauth.kakao.com/oauth/token",
        data={
            "grant_type": "authorization_code",
            "client_id": REST_API_KEY,
            "redirect_uri": REDIRECT_URI,
            "code": AUTHORIZATION_CODE,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()

    print("access_token:", data.get("access_token"))
    print("refresh_token:", data.get("refresh_token"))
    print("scope:", data.get("scope"))


if __name__ == "__main__":
    main()
