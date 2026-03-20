from pymongo import MongoClient

MONGO_URL = "mongodb+srv://3658831900101_db_user:s7OCVH1B0FitovSW@cluster0.2yckis5.mongodb.net/"

client = MongoClient(MONGO_URL)
db = client["flask_app"]
user_col = db["users"]