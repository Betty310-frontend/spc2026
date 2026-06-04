import os
import json
import random
import time
import threading
from datetime import datetime
from collections import deque
from dotenv import load_dotenv

from flask import Flask, request, jsonify, send_from_directory, Response, stream_with_context

from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

app = Flask(__name__, static_folder='public', static_url_path='')
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# ──────────────────────────────────────────────
# 가상 시장 데이터 (인메모리 상태)
# ──────────────────────────────────────────────
TICKERS = {
    "AAPL":  {"name": "Apple",     "price": 189.0,  "prev": 189.0},
    "MSFT":  {"name": "Microsoft", "price": 420.0,  "prev": 420.0},
    "NVDA":  {"name": "NVIDIA",    "price": 875.0,  "prev": 875.0},
    "TSLA":  {"name": "Tesla",     "price": 178.0,  "prev": 178.0},
    "AMZN":  {"name": "Amazon",    "price": 185.0,  "prev": 185.0},
}
USD_KRW = {"rate": 1380.0, "prev": 1380.0}

# 포트폴리오
portfolio = {
    "krw":      5_000_000,   # 원화 잔고
    "usd":      200.0,       # 달러 잔고
    "stocks":   {},          # {"AAPL": 2, ...}
    "history":  [],          # 거래 로그
}

# 예약 목록
reservations = []
reservation_id_counter = [1]

# 승인 대기 큐 (HITL)
pending_approvals = []
approval_id_counter = [1]

# SSE 알림 버퍼
notifications = deque(maxlen=100)

# ──────────────────────────────────────────────
# 시세 시뮬레이션 (백그라운드 스레드)
# ──────────────────────────────────────────────
def simulate_market():
    while True:
        for sym, data in TICKERS.items():
            data["prev"] = data["price"]
            data["price"] = round(data["price"] * (1 + random.uniform(-0.003, 0.003)), 2)
        USD_KRW["prev"] = USD_KRW["rate"]
        USD_KRW["rate"] = round(USD_KRW["rate"] * (1 + random.uniform(-0.001, 0.001)), 2)
        _check_reservations()
        time.sleep(2)

def _check_reservations():
    triggered = []
    for rsv in reservations:
        if rsv["status"] != "active":
            continue
        if rsv["type"] == "buy":
            price = TICKERS.get(rsv["symbol"], {}).get("price")
            if price and price <= rsv["target_price"]:
                _request_approval(rsv, price)
                triggered.append(rsv["id"])
        elif rsv["type"] == "sell":
            price = TICKERS.get(rsv["symbol"], {}).get("price")
            if price and price >= rsv["target_price"]:
                _request_approval(rsv, price)
                triggered.append(rsv["id"])
        elif rsv["type"] == "exchange_krw_to_usd":
            if USD_KRW["rate"] <= rsv["target_rate"]:
                _request_approval(rsv, USD_KRW["rate"])
                triggered.append(rsv["id"])
    for rid in triggered:
        for rsv in reservations:
            if rsv["id"] == rid:
                rsv["status"] = "pending_approval"

def _request_approval(rsv, current_value):
    aid = approval_id_counter[0]
    approval_id_counter[0] += 1
    approval = {
        "id": aid,
        "reservation_id": rsv["id"],
        "rsv": rsv,
        "current_value": current_value,
        "status": "waiting",
        "created_at": datetime.now().strftime("%H:%M:%S"),
    }
    pending_approvals.append(approval)
    _add_log(f"⏳ 승인대기 | {rsv['label']} @ {current_value}")
    notifications.appendleft({
        "type": "approval",
        "message": f"승인 요청: {rsv['label']} @ {current_value}",
        "id": aid,
    })

def _execute_reservation(rsv):
    now = datetime.now().strftime("%H:%M:%S")
    if rsv["type"] == "buy":
        sym = rsv["symbol"]
        price = TICKERS[sym]["price"]
        qty = rsv["qty"]
        total_usd = price * qty
        # 달러 부족 시 원화 자동 환전
        if portfolio["usd"] < total_usd:
            shortage_usd = total_usd - portfolio["usd"]
            rate = USD_KRW["rate"]
            needed_krw = int(shortage_usd * rate * 1.01) + 1
            if portfolio["krw"] < needed_krw:
                _add_log(f"❌ 잔고 부족 | {sym} 매수 실패 (달러·원화 모두 부족)")
                return False
            usd_gained = round(needed_krw / rate, 2)
            portfolio["krw"] -= needed_krw
            portfolio["usd"] += usd_gained
            _add_log(f"🔄 자동환전 | ₩{needed_krw:,} → ${usd_gained:.2f} (환율 {rate:.2f})")
        portfolio["usd"] -= total_usd
        portfolio["stocks"][sym] = portfolio["stocks"].get(sym, 0) + qty
        _add_log(f"✅ 매수완료 | {sym} {qty}주 @ ${price:.2f}")
    elif rsv["type"] == "sell":
        sym = rsv["symbol"]
        price = TICKERS[sym]["price"]
        qty = rsv["qty"]
        if portfolio["stocks"].get(sym, 0) < qty:
            _add_log(f"❌ 보유 부족 | {sym} 매도 실패")
            return False
        portfolio["stocks"][sym] -= qty
        if portfolio["stocks"][sym] == 0:
            del portfolio["stocks"][sym]
        portfolio["usd"] += price * qty
        _add_log(f"✅ 매도완료 | {sym} {qty}주 @ ${price:.2f}")
    elif rsv["type"] == "exchange_krw_to_usd":
        krw_amount = rsv["krw_amount"]
        rate = USD_KRW["rate"]
        if portfolio["krw"] < krw_amount:
            _add_log(f"❌ 원화 부족 | 환전 실패")
            return False
        usd_amount = round(krw_amount / rate, 2)
        portfolio["krw"] -= krw_amount
        portfolio["usd"] += usd_amount
        _add_log(f"✅ 환전완료 | ₩{krw_amount:,} → ${usd_amount:.2f} (환율 {rate})")
    return True

def _add_log(message):
    portfolio["history"].insert(0, {
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": message,
    })
    if len(portfolio["history"]) > 50:
        portfolio["history"] = portfolio["history"][:50]

market_thread = threading.Thread(target=simulate_market, daemon=True)
market_thread.start()

# ──────────────────────────────────────────────
# LangChain Tools
# ──────────────────────────────────────────────
@tool
def get_stock_price(symbol: str) -> str:
    """주식 현재 시세를 조회합니다. symbol 예: AAPL, MSFT, NVDA, TSLA, AMZN"""
    sym = symbol.upper()
    if sym not in TICKERS:
        return f"{sym}은 지원하지 않는 종목입니다. 지원 종목: {', '.join(TICKERS.keys())}"
    p = TICKERS[sym]["price"]
    return f"{sym} ({TICKERS[sym]['name']}) 현재가: ${p:.2f}"

@tool
def get_exchange_rate() -> str:
    """현재 달러/원 환율을 조회합니다."""
    return f"현재 USD/KRW 환율: {USD_KRW['rate']:.2f}원"

@tool
def get_portfolio() -> str:
    """내 잔고(원화, 달러)와 보유 주식을 조회합니다."""
    rate = USD_KRW["rate"]
    stock_val_usd = sum(TICKERS.get(s, {}).get("price", 0) * q for s, q in portfolio["stocks"].items())
    total_usd = portfolio["usd"] + stock_val_usd
    total_krw = portfolio["krw"] + total_usd * rate
    stocks_str = ", ".join([f"{s}: {q}주" for s, q in portfolio["stocks"].items()]) or "없음"
    return (
        f"💰 원화: ₩{portfolio['krw']:,.0f}\n"
        f"💵 달러: ${portfolio['usd']:.2f}\n"
        f"📈 보유주식: {stocks_str}\n"
        f"📊 총 자산(환산): ₩{total_krw:,.0f}"
    )

@tool
def reserve_buy(symbol: str, target_price: float, qty: int) -> str:
    """목표 주가 이하가 되면 주식을 매수 예약합니다.
    symbol: 종목코드(AAPL 등), target_price: 목표가(USD), qty: 수량"""
    sym = symbol.upper()
    if sym not in TICKERS:
        return f"{sym}은 지원하지 않는 종목입니다."
    rid = reservation_id_counter[0]
    reservation_id_counter[0] += 1
    label = f"{sym} {qty}주 매수 @ ≤${target_price}"
    reservations.append({
        "id": rid, "type": "buy", "symbol": sym,
        "target_price": target_price, "qty": qty,
        "label": label, "status": "active",
        "created_at": datetime.now().strftime("%H:%M:%S"),
    })
    _add_log(f"📌 예약추가 | {label}")
    return f"매수 예약이 등록되었습니다: {label}"

@tool
def reserve_sell(symbol: str, target_price: float, qty: int) -> str:
    """목표 주가 이상이 되면 주식을 매도 예약합니다.
    symbol: 종목코드(AAPL 등), target_price: 목표가(USD), qty: 수량"""
    sym = symbol.upper()
    if sym not in TICKERS:
        return f"{sym}은 지원하지 않는 종목입니다."
    rid = reservation_id_counter[0]
    reservation_id_counter[0] += 1
    label = f"{sym} {qty}주 매도 @ ≥${target_price}"
    reservations.append({
        "id": rid, "type": "sell", "symbol": sym,
        "target_price": target_price, "qty": qty,
        "label": label, "status": "active",
        "created_at": datetime.now().strftime("%H:%M:%S"),
    })
    _add_log(f"📌 예약추가 | {label}")
    return f"매도 예약이 등록되었습니다: {label}"

@tool
def reserve_exchange(target_rate: float, krw_amount: int) -> str:
    """목표 환율 이하가 되면 원화를 달러로 환전 예약합니다.
    target_rate: 목표 환율(원/달러), krw_amount: 환전할 원화 금액"""
    rid = reservation_id_counter[0]
    reservation_id_counter[0] += 1
    label = f"₩{krw_amount:,} 환전 @ ≤{target_rate}원"
    reservations.append({
        "id": rid, "type": "exchange_krw_to_usd",
        "target_rate": target_rate, "krw_amount": krw_amount,
        "label": label, "status": "active",
        "created_at": datetime.now().strftime("%H:%M:%S"),
    })
    _add_log(f"📌 예약추가 | {label}")
    return f"환전 예약이 등록되었습니다: {label}"

@tool
def buy_stock_now(symbol: str, qty: int) -> str:
    """현재 시세로 즉시 주식을 매수합니다. 달러 잔고에서 차감됩니다. 달러가 부족하면 원화를 자동 환전합니다."""
    sym = symbol.upper()
    if sym not in TICKERS:
        return f"{sym}은 지원하지 않는 종목입니다."
    price = TICKERS[sym]["price"]
    total = price * qty
    log_msgs = []
    # 달러 부족 시 원화 자동 환전
    if portfolio["usd"] < total:
        shortage_usd = total - portfolio["usd"]
        rate = USD_KRW["rate"]
        needed_krw = int(shortage_usd * rate * 1.01) + 1  # 수수료 여유 1%
        if portfolio["krw"] < needed_krw:
            return (
                f"달러와 원화 잔고 모두 부족합니다. "
                f"필요: ${total:.2f} (약 ₩{int(total*rate):,}), "
                f"보유 달러: ${portfolio['usd']:.2f}, 보유 원화: ₩{portfolio['krw']:,}"
            )
        usd_gained = round(needed_krw / rate, 2)
        portfolio["krw"] -= needed_krw
        portfolio["usd"] += usd_gained
        log_msgs.append(f"🔄 자동환전 | ₩{needed_krw:,} → ${usd_gained:.2f} (환율 {rate:.2f})")
        _add_log(log_msgs[-1])
    portfolio["usd"] -= total
    portfolio["stocks"][sym] = portfolio["stocks"].get(sym, 0) + qty
    _add_log(f"✅ 즉시매수 | {sym} {qty}주 @ ${price:.2f}")
    prefix = f"[자동환전 후 매수] " if log_msgs else ""
    return f"{prefix}{sym} {qty}주를 ${price:.2f}에 매수했습니다. 총 ${total:.2f} 차감."

@tool
def sell_stock_now(symbol: str, qty: int) -> str:
    """현재 시세로 즉시 주식을 매도합니다. 달러 잔고에 추가됩니다."""
    sym = symbol.upper()
    if portfolio["stocks"].get(sym, 0) < qty:
        return f"보유 수량 부족. 보유: {portfolio['stocks'].get(sym, 0)}주"
    price = TICKERS[sym]["price"]
    total = price * qty
    portfolio["stocks"][sym] -= qty
    if portfolio["stocks"][sym] == 0:
        del portfolio["stocks"][sym]
    portfolio["usd"] += total
    _add_log(f"✅ 즉시매도 | {sym} {qty}주 @ ${price:.2f}")
    return f"{sym} {qty}주를 ${price:.2f}에 매도했습니다. 총 ${total:.2f} 추가."

@tool
def exchange_krw_to_usd_now(krw_amount: int) -> str:
    """현재 환율로 즉시 원화를 달러로 환전합니다."""
    if portfolio["krw"] < krw_amount:
        return f"원화 잔고 부족. 필요: ₩{krw_amount:,}, 보유: ₩{portfolio['krw']:,}"
    rate = USD_KRW["rate"]
    usd = round(krw_amount / rate, 2)
    portfolio["krw"] -= krw_amount
    portfolio["usd"] += usd
    _add_log(f"✅ 즉시환전 | ₩{krw_amount:,} → ${usd:.2f} (환율 {rate:.2f})")
    return f"₩{krw_amount:,}을 현재 환율 {rate:.2f}원으로 환전했습니다. ${usd:.2f} 추가."

tools = [
    get_stock_price, get_exchange_rate, get_portfolio,
    reserve_buy, reserve_sell, reserve_exchange,
    buy_stock_now, sell_stock_now, exchange_krw_to_usd_now,
]

# ──────────────────────────────────────────────
# LangChain Agent (langchain 1.x / langgraph)
# ──────────────────────────────────────────────
SYSTEM_PROMPT = (
    "당신은 가상 트레이딩 봇 어시스턴트입니다. "
    "사용자의 주식 매매, 환전, 잔고 조회 요청을 처리합니다. "
    "항상 한국어로 답변하세요. "
    "매매/환전 실행 전에 도구를 통해 잔고를 확인하고, "
    "필요한 경우 환전(원화→달러) 후 주식 매매를 진행하세요."
)

checkpointer = MemorySaver()

agent = create_agent(
    model="gpt-4o-mini",
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

# ──────────────────────────────────────────────
# Flask Routes
# ──────────────────────────────────────────────
@app.after_request
def set_utf8_header(response):
    if response.content_type.startswith('application/json'):
        response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/market')
def api_market():
    stocks = []
    for sym, data in TICKERS.items():
        change = round(data["price"] - data["prev"], 2)
        change_pct = round((change / data["prev"]) * 100, 2) if data["prev"] else 0
        stocks.append({
            "symbol": sym, "name": data["name"],
            "price": data["price"], "change": change, "change_pct": change_pct,
        })
    rate_change = round(USD_KRW["rate"] - USD_KRW["prev"], 2)
    return jsonify({
        "stocks": stocks,
        "usd_krw": {
            "rate": USD_KRW["rate"],
            "change": rate_change,
        },
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })

@app.route('/api/portfolio')
def api_portfolio():
    rate = USD_KRW["rate"]
    stock_val_usd = sum(TICKERS.get(s, {}).get("price", 0) * q for s, q in portfolio["stocks"].items())
    total_usd = portfolio["usd"] + stock_val_usd
    total_krw = portfolio["krw"] + total_usd * rate
    stocks_detail = []
    for sym, qty in portfolio["stocks"].items():
        price = TICKERS.get(sym, {}).get("price", 0)
        stocks_detail.append({
            "symbol": sym, "qty": qty,
            "price": price, "value_usd": round(price * qty, 2),
            "value_krw": round(price * qty * rate, 0),
        })
    return jsonify({
        "krw": portfolio["krw"],
        "usd": round(portfolio["usd"], 2),
        "stocks": stocks_detail,
        "total_krw": round(total_krw, 0),
        "total_usd": round(total_usd, 2),
    })

@app.route('/api/reservations')
def api_reservations():
    return jsonify({"reservations": reservations})

@app.route('/api/reservations/<int:rid>', methods=['DELETE'])
def delete_reservation(rid):
    global reservations
    reservations = [r for r in reservations if r["id"] != rid]
    return jsonify({"ok": True})

@app.route('/api/approvals')
def api_approvals():
    waiting = [a for a in pending_approvals if a["status"] == "waiting"]
    return jsonify({"approvals": waiting})

@app.route('/api/approvals/<int:aid>/approve', methods=['POST'])
def approve(aid):
    for ap in pending_approvals:
        if ap["id"] == aid and ap["status"] == "waiting":
            ap["status"] = "approved"
            rsv = ap["rsv"]
            _execute_reservation(rsv)
            for r in reservations:
                if r["id"] == rsv["id"]:
                    r["status"] = "done"
            return jsonify({"ok": True})
    return jsonify({"ok": False}), 404

@app.route('/api/approvals/<int:aid>/reject', methods=['POST'])
def reject(aid):
    for ap in pending_approvals:
        if ap["id"] == aid and ap["status"] == "waiting":
            ap["status"] = "rejected"
            rsv = ap["rsv"]
            _add_log(f"🚫 거절 | {rsv['label']}")
            for r in reservations:
                if r["id"] == rsv["id"]:
                    r["status"] = "rejected"
            return jsonify({"ok": True})
    return jsonify({"ok": False}), 404

@app.route('/api/logs')
def api_logs():
    return jsonify({"logs": portfolio["history"][:30]})

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    session_id = data.get("session_id", "default")
    if not user_msg:
        return jsonify({"error": "메시지를 입력하세요."}), 400
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_msg}]},
            config={"configurable": {"thread_id": session_id}},
        )
        return jsonify({"reply": result["messages"][-1].content})
    except Exception as e:
        return jsonify({"reply": f"오류가 발생했습니다: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
