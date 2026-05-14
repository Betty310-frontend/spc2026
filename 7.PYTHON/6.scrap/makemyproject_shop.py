"""
1. 각 페이지마다 상품명, 가격 가져오기
2. 각 페이지 안의 설명, 구매량, 댓글 가져오기
3. 로그인 후 추가 상품정보 가져오기
"""

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv
import json
import re
from urllib.parse import urljoin
import os
from dotenv import load_dotenv


def to_int(text: str) -> int:
    digits = re.sub(r'[^0-9]', '', text or '')
    return int(digits) if digits else 0


def login(page, base_url: str, user_id: str, password: str) -> None:
    page.goto(base_url, wait_until='networkidle')

    id_input = page.locator('input#uid').first
    pw_input = page.locator('input#upw').first
    login_button = page.locator('button#loginBtn').first

    id_input.fill(user_id)
    pw_input.fill(password)
    login_button.click()

    page.wait_for_function(
        """() => !document.body.innerText.includes('현재 비회원')""",
        timeout=10000
    )

    status_text = page.locator('body').inner_text()
    if '현재 비회원' in status_text:
        raise RuntimeError('로그인 실패: 아직 비회원 상태입니다. 아이디/비밀번호 또는 선택자를 확인하세요.')


def collect_links(page, base_url: str, label: str) -> list[str]:
    links = []
    page_num = 1

    while True:
        print(f"[{label}] 페이지 {page_num} 크롤링 시작...")

        html = page.content()
        soup = BeautifulSoup(html, 'html.parser')
        cards = soup.select('div#products .card')

        for card in cards:
            link = card.find('a', href=True)
            if link:
                links.append(urljoin(base_url, link['href']))

        print(f"[{label}] 페이지 {page_num}에서 {len(cards)}개의 상품 링크 수집 완료.")

        next_page_num = page_num + 1
        next_button = page.locator(f'.pager button:has-text("{next_page_num}")').first

        if next_button.count() == 0 or next_button.is_disabled():
            print(f"[{label}] 페이지 {page_num}까지 수집 완료(다음 페이지 없음).")
            break

        next_button.click()
        page.wait_for_function(
            """(n) => {
                const btn = [...document.querySelectorAll('.pager button')]
                    .find((b) => b.textContent.trim() === String(n));
                return !!btn && btn.disabled;
            }""",
            arg=next_page_num,
        )
        page_num = next_page_num

    unique_links = list(dict.fromkeys(links))
    print(f"[{label}] 총 {len(unique_links)}개의 상품 링크 수집 완료.")
    return unique_links


def collect_products(page, links: list[str], label: str) -> list[dict]:
    products = []

    for idx, link in enumerate(links, start=1):
        print(f"[{label}] 상세 페이지 크롤링 중... ({idx}/{len(links)})")
        page.goto(link, wait_until='networkidle')

        detail_html = page.content()
        detail_soup = BeautifulSoup(detail_html, 'html.parser')

        h2_tag = detail_soup.select_one('h2')
        name = h2_tag.get_text(strip=True) if h2_tag else ''

        description_tag = h2_tag.find_next_sibling(class_='muted') if h2_tag else None
        description = description_tag.get_text(strip=True) if description_tag else ''

        origin_price_text = detail_soup.select_one('#priceSummary .muted')
        sale_price_text = detail_soup.select_one('#priceSummary b')
        sales_text = detail_soup.select_one('#sales')

        review_list = []
        for review in detail_soup.select('.review'):
            user_tag = review.select_one('b')
            content_tag = review.select_one('div')
            review_list.append(
                {
                    'user': user_tag.get_text(strip=True) if user_tag else '',
                    'content': content_tag.get_text(' ', strip=True) if content_tag else '',
                }
            )

        products.append(
            {
                'url': link,
                'name': name,
                'origin_price': to_int(origin_price_text.get_text(strip=True) if origin_price_text else ''),
                'sale_price': to_int(sale_price_text.get_text(strip=True) if sale_price_text else ''),
                'description': description,
                'sales': to_int(sales_text.get_text(strip=True) if sales_text else ''),
                'review': json.dumps(review_list, ensure_ascii=False),
            }
        )

    print(f"[{label}] 총 {len(products)}개의 상세 상품 데이터 수집 완료.")
    return products


def write_products_csv(file_name: str, products: list[dict]) -> None:
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=['url', 'name', 'origin_price', 'sale_price', 'description', 'sales', 'review'],
        )
        writer.writeheader()
        writer.writerows(products)


def build_visibility_rows(guest_products: list[dict], login_products: list[dict]) -> list[dict]:
    guest_map = {item['url']: item for item in guest_products}
    login_map = {item['url']: item for item in login_products}

    rows = []
    for url in sorted(set(guest_map.keys()) | set(login_map.keys())):
        base = login_map.get(url) or guest_map.get(url)
        rows.append(
            {
                'url': url,
                'name': base['name'],
                'origin_price': base['origin_price'],
                'sale_price': base['sale_price'],
                'description': base['description'],
                'sales': base['sales'],
                'review': base['review'],
                'guest_visible': 'O' if url in guest_map else 'X',
                'login_visible': 'O' if url in login_map else 'X',
            }
        )
    return rows

try:
    load_dotenv()
    url = os.environ.get('BASE_URL')
    user_id = os.environ.get('USER_ID')
    password = os.environ.get('PASSWORD')
    if not url or not user_id or not password:
        raise RuntimeError('.env 파일에 BASE_URL, USER_ID, PASSWORD가 모두 정의되어야 합니다.')

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        try:
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')
            guest_links = collect_links(page, url, '비로그인')
            guest_products = collect_products(page, guest_links, '비로그인')
            write_products_csv('makemyproject_shop_products.csv', guest_products)
            print(f"비로그인 상품 저장 완료: {len(guest_products)}개")

            login(page, url, user_id, password)
            print('로그인 성공. 회원 데이터 수집을 시작합니다.')
            login_links = collect_links(page, url, '로그인')
            login_products = collect_products(page, login_links, '로그인')
            write_products_csv('makemyproject_shop_products_by_login.csv', login_products)
            print(f"로그인 상품 저장 완료: {len(login_products)}개")

            visibility_rows = build_visibility_rows(guest_products, login_products)
            with open('makemyproject_shop_products_visibility.csv', 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        'url',
                        'name',
                        'origin_price',
                        'sale_price',
                        'description',
                        'sales',
                        'review',
                        'guest_visible',
                        'login_visible',
                    ],
                )
                writer.writeheader()
                writer.writerows(visibility_rows)
            print(f"통합 노출여부 파일 저장 완료: {len(visibility_rows)}개")
        finally:
            browser.close()

except Exception as e:
    print(f"Error occurred while defining the URL: {e}")