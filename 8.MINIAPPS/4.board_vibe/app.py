import os
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                vibe_cool INTEGER DEFAULT 0,
                vibe_fire INTEGER DEFAULT 0,
                vibe_chill INTEGER DEFAULT 0
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/posts', methods=['GET'])
def get_posts():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM posts ORDER BY id DESC')
            posts = [dict(row) for row in cursor.fetchall()]
        return jsonify(posts)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    title = data.get('title', '').strip()
    message = data.get('message', '').strip()
    
    if not title or not message:
        return jsonify({"error": "Title and message are required"}), 400
    
    if len(title) > 100 or len(message) > 1000:
        return jsonify({"error": "Title or message too long"}), 400

    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO posts (title, message) VALUES (?, ?)',
                (title, message)
            )
            conn.commit()
            post_id = cursor.lastrowid
            
            # Fetch the newly created post
            cursor.execute('SELECT * FROM posts WHERE id = ?', (post_id,))
            new_post = dict(cursor.fetchone())
            
        return jsonify(new_post), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts/<int:post_id>/react', methods=['POST'])
def react_post(post_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    vibe_type = data.get('vibe_type')
    if vibe_type not in ['cool', 'fire', 'chill']:
        return jsonify({"error": "Invalid vibe type"}), 400
    
    column = f"vibe_{vibe_type}"
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            # Check if post exists
            cursor.execute('SELECT id FROM posts WHERE id = ?', (post_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Post not found"}), 404
            
            # Increment the reaction
            cursor.execute(f'UPDATE posts SET {column} = {column} + 1 WHERE id = ?', (post_id,))
            conn.commit()
            
            # Get updated counts
            cursor.execute(f'SELECT vibe_cool, vibe_fire, vibe_chill FROM posts WHERE id = ?', (post_id,))
            updated_vibes = dict(cursor.fetchone())
            
        return jsonify(updated_vibes)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM posts WHERE id = ?', (post_id,))
            if not cursor.fetchone():
                return jsonify({"error": "Post not found"}), 404
            
            cursor.execute('DELETE FROM posts WHERE id = ?', (post_id,))
            conn.commit()
        return jsonify({"success": True, "message": "Post deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
