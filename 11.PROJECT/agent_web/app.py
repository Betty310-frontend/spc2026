"""
금융 도우미 에이전트 챗봇 Web버전 만들기

- 툴 추가
  - from fin_tools.py
"""
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from fin_tools import TOOLS

import json
from langchain_core.messages import AIMessageChunk
from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

SYSTEM = """
    당신은 금융 정보 비서입니다.
    다음과 같은 도구들을 활용해서 사용자의 질문에 답변하세요.
    
    도구 사용 가이드:
    1. get_news
      - 네이버 뉴스를 가져오는 도구입니다. 'query' 인자로 검색어를 입력하면 관련 뉴스를 반환합니다.
    2. get_company_info
      - 구글 검색으로 기업 개요/최근 정보를 조회하는 도구입니다. 'company_name' 인자로 기업명을 입력하면 관련 정보를 반환합니다.
    3. get_exchange_rate
      - 환율을 조회하는 도구입니다. 'rate_code'에 인자로 통화 코드를 입력하면 원화(KRW) 기준으로 환율을 반환합니다.
    4. get_stock_price
      - 주가를 조회하는 도구입니다. 'ticker' 인자로 기업의 티커 코드를 입력하면 주가를 반환합니다.

    환율/주가 같은 수치 데이터는 반드시 도구를 통해서 확인하세요. (추측 또는 과거 데이터 이용 금지)
    출처 링크가 있으면 반드시 함께 제시하세요.
    금융 정보 외 질문에는 답변하지 마세요.
"""

agent = create_agent(llm, TOOLS, system_prompt=SYSTEM)

def ask(question):
    try:
        result = agent.invoke({
            "messages": [("user", question)]
        })
        tool_used = [call["name"] for msg in result["messages"]
                if getattr(msg, "tool_calls", None) for call in msg.tool_calls]
        print(f"사용된 도구: {tool_used or '(없음)'}")
        return result['messages'][-1].content
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"
    
app = Flask(__name__, static_folder="public", static_url_path="")

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set UTF-8 in response headers (JSON only — SSE must not be overridden)
@app.after_request
def set_utf8_header(response):
    if response.content_type.startswith('application/json'):
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.post('/api/ask')
def api_ask():
  """
  일반 질문-답변 API (스트리밍 X)
  """
  try:
    question = request.json.get('question', '')

    if not question:
        return jsonify({'result': 'error', 'message': '질문이 없습니다.'}), 400
    
    answer = ask(question)
    return jsonify({'result': 'success', 'answer': answer})
  
  except Exception as e:
    return jsonify({'result': 'error', 'message': str(e)}), 500

@app.post('/api/ask-stream')
def api_ask_stream():
    try:
        question = request.json.get('question', '')
        if not question:
            return jsonify({'result': 'error', 'message': '질문이 없습니다.'}), 400

        @stream_with_context
        def generate():
            try:
                for chunk, _ in agent.stream(
                    {"messages": [("user", question)]},
                    stream_mode="messages"
                ):
                    if (
                        isinstance(chunk, AIMessageChunk)
                        and chunk.content
                        and not getattr(chunk, 'tool_call_chunks', None)
                    ):
                        data = json.dumps({"token": chunk.content}, ensure_ascii=False)
                        yield f"data: {data}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                data = json.dumps({"error": str(e)}, ensure_ascii=False)
                yield f"data: {data}\n\n"

        return Response(
            generate(),
            mimetype='text/event-stream',
            headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
        )
    except Exception as e:
        return jsonify({'result': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)