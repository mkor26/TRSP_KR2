# headers.py
from fastapi import APIRouter, Header, HTTPException, Request
from datetime import datetime, timezone
from models import CommonHeaders

router = APIRouter()

@router.get("/headers")
async def get_headers(
        user_agent: str = Header(..., alias="User-Agent"),
        accept_language: str = Header(..., alias="Accept-Language")
):
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language
    }

@router.get("/info")
async def get_info(
        request: Request,
        user_agent: str = Header(..., alias="User-Agent"),
        accept_language: str = Header(..., alias="Accept-Language")
):

    if not accept_language or not any(part.strip() for part in accept_language.split(',')):
        raise HTTPException(status_code=400, detail="Invalid Accept-Language format")
    current_time = datetime.now(timezone.utc).isoformat()
    return {
        "message": "Добро пожаловать! Ваши заголовки успешно обработаны.",
        "headers": {
            "User-Agent": user_agent,
            "Accept-Language": accept_language
        }
    }