from datetime import datetime, timedelta
import jwt
from passlib.context import CryptContext
from app.core.settings import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    data: dict, secret_key: str, algorithm: str = "HS256", expires_minutes: int = 60
) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
