import requests
import os
from dotenv import load_dotenv


try:
    load_dotenv()
    url = os.environ.get('GITHUB_URL')

    resp = requests.get(url)
    repos = resp.json()

    # print(data)
    data = []

    for repo in repos:
        name = repo['name']
        html_url = repo['html_url']
        description = repo['description']
        data.append({'name':name, 'html_url':html_url, 'desc':description})

    print(f"{'리포이름':<30} {'리포URL':<50} 설명: {'설명':<20}")
    for d in data:
        print(f"{d['name']:<30} {d['html_url']:<50} {d['desc']:<20}")

except Exception as e:
    print(e)


