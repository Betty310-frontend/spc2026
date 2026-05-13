# -*- coding: utf-8 -*-
from flask import Flask, render_template

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# set UTF-8 in response headers
@app.after_request
def set_utf8_header(response):
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)