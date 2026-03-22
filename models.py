# models.py
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: Optional[int] = Field(None, ge=1)
    is_subscribed: Optional[bool] = False

class CommonHeaders(BaseModel):
    user_agent: str = Field(..., alias="User-Agent")
    accept_language: str = Field(..., alias="Accept-Language")
    class Config:
        populate_by_name = True

    @field_validator("accept_language")
    @classmethod
    def validate_accept_language(cls, v: str) -> str:
        # Простейшая валидация формата Accept-Language
        if not v or not any(part.strip() for part in v.split(',')):
            raise ValueError("Invalid Accept-Language format")
        return v