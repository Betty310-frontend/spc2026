from flask import Flask, make_response, request

app = Flask(__name__)

COOKIE_NAME = "my-data"

@app.route("/")
def main():
    cookie = request.cookies.get(COOKIE_NAME)

    if cookie:
        return f"안녕, {cookie} 야"
    else:
        resp = make_response("안녕하세요, 첫 방문이시군요!!")
        resp.set_cookie(COOKIE_NAME, "spc2026")
        return resp

if __name__ == "__main__":
    app.run(debug=True)