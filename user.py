from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.dbsparta

email = input()
password = input()
is_login = 0

a = db.users.find_one({"email": email})

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
        element = lists.find_one({"title": to_buy}, {"_id": 0})
        print(element)
        // user db update
    if todo == "logout":
        is_login = 0
        print("logout")
