import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# ─── Request schemas (what the client sends) ──────────────────────────────────

class UserRegister(BaseModel):
    """Payload for POST /api/v1/auth/register"""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    full_name: str = Field(min_length=1, max_length=255)


class UserLogin(BaseModel):
    """Payload for POST /api/v1/auth/login"""
    email: EmailStr
    password: str


class TokenRefresh(BaseModel):
    """Payload for POST /api/v1/auth/refresh"""
    refresh_token: str


class UserUpdate(BaseModel):
    """Payload for PATCH /api/v1/users/me"""
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    bio: str | None = None


# ─── Response schemas (what we send back) ─────────────────────────────────────

class UserResponse(BaseModel):
    """Public user representation. Never includes hashed_password."""
    id: uuid.UUID
    email: str
    full_name: str
    bio: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}  # Allows .model_validate(db_user)


class TokenResponse(BaseModel):
    """Returned after login or token refresh."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class HealthResponse(BaseModel):
    status: str
    service: str
    db: str
