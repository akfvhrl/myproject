from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.dbsparta

delete = db.users.delete_many({})
delete.deleted_count

delete = db.users_trade.delete_many({})
delete.deleted_count
