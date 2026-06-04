"""
Whisper (속삭임)
말을 기반으로 text로 변환: STT (Speech-to-Text)
"""

from dotenv import load_dotenv

from openai import OpenAI

load_dotenv()

client = OpenAI()

def transcribe_audio(file):
    """
    오디오를 설명하는 함수
    """
    with open(file, 'rb') as af:
        transcript = client.audio.transcriptions.create(
            file=af,
            model='whisper-1',
            response_format='text',
            language='ko', # en, ko, ja, zh 등등
            # prompt='이 오디오 파일은 무엇에 관한 것인가요?'
        )

        return transcript
    
result = transcribe_audio('sample.mp3')
print('음성 인식 결과:', result)
