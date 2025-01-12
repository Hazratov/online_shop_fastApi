from typing import Mapping

from app.api.schemas.auth import UserCreate

class UserSerializer:
    def serialize(self, data: Mapping) -> UserCreate:
        return UserCreate.model_validate(data)