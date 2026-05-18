# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from dotenv import load_dotenv
import sqlite3, hashlib, jwt, datetime, os

load_dotenv()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
SECRET_KEY = os.getenv("SECRET_KEY")
DB_NAME = os.getenv("DB_NAME")
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

# ──────────────────────────────────────────
# CORS
# ──────────────────────────────────────────
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ──────────────────────────────────────────
# Swagger 설정
# ──────────────────────────────────────────
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs",
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "🛍️ Shop REST API",
        "description": "Flask + SQLite 기반 쇼핑몰 REST API\n\n"
                       "## 인증 방법\n"
                       "로그인 후 발급된 JWT 토큰을 `Authorization` 헤더에 `Bearer <token>` 형식으로 전달하세요.",
        "version": "1.0.0",
        "contact": {"email": "admin@testshop.com"},
    },
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT 토큰을 입력하세요. 예: `Bearer eyJhbGci...`",
        }
    },
    "tags": [
        {"name": "Auth",     "description": "회원가입 / 로그인 / 내 정보"},
        {"name": "Products", "description": "상품 목록 / 상세 / 카테고리"},
        {"name": "Cart",     "description": "장바구니 전체 비우기 / 개별 삭제 / 조회 / 추가 / 수량 수정 (로그인 필요)"},
    ],
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

@app.after_request
def set_utf8_header(response):
    if response.content_type.startswith('application/json'):
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# ──────────────────────────────────────────
# DB 초기화
# ──────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    # 회원 테이블
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            username   TEXT    UNIQUE NOT NULL,
            password   TEXT    NOT NULL,
            email      TEXT    NOT NULL,
            created_at TEXT    DEFAULT (datetime('now','localtime'))
        )
    ''')

    # 상품 테이블
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            price       INTEGER NOT NULL,
            description TEXT,
            image_url   TEXT,
            category    TEXT,
            stock       INTEGER DEFAULT 100
        )
    ''')

    # 장바구니 테이블
    cur.execute('''
        CREATE TABLE IF NOT EXISTS cart (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity   INTEGER NOT NULL DEFAULT 1,
            FOREIGN KEY (user_id)    REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id),
            UNIQUE (user_id, product_id)
        )
    ''')

    # 샘플 상품 추가 (최초 1회)
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        sample_products = [
            ('맥북 프로 M4', 3490000, '애플 실리콘 M4 탑재 최신 맥북 프로',
             'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop', '전자기기', 50),
            ('아이폰 16 Pro', 1550000, '티타늄 디자인, A18 Pro 칩, 48MP 카메라',
             'https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=400&h=300&fit=crop', '전자기기', 80),
            ('에어팟 프로 2세대', 359000, '액티브 노이즈 캔슬링, H2 칩, MagSafe 충전',
             'https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?w=400&h=300&fit=crop', '전자기기', 120),
            ('나이키 에어맥스 270', 149000, '경량 에어쿠션 탑재, 데일리 스니커즈',
             'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop', '신발', 60),
            ('아디다스 울트라부스트 22', 179000, '부스트 쿠션 기술, 러닝 퍼포먼스 극대화',
             'https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&h=300&fit=crop', '신발', 45),
            ('무인양품 캔버스 토트백', 39900, '심플한 디자인의 캔버스 소재 토트백',
             'https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=300&fit=crop', '가방', 200),
            ('다이슨 V15 청소기', 989000, '레이저 먼지 감지, 강력한 흡입력',
             'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop', '가전', 30),
            ('레고 테크닉 42196', 89000, '성인 레고 테크닉 시리즈, 고난이도 조립',
             'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop', '완구', 75),
            ('스타벅스 텀블러 500ml', 29500, '스테인리스 더블월 보온보냉 텀블러',
             'https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&h=300&fit=crop', '생활용품', 150),
            ('갤럭시 버즈 3 Pro', 279000, 'ANC 탑재, 삼성 생태계 연동 무선이어폰',
             'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=300&fit=crop', '전자기기', 90),
        ]
        cur.executemany(
            "INSERT INTO products (name, price, description, image_url, category, stock) VALUES (?,?,?,?,?,?)",
            sample_products
        )
    else:
        # 기존 데이터의 이미지 URL 업데이트
        image_updates = [
            ('https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400&h=300&fit=crop', '맥북 프로 M4'),
            ('https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=400&h=300&fit=crop', '아이폰 16 Pro'),
            ('https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?w=400&h=300&fit=crop', '에어팟 프로 2세대'),
            ('https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=300&fit=crop', '나이키 에어맥스 270'),
            ('https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400&h=300&fit=crop', '아디다스 울트라부스트 22'),
            ('https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=400&h=300&fit=crop', '무인양품 캔버스 토트백'),
            ('https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop', '다이슨 V15 청소기'),
            ('https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=300&fit=crop', '레고 테크닉 42196'),
            ('https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?w=400&h=300&fit=crop', '스타벅스 텀블러 500ml'),
            ('https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=300&fit=crop', '갤럭시 버즈 3 Pro'),
        ]
        for image_url, name in image_updates:
            cur.execute("UPDATE products SET image_url=? WHERE name=?", (image_url, name))

    conn.commit()
    conn.close()

# ──────────────────────────────────────────
# JWT 유틸
# ──────────────────────────────────────────
def create_token(user_id, username):
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth[7:]
    return verify_token(token)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

# ──────────────────────────────────────────
# 기본 라우트
# ──────────────────────────────────────────
@app.route('/')
def index():
    return jsonify({'message': '쇼핑몰 REST API 서버가 실행 중입니다.'}), 200

# ──────────────────────────────────────────
# [AUTH] 회원가입 / 로그인
# ──────────────────────────────────────────
@app.route('/api/auth/register', methods=['POST'])
def register():
    """
    회원가입
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [username, password, email]
          properties:
            username:
              type: string
              example: testuser
            password:
              type: string
              example: "1234"
            email:
              type: string
              example: test@test.com
    responses:
      201:
        description: 회원가입 성공
      400:
        description: 필수 항목 누락
      409:
        description: 중복 아이디
    """
    data     = request.get_json()
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()
    email    = (data.get('email') or '').strip()

    if not username or not password or not email:
        return jsonify({'error': '아이디, 비밀번호, 이메일은 필수 항목입니다.'}), 400

    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hash_password(password), email)
        )
        conn.commit()
        return jsonify({'message': '회원가입이 완료되었습니다.'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': '이미 사용 중인 아이디입니다.'}), 409
    finally:
        conn.close()

@app.route('/api/auth/login', methods=['POST'])
def login():
    """
    로그인
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [username, password]
          properties:
            username:
              type: string
              example: testuser
            password:
              type: string
              example: "1234"
    responses:
      200:
        description: 로그인 성공 (JWT 토큰 반환)
        schema:
          type: object
          properties:
            message:
              type: string
            token:
              type: string
            user:
              type: object
              properties:
                id:
                  type: integer
                username:
                  type: string
                email:
                  type: string
      400:
        description: 입력값 누락
      401:
        description: 인증 실패
    """
    data     = request.get_json()
    username = (data.get('username') or '').strip()
    password = (data.get('password') or '').strip()

    if not username or not password:
        return jsonify({'error': '아이디와 비밀번호를 입력해주세요.'}), 400

    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({'error': '아이디 또는 비밀번호가 올바르지 않습니다.'}), 401

    token = create_token(user['id'], user['username'])
    return jsonify({
        'message': '로그인 성공',
        'token': token,
        'user': {'id': user['id'], 'username': user['username'], 'email': user['email']}
    }), 200

@app.route('/api/auth/me', methods=['GET'])
def me():
    """
    내 정보 조회
    ---
    tags:
      - Auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: 회원 정보 반환
        schema:
          type: object
          properties:
            id:
              type: integer
            username:
              type: string
            email:
              type: string
            created_at:
              type: string
      401:
        description: 인증 필요
      404:
        description: 사용자 없음
    """
    user = get_current_user()
    if not user:
        return jsonify({'error': '인증이 필요합니다.'}), 401
    conn = get_db()
    row = conn.execute(
        "SELECT id, username, email, created_at FROM users WHERE id=?", (user['user_id'],)
    ).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': '사용자를 찾을 수 없습니다.'}), 404
    return jsonify(dict(row)), 200

# ──────────────────────────────────────────
# [PRODUCTS] 상품 목록 / 상세
# ──────────────────────────────────────────
@app.route('/api/products', methods=['GET'])
def get_products():
    """
    상품 목록 조회
    ---
    tags:
      - Products
    parameters:
      - in: query
        name: category
        type: string
        description: 카테고리 필터
        example: 전자기기
      - in: query
        name: keyword
        type: string
        description: 상품명/설명 검색어
        example: 맥북
      - in: query
        name: page
        type: integer
        default: 1
        description: 페이지 번호
      - in: query
        name: per_page
        type: integer
        default: 10
        description: 페이지당 상품 수
    responses:
      200:
        description: 상품 목록
        schema:
          type: object
          properties:
            products:
              type: array
              items:
                type: object
            total:
              type: integer
            page:
              type: integer
            per_page:
              type: integer
            total_pages:
              type: integer
    """
    category = request.args.get('category')
    keyword  = request.args.get('keyword')
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset   = (page - 1) * per_page

    conn   = get_db()
    query  = "SELECT * FROM products WHERE 1=1"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)
    if keyword:
        query += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f'%{keyword}%', f'%{keyword}%'])

    total    = conn.execute(f"SELECT COUNT(*) FROM ({query})", params).fetchone()[0]
    products = conn.execute(query + " LIMIT ? OFFSET ?", params + [per_page, offset]).fetchall()
    conn.close()

    return jsonify({
        'products': [dict(p) for p in products],
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    }), 200

@app.route('/api/products/categories', methods=['GET'])
def get_categories():
    """
    카테고리 목록 조회
    ---
    tags:
      - Products
    responses:
      200:
        description: 카테고리 목록
        schema:
          type: object
          properties:
            categories:
              type: array
              items:
                type: string
              example: ["가방", "가전", "신발", "완구", "전자기기", "생활용품"]
    """
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    conn.close()
    return jsonify({'categories': [r['category'] for r in rows]}), 200

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    상품 상세 조회
    ---
    tags:
      - Products
    parameters:
      - in: path
        name: product_id
        type: integer
        required: true
        description: 상품 ID
        example: 1
    responses:
      200:
        description: 상품 상세 정보
        schema:
          type: object
          properties:
            id:
              type: integer
            name:
              type: string
            price:
              type: integer
            description:
              type: string
            image_url:
              type: string
            category:
              type: string
            stock:
              type: integer
      404:
        description: 상품 없음
    """
    conn    = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    conn.close()
    if not product:
        return jsonify({'error': '상품을 찾을 수 없습니다.'}), 404
    return jsonify(dict(product)), 200

# ──────────────────────────────────────────
# [CART] 장바구니 CRUD (로그인 필요)
# ──────────────────────────────────────────
def require_auth():
    user = get_current_user()
    if not user:
        return None, (jsonify({'error': '로그인이 필요한 서비스입니다.', 'code': 'UNAUTHORIZED'}), 401)
    return user, None

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """
    장바구니 조회
    ---
    tags:
      - Cart
    security:
      - BearerAuth: []
    responses:
      200:
        description: 장바구니 항목 목록 및 합계 금액
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  product_id:
                    type: integer
                  name:
                    type: string
                  price:
                    type: integer
                  quantity:
                    type: integer
                  image_url:
                    type: string
                  category:
                    type: string
                  stock:
                    type: integer
            total_price:
              type: integer
            count:
              type: integer
      401:
        description: 로그인 필요
    """
    user, err = require_auth()
    if err: return err

    conn = get_db()
    rows = conn.execute('''
        SELECT c.id, c.quantity,
               p.id AS product_id, p.name, p.price, p.image_url, p.category, p.stock
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
        ORDER BY c.id DESC
    ''', (user['user_id'],)).fetchall()
    conn.close()

    items       = [dict(r) for r in rows]
    total_price = sum(item['price'] * item['quantity'] for item in items)
    return jsonify({'items': items, 'total_price': total_price, 'count': len(items)}), 200

@app.route('/api/cart', methods=['POST'])
def add_to_cart():
    """
    장바구니 상품 추가
    ---
    tags:
      - Cart
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [product_id]
          properties:
            product_id:
              type: integer
              example: 1
            quantity:
              type: integer
              default: 1
              example: 2
    responses:
      200:
        description: 추가 성공 (이미 있으면 수량 합산)
      400:
        description: 잘못된 입력값
      401:
        description: 로그인 필요
      404:
        description: 상품 없음
    """
    user, err  = require_auth()
    if err: return err

    data       = request.get_json()
    product_id = data.get('product_id')
    quantity   = int(data.get('quantity', 1))

    if not product_id or quantity < 1:
        return jsonify({'error': '상품 ID와 수량(1 이상)을 입력해주세요.'}), 400

    conn    = get_db()
    product = conn.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
    if not product:
        conn.close()
        return jsonify({'error': '존재하지 않는 상품입니다.'}), 404

    existing = conn.execute(
        "SELECT * FROM cart WHERE user_id=? AND product_id=?",
        (user['user_id'], product_id)
    ).fetchone()

    if existing:
        conn.execute(
            "UPDATE cart SET quantity = quantity + ? WHERE user_id=? AND product_id=?",
            (quantity, user['user_id'], product_id)
        )
        msg = '장바구니 수량이 업데이트되었습니다.'
    else:
        conn.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?,?,?)",
            (user['user_id'], product_id, quantity)
        )
        msg = '장바구니에 상품이 추가되었습니다.'

    conn.commit()
    conn.close()
    return jsonify({'message': msg}), 200

@app.route('/api/cart/<int:cart_id>', methods=['PUT'])
def update_cart_item(cart_id):
    """
    장바구니 수량 수정
    ---
    tags:
      - Cart
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: cart_id
        type: integer
        required: true
        description: 장바구니 항목 ID
        example: 1
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [quantity]
          properties:
            quantity:
              type: integer
              minimum: 1
              example: 3
    responses:
      200:
        description: 수량 수정 성공
      400:
        description: 잘못된 수량
      401:
        description: 로그인 필요
      404:
        description: 항목 없음
    """
    user, err = require_auth()
    if err: return err

    data     = request.get_json()
    quantity = int(data.get('quantity', 1))

    if quantity < 1:
        return jsonify({'error': '수량은 1 이상이어야 합니다.'}), 400

    conn = get_db()
    row  = conn.execute(
        "SELECT * FROM cart WHERE id=? AND user_id=?", (cart_id, user['user_id'])
    ).fetchone()

    if not row:
        conn.close()
        return jsonify({'error': '장바구니 항목을 찾을 수 없습니다.'}), 404

    conn.execute("UPDATE cart SET quantity=? WHERE id=?", (quantity, cart_id))
    conn.commit()
    conn.close()
    return jsonify({'message': '수량이 수정되었습니다.'}), 200

@app.route('/api/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart_item(cart_id):
    """
    장바구니 개별 상품 삭제
    ---
    tags:
      - Cart
    security:
      - BearerAuth: []
    parameters:
      - in: path
        name: cart_id
        type: integer
        required: true
        description: 장바구니 항목 ID
        example: 1
    responses:
      200:
        description: 삭제 성공
      401:
        description: 로그인 필요
      404:
        description: 항목 없음
    """
    user, err = require_auth()
    if err: return err

    conn = get_db()
    row  = conn.execute(
        "SELECT * FROM cart WHERE id=? AND user_id=?", (cart_id, user['user_id'])
    ).fetchone()

    if not row:
        conn.close()
        return jsonify({'error': '장바구니 항목을 찾을 수 없습니다.'}), 404

    conn.execute("DELETE FROM cart WHERE id=?", (cart_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': '상품이 장바구니에서 삭제되었습니다.'}), 200

@app.route('/api/cart', methods=['DELETE'])
def clear_cart():
    """
    장바구니 전체 비우기
    ---
    tags:
      - Cart
    security:
      - BearerAuth: []
    responses:
      200:
        description: 전체 삭제 성공
      401:
        description: 로그인 필요
    """
    user, err = require_auth()
    if err: return err

    conn = get_db()
    conn.execute("DELETE FROM cart WHERE user_id=?", (user['user_id'],))
    conn.commit()
    conn.close()
    return jsonify({'message': '장바구니를 비웠습니다.'}), 200

# ──────────────────────────────────────────
# 앱 시작
# ──────────────────────────────────────────
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)