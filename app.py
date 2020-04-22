from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

client = MongoClient("127.0.0.1", 27017)
db = client.dbsparta

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/main")
def main():
    return render_template("main.html")


@app.route("/main/stock", methods=["GET"])
def get_stock():
    code = request.form["code"]
    stock = db.stocks.find_one({"code": code}, {"_id": 0})
    return jsonify({"result": "success", "msg": "저장되었습니다.", "data": stock})


@app.route("/mypage")
def mypage():
    return render_template("mypage.html")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
