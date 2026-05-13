from playwright.sync_api import sync_playwright
import csv

links = []
news_data = []

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        url = 'https://news.naver.com/section/105'
        page.goto(url, wait_until='networkidle')

        headlines = page.locator('.sa_text a')

        for i in range(headlines.count()):
            news = headlines.nth(i)

            title = news.inner_text().strip()

            href = news.get_attribute('href')

            if title and href:
                links.append({
                    "title": title,
                    "href": href
                })

        for news in links:
            print('-' * 50)
            
            try:
                title = news['title']
                href = news['href']

                page.goto(href, wait_until='networkidle')

                content = page.locator('#dic_area').inner_text().strip()
                # print('Content:', content[:100])

                news_data.append({
                    "title": title,
                    "href": href,
                    "content": content
                })
            except Exception as e:
                print(f"Error processing news item '{news['title']}': {e}")
                continue

        browser.close()

except Exception as e:
    print(f"Error occurred: {e}")

try:
    with open('naver_news_with_playwright.csv', 'w', newline='', encoding='utf-8') as file:
        headers = news_data[0].keys()
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(news_data)
except Exception as e:
    print(f"Error writing to CSV: {e}")