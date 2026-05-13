from bs4 import BeautifulSoup
import csv
import re
from pathlib import Path
from urllib.parse import urljoin

import requests

SEARCH_URL = 'https://www.jobkorea.co.kr/Search/?stext=%EA%B0%9C%EB%B0%9C&tabType=recruit'
HEADERS = {"User-Agent": "Mozilla/5.0"}


def extract_skills(q_div):
    spans = q_div.find_all('span')
    if not spans:
        return None

    label = spans[0].get_text(strip=True)
    if '스킬' not in label:
        return None

    # 카드마다 마크업이 달라 span/a/li에 스킬이 나뉘어 있을 수 있어 모두 수집한다.
    skill_candidates = []
    for node in q_div.select('span, a, li'):
        text = node.get_text(strip=True)
        if text and text != label:
            skill_candidates.append(text)

    if skill_candidates:
        return ', '.join(skill_candidates)

    # 셀렉터로 수집이 안 되는 케이스를 위해 텍스트 기반으로 한 번 더 시도한다.
    full_text = q_div.get_text(' ', strip=True)
    full_text = re.sub(r'^.*?스킬', '', full_text).strip(' ,')
    return full_text if full_text else '(없음)'

try:
    response = requests.get(SEARCH_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    job_cards = soup.select('div[data-sentry-component="CardJob"]')

    links = []
    job_data = []

    for card in job_cards[:20]:  # 상위 20개 공고만 처리
        link_tag = card.select_one('a[href]')
        if link_tag:
            links.append(link_tag['href'])

    links = list(dict.fromkeys(links))  # 중복 제거
    print(f'처리할 링크: {len(links)}개\n')

    for idx, link in enumerate(links, 1):
        res = requests.get(link, headers=HEADERS, timeout=15)
        res.raise_for_status()
        job_soup = BeautifulSoup(res.text, 'html.parser')
        company_name_tag = job_soup.select_one('h2')
        company_name = company_name_tag.get_text(strip=True) if company_name_tag else 'N/A'
        skills_text = '(없음)'

        q_divs = job_soup.select('div[data-sentry-component="QualificationItem"]')
        print(f'{idx}. [{company_name}] - QualificationItem {len(q_divs)}개')

        for q_div in q_divs:
            spans = q_div.find_all('span')
            if not spans:
                continue

            label = spans[0].get_text(strip=True)
            print(f'   - {label}')

            extracted = extract_skills(q_div)
            if extracted is not None:
                skills_text = extracted
                print(f'      -> 추출 스킬: {skills_text}')

        job_data.append({'company': company_name, 'skills': skills_text, 'link': link})
            

except Exception as e:
    print(f'알 수 없는 에러 발생: {e}')

print(f'\n\n수집 완료: {len(job_data)}개의 스킬 데이터')

# CSV 파일로 저장
try:
    with open('jobkorea_jobs.csv', 'w', newline='', encoding='utf-8') as file:
        fieldnames = job_data[0].keys() if job_data else ['company', 'skills', 'link']  # 데이터가 없을 경우 기본 필드명 설정
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for job in job_data:
            writer.writerow(job)
except Exception as e:
    print(f'CSV 파일 저장 중 에러 발생: {e}')