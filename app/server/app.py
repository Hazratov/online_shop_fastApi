from fastapi import FastAPI

from app.core.settings import get_settings
from app.api.views.auth import auth_router
from app.api.views.user import user_router
from app.api.views.product import product_router
from app.api.views.order import order_router

settings = get_settings()


def create_app() -> FastAPI:
    app_ = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )
    app_.include_router(auth_router, prefix="/auth", tags=["Authoration"])
    app_.include_router(user_router, prefix="/api", tags=["User"])
    app_.include_router(product_router, prefix="/api", tags=["Product"])
    app_.include_router(order_router, prefix="/api", tags=["Order"])
    return app_
