from typing import List, Optional
from datetime import datetime
from db.db import User
from models.queue import Queue as QueueModel
from schemas.live_queue import LiveQueueBase
from schemas.queue import QueueBase, QueueCreate, QueueUpdate, QueueUpdateEnd
from models.queue import Queue
from sqlalchemy import extract, select, update
from sqlalchemy.orm import Session
from utils import *


class QueueRepository():
    async def create(q: QueueCreate, db: Session, user: User) -> QueueCreate:
        queue = Queue(**q.dict())
        queue.user_id = user.id
        queue.is_started = False
        queue.ended_at = None
        queue.started_at = None
        db.add(queue)
        await db.commit()
        db.refresh(queue)
        return queue

    async def create_from_live_queue(q: LiveQueueBase, db: Session, user_id: UUID_ID) -> QueueCreate:
        queue = Queue()
        queue.master_id = q.master_id
        queue.user_id = user_id
        queue.starts_at = q.deleted_at
        queue.is_started = False
        queue.ended_at = None
        queue.started_at = None
        db.add(queue)
        await db.commit()
        db.refresh(queue)
        return queue

    async def mark_as_started(db: Session, q: QueueUpdate) -> QueueBase:
        queue_old = await db.execute(
            select(Queue).where(Queue.id == q.id)
        )
        queue_old = queue_old.scalars().first()
        queue = await db.execute(
            update(Queue).where(Queue.id == queue_old.id).values(
                is_started=q.is_started,
                started_at=q.started_at,
            ))

        await db.commit()
        queue_new = await db.execute(
            select(Queue).where(Queue.id == queue_old.id)
        )
        return queue_new.scalars().first()

    async def mark_as_ended(db: Session, q: QueueUpdateEnd) -> QueueBase:
        queue_old = await db.execute(
            select(Queue).where(Queue.id == q.id)
        )
        queue_old = queue_old.scalars().first()
        queue = await db.execute(
            update(Queue).where(Queue.id == queue_old.id).values(
                ended_at=q.ended_at
            ))

        await db.commit()
        queue_new = await db.execute(
            select(Queue).where(Queue.id == queue_old.id)
        )
        return queue_new.scalars().first()

    async def get_all(db: Session) -> List[QueueBase]:
        result = await db.execute(select(Queue))
        return list(result.scalars())

    async def get_all_today(db: Session) -> List[QueueBase]:
        result = await db.execute(select(Queue).where(
            extract('month', Queue.starts_at) >= datetime.today().month,
            extract('year', Queue.starts_at) >= datetime.today().year,
            extract('day', Queue.starts_at) >= datetime.today().day
        ))
        return list(result.scalars())

    # async def get_master(master_id: UUID_ID, db: Session, user: User) -> List[QueueBase]:
    #     if user.role != 'client':
    #         return None
    #     result = await db.execute(select(Queue).where(Queue.master_id == master_id))
    #     return list(result.scalars())

    async def delete(db: Session, id: int):
        queue = await db.execute(select(Queue).where(Queue.id == id))
        queue = queue.scalars().first()
        await db.delete(queue)
        await db.commit()
        return f'Deleted id: {id}'

    async def get_by_master_id(db: Session, master_id: int) -> List[QueueBase]:
        result = await db.execute(select(Queue).where(Queue.master_id == master_id))
        return list(result.scalars())

    async def get_by_master_id_today(db: Session, master_id: int) -> List[QueueBase]:
        result = await db.execute(select(Queue).where(
            Queue.master_id == master_id,
            extract('month', Queue.starts_at) >= datetime.today().month,
            extract('year', Queue.starts_at) >= datetime.today().year,
            extract('day', Queue.starts_at) >= datetime.today().day
        ))
        return list(result.scalars())

    async def is_exist(db: Session, id: int) -> bool:  # move to masters
        is_exist = await db.execute(
            select(Queue).where(
                (Queue.id == id)
            )
        )
        is_exist = is_exist.first()

        return True if is_exist else False

    async def is_free(db: Session, master_id: int, time: datetime) -> bool:
        result = await db.execute(
            select(Queue).where(
                (Queue.master_id == master_id) &
                (Queue.starts_at > check_timedelta_before(time=time)) &
                (Queue.starts_at < check_timedelta_after(time=time))
            )
        )
        result = result.first()
        print(f'{result=}')
        return False if result else True
