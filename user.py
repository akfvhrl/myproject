from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.dbsparta

email = input()
password = input()
is_login = 0

a = db.users.find_one({"email": email})
users = db.users

if a is None:
    user = input("이름을 입력해주세요")
    new_user = {
        "email": email,
        "name": user,
        "password": password,
        "money": 100000000,
        "get_stocks": {},
        "to_buy": {},
        "to_sale": {},
    }
    db.users.insert_one(new_user)
else:
    if a["password"] is password:
        print("로그인")
        is_login = 1
    else:
        print("비밀번호가 틀렸습니다.")

while is_login is 1:
    todo = input()
    if todo == "buy":
        lists = db.stocks
        for element in lists.find({}, {"_id": 0}):
            print(element)
        to_buy = input()
        buy_cnt = int(input())
        element = lists.find_one({"title": to_buy}, {"_id": 0})
        print(element)
        users.update_one(
            {"email": email},
            {
                "$set": {
                    "get_stocks": [element["title"], buy_cnt],
                    "money": (
                        users.find_one({"email": email})["money"]
                        - int(element["share"].replace(",", ""))
                    )
                    * buy_cnt,
                }
            },
        )
        # user db update
    if todo == "sale":
        for user in users.find({"email": email}, {"_id": 0, "get_stocks": 1}):
            print(user)
        to_sale = input()
        users.update_one(
            {"email": email},
            {
                "$set": {
                    "money": users.find_one({"email": email})["money"]
                    + users.find_one({"email": email})["get_stocks"][1],
                    "get_stocks": [],
                }
            },
        )
    if todo == "money":
        print(users.find_one({"email": email})["money"])
    if todo == "logout":
        is_login = 0
        print("logout")
