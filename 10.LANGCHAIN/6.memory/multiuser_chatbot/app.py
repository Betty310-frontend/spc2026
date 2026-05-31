from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()

app = Flask(__name__)
app.secret_key = 'chatbot_secret_key_2026'

# ─── 간단한 사용자 DB (실제 서비스에서는 DB 사용 권장) ───────────────
USERS = {
    'user1': '1234',
    'user2':   '1234',
    'user3': '1234',
}

# ─── LangChain 설정 ───────────────────────────────────────────────────
llm = ChatOpenAI(model='gpt-4o-mini')

parser = StrOutputParser()

prompt = ChatPromptTemplate.from_messages([
    ('system', '당신은 친절하고 유능한 한국어 AI 어시스턴트입니다. 사용자의 이전 대화를 기억하고 자연스럽게 대화를 이어가세요.'),
    MessagesPlaceholder('history'),
    ('user', '{input}'),
])

chain = prompt | llm | parser

# ─── 세션별 대화 기록 저장소 ─────────────────────────────────────────
# key: username, value: InMemoryChatMessageHistory
user_histories: dict[str, InMemoryChatMessageHistory] = {}

MAX_HISTORY = 20  # 최근 20개 메시지까지만 유지

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """사용자 ID로 대화 기록을 가져오거나 새로 생성한다."""
    if session_id not in user_histories:
        user_histories[session_id] = InMemoryChatMessageHistory()
    return user_histories[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history',
)

# ─── 라우트 ──────────────────────────────────────────────────────────
@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('chat_page'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('chat_page'))
        else:
            error = '아이디 또는 비밀번호가 올바르지 않습니다.'

    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/chat')
def chat_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    # 기존 대화 기록 가져오기 (최근 20개)
    history = get_session_history(username)
    messages = history.messages[-MAX_HISTORY:]

    chat_history = []
    for msg in messages:
        role = 'user' if msg.__class__.__name__ == 'HumanMessage' else 'ai'
        chat_history.append({'role': role, 'content': msg.content})

    return render_template('chat.html', username=username, chat_history=chat_history)


@app.route('/api/chat', methods=['POST'])
def api_chat():
    if 'username' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    username = session['username']
    data = request.get_json()
    user_input = data.get('message', '').strip()

    if not user_input:
        return jsonify({'error': '메시지를 입력해주세요.'}), 400

    # 히스토리를 최근 MAX_HISTORY 개로 잘라서 프롬프트에 넘기기 위해
    # history 슬라이싱을 직접 처리
    history_obj = get_session_history(username)

    # 최근 MAX_HISTORY 개만 사용하는 임시 래퍼
    trimmed_messages = history_obj.messages[-(MAX_HISTORY):]

    answer = chain.invoke({
        'input': user_input,
        'history': trimmed_messages,
    })

    # 실제 히스토리에 저장
    history_obj.add_user_message(user_input)
    history_obj.add_ai_message(answer)

    # 전체 메시지가 MAX_HISTORY를 초과하면 오래된 것부터 제거
    if len(history_obj.messages) > MAX_HISTORY:
        # InMemoryChatMessageHistory는 messages 리스트를 직접 수정 가능
        history_obj.messages = history_obj.messages[-MAX_HISTORY:]

    return jsonify({'answer': answer})


@app.route('/api/history/clear', methods=['POST'])
def clear_history():
    """현재 로그인한 사용자의 대화 기록을 초기화한다."""
    if 'username' not in session:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    username = session['username']
    if username in user_histories:
        user_histories[username].clear()

    return jsonify({'message': '대화 기록이 초기화되었습니다.'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
