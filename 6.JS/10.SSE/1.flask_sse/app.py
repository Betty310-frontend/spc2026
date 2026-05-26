# 별도의 라이브러리 없이 Flask에 있는 Response를 통해 stream 형식으로 데이터를 반환할 수 있다.

from flask import Flask, Response, send_from_directory, request
from queue import Queue

app = Flask(__name__)

# 연결된 사용자들 관리를 위한 큐
clients = []

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# 클라이언트에게 응답을 보낼 API - SSE 방식으로 보낼 API, 상대방이 여기를 바라보고 있으면, 내가 여기를 통해서 메시지를 보낼 때마다 클라이언트에게 전달 됌. -> Event Streaming 방식
@app.route('/stream')
def stream():
    print('클라이언트 연결됨 - 누가 이 API를 듣고 있음')

    def event_stream():
        q = Queue()
        clients.append(q) # 응답을 보낼 사용자 목록에 이 새로운 사용자를 추가
        try:
            yield f"data: 서버에 연결되었습니다.\n\n" # 메시지가 오면 클라이언트로 보냄

            while True:
                message = q.get()
                if message is None: # None이 오면 연결 종료 신호로 간주
                    break
                yield f"data: {message}\n\n" # 메시지가 오면 클라이언트로 보냄, 웹표준 event-stream 으로 보낼 때 data: <메시지>\n\n

        except GeneratorExit: # 클라이언트가 연결을 끊으면 GeneratorExit 예외가 발생
            print('클라이언트 연결 끊김')
        finally:
            clients.remove(q) # 사용자 목록에서 이 사용자를 제거

    return Response(event_stream(), mimetype='text/event-stream')

# 클라이언트가 나에게 보내는 API
@app.route('/send', methods=['POST'])
def send():
    message = request.form.get('message' ,'')
    print('클라이언트로부터 받은 메시지: ', message)
    for q in clients:
        q.put(f"서버가 받은 메시지: {message}")
    return ("", 204)

if __name__ == '__main__':
    app.run(debug=True)