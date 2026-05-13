from playwright.sync_api import sync_playwright

url = 'https://www.naver.com'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto(url)

    # 뉴스 섹션 가져오기
    page.click('text=엔터')
    page.wait_for_load_state('networkidle')

    articles = page.locator()

    browser.close()