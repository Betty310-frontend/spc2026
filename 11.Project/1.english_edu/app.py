"""
1. openai 관련 라이브러리를 다 불러온다. (dotenv, openai 등등)
2. 최종 페이지에서 채팅창 기능을 구현한다.
2-1. openai api를 호출해서 대화하는 기능을 만든다.
2-2. form 데이터를 받아서 BE에서 openai api를 호출하는 기능을 만든다.
2-3. openai api에서 스트리밍으로 응답이 오도록 해서, 채팅창에 실시간으로 답변이 뜨도록 한다. (SSE 적용해보자)
3. 학년, 커리큘럼에 따른 페이지에서 영어로 대화하도록 한다.
4. [추가] 메모리를 통해 대화 내용 컨텍스트를 기억하도록 한다.
"""

# -*- coding: utf-8 -*-
import os, requests
from dotenv import load_dotenv
from openai import OpenAI

from flask import Flask, jsonify, request, render_template

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# 각 학년별 커리큘럼 데이터
curriculums = { 
    1: [ "인사와 감정", "색깔과 숫자", "가족과 친구", "동물", "음식", "교실 물건", "날씨", "간단한 자기 표현" ], 
    2: [ "자기소개(이름, 나이, 좋아하는 것)", "우리 집/우리 가족", "음식 주문 기초", "취미와 놀이", "계절과 옷", "장소(학교, 공원, 집)", "시간 기초(아침/점심/저녁)", "간단한 묻고 답하기(What/Do you like...?)" ], 
    3: [ "학교생활(과목, 준비물)", "길 묻기 기초(Where is...?)", "하루 일과(시간+동작)", "건강(몸, 기분, 습관)", "쇼핑 기초(가격, 개수)", "여행/교통수단", "동물 비교(big/small, fast/slow)", "미니 스토리 만들기" ], 
    4: [ "문제 해결 대화(분실물, 도움 요청)", "음식/건강한 식습관", "취미 소개와 추천", "동네 소개", "환경 기초(재활용, 절약)", "문화(세계 인사법/축제)", "의견 말하기(I think..., In my opinion...)", "짧은 발표" ], 
    5: [ "세계 문화/나라 소개", "과학·자연 기초 주제(날씨, 동물 서식지)", "디지털 시민성(안전한 인터넷)", "진로 기초(꿈, 직업)", "협동 문제 해결(팀 미션)", "뉴스형 짧은 읽기", "이메일/메시지 영어", "프로젝트 준비" ], 
    6: [ "SDGs/환경/지역사회 문제", "미디어 리터러시(정보 비교)", "토론 기초(근거 제시)", "여행 기획(일정/예산)", "학교 행사 기획", "인터뷰와 설문", "결과 보고서 작성", "최종 영어 프로젝트 발표" ] }

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/')
def home():
    return render_template('home.html', grades=curriculums.keys())

@app.route('/grade/<int:grade>')
def grade(grade):
    if grade in curriculums:
        curriculums_index = list(enumerate(curriculums[grade]))
        return render_template('grade.html', grade=grade, curriculums=curriculums_index)
    return '해당 학년은 존재하지 않습니다.', 404

@app.route('/curriculum/<int:grade>/curriculum/<int:curriculum_id>')
def curriculum(grade, curriculum_id):
    if grade in curriculums and 0 <= curriculum_id < len(curriculums[grade]):
        curriculum_title = curriculums[grade][curriculum_id]
        return render_template('curriculum.html', grade=grade, curriculum_title=curriculum_title)
    return '해당 커리큘럼은 존재하지 않습니다.', 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)