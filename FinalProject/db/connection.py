import pymongo

# connect to mongodb
client_uri = "mongodb://localhost:27017/"
client = pymongo.MongoClient(client_uri)
db = client["zmanim_and_weather"]

users_collection = db["users"]
user_preferences = db["user_preferences"]
notifications_collection = db["notifications"]