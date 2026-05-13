from playwright.sync_api import sync_playwright
import csv

url = 'https://news.naver.com/section/105'

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto(url, wait_until='networkidle')

        news_data = []

        news_items = page.locator('a.sa_text_title')

        for i in range(news_items.count()):
            title = news_items.nth(i).inner_text()
            news_items.nth(i).click()
            page.wait_for_load_state('networkidle')
            page.wait_for_selector('#dic_area')  # 본문이 로드될 때까지 대기

            content = page.locator('#dic_area').inner_text()

            news_data.append({
                "title": title,
                "content": content
            })

            page.go_back()
            page.wait_for_load_state('networkidle')
            new_items = page.locator('a.sa_text_title')  # 뉴스 아이템 다시 로드

        browser.close()

except Exception as e:
    print(f"Error occurred: {e}")

print(news_data)

try:
    with open('naver_news_with_playwright.csv', 'w', newline='', encoding='utf-8') as file:
        headers = news_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(news_data)
except Exception as e:
    print(f"Error writing to CSV: {e}")