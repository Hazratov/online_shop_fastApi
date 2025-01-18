from fastapi import APIRouter, Depends, status
from app.api.schemas.auth import (
    UserCreate,
    UserLogin,
    TokenResponse,
    EmailVerification,
    ForgotPassword
)
from fastapi.security import OAuth2PasswordRequestForm
from app.api.controllers.auth import AuthController

auth_router = APIRouter()
    

@auth_router.post("/register", status_code=201)
async def register_user(
    user_data: UserCreate, auth_controller: AuthController = Depends()
):
    return await auth_controller.register_user(user_data)


@auth_router.post("/login", response_model=TokenResponse)
async def login_user(
        user_login: UserLogin, auth_controller: AuthController = Depends()
):
    return await auth_controller.login_user(user_login)

