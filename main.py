# main.py
from fastapi import FastAPI
from products import router as products_router
from auth import router as auth_router
from headers import router as headers_router
from models import UserCreate

app = FastAPI(
    title="Контрольная работа №2",
    version="1.0",
    description="API для контрольной работы по FastAPI"
)

# Задание 3.1 – маршрут создания пользователя
@app.post("/create_user", response_model=UserCreate, tags=["users"])
async def create_user(user: UserCreate):
    return user

# Подключаем роутеры
app.include_router(products_router, tags=["products"])
app.include_router(auth_router, tags=["auth"])  # Здесь подключены маршруты /login, /user
app.include_router(headers_router, tags=["headers"])

@app.get("/")
async def root():
    return {
        "message": "FastAPI сервер запущен",
        "endpoints": {
            "users": "/create_user (POST)",
            "products": "/product/{id} (GET), /products/search (GET)",
            "auth": "/login (POST), /user (GET), /logout (POST)",
            "headers": "/headers (GET), /info (GET)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)