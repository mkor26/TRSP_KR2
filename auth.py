# auth.py
import uuid
from fastapi import APIRouter, HTTPException, Response, Request, Cookie, status
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

# Хранилище сессий и пользователей
# В реальном приложении это была бы база данных
sessions = {}  # {session_token: username}
users_db = {}  # {username: {"password": str, "user_id": str, "email": str}}


# Модель для логина
class LoginRequest(BaseModel):
    username: str
    password: str


# Модель для ответа с профилем
class UserProfile(BaseModel):
    username: str
    user_id: str
    email: str



def verify_credentials(username: str, password: str) -> Optional[dict]:


    test_users = {
        "user123": {"password": "password123", "user_id": str(uuid.uuid4()), "email": "user123@example.com"},
        "alice": {"password": "alice123", "user_id": str(uuid.uuid4()), "email": "alice@example.com"},
        "bob": {"password": "bob123", "user_id": str(uuid.uuid4()), "email": "bob@example.com"}
    }

    if username in test_users and test_users[username]["password"] == password:
        return test_users[username]
    return None


# Задание 5.1 - Маршрут логина
@router.post("/login")
async def login(login_data: LoginRequest, response: Response):


    user_data = verify_credentials(login_data.username, login_data.password)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )

    session_token = str(uuid.uuid4())


    sessions[session_token] = {
        "username": login_data.username,
        "user_id": user_data["user_id"],
        "email": user_data["email"]
    }

    # Устанавливаем cookie
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,  # Защита от XSS - JavaScript не может получить доступ к cookie
        max_age=300,  # Время жизни 5 минут (как в задании 5.3)
        secure=False,  # Для тестирования (в продакшене должно быть True)
        samesite="lax"  # Защита от CSRF
    )

    return {
        "message": "Успешный вход в систему",
        "session_token": session_token,  # Выводим токен в ответе для наглядности
        "user_id": user_data["user_id"]
    }


# Задание 5.1 - Защищенный маршрут /user (в задании указан /user)
@router.get("/user")
async def get_user_profile(session_token: Optional[str] = Cookie(None)):

    # Проверяем наличие токена
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    # Проверяем валидность токена
    if session_token not in sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized"
        )

    # Получаем данные пользователя
    user_info = sessions[session_token]

    return {
        "message": "Информация профиля пользователя",
        "username": user_info["username"],
        "user_id": user_info["user_id"],
        "email": user_info["email"]
    }


# Дополнительный маршрут для выхода (logout)
@router.post("/logout")
async def logout(response: Response, session_token: Optional[str] = Cookie(None)):

    if session_token and session_token in sessions:
        del sessions[session_token]

    # Удаляем cookie
    response.delete_cookie("session_token")

    return {"message": "Выход выполнен успешно"}


# Маршрут для просмотра активных сессий (только для отладки)
@router.get("/sessions")
async def list_sessions():

    active_sessions = []
    for token, user_info in sessions.items():
        active_sessions.append({
            "session_token": token,
            "username": user_info["username"],
            "user_id": user_info["user_id"]
        })
    return {"active_sessions": active_sessions}