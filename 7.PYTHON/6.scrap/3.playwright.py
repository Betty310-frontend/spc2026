from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

import csv

url = 'https://www.naver.com'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    # 새 페이지 열기
    page = browser.new_page()

    # 페이지 로드
    page.goto(url, wait_until='networkidle')

    # 스크린샷 저장
    # page.screenshot(path='naver.png')

    # 콘텐츠 추출
    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')

    # print(soup)

    browser.close()