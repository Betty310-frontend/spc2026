"""
- 툴 추가
  1. 네이버 뉴스를 가져온다. (API_key 필요)
  2. 구글 검색으로 기업 개요/최근 정보를 조회한다. (API_key 필요)
  3. 환율을 조회한다. (https://open.er-api.com/v6/latest/USD)
  4. 주가를 조회한다.
"""

import os, requests
from dotenv import load_dotenv

from langchain_core.tools import tool

load_dotenv()

@tool
def get_news(query: str) -> str:
    """
    네이버 뉴스를 가져오는 도구입니다. 'query' 인자로 검색어를 입력하면 관련 뉴스를 반환합니다.
    """
    client_id = os.getenv('NAVER_CLIENT_ID')
    client_secret = os.getenv('NAVER_CLIENT_SECRET')
    news_url = os.getenv('NAVER_SEARCH_NEWS_URL')   

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }

    params = {
        "query": query,
        "display": 3,
        "start": 1,
        "sort": "sim"
    }

    try:
        response = requests.get(news_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

@tool
def get_company_info(company_name: str) -> str:
    """
    구글 검색(Serper)으로 기업 개요/최근 정보를 조회하는 도구입니다. 'company_name' 인자로 기업명을 입력하면 관련 정보를 반환합니다.
    """
    serper_api_key = os.getenv('SERPER_API_KEY')
    serper_google_search_url = os.getenv('SERPER_GOOGLE_SEARCH_URL')

    headers = { 
        'X-API-KEY': serper_api_key, 
        'Content-Type': 'application/json'
    }

    data = {
        "q": company_name,
        "hl": "ko"
    }

    try:
        response = requests.post(serper_google_search_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

@tool
def get_exchange_rate(rate_code: str) -> float:
    """
    환율을 조회하는 도구입니다. 'rate_code'에 인자로 통화 코드를 입력하면 원화(KRW) 기준으로 환율을 반환합니다.
    """
    exchange_api_url = os.getenv('EXCHANGE_API_URL')
    krw_key = 'KRW'
    target_key = rate_code.upper()

    try:
        response = requests.get(exchange_api_url)
        response.raise_for_status()
        data = response.json()
        rates = data.get('rates', {})
        if krw_key in rates and target_key in rates:
            return rates[krw_key] / rates[target_key]
        else:
            return {"error": "해당 통화 코드를 찾을 수 없습니다."}
    except requests.RequestException as e:
        return {"error": str(e)}

@tool
def get_stock_price(ticker: str) -> float:
    """
    yfinance 라이브러리를 사용하여 다양한 기업의 주가 조회 가능
    'ticker' 인자로 기업의 티커 코드를 입력하면 주가를 반환합니다.
    ex) 애플('AAPL'), 삼성전자('005930.KS')
    """
    # pip install yfinance
    import yfinance as yf

    data = yf.Ticker(ticker).history(period='1d')

    if not data.empty:
        return data['Close'].iloc[-1]
    else:
        return {"error": "주가 데이터를 가져올 수 없습니다."}

TOOLS = [get_news, get_company_info, get_exchange_rate, get_stock_price]