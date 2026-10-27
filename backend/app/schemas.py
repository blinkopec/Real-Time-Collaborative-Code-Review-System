from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# Схемы для пользователей
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Схемы для снипетов
class SnippetCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    language: str = "python"
    code: str = Field(min_length=1)


class SnippetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    language: str
    code: str
    author_id: int
    created_at: datetime


# Схемы для комментариев
class CommentCreate(BaseModel):
    line_number: int = Field(ge=1)
    body: str = Field(min_length=1)


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    snippet_id: int
    author_id: int
    line_number: int
    body: str
    created_at: datetime
