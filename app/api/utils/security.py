from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.api.repositories.user import UserRepository
from app.core.settings import get_settings

settings = get_settings()

# Password hashing utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a plain text password."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifies a password against a hashed password."""
    return pwd_context.verify(password, hashed_password)

# Token utilities
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=24)) -> str:
    """Creates a JWT token with an expiration."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def decode_token(token: str, secret_key: str, algorithm: str = "HS256") -> dict:
    """Decodes a JWT token, raises an exception if invalid."""
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_repo: UserRepository = Depends(),
):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ENCRYPT_ALGORITHM]
        )
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token: missing email")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = await user_repo.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user