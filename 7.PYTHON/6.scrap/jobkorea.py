from bs4 import BeautifulSoup
import csv
from pathlib import Path
from urllib.parse import urljoin

import requests

SEARCH_URL = 'https://www.jobkorea.co.kr/Search/?stext=%EA%B0%9C%EB%B0%9C&tabType=recruit'
HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/136.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

try:
    response = requests.get(SEARCH_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    job_cards = soup.select('div', attrs={'data-sentry-component': 'CardJob'})
    
    links = []

    for card in job_cards:
        link_tag = card.select_one('a')
        if link_tag and 'href' in link_tag.attrs:
            job_link = urljoin(SEARCH_URL, link_tag['href'])
            links.append(job_link)
except:
    print('알 수 없는 에러 발생')