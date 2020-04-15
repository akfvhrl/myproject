
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.dbsparta

user = input()
password = input()

a = db.users.find({"name":user})

if a is not None:
    if a["password"] == password:
        print("로그인")
    else:
        print("잘못된 비밀번호")
else:
    new_user = {"name":user, "password":password, "money":100000000, "get_stocks":{}, "to_buy": {}, "to_sale": {}}
    db.users.insert_one(new_user)
