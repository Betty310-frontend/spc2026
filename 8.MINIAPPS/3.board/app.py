# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, send_from_directory

from database import MyDatabase

db = MyDatabase()

app = Flask(__name__, static_folder='static')
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

@app.route('/')
def index():
    return send_from_directory('static', 'index.html', mimetype='text/html')

@app.route('/api/board', methods=['GET'])
def get_board():
    rows = db.execute_fetch("SELECT id, title, message FROM board")
    result = [
        {'id': row[0], 'title': row[1], 'message': row[2]}
        for row in rows
    ]
    return jsonify(result)

@app.route('/api/board', methods=['POST'])
def create_board():
    data = request.get_json()
    title = data.get('title').strip()
    message = data.get('message').strip()
    db.execute("INSERT INTO board (title, message) VALUES (?, ?)", (title, message))
    db.commit()
    return jsonify({'message': '게시글이 성공적으로 생성되었습니다.'}), 201

@app.route('/api/board/<int:board_id>', methods=['PUT'])
def update_board(board_id):
    data = request.get_json()
    title = data.get('title').strip()
    message = data.get('message').strip()
    db.execute("UPDATE board SET title=?, message=? WHERE id=?", (title, message, board_id))
    db.commit()
    return jsonify({'message': '게시글이 성공적으로 수정되었습니다.'}), 200

@app.route('/api/board/<int:board_id>', methods=['DELETE'])
def delete_board(board_id):
    db.execute("DELETE FROM board WHERE id=?", (board_id,))
    db.commit()
    return jsonify({'message': '게시글이 성공적으로 삭제되었습니다.'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)