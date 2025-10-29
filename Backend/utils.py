import jwt
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")

def hash_password(password: str) -> str:
    return bcrypt.hash(password[:72])


def verify_password(password: str, hashed: str):
    return bcrypt.verify(password, hashed)

def create_jwt_token(user_id: str):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=3)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def decode_jwt_token(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
def get_user_id_from_token(token: str):
    data = decode_jwt_token(token)
    if data:
        return data.get("user_id")
    return None

