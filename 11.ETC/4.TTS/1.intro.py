from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# text = "안녕하세요, OpenAI의 음성 생성 예제입니다. 한국말을 얼마나 잘 하는지 확인 중입니다."
text = """
    간장 공장 공장장은 강 공장장이고 된장 공장 공장장은 장 공장장이다.
    들의 콩깍지는 깐 콩깍지냐, 안 깐 콩깍지냐. 
    깐 콩깍지면 어떻고 안 깐 콩깍지면 어떠냐. 
    깐 콩깍지나 안 깐 콩깍지나 콩깍지는 다 콩깍지인데.
    안 촉촉한 초코칩 나라에 살던 안 촉촉한 초코칩이
    촉촉한 초코칩 나라의 촉촉한 초코칩을 보고
    촉촉한 초코칩이 되고 싶어서
    촉촉한 초코칩 나라에 갔는데,
    촉촉한 초코칩 나라의 촉촉한 문지기가
    "넌 촉촉한 초코칩이 아니고 안 촉촉한 초코칩이니까
    안 촉촉한 초코칩 나라에서 살아"
    라고 해서 안 촉촉한 초코칩은
    촉촉한 초코칩이 되는 것을 포기하고
    안 촉촉한 눈물을 흘리며 안 촉촉한 초코칩 나라로 돌아갔다.
"""

response = client.audio.speech.create(
    model='tts-1',
    voice='alloy',
    input=text
)

response.write_to_file('output.mp3')
print('음성 생성 완료: output.mp3')