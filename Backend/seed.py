import os
import sys
from pymongo import MongoClient
from datetime import datetime
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# 2. Connect to Database (Robust Connection)
uri = os.getenv("MONGO_URI")

if not uri:
    print("❌ Error: MONGO_URI not found in .env file.")
    sys.exit(1)

try:
    client = MongoClient(uri)
    # FIX: Force the code to use your specific database name
    db = client["course_portal_db"]
    print(f"🔌 Connected to Database: {db.name}")
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    sys.exit(1)

# ==========================================
#  SECTION A: SEED COURSES
# ==========================================
courses_data = [
    {"title": "Full Stack Web Development", "description": "Master MERN stack: MongoDB, Express, React, Node.js.", "instructor": "Dr. Angela Yu"},
    {"title": "Data Science with Python", "description": "Learn Pandas, NumPy, and Machine Learning basics.", "instructor": "Prof. Andrew Ng"},
    {"title": "Cyber Security", "description": "Network security, ethical hacking, and safety protocols.", "instructor": "Mr. Robot"},
    {"title": "UI/UX Design", "description": "Design user-friendly interfaces with Figma.", "instructor": "Don Norman"},
    {"title": "Cloud Computing", "description": "Introduction to AWS, Azure, and Google Cloud.", "instructor": "Satya Nadella"},
    {"title": "Digital Marketing", "description": "SEO, Social Media strategies, and Content Marketing.", "instructor": "Gary Vaynerchuk"},
    {"title": "Game Development", "description": "Build 2D and 3D games using Unity.", "instructor": "Hideo Kojima"},
    {"title": "Blockchain Basics", "description": "Understanding Crypto and Smart Contracts.", "instructor": "Satoshi Nakamoto"}
]

print("\n🌱 Seeding Courses...")
for course in courses_data:
    # Avoid duplicates: Check if title exists
    if not db.courses.find_one({"title": course["title"]}):
        course["created_at"] = datetime.utcnow()
        db.courses.insert_one(course)
        print(f"   ✅ Added Course: {course['title']}")
    else:
        print(f"   ⚠️  Skipped Course (Exists): {course['title']}")

# ==========================================
#  SECTION B: SEED USERS (With Hashed Passwords)
# ==========================================
users_data = [
    {
        "name": "Admin User",
        "email": "admin@test.com",
        "password": "password123",  # Will be hashed
        "role": "admin"
    },
    {
        "name": "Student One",
        "email": "student1@test.com",
        "password": "password123",
        "role": "student"
    },
    {
        "name": "Student Two",
        "email": "student2@test.com",
        "password": "password123",
        "role": "student"
    }
]

print("\n👤 Seeding Users...")
for user in users_data:
    if not db.users.find_one({"email": user["email"]}):
        # HASH THE PASSWORD so login actually works
        hashed_pw = generate_password_hash(user["password"])
        
        new_user = {
            "name": user["name"],
            "email": user["email"],
            "password": hashed_pw,
            "role": user["role"],
            "created_at": datetime.utcnow()
        }
        db.users.insert_one(new_user)
        print(f"   ✅ Added User: {user['email']} (Password: password123)")
    else:
        print(f"   ⚠️  Skipped User (Exists): {user['email']}")

print("\n🎉 Seeding Complete! Go refresh your website.")
