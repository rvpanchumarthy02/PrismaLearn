from config.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User:
    @staticmethod
    def create_user(name, email, password):
        # 1. Check duplication
        if db.users.find_one({"email": email}):
            return None # User exists

        # 2. Hash password
        hashed_password = generate_password_hash(password)

        # 3. Create document
        new_user = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": "student", # Default role
            "created_at": datetime.utcnow()
        }
        
        result = db.users.insert_one(new_user)
        return result.inserted_id

    @staticmethod
    def login_user(email, password):
        user = db.users.find_one({"email": email})
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def get_user_by_id(user_id):
        from bson.objectid import ObjectId
        return db.users.find_one({"_id": ObjectId(user_id)})