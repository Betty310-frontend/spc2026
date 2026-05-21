from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import sqlite3
import os
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super_secret_music_key_12345'
DATABASE_FILE = 'music_app.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# 로그인 필수 데코레이터
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('이 기능을 사용하려면 로그인이 필요합니다.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 어드민 필수 데코레이터
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('관리자 권한이 필요합니다.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# 모든 템플릿에 알림 개수 바인딩
@app.context_processor
def inject_notifications_count():
    if 'user_id' in session:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM notifications WHERE user_id = ? AND is_read = 0", (session['user_id'],))
        count = cursor.fetchone()[0]
        conn.close()
        return dict(unread_notifications_count=count)
    return dict(unread_notifications_count=0)


# ==========================================
# 1. 회원가입, 로그인, 로그아웃 라우트
# ==========================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        
        if not username or not email or not password:
            flash('모든 필드를 입력해 주세요.', 'warning')
            return render_template('register.html')
            
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 중복 체크
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (username, email))
        if cursor.fetchone():
            flash('이미 존재하는 사용자 이름 또는 이메일입니다.', 'warning')
            conn.close()
            return render_template('register.html')
            
        # 유저 추가
        password_hash = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, email, password_hash, role) VALUES (?, ?, ?, 'user')",
                       (username, email, password_hash))
        conn.commit()
        conn.close()
        
        flash('회원가입이 완료되었습니다! 로그인해 주세요.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_or_email = request.form['username_or_email'].strip()
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username_or_email, username_or_email))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['email'] = user['email']
            flash(f'{user["username"]}님, 환영합니다!', 'success')
            return redirect(url_for('index'))
        else:
            flash('사용자 이름, 이메일 또는 비밀번호가 올바르지 않습니다.', 'danger')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('로그아웃 되었습니다.', 'success')
    return redirect(url_for('index'))


# ==========================================
# 2. 홈 화면 및 음악 조회 관련
# ==========================================

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 음악 목록 조회
    cursor.execute("SELECT * FROM songs ORDER BY id DESC")
    songs = [dict(row) for row in cursor.fetchall()]
    
    # 로그인 사용자의 좋아요 목록 매핑
    user_likes = []
    if 'user_id' in session:
        cursor.execute("SELECT song_id FROM likes WHERE user_id = ?", (session['user_id'],))
        user_likes = [row['song_id'] for row in cursor.fetchall()]
        
    conn.close()
    
    # 각 음악 카드에 좋아요 활성화 여부 주입
    for song in songs:
        song['user_liked'] = song['id'] in user_likes
        
    return render_template('index.html', songs=songs)

@app.route('/song/<int:song_id>')
def song_detail(song_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 곡 조회
    cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
    song = cursor.fetchone()
    if not song:
        flash('존재하지 않는 곡입니다.', 'danger')
        conn.close()
        return redirect(url_for('index'))
        
    song = dict(song)
    
    # 사용자가 곡에 좋아요를 눌렀는지 확인
    user_liked = False
    if 'user_id' in session:
        cursor.execute("SELECT id FROM likes WHERE user_id = ? AND song_id = ?", (session['user_id'], song_id))
        if cursor.fetchone():
            user_liked = True
            
    # 댓글 목록 조회 (유저 정보 조인)
    cursor.execute('''
    SELECT c.*, u.username, u.role
    FROM comments c
    JOIN users u ON c.user_id = u.id
    WHERE c.song_id = ?
    ORDER BY c.created_at DESC
    ''', (song_id,))
    comments = [dict(row) for row in cursor.fetchall()]
    
    # 댓글별 좋아요 개수 및 로그인 유저의 좋아요 상태 조회
    comment_likes_dict = {}
    user_liked_comments = []
    
    for c in comments:
        cursor.execute("SELECT COUNT(*) FROM comment_likes WHERE comment_id = ?", (c['id'],))
        c['likes_count'] = cursor.fetchone()[0]
        
        if 'user_id' in session:
            cursor.execute("SELECT id FROM comment_likes WHERE user_id = ? AND comment_id = ?", (session['user_id'], c['id']))
            c['user_liked'] = cursor.fetchone() is not None
        else:
            c['user_liked'] = False
            
    conn.close()
    return render_template('detail.html', song=song, user_liked=user_liked, comments=comments)


# ==========================================
# 3. 음악 및 댓글 좋아요 AJAX 라우트
# ==========================================

@app.route('/like/<int:song_id>', methods=['POST'])
@login_required
def toggle_song_like(song_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 곡 존재 체크
    cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
    song = cursor.fetchone()
    if not song:
        conn.close()
        return jsonify({'error': '곡이 존재하지 않습니다.'}), 404
        
    # 기존 좋아요 여부 확인
    cursor.execute("SELECT id FROM likes WHERE user_id = ? AND song_id = ?", (user_id, song_id))
    like_row = cursor.fetchone()
    
    liked = False
    if like_row:
        # 좋아요 취소
        cursor.execute("DELETE FROM likes WHERE id = ?", (like_row['id'],))
        cursor.execute("UPDATE songs SET likes_count = MAX(0, likes_count - 1) WHERE id = ?", (song_id,))
    else:
        # 좋아요 추가
        cursor.execute("INSERT INTO likes (user_id, song_id) VALUES (?, ?)", (user_id, song_id))
        cursor.execute("UPDATE songs SET likes_count = likes_count + 1 WHERE id = ?", (song_id,))
        liked = True
        
        # 알림 생성: 내가 좋아요 한 음악에 다른 사람이 좋아요 하면 알림
        # 즉, 이 곡을 좋아요 했던 다른 모든 유저들에게 알림을 발송 (좋아요 누른 본인 제외)
        cursor.execute("SELECT DISTINCT user_id FROM likes WHERE song_id = ? AND user_id != ?", (song_id, user_id))
        other_liked_users = [r['user_id'] for r in cursor.fetchall()]
        
        for o_user_id in other_liked_users:
            cursor.execute('''
            INSERT INTO notifications (user_id, actor_id, type, song_id, is_read)
            VALUES (?, ?, 'song_like', ?, 0)
            ''', (o_user_id, user_id, song_id))
            
    conn.commit()
    
    # 갱신된 좋아요 개수 가져오기
    cursor.execute("SELECT likes_count FROM songs WHERE id = ?", (song_id,))
    new_likes_count = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({
        'success': True,
        'liked': liked,
        'likes_count': new_likes_count
    })

@app.route('/comment/<int:comment_id>/like', methods=['POST'])
@login_required
def toggle_comment_like(comment_id):
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 댓글 존재 여부 및 작성자 조회
    cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
    comment = cursor.fetchone()
    if not comment:
        conn.close()
        return jsonify({'error': '댓글이 존재하지 않습니다.'}), 404
        
    comment_author_id = comment['user_id']
    song_id = comment['song_id']
    
    cursor.execute("SELECT id FROM comment_likes WHERE user_id = ? AND comment_id = ?", (user_id, comment_id))
    like_row = cursor.fetchone()
    
    liked = False
    if like_row:
        cursor.execute("DELETE FROM comment_likes WHERE id = ?", (like_row['id'],))
    else:
        cursor.execute("INSERT INTO comment_likes (user_id, comment_id) VALUES (?, ?)", (user_id, comment_id))
        liked = True
        
        # 알림 생성: 누군가 내 코멘트에 좋아요 하면 코멘트 원작자에게 알림
        if user_id != comment_author_id:
            cursor.execute('''
            INSERT INTO notifications (user_id, actor_id, type, song_id, comment_id, is_read)
            VALUES (?, ?, 'comment_like', ?, ?, 0)
            ''', (comment_author_id, user_id, song_id, comment_id))
            
    conn.commit()
    
    # 댓글 좋아요 개수 집계
    cursor.execute("SELECT COUNT(*) FROM comment_likes WHERE comment_id = ?", (comment_id,))
    new_likes_count = cursor.fetchone()[0]
    conn.close()
    
    return jsonify({
        'success': True,
        'liked': liked,
        'likes_count': new_likes_count
    })


# ==========================================
# 4. 해시태그 추가 / 삭제 AJAX 라우트
# ==========================================

@app.route('/song/<int:song_id>/tag/add', methods=['POST'])
@login_required
def add_hashtag(song_id):
    tag = request.form.get('tag', '').strip()
    if not tag:
        return jsonify({'error': '태그 내용을 입력해주세요.'}), 400
        
    # '#' 기호 보장
    if not tag.startswith('#'):
        tag = '#' + tag
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT hashtags FROM songs WHERE id = ?", (song_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return jsonify({'error': '곡이 존재하지 않습니다.'}), 404
        
    current_tags = row['hashtags'].split()
    
    if tag in current_tags:
        conn.close()
        return jsonify({'error': '이미 등록된 해시태그입니다.'}), 400
        
    current_tags.append(tag)
    new_tags_str = ' '.join(current_tags)
    
    cursor.execute("UPDATE songs SET hashtags = ? WHERE id = ?", (new_tags_str, song_id))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'tag': tag,
        'all_tags': current_tags
    })

@app.route('/song/<int:song_id>/tag/delete', methods=['POST'])
@login_required
def delete_hashtag(song_id):
    tag = request.form.get('tag', '').strip()
    if not tag:
        return jsonify({'error': '삭제할 태그가 지정되지 않았습니다.'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT hashtags FROM songs WHERE id = ?", (song_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return jsonify({'error': '곡이 존재하지 않습니다.'}), 404
        
    current_tags = row['hashtags'].split()
    
    if tag not in current_tags:
        conn.close()
        return jsonify({'error': '존재하지 않는 해시태그입니다.'}), 400
        
    current_tags.remove(tag)
    new_tags_str = ' '.join(current_tags)
    
    cursor.execute("UPDATE songs SET hashtags = ? WHERE id = ?", (new_tags_str, song_id))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'deleted_tag': tag,
        'all_tags': current_tags
    })


# ==========================================
# 5. 코멘트 CUD 라우트 (비로그인 로그인 유도 포함)
# ==========================================

@app.route('/song/<int:song_id>/comment/add', methods=['POST'])
def add_comment(song_id):
    if 'user_id' not in session:
        # 로그인하지 않은 유저가 접근할 시 AJAX 또는 json 응답
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({'error': 'login_required', 'message': '댓글 작성을 위해 로그인이 필요합니다.'}), 401
        flash('댓글 작성을 위해 로그인이 필요합니다.', 'danger')
        return redirect(url_for('login'))
        
    user_id = session['user_id']
    content = request.form.get('content', '').strip()
    
    if not content:
        flash('댓글 내용을 입력해주세요.', 'warning')
        return redirect(url_for('song_detail', song_id=song_id))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 댓글 입력
    cursor.execute("INSERT INTO comments (user_id, song_id, content) VALUES (?, ?, ?)", (user_id, song_id, content))
    comment_id = cursor.lastrowid
    
    # 내가 좋아요 한 음악에 다른 사람이 댓글을 달면 알림 생성
    # 즉, 이 노래를 좋아요 한 다른 모든 사용자들에게 알림을 발송 (댓글 단 본인 제외)
    cursor.execute("SELECT DISTINCT user_id FROM likes WHERE song_id = ? AND user_id != ?", (song_id, user_id))
    other_liked_users = [r['user_id'] for r in cursor.fetchall()]
    
    for o_user_id in other_liked_users:
        cursor.execute('''
        INSERT INTO notifications (user_id, actor_id, type, song_id, comment_id, is_read)
        VALUES (?, ?, 'song_comment', ?, ?, 0)
        ''', (o_user_id, user_id, song_id, comment_id))
        
    conn.commit()
    conn.close()
    
    flash('댓글이 성공적으로 등록되었습니다!', 'success')
    return redirect(url_for('song_detail', song_id=song_id))

@app.route('/comment/<int:comment_id>/edit', methods=['POST'])
@login_required
def edit_comment(comment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
    comment = cursor.fetchone()
    if not comment:
        conn.close()
        return jsonify({'error': '댓글이 존재하지 않습니다.'}), 404
        
    # 작성자 본인 확인
    if comment['user_id'] != session['user_id']:
        conn.close()
        return jsonify({'error': '수정 권한이 없습니다.'}), 403
        
    new_content = request.form.get('content', '').strip()
    if not new_content:
        conn.close()
        return jsonify({'error': '댓글 내용을 입력해주세요.'}), 400
        
    cursor.execute("UPDATE comments SET content = ? WHERE id = ?", (new_content, comment_id))
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': '댓글이 성공적으로 수정되었습니다.',
        'content': new_content
    })

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM comments WHERE id = ?", (comment_id,))
    comment = cursor.fetchone()
    if not comment:
        conn.close()
        return jsonify({'error': '댓글이 존재하지 않습니다.'}), 404
        
    # 작성자 본인 또는 어드민인지 확인
    if comment['user_id'] != session['user_id'] and session.get('role') != 'admin':
        conn.close()
        return jsonify({'error': '삭제 권한이 없습니다.'}), 403
        
    cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    # 연관된 대댓글 좋아요 및 알림은 외래키 제약조건(ON DELETE CASCADE)으로 자동 삭제됨
    conn.commit()
    conn.close()
    
    return jsonify({
        'success': True,
        'message': '댓글이 성공적으로 삭제되었습니다.'
    })


# ==========================================
# 6. TopLikes 및 Hashtags 라우트
# ==========================================

@app.route('/top-likes')
def top_likes():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 좋아요 수 기준으로 정렬하여 음악들 조회
    cursor.execute("SELECT * FROM songs ORDER BY likes_count DESC, title ASC")
    songs = [dict(row) for row in cursor.fetchall()]
    
    # 각 음악마다 좋아요를 누른 유저 목록 수집
    for song in songs:
        cursor.execute('''
        SELECT u.username
        FROM likes l
        JOIN users u ON l.user_id = u.id
        WHERE l.song_id = ?
        ORDER BY l.created_at ASC
        ''', (song['id'],))
        song['liked_users'] = [r['username'] for r in cursor.fetchall()]
        
    conn.close()
    return render_template('top_likes.html', songs=songs)

@app.route('/hashtags')
def hashtags():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 전체 곡의 해시태그 집계
    cursor.execute("SELECT hashtags FROM songs")
    rows = cursor.fetchall()
    
    tag_counts = {}
    for row in rows:
        tags = row['hashtags'].split()
        for t in tags:
            if t.startswith('#'):
                tag_counts[t] = tag_counts.get(t, 0) + 1
                
    # 빈도수가 높은 순으로 정렬
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    
    # 시각화 막대 그래프용 비율 계산 (가장 많은 태그 개수를 100% 기준으로 비율 설정)
    max_count = sorted_tags[0][1] if sorted_tags else 1
    visual_tags = []
    for tag, count in sorted_tags:
        percentage = int((count / max_count) * 100)
        visual_tags.append({
            'name': tag,
            'count': count,
            'percentage': percentage
        })
        
    conn.close()
    return render_template('hashtags.html', tags=visual_tags)


# ==========================================
# 7. 알림(Notifications) 라우트
# ==========================================

@app.route('/notifications')
@login_required
def notifications_view():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 알림 내역 전체 조회 (알림 유발자 username과 해당 곡 타이틀 조인)
    cursor.execute('''
    SELECT n.*, u.username as actor_name, s.title as song_title, c.content as comment_snippet
    FROM notifications n
    JOIN users u ON n.actor_id = u.id
    LEFT JOIN songs s ON n.song_id = s.id
    LEFT JOIN comments c ON n.comment_id = c.id
    WHERE n.user_id = ?
    ORDER BY n.created_at DESC
    ''', (user_id,))
    notifications = [dict(row) for row in cursor.fetchall()]
    
    # 읽음 처리 수행
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    return render_template('notifications.html', notifications=notifications)


# ==========================================
# 8. 프로필(Profile) 라우트
# ==========================================

@app.route('/profile')
@login_required
def profile_view():
    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 내가 작성한 댓글 목록 조회
    cursor.execute('''
    SELECT c.*, s.title as song_title
    FROM comments c
    JOIN songs s ON c.song_id = s.id
    WHERE c.user_id = ?
    ORDER BY c.created_at DESC
    ''', (user_id,))
    comments = [dict(row) for row in cursor.fetchall()]
    
    # 내가 좋아요 한 곡 리스트 조회
    cursor.execute('''
    SELECT s.*
    FROM likes l
    JOIN songs s ON l.song_id = s.id
    WHERE l.user_id = ?
    ORDER BY l.created_at DESC
    ''', (user_id,))
    liked_songs = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return render_template('profile.html', comments=comments, liked_songs=liked_songs)


# ==========================================
# 9. 어드민 관리 기능 (회원 관리, 댓글 관리)
# ==========================================

@app.route('/admin/users')
@admin_required
def manage_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, role, created_at FROM users ORDER BY role ASC, id ASC")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('manage_users.html', users=users)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    if user_id == session['user_id']:
        flash('본인 계정은 삭제할 수 없습니다.', 'danger')
        return redirect(url_for('manage_users'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    
    flash('성공적으로 유저가 강제 탈퇴 처리되었습니다.', 'success')
    return redirect(url_for('manage_users'))

@app.route('/admin/comments')
@admin_required
def manage_comments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT c.*, u.username, s.title as song_title
    FROM comments c
    JOIN users u ON c.user_id = u.id
    JOIN songs s ON c.song_id = s.id
    ORDER BY c.created_at DESC
    ''')
    comments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return render_template('manage_comments.html', comments=comments)

@app.route('/admin/comments/<int:comment_id>/delete', methods=['POST'])
@admin_required
def delete_comment_admin(comment_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
    conn.commit()
    conn.close()
    
    flash('댓글이 강제 삭제되었습니다.', 'success')
    return redirect(url_for('manage_comments'))


# ==========================================
# 메인 서버 구동
# ==========================================

if __name__ == '__main__':
    # 디버그 모드로 구동
    app.run(host='0.0.0.0', port=5000, debug=True)
