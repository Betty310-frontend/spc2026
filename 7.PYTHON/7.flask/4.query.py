# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, render_template, make_response

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/search')
def search():
    query = request.args.get('q', '')
    page = request.args.get('page', default=1, type=int)
    user_input = f"Your query is {query}, page {page}"

    return {'message': user_input}, 200

@app.route('/user/<username>/post', methods=['GET'])
def user_post(username):
    page = request.args.get('page', default=1, type=int)
    data = {'username': username, 'posts': []} 
    return jsonify({'status': 'success', 'data': data, 'page': page}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)