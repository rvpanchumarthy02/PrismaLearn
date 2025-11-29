import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Fallback to local if no URI is found (prevents crash on start)
if not MONGO_URI:
    print("⚠️  MONGO_URI not found in .env, using localhost default")
    MONGO_URI = "mongodb://localhost:27017/course_portal_db"

try:
    client = MongoClient(MONGO_URI)
    
    # FIX: Explicitly select the database name 'course_portal_db'
    # This fixes the "No default database defined" error even if your URI is missing it
    db = client["course_portal_db"] 
    
    # Test the connection immediately
    client.admin.command('ping')
    print(f"✅ MongoDB Connected Successfully to: {db.name}")

except Exception as e:
    print(f"❌ Error connecting to MongoDB: {e}")
    db = None
