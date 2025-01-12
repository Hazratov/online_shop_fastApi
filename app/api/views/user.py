from typing import List

from fastapi import APIRouter, Depends, Path, status, Body
from fastapi.security import OAuth2PasswordBearer

from app.api.controllers.user import UserController
from app.api.schemas.auth import UserAlertSchema, UserUpdate

user_router = APIRouter(prefix="/users", tags=["User"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@user_router.get("/me", response_model=UserAlertSchema)
async def get_myself(
    token: str = Depends(oauth2_scheme), controller: UserController = Depends()
):
    current_user = await controller.get_current_user(token)
    return current_user



@user_router.get("/", response_model=List[UserAlertSchema])
async def get_all_users(
    token: str = Depends(oauth2_scheme),
    controller: UserController = Depends()
):
    current_user = await controller.get_current_user(token)
    return await controller.get_users(current_user)


@user_router.get("/{user_id}", response_model=UserAlertSchema)
async def get_user_by_id(
    user_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
    controller: UserController = Depends()
):
    current_user = await controller.get_current_user(token)
    return await controller.get_users(current_user, user_id)


@user_router.patch("/{user_id}", response_model=UserAlertSchema)
async def patch_user(
    user_id: int = Path(...),
    update_data: UserUpdate = Body(...),
    token: str = Depends(oauth2_scheme),
    controller: UserController = Depends(),
):

    current_user = await controller.get_current_user(token)
    return await controller.update_user(current_user, user_id, update_data.dict(exclude_unset=True), partial=True)


@user_router.put("/{user_id}", response_model=UserAlertSchema)
async def put_user(
    user_id: int = Path(...),
    update_data: UserUpdate = Body(...),
    token: str = Depends(oauth2_scheme),
    controller: UserController = Depends(),
):

    current_user = await controller.get_current_user(token)
    return await controller.update_user(current_user, user_id, update_data.dict(), partial=False)


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int = Path(...),
    token: str = Depends(oauth2_scheme),
    controller: UserController = Depends(),
):

    current_user = await controller.get_current_user(token)
    await controller.delete_user(current_user, user_id)

