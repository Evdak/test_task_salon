import uuid

from fastapi_users import schemas


class User(schemas.BaseUser):
    role: str
    # pass


class UserRead(schemas.BaseUser[uuid.UUID]):
    role: str
    # pass


class UserCreate(schemas.BaseUserCreate):
    role: str
    # pass


class UserUpdate(schemas.BaseUserUpdate):
    role: str
    # pass
