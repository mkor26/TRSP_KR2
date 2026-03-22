import uuid
import time
from fastapi import APIRouter, HTTPException, Response, Request, Cookie, status
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from pydantic import BaseModel

router = APIRouter()

SECRET_KEY = "my-super-secret-key-for-signing-sessions"
serializer = URLSafeTimedSerializer(SECRET_KEY)
sessions = {}

class LoginForm(BaseModel):
    username: str
    password: str

def verify_credentials(username: str, password: str) -> bool:
    return bool(username and password)

@router.post("/login")
async def login(login_data: LoginForm, response: Response):
    if not verify_credentials(login_data.username, login_data.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user_id = str(uuid.uuid4())
    current_time = int(time.time())

    sessions[user_id] = {"last_activity": current_time}

    data = f"{user_id}.{current_time}"
    signed_token = serializer.dumps(data)

    response.set_cookie(
        key="session_token",
        value=signed_token,
        httponly=True,
        max_age=300,
        secure=False
    )
    return {"message": "Login successful"}

@router.get("/profile")
async def get_profile(request: Request, response: Response, session_token: str = Cookie(None)):
    if not session_token:
        raise HTTPException(status_code=401, detail="Session expired")

    try:
        data = serializer.loads(session_token, max_age=300)
        user_id, timestamp_str = data.split(".")
        timestamp = int(timestamp_str)
    except (BadSignature, SignatureExpired, ValueError):
        raise HTTPException(status_code=401, detail="Invalid session")

    if user_id not in sessions:
        raise HTTPException(status_code=401, detail="Session expired")

    last_activity = sessions[user_id]["last_activity"]
    current_time = int(time.time())
    elapsed = current_time - last_activity

    if elapsed > 300:
        del sessions[user_id]
        raise HTTPException(status_code=401, detail="Session expired")

    if timestamp != last_activity:
        raise HTTPException(status_code=401, detail="Invalid session")

    if elapsed >= 180 and elapsed < 300:
        new_timestamp = current_time
        sessions[user_id]["last_activity"] = new_timestamp
        new_data = f"{user_id}.{new_timestamp}"
        new_signed = serializer.dumps(new_data)
        response.set_cookie(
            key="session_token",
            value=new_signed,
            httponly=True,
            max_age=300,
            secure=False
        )

    return {
        "user_id": user_id,
        "username": "testuser",
        "last_activity": sessions[user_id]["last_activity"]
    }