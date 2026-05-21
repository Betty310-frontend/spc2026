import imaplib
import email
from email.header import decode_header

from dotenv import load_dotenv
import os

load_dotenv()

NAVER_IMAP_SERVER = os.getenv('NAVER_IMAP_SERVER')
NAVER_IMAP_PORT = int(os.getenv('NAVER_IMAP_PORT'))

NAVER_ID = os.getenv('NAVER_ID')
NAVER_EMAIL = f"{NAVER_ID}@naver.com"
NAVER_EMAIL_PASSWORD = os.getenv('NAVER_EMAIL_PASSWORD')

mail = imaplib.IMAP4_SSL(NAVER_IMAP_SERVER, NAVER_IMAP_PORT)
mail.login(NAVER_ID, NAVER_EMAIL_PASSWORD)

mail.select("inbox") # 받은 편지함 선택
status, messages = mail.search(None, "ALL") # 모든 이메일 검색

email_ids = messages[0].split()
latest_email_id = email_ids[-1] # 가장 최근 이메일 ID 가져오기

# print(f"나의 메일들: {email_ids}")
# print(f"가장 최근 메일 ID: {latest_email_id}")

status, msg_data = mail.fetch(latest_email_id, "RFC822") # 이메일 데이터 가져오기
# print(status, msg_data)

for response_part in msg_data:
    if isinstance(response_part, tuple):
        msg = email.message_from_bytes(response_part[1]) # 이메일 메시지 객체 생성

        # 이메일 제목 디코딩
        subject, encoding = decode_header(msg['Subject'])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else 'utf-8')

        print(f"제목: {subject}")

        from_ = msg.get('From')
        print(f"보낸 사람: {from_}")

        to_ = msg.get('To')
        print(f"받는 사람: {to_}")

        # 이메일 본문 추출
        if msg.is_multipart():
            print('멀티파트 생략')
        else:
            body = msg.get_payload(decode=True).decode('utf-8')
            print(f"본문: {body}")