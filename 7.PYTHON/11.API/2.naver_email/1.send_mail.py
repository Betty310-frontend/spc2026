# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template, make_response

import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

load_dotenv()

NAVER_SMTP_SERVER = os.getenv('NAVER_SMTP_SERVER')
NAVER_SMTP_PORT = int(os.getenv('NAVER_SMTP_PORT'))

NAVER_ID = os.getenv('NAVER_ID')
NAVER_EMAIL = f"{NAVER_ID}@naver.com"
NAVER_EMAIL_PASSWORD = os.getenv('NAVER_EMAIL_PASSWORD')

subject = "네이버 메일 보내기 테스트"
body = """
    <h1>이 메일은 파이썬을 통해서 발송된 테스트 메일입니다.</h1>
    <p>네이버 SMTP 서버를 사용하여 메일을 발송하는 예제입니다.</p>
"""

"""
MIMEText 객체를 생성하여 이메일이 작성 됌. 
MIMEText는 이메일의 본문을 나타내는 객체로, 
이메일의 내용을 텍스트 형식으로 표현할 수 있도록 도와줌.
"""
message = MIMEText(body, _subtype='html', _charset='utf-8')
message['Subject'] = subject
message['From'] = NAVER_EMAIL
message['To'] = NAVER_EMAIL

try:
    smtp = smtplib.SMTP(NAVER_SMTP_SERVER, NAVER_SMTP_PORT)
    smtp.starttls() # TLS(Transport Layer Security)를 사용하여 SMTP 서버와의 통신을 암호화
    smtp.login(NAVER_ID, NAVER_EMAIL_PASSWORD)
    smtp.sendmail(NAVER_EMAIL, message['To'], message.as_string())
    print("메일이 성공적으로 발송되었습니다.")
except Exception as e:
    print(f"메일 발송 중 오류 발생: {e}")
finally:
    smtp.quit() # SMTP 서버와의 연결을 종료