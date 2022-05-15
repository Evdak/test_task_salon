from typing import List, Optional
from datetime import datetime
from db.db import User
from models import feedback
from models.feedback import Feedback as FeedbackModel
from schemas.feedback import FeedbackBase, FeedbackCreate, FeedbackUpdate
from sqlalchemy import extract, select, update
from sqlalchemy.orm import Session
from utils import *


class FeedbackRepository():
    async def create(f: FeedbackCreate, db: Session, user: User) -> FeedbackCreate:
        feedback = FeedbackModel(**f.dict())
        feedback.user_id = user.id
        db.add(feedback)
        await db.commit()
        db.refresh(feedback)
        return feedback

    async def update(f: FeedbackUpdate, db: Session) -> FeedbackBase:
        feedback_old = await db.execute(
            select(FeedbackModel).where(FeedbackModel.id == f.id)
        )
        feedback_old = feedback_old.scalars().first()
        feedback = await db.execute(
            update(FeedbackModel).where(FeedbackModel.id == FeedbackModel.id).values(
                rate=f.rate,
                text=f.text
            ))

        await db.commit()
        feedback_new = await db.execute(
            select(FeedbackModel).where(FeedbackModel.id == feedback_old.id)
        )
        return feedback_new.scalars().first()

    async def get_all(db: Session) -> List[FeedbackBase]:
        result = await db.execute(select(FeedbackModel))
        return list(result.scalars())

    async def get_by_id(id: int, db: Session) -> FeedbackBase:
        result = await db.execute(select(FeedbackModel).where(FeedbackModel.id == id))
        return list(result.scalars().first())

    async def get_by_user_id(user_id: UUID_ID, db: Session) -> List[FeedbackBase]:
        result = await db.execute(select(FeedbackModel).where(FeedbackModel.user_id == user_id))
        return list(result.scalars())

    async def get_by_master_id(master_id: UUID_ID, db: Session) -> List[FeedbackBase]:
        result = await db.execute(select(FeedbackModel).where(FeedbackModel.master_id == master_id))
        return list(result.scalars())

    async def delete(db: Session, id: int):
        feedback = await db.execute(select(FeedbackModel).where(FeedbackModel.id == id))
        feedback = feedback.scalars().first()
        await db.delete(feedback)
        await db.commit()
        return f'Deleted id: {id}'

    async def is_exist(db: Session, id: int) -> bool:  # move to masters
        is_exist = await db.execute(
            select(FeedbackModel).where(
                (FeedbackModel.id == id)
            )
        )
        is_exist = is_exist.first()

        return True if is_exist else False

    async def is_by_user(db: Session, id: int, user_id: UUID_ID) -> bool:  # move to masters
        is_by_user = await db.execute(
            select(FeedbackModel).where(
                (FeedbackModel.id == id)
            )
        )
        is_by_user = is_by_user.scalars().first()

        return True if is_by_user.user_id == user_id else False
