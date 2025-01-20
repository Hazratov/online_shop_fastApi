from typing import Optional, Sequence
from fastapi import Depends, HTTPException, status
from app.api.models.user import User
from app.api.repositories.user import UserRepository
from app.api.schemas.auth import (UserAlertSchema)
from app.api.utils.security import decode_token
from app.core.settings import get_settings, Settings


class UserController:
    def __init__(
        self,
        user_repo: UserRepository = Depends(),
        settings: Settings = Depends(get_settings),
    ):
        self.user_repo = user_repo
        self.settings = settings

    async def get_current_user(self, token: str) -> UserAlertSchema:
        payload = decode_token(token, self.settings.JWT_SECRET_KEY, "HS256")
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid Email")
        user = await self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    async def get_users(self, current_user: UserAlertSchema, user_id: Optional[int] = None) -> Sequence[UserAlertSchema]:
        if current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        if user_id:
            user = await self.user_repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                )
            return user

        return await self.user_repo.all_users()

    async def update_user(self, current_user: UserAlertSchema, user_id: int, update_data: dict, partial: bool = True):

        if current_user.role.value != "admin" and current_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        return await self.user_repo.update_user(user)

    async def delete_user(self, current_user: UserAlertSchema, user_id: int):

        if current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        await self.user_repo.delete_user(user)

