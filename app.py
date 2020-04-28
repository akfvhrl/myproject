from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27017)
db = client.dbsparta

app = Flask(__name__)
email = ""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    global email
    email = request.form["email"]
    password = request.form["password"]
    user = db.users.find_one({"email": email}, {"_id": 0})
    if user == None:
        return jsonify({"result": "fail", "msg": "없는 이메일입니다."})
    if user["password"] == password:
        return jsonify({"result": "success", "msg": "로그인 되었습니다."})
    else:
        return jsonify({"result": "fail", "msg": "암호가 틀렸습니다."})


@app.route("/signup", methods=["POST"])
def signup():
    email = request.form["email"]
    password = request.form["password"]
    name = request.form["name"]
    if db.users.find_one({"email": email}) != None:
        return jsonify({"result": "fail", "msg": "이미 있는 이메일입니다."})
    if len(password) < 8:
        return jsonify(
            {"result": "fail", "msg": "비밀번호가 너무 짧습니다. 8자리 이상의 비밀번호로 만들어 주십시오."}
        )
    new_user = {
        "email": email,
        "name": name,
        "password": password,
        "money": 100000000,
    }
    new_trade = {"email": email, "get_stocks": {}}
    db.users.insert_one(new_user)
    db.users_trade.insert_one(new_trade)
    return jsonify(
        {"result": "success", "msg": "회원가입이 성공적으로 이루어졌습니다. 로그인 해주십시오."}
    )


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/main/right", methods=["POST"])
def get_right():
    money = db.users.find_one({"email": email})["money"]
    return jsonify({"result": "success", "msg": "저장되었습니다.", "data": money})


@app.route("/main/my_stock", methods=["POST"])
def my_stock():
    my_stocks = db.users_trade.find_one({"email": email})["get_stocks"]
    return jsonify(
        {
            "result": "success",
            "msg": "저장되었습니다.",
            "data": my_stocks,
            "size": len(my_stocks),
        }
    )


@app.route("/main/stock", methods=["POST"])
def get_stock():
    code = request.form["code"]
    stock = db.stocks.find_one({"code": code}, {"_id": 0})
    return jsonify({"result": "success", "msg": "저장되었습니다.", "data": stock})


@app.route("/main/left", methods=["POST"])
def make_left():
    stocks = db.stocks.find({}, {"_id": 0})
    return_stock = []
    for stock in stocks:
        return_stock.append(stock)
    return jsonify({"result": "success", "msg": "성공", "data": return_stock})


@app.route("/main/buy", methods=["POST"])
def buy_stock():
    code = request.form["code"]
    count = int(request.form["count"])
    price = int(
        db.stocks.find_one({"code": code}, {"_id": 0})["share"].replace(
            ",", ""
        )
    )
    money = db.users.find_one({"email": email})["money"]
    if money <= price * count:
        return jsonify({"result": "fail", "msg": "잔고가 부족합니다."})
    else:
        to_buy = db.users_trade.find_one({"email": email}, {"_id": 0})[
            "get_stocks"
        ]
        key = db.stocks.find_one({"code": code}, {"_id": 0})["title"]
        if key in to_buy.keys():
            to_buy[key][1] += price * count
            to_buy[key][2] += count
        else:
            to_buy[key] = [code, price * count, count]
        db.users_trade.update_one(
            {"email": email}, {"$set": {"get_stocks": to_buy}}
        )
        db.users.update_one(
            {"email": email}, {"$set": {"money": money - (price * count)}}
        )
    return jsonify({"result": "success", "msg": "구매에 성공했습니다."})


@app.route("/main/sale", methods=["POST"])
def sale_stock():
    code = request.form["code"]
    count = int(request.form["count"])
    find_code = db.users_trade.find_one({"email": email}, {"_id": 0})[
        "get_stocks"
    ][db.stocks.find_one({"code": code}, {"_id": 0})["title"]]
    if count <= find_code[2]:
        price_one = find_code[1] / find_code[2]
        money = db.users.find_one({"email": email}, {"_id": 0})["money"]
        money += price_one * count
        db.users.update_one({"email": email}, {"$set": {"money": money}})
        cnt = find_code[2] - count
        my_stocks = db.users_trade.find_one({"email": email}, {"_id": 0})[
            "get_stocks"
        ]
        if count < find_code[2]:
            my_stocks[db.stocks.find_one({"code": code}, {"_id": 0})["title"]][
                2
            ] = cnt
            my_stocks[db.stocks.find_one({"code": code}, {"_id": 0})["title"]][
                1
            ] = (price_one * cnt)
        else:
            del my_stocks[
                db.stocks.find_one({"code": code}, {"_id": 0})["title"]
            ]
        db.users_trade.update_one(
            {"email": email}, {"$set": {"get_stocks": my_stocks}}
        )
        return jsonify({"result": "success", "msg": "판매에 성공했습니다."})
    else:
        return jsonify({"result": "fail", "msg": "판매에 실패했습니다.(보유 주식 부족)"})


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
