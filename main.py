# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from products import router as products_router
from auth import router as auth_router
from headers import router as headers_router
from models import UserCreate

app = FastAPI()

@app.post("/create_user", response_model=UserCreate)
async def create_user(user: UserCreate):
    return user

app.include_router(products_router)
app.include_router(auth_router)
app.include_router(headers_router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.get("/")
async def root():
    return {
        "message": "FastAPI сервер запущен",
        "endpoints": {
            "users": "/create_user (POST)",
            "products": "/product/{id} (GET), /products/search (GET)",
            "auth": "/login (POST), /profile (GET)",
            "headers": "/headers (GET), /info (GET)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)