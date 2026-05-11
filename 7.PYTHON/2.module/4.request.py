# 외부 모듈은 pip install 명령어로 설치해야 사용할 수 있다.
# 외부 HTTP 요청을 대신 해주는 라이브러리
import requests

# response = requests.get('http://httpbin.org/get')

# print('--- response status code ---')
# print(response.status_code)
# print('\n--- response header ---')
# print(response.headers)
# print('\n--- response text ---')
# print(response.text)

resp = requests.get('https://api.github.com')
if (resp.status_code == 200):
    print(resp.text)
else:
    print(f"HTTP 요청 실패: {resp.status_code}")

# curr_user_url = resp.json()["current_user_url"]
# curr_user_resp = requests.get(curr_user_url)
# print(curr_user_resp.text)