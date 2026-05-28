# -*- coding: utf-8 -*-
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from flask import Flask, jsonify, request, render_template, make_response

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/api/name')
def name():
    prompt = [
        SystemMessage(content='You are a creative branding expert.'),
        HumanMessage(content="What's a good company name that makes computer games. Do not give any explanation. Just give me the names."),
    ]
    result = llm.invoke(prompt)
    return jsonify({'result':'success', 'chatbot': result.content})

@app.route('/api/dinner')
def dinner():
    prompt = [
        SystemMessage(content='당신은 경력 10년 차 호텔 쉐프입니다.'),
        HumanMessage(content='오늘 저녁 메뉴를 추천해줘.'),
    ]
    result = llm.invoke(prompt)
    # print(result.content)
    return jsonify({'result':'success', 'chatbot': result.content})

@app.route('/api/name', methods=['POST'])
def name2():
    data = request.get_json()
    product = data.get('product')
    user_prompt = f"What's a good company name for a {product}? Do not give any explanation. Just give me the names."
    print(user_prompt)

    prompt = [
        SystemMessage(content='You are a creative branding expert.'),
        HumanMessage(content=user_prompt),
    ]
    result = llm.invoke(prompt)
    return jsonify({'result':'success', 'chatbot': result.content})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
