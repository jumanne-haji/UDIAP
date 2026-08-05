"""
Authentication Service
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User, UserRole
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.schemas.user import UserOut


class AuthService:
    async def register(self, data: RegisterRequest, db: AsyncSession) -> dict:
        # Check existing
        result = await db.execute(select(User).where(User.email == data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        user = User(
            name=data.name,
            email=data.email,
            password_hash=get_password_hash(data.password),
            role=UserRole.USER,
        )
        db.add(user)
        await db.flush()
        await db.refresh(user)

        tokens = self._issue_tokens(user)
        return {**tokens, "user": UserOut.model_validate(user)}

    async def login(self, data: LoginRequest, db: AsyncSession) -> dict:
        result = await db.execute(select(User).where(User.email == data.email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated",
            )

        tokens = self._issue_tokens(user)
        return {**tokens, "user": UserOut.model_validate(user)}

    def _issue_tokens(self, user: User) -> dict:
        payload = {"sub": str(user.id), "role": user.role.value}
        return {
            "access_token": create_access_token(payload),
            "refresh_token": create_refresh_token(payload),
            "token_type": "bearer",
        }


auth_service = AuthService()
