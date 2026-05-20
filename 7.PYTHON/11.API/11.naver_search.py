# -*- coding: utf-8 -*-
import requests
from dotenv import load_dotenv
import os

try:
    load_dotenv()

    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
    NAVER_REQUEST_URL = os.getenv("NAVER_REQUEST_URL")

    text = "생성형 AI"

    headers = {
        "X-Naver-Client-Id": NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
    }

    params = {
        "query": text,
        "display": 10,
        "start": 1,
        "sort": "sim"
    }

    response = requests.get(NAVER_REQUEST_URL, headers=headers, params=params)
    data = response.json()
    for item in data['items']:
        print(item)

except Exception as e:
    print("Error:", e)