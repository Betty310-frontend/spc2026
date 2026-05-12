
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://news.naver.com'

res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

# print(soup.prettify())

news_data = []

news_feed = soup.select('.comp_news_feed')

for feed in news_feed:
    try:
        journal_name = feed.select_one('.cnf_journal_name').text
        news_time = feed.select_one('.cnf_journal_sub').text
        news_title = feed.select_one('.cnf_news_title').text
        news_items = feed.select('.cnf_news_item')

        news_data.append({
            'journal_name': journal_name,
            'news_title': news_title,
            'news_time': news_time
        })

        for item in news_items:
            item_title = item.select('a')[0].text
            news_data.append({
                'journal_name': journal_name,
                'news_title': item_title,
                'news_time': news_time
            })
    except:
        # print(feed) # 네이버 뉴스 내 "언론사별 심층기획" 섹션은 구조가 달라서 에러 발생. 제외 처리
        continue

with open('naver_news.csv', 'w', newline='', encoding='utf-8') as file:
    headers = news_data[0].keys()
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(news_data)