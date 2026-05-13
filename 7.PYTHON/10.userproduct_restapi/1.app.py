# -*- coding: utf-8 -*-
from flask import Flask, send_from_directory, request, jsonify

"""
1. /user 라는 경로를 만들고 url 파라미터를 기반으로 사용자를 조회할 수 있다.
    1-1. /user는 모든 사용자 조회, /user/<id>는 특정 사용자 조회
2. /product 라는 경로를 만들고 url 쿼리를 기반으로 상품을 조회할 수 있다.
    2-1. /product는 모든 상품 조회, /product?id=<id>는 특정 상품 조회, /product?name=<name>은 이름으로 시작하는 상품 조회   
"""

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

"""
dict 인덱스를 통한 빠른 조회 가능 (굳이 for u in users 같은 반복문 필요 없음)
"""
users = {
    1: {'id': 1, 'name': '홍길동', 'email': 'hong@example.com'},
    2: {'id': 2, 'name': '김철수', 'email': 'kim@example.com'},
    3: {'id': 3, 'name': '이영희', 'email': 'lee@example.com'},
    4: {'id': 4, 'name': '박민수', 'email': 'park@example.com'},
    5: {'id': 5, 'name': '최지은', 'email': 'choi@example.com'}
}

products = {
    101: {'id': 101, 'name': '노트북', 'price': 1200000},
    102: {'id': 102, 'name': '스마트폰', 'price': 800000},
    103: {'id': 103, 'name': '태블릿', 'price': 600000},
    104: {'id': 104, 'name': '무선이어폰', 'price': 150000},
    105: {'id': 105, 'name': '스마트워치', 'price': 300000}
}

# set UTF-8 in response headers
# @app.after_request
# def set_utf8_header(response):
#     response.headers['Content-Type'] = 'text/html; charset=utf-8'
#     return response

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/users')
def users_page():
    return send_from_directory('static', 'user.html')

@app.route('/products')
def products_page():
    return send_from_directory('static', 'product.html')

####################
# API용 라우팅
####################
@app.route('/api/users', methods=['GET'])
@app.route('/api/users/<int:user_id>', methods=['GET'])
def api_get_user(user_id=None):
    if user_id is None:
        return jsonify({"result": list(users.values())})
    
    user = users.get(user_id)
    if user:
        return jsonify({"result": user})
    else:
        return jsonify({"error": "Not found"}), 404

@app.route('/api/products', methods=['GET'])
def api_get_products():
    product_id = request.args.get('id', type=int)
    product_name = request.args.get('name', type=str)

    if product_id:
        product = products.get(product_id)
        if product:
            return jsonify({"result": product})
        else:
            return jsonify({"error": "Not found"}), 404

    if product_name:
        filtered_products = [p for p in products.values() if p['name'].startswith(product_name)]
        if filtered_products:
            return jsonify({"result": filtered_products})
        else:
            return jsonify({"error": "Not found"}), 404

    return jsonify({"result": list(products.values())})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)