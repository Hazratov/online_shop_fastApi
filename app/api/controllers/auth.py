from fastapi import Depends, HTTPException, status

from passlib.hash import bcrypt
import jwt

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from app.api.repositories.auth import AuthRepository
from app.api.schemas.auth import UserCreate, UserLogin, TokenResponse, EmailVerification, ForgotPassword
from app.api.utils.security import create_access_token, verify_password


from app.core.settings import get_settings, Settings

# settings = get_settings()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class AuthController:
    def __init__(self,
                 auth_repo: AuthRepository = Depends(),
                 settings: Settings = Depends(get_settings)
                 ):
        self.auth_repo = auth_repo
        self.settings = settings

    async def register_user(self, user_data: UserCreate):
        existing_user = await self.auth_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        user_data.password = bcrypt.hash(user_data.password)
        return await self.auth_repo.create_user(user_data)

    async def login_user(self, user_login: UserLogin) -> TokenResponse:
        user = await self.auth_repo.get_user_by_email(user_login.email)
        if not user or not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email or password",
            )

        access_token = create_access_token(
            data={"email": user.email, "role": user.role.value, "sub": user.id},
        )
        return TokenResponse(access_token=access_token, token_type="bearer")

