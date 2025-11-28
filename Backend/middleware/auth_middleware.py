from functools import wraps
from flask import request, jsonify
import jwt
import os
from config.db import db
from bson.objectid import ObjectId

SECRET_KEY = os.getenv("SECRET_KEY")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check header: Authorization: Bearer <token>
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except IndexError:
                return jsonify({"message": "Token is missing or invalid format!"}), 401

        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = db.users.find_one({"_id": ObjectId(data["user_id"])})
            
            if not current_user:
                return jsonify({"message": "Invalid Token!"}), 401
                
            # Attach user_id to the request context for the route to use
            request.user_id = str(current_user["_id"])
            
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired!"}), 401
        except Exception as e:
            return jsonify({"message": "Token is invalid!"}), 401

        return f(*args, **kwargs)

    return decorated