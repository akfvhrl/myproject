from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.dbsparta

email = input()
password = input()

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
    else:
        print("비밀번호가 틀렸습니다.")
