import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserRegister, UserUpdate
from app.services.auth import hash_password


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Fetch a user by email. Returns None if not found."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    """Fetch a user by their UUID. Returns None if not found."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, payload: UserRegister) -> User:
    """Create a new user.

    Raises:
        HTTPException 409: If a user with that email already exists.
    """
    existing = await get_user_by_email(db, payload.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
        )

    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        full_name=payload.full_name,
    )
    db.add(user)
    await db.flush()  # Gets the generated UUID without committing
    await db.refresh(user)  # Loads server-set fields (created_at, etc.)
    return user


async def update_user(db: AsyncSession, user: User, payload: UserUpdate) -> User:
    """Update mutable user fields. Only updates fields that are provided."""
    update_data = payload.model_dump(exclude_unset=True)  # Only set fields
    for field, value in update_data.items():
        setattr(user, field, value)
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user
