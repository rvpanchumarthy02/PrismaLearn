import jwt
import datetime
import os
from dotenv import load_dotenv

# 1. Force load the environment variables
load_dotenv()

# 2. Get the key, but add a default string just in case .env fails
SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key_12345")

def generate_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    # 3. Use the key correctly
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")