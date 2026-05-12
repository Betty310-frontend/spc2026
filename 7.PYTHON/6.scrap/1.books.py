"""
# 1. https://books.toscrape.com 에 접속해서 페이지를 받아온다
# 2. DOM 을 bs4로 구성한다
# 3. 첫 페이지의 도서명, 평점, 가격을 받아온다
# 4. CSV파일로 저장한다.
"""

import requests
from bs4 import BeautifulSoup
import csv

url = "https://books.toscrape.com"

res = requests.get(url)
soup = BeautifulSoup(res.text, "html.parser")


products = soup.select(".product_pod")

books = []
korean_won = 2016.79 # 2025-05-12 기준 환율
rating_num_dict = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}
full_star = '★'
empty_star = '☆'
rating_star_dict = {
    'One': full_star + empty_star*4,
    'Two': full_star*2 + empty_star*3,
    'Three': full_star*3 + empty_star*2,
    'Four': full_star*4 + empty_star,
    'Five': full_star*5
}

for product in products:
    title = product.select('h3 a')[0]['title']
    thumbnail = product.select('.image_container img')[0]['src']
    rating = product.select('.star-rating')[0]['class'][1]
    price = product.select('.product_price .price_color')[0].text
    parsed_price = price.replace('Â£', '')  # 'Â£' 제거
    won_price = float(parsed_price.replace('£', '')) * korean_won

    books.append({"Title": title, "Thumbnail": thumbnail, "Rating": rating_num_dict[rating], "Rating Stars": rating_star_dict[rating], "Price (£)": parsed_price, "Price (₩)": round(won_price, 2)})

# print(books)

with open('books.csv', 'w', newline='', encoding='utf-8') as file:
    fieldnames = books[0].keys() # Header = 딕셔너리의 키
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader() # Header 작성
    writer.writerows(books)