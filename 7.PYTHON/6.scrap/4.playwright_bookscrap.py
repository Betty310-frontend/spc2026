from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto('https://books.toscrape.com')

    # 책 목록 가져오기
    books = page.locator('article.product_pod')
    # print(books.count())

    rating_num_dict = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5
    }

    for i in range(books.count()):
        book = books.nth(i)
        title = book.locator('h3 a').get_attribute('title')
        price = book.locator('.price_color').inner_text()
        price = price.replace('£', '')  # '£' 제거

        rating = book.locator('p.star-rating').get_attribute('class').split()[1] 
        rating = rating_num_dict.get(rating, 0)  # 문자열 평점을 숫자로 변환

        print(f'Title: {title}, Price: {price}, Rating: {rating}')

    browser.close()