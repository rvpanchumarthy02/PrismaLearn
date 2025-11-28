import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

try:
    client = MongoClient(MONGO_URI)
    db = client.get_database() 
    print("✅ Connected to MongoDB")
except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    db = None