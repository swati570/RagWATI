from fastapi import APIRouter, Form
from backend.utils import hash_password, verify_password, create_jwt_token
from backend.db_mongo import users_col  

router = APIRouter()

@router.post("/register")
def register_user(username: str = Form(...), password: str = Form(...)):
    if users_col.find_one({"username": username}):
        return {"error": "User already exists"}
    hashed = hash_password(password)
    users_col.insert_one({"username": username, "password": hashed})

    return {"message": "User registered successfully"}

@router.post("/login")
def login_user(username: str = Form(...), password: str = Form(...)):
    user = users_col.find_one({"username": username})
    if not user or not verify_password(password, user["password"]):
        return {"error": "Invalid credentials"}
    token = create_jwt_token(user_id=username)
    return {"token": token}


