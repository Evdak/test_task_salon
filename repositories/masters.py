from typing import List, Optional
from datetime import datetime
from db.db import User
from models import masters
from schemas.masters import MasterBase, MasterCreate, MasterUpdate
from models.masters import Master
from sqlalchemy import extract, select, update
from sqlalchemy.orm import Session
from utils import *


class MasterRepository():
    async def create(db: Session, user: User) -> MasterBase:
        master = Master()
        master.master_id = user.id
        master.rate_count = 0
        master.rating = 0
        db.add(master)
        await db.commit()
        await db.refresh(master)
        return master

    async def update(db: Session, m: MasterUpdate) -> MasterBase:
        # if user.role != 'admin':
        #     return None  # access denied
        master = await db.execute(select(Master).where(Master.id == m.id))
        master = master.scalars().first()
        master.text = m.text
        db.add(master)
        await db.commit()
        await db.refresh(master)
        return master

    async def get_all(db: Session) -> List[MasterBase]:
        result = await db.execute(select(Master))
        return list(result.scalars())

    async def get_master(master_id: UUID_ID, db: Session) -> MasterBase:
        result = await db.execute(select(Master).where(Master.master_id == master_id))
        return result.scalars().first()

    async def delete(db: Session, id: int):
        # if user.role != 'admin':
        #     return None
        master = await db.execute(select(Master).where(Master.id == id))
        master = master.scalars().first()
        await db.delete(master)
        await db.commit()
        return f'Deleted id: {id}'

    async def is_exist_master(db: Session, master_id: int) -> bool:  # move to masters
        is_exist = await db.execute(
            select(Master).where(
                (Master.master_id == master_id)
            )
        )

        is_exist = is_exist.first()

        return True if is_exist else False

    async def is_exist(db: Session, id: int) -> bool:  # move to masters
        is_exist = await db.execute(
            select(Master).where(
                (Master.id == id)
            )
        )

        is_exist = is_exist.first()

        return True if is_exist else False

    async def rate(master_id: UUID_ID, rate: int,  db: Session) -> MasterBase:
        master_old = await db.execute(
            select(Master).where(Master.master_id == master_id)
        )
        master_old = master_old.scalars().first()
        new_count = master_old.rate_count + 1
        new_rating = ((master_old.rating * master_old.rate_count) +
                      rate) / new_count

        master = await db.execute(
            update(Master).where(Master.id == master_old.id).values(
                rate_count=new_count,
                rating=new_rating
            ))

        await db.commit()
        master_new = await db.execute(
            select(Master).where(Master.id == master_old.id)
        )
        return master_new.scalars().first()
