import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE_FILE = 'music_app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    print("데이터베이스 초기화 중...")
    
    # 만약 기존 db가 있다면 삭제하지 않고 그대로 진행하거나 테이블 생성
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. users 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 2. songs 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS songs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist TEXT NOT NULL,
        hashtags TEXT NOT NULL,
        album_image TEXT NOT NULL, -- CSS 그라데이션 클래스명 (예: grad-1, grad-2 등)
        likes_count INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 3. likes 테이블 (곡 좋아요)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        song_id INTEGER NOT NULL REFERENCES songs(id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, song_id)
    )
    ''')
    
    # 4. comments 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        song_id INTEGER NOT NULL REFERENCES songs(id) ON DELETE CASCADE,
        content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # 5. comment_likes 테이블 (댓글 좋아요)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comment_likes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        comment_id INTEGER NOT NULL REFERENCES comments(id) ON DELETE CASCADE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(user_id, comment_id)
    )
    ''')
    
    # 6. notifications 테이블
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        actor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
        type TEXT NOT NULL, -- 'song_like', 'song_comment', 'comment_like'
        song_id INTEGER REFERENCES songs(id) ON DELETE CASCADE,
        comment_id INTEGER REFERENCES comments(id) ON DELETE CASCADE,
        is_read INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    print("테이블 생성 완료.")
    
    # 테스트 계정 시딩
    print("기본 계정 시딩 중...")
    users_data = [
        ('admin', 'admin@music.com', generate_password_hash('admin123'), 'admin'),
        ('user', 'user@music.com', generate_password_hash('user123'), 'user'),
        ('user2', 'user2@music.com', generate_password_hash('user123'), 'user')
    ]
    
    for username, email, pw_hash, role in users_data:
        try:
            cursor.execute('''
            INSERT INTO users (username, email, password_hash, role)
            VALUES (?, ?, ?, ?)
            ''', (username, email, pw_hash, role))
        except sqlite3.IntegrityError:
            # 이미 있으면 무시
            pass
            
    conn.commit()
    
    # 실제 명곡 데이터 시딩
    print("실제 인기 명곡 데이터 시딩 중...")
    songs_data = [
        ("Dynamite", "BTS", "#kpop #pop #disco", "grad-1"),
        ("Blinding Lights", "The Weeknd", "#pop #synthwave #retro", "grad-2"),
        ("Hype Boy", "NewJeans", "#kpop #dance #hypeboy", "grad-3"),
        ("Shape of You", "Ed Sheeran", "#pop #acoustic #british", "grad-4"),
        ("Seven", "Jungkook", "#kpop #pop #summer", "grad-5"),
        ("Ditto", "NewJeans", "#kpop #chill #winter", "grad-6"),
        ("Love Dive", "IVE", "#kpop #pop #lovedive", "grad-7"),
        ("Perfect", "Ed Sheeran", "#ballad #pop #romantic", "grad-1"),
        ("Stay", "The Kid LAROI & Justin Bieber", "#pop #upbeat #stay", "grad-2")
    ]
    
    for title, artist, hashtags, album_image in songs_data:
        # 이미 있는 노래인지 중복 확인
        cursor.execute("SELECT id FROM songs WHERE title = ? AND artist = ?", (title, artist))
        exists = cursor.fetchone()
        if not exists:
            cursor.execute('''
            INSERT INTO songs (title, artist, hashtags, album_image, likes_count)
            VALUES (?, ?, ?, ?, 0)
            ''', (title, artist, hashtags, album_image))
            
    conn.commit()
    print("음악 데이터 시딩 완료.")
    
    # 초기 좋아요 및 댓글 샘플 입력 (알림 기능 데모용)
    cursor.execute("SELECT id FROM users WHERE username = 'user'")
    user_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM users WHERE username = 'user2'")
    user2_id = cursor.fetchone()[0]
    
    cursor.execute("SELECT id FROM songs WHERE title = 'Dynamite'")
    dynamite_id = cursor.fetchone()[0]
    cursor.execute("SELECT id FROM songs WHERE title = 'Hype Boy'")
    hypeboy_id = cursor.fetchone()[0]
    
    # user가 Dynamite를 좋아요함
    try:
        cursor.execute("INSERT INTO likes (user_id, song_id) VALUES (?, ?)", (user_id, dynamite_id))
        cursor.execute("UPDATE songs SET likes_count = likes_count + 1 WHERE id = ?", (dynamite_id,))
    except sqlite3.IntegrityError:
        pass
        
    # user2가 Hype Boy를 좋아요함
    try:
        cursor.execute("INSERT INTO likes (user_id, song_id) VALUES (?, ?)", (user2_id, hypeboy_id))
        cursor.execute("UPDATE songs SET likes_count = likes_count + 1 WHERE id = ?", (hypeboy_id,))
    except sqlite3.IntegrityError:
        pass

    # user가 Hype Boy에 댓글을 담 (user2가 Hype Boy를 좋아요했으므로 user2에게 알림이 가도록 설정할 수 있음)
    cursor.execute("SELECT COUNT(*) FROM comments")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO comments (user_id, song_id, content) VALUES (?, ?, ?)", 
                       (user_id, hypeboy_id, "NewJeans 노래 정말 너무 상큼하고 좋네요! 😊"))
        comment_id = cursor.lastrowid
        
        # user2가 좋아한 곡에 user가 댓글을 달았으므로 알림 생성
        cursor.execute('''
        INSERT INTO notifications (user_id, actor_id, type, song_id, comment_id, is_read)
        VALUES (?, ?, 'song_comment', ?, ?, 0)
        ''', (user2_id, user_id, hypeboy_id, comment_id))
        
    conn.commit()
    print("샘플 데이터 및 알림 데이터 생성 완료.")
    
    conn.close()
    print("데이터베이스 초기화 작업이 성공적으로 완료되었습니다!")

if __name__ == '__main__':
    init_db()
