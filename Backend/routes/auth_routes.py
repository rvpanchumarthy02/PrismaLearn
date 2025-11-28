from flask import Blueprint, request
from models.user_model import User
from utils.token_helper import generate_token
from utils.error_handler import error_response, success_response

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return error_response("Missing fields", 400)

    user_id = User.create_user(name, email, password)
    
    if not user_id:
        return error_response("User with this email already exists", 409)

    return success_response({"user_id": str(user_id)}, "User registered successfully", 201)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.login_user(email, password)

    if not user:
        return error_response("Invalid credentials", 401)

    token = generate_token(user['_id'])
    return success_response({"token": token, "name": user['name']}, "Login successful")