from db.db import User
from sqlalchemy import extract, select, update
from sqlalchemy.orm import Session
from utils import *


class UserRepository():
    async def is_exist(db: Session, id: UUID_ID) -> bool:  # move to masters
        is_exist = await db.execute(
            select(User).where(
                (User.id == id)
            )
        )
        is_exist = is_exist.first()

        return True if is_exist else False
