import requests
from bs4 import BeautifulSoup

url = 'https://www.example.com'

res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')
# print(soup.prettify())

print('\n' + '-'*50 + '\n')

title = soup.find('title')
print(title)

paragraphs = soup.find_all('p')
print(paragraphs)


divs = soup.find_all('div')
print(divs)

for elem in divs:
    # link = elem.find('a')
    link = elem.a
    if link:
        print(link['href'])