import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


client = MongoClient("localhost", 27017)
db = client.dbsparta

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}
data = requests.get("https://finance.naver.com/sise/sise_market_sum.nhn", headers=headers)

soup = BeautifulSoup(data.text, "html.parser")

stocks = soup.select("table.type_2 > tbody > tr")
delete = db.stocks.delete_many({})
delete.deleted_count

cnt = 0
for stock in stocks:
    a_title = stock.select_one("td > a")
    if a_title is not None:
        cnt += 1
        title = a_title.text
        share = stock.select_one("td.number").text
        full_code = a_title["href"].split("=")
        code = full_code[-1]
        doc = {"title": title, "code": code, "share": share, "variance": 0, "variance_rate": 0}
        db.stocks.insert_one(doc)
        if cnt == 20:
            break
