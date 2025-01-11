from pydantic import BaseModel
from typing import Optional

from app.api.models.user import UserRole



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[UserRole] = None