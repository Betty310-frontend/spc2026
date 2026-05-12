import requests

url = 'https://www.example.com'

res = requests.get(url)

html = res.text
print(type(html)) # <class 'str'>

print('\n' + '-'*50 + '\n')

while "<h1>" in html:
    start = html.find('<h1>')
    end = html.find('</h1>')

    text = html[start:end+len('</h1>')]
    print(text)
    break

