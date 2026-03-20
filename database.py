from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["financial_db"]
collection = db["transactions"]