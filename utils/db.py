from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")
db = client['axie']  # 获得数据库的句柄

