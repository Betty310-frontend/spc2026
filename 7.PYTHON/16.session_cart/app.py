"""
세션 안에 여러 개의 정보를 담아 처리
상품 페이지, 장바구니 (이동 시에도 유지 필요)

필요 페이지
- 상품 리스트 (홈)
- 상품 상세
- 장바구니
  - 각각 제품 제거
  - 전체 제거
"""

# -*- coding: utf-8 -*-
from flask import Flask, render_template, redirect, request, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'hello1234'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

items = [
    {'id': 'item1', 'name': '햄버거', 'price': 3000, 'image': 'img/burger.webp', 'description': '맛있는 햄버거입니다.'},
    {'id': 'item2', 'name': '핫도그', 'price': 2000, 'image': 'img/hotdog.jpg', 'description': '맛있는 핫도그입니다.'},
    {'id': 'item3', 'name': '감자튀김', 'price': 1200, 'image': 'img/fries.jpg', 'description': '바삭한 감자튀김입니다.'},
    {'id': 'item4', 'name': '콜라', 'price': 1500, 'image': 'img/cola.jpg', 'description': '시원한 콜라입니다.'},
]

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/')
def product_list():
    return render_template('product-list.html', items=items)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', {})
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add_to_cart/<item_id>')
def add_to_cart(item_id):
    item = next((item for item in items if item['id'] == item_id), None)
    if item is None:
        return redirect(url_for('product_list'))
    
    if 'cart' not in session:
        session['cart'] = {}

    if item_id in session['cart']:
        session['cart'][item_id]['quantity'] += 1
    else:
        session['cart'][item_id] = {'quantity': 1, 'item': item}

    # session.modified = True  # 세션이 변경되었음을 명시적으로 표시 (필요한 경우)
    cart = session.get('cart', {})
    cart[item_id] = session['cart'][item_id]
    session['cart'] = cart

    return redirect(url_for('product_list'))

@app.route('/remove_from_cart/<item_id>')
def remove_from_cart(item_id):
    cart = session.get('cart', {})
    if item_id in cart:
        del cart[item_id]
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('cart'))

@app.route('/update_cart/<item_id>', methods=['POST'])
def update_cart(item_id):
    data = request.get_json()  # JSON 데이터 읽기
    new_quantity = data.get('quantity')  # JSON에서 수량 가져오기

    if new_quantity and isinstance(new_quantity, int):  # 수량이 정수인지 확인
        cart = session.get('cart', {})
        if item_id in cart:
            cart[item_id]['quantity'] = new_quantity
            session['cart'] = cart
            session.modified = True  # Session 변경 사항 반영
            return {"success": True, "message": "Cart updated successfully"}, 200

    return {"success": False, "message": "Invalid item or quantity"}, 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)