from bs4 import BeautifulSoup

html = """
<html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Title</h1>
        <p>Paragraph1</p>
        <p>Paragraph2</p>
    </body>
</html>"""

soup = BeautifulSoup(html, 'html.parser')

# print(soup)

heading = soup.find_all('h1')
paragraphs = soup.find_all('p')

print(heading)
print(paragraphs)