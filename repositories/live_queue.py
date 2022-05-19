from typing import Any, List, Optional
from datetime import datetime
from db.db import User
from models import queue
from schemas.live_queue import LiveQueueBase, LiveQueueCreate, LiveQueueUpdate, LiveQueueInDBBase
from models.live_queue import LiveQueue
from repositories.queue import QueueRepository
from sqlalchemy import extract, select, update
from sqlalchemy.orm import Session
from utils import *


class LiveQueueRepository():
    async def create(q: LiveQueueCreate, db: Session, user: User) -> LiveQueueBase:
        queue = LiveQueue(**q.dict())
        queue.user_id = user.id
        db.add(queue)
        await db.commit()
        await db.refresh(queue)
        return queue

    async def update(master_id: UUID_ID, db: Session, q: LiveQueueUpdate) -> LiveQueue:
        # if user.role != 'admin':
        #     return None  # access denied
        queue = await db.execute(
            update(LiveQueue).where(LiveQueue.master_id == q.master_id).values(
                deleted_at=datetime.now(tz=utc))
        )
        queue = queue.scalars()
        print(f'UPDATED {queue=}')
        await db.commit()
        await db.refresh(queue)
        return queue

    async def get_all(db: Session) -> List[LiveQueueBase]:
        result = await db.execute(select(LiveQueue))
        return list(result.scalars())

    async def get_all_today(db: Session) -> List[LiveQueueBase]:
        result = await db.execute(select(LiveQueue).where(
            extract('month', LiveQueue.created_at) >= datetime.today().month,
            extract('year', LiveQueue.created_at) >= datetime.today().year,
            extract('day', LiveQueue.created_at) >= datetime.today().day
        ))
        return list(result.scalars())

    async def get_by_master_id(master_id: UUID_ID, db: Session) -> List[LiveQueueBase]:
        # if user.role != 'client':
        #     return None
        result = await db.execute(select(LiveQueue).where(LiveQueue.master_id == master_id))
        return list(result.scalars())

    async def get_by_master_id_today(master_id: UUID_ID, db: Session) -> List[LiveQueueBase]:
        # if user.role != 'client':
        #     return None
        result = await db.execute(select(LiveQueue).where(
            LiveQueue.master_id == master_id,
            extract('month', LiveQueue.created_at) >= datetime.today().month,
            extract('year', LiveQueue.created_at) >= datetime.today().year,
            extract('day', LiveQueue.created_at) >= datetime.today().day
        ))
        return list(result.scalars())

    async def get_queue_count(master_id: UUID_ID, db: Session) -> int:
        result = await db.execute(select(LiveQueue).where(
            (LiveQueue.master_id == master_id) &
            (LiveQueue.deleted_at == None)
        ))

        return len(list(result.scalars()))

    async def get_queue_number(master_id: UUID_ID, db: Session) -> int:
        result = await db.execute(select(LiveQueue).where(
            (LiveQueue.master_id == master_id) &
            (LiveQueue.deleted_at == None)
        ))

        return len(list(result.scalars())) - 1

    async def is_booking_avaliable(master_id: UUID_ID, db: Session) -> bool:
        master_queue = await QueueRepository.get_by_master_id_today(master_id=master_id, db=db)
        master_queue = [el for el in master_queue if el.starts_at >
                        check_timedelta_before(time=datetime.now())]

        master_live_queue_count = await LiveQueueRepository.get_queue_count(master_id=master_id, db=db)

        if (len(master_queue) + master_live_queue_count) < get_live_queue_max_count():
            return True
        else:
            return False

    async def call_a_client(master_id: UUID_ID, db: Session) -> LiveQueueBase:
        queue_old = await db.execute(
            select(LiveQueue).where(
                LiveQueue.master_id == master_id,
                LiveQueue.deleted_at == None
            ))
        queue_old = queue_old.scalars().first()
        queue = await db.execute(
            update(LiveQueue).where(LiveQueue.id == queue_old.id).values(
                deleted_at=datetime.now())
        )

        await db.commit()
        queue_new = await db.execute(
            select(LiveQueue).where(LiveQueue.id == queue_old.id)
        )
        return queue_new.scalars().first()

    async def delete(db: Session, id: int):

        queue = await db.execute(select(LiveQueue).where(LiveQueue.id == id))
        queue = queue.scalars().first()
        await db.delete(queue)
        await db.commit()
        return f'Deleted id: {id}'

        # async def get_by_master_id(db: Session, master_id: int, user: User) -> List[QueueBase]:
        #     result = await db.execute(select(Queue).where(Queue.master_id == master_id))
        #     return list(result.scalars())

        # async def get_by_master_id_today(db: Session, master_id: int, user: User) -> List[QueueBase]:
        #     result = await db.execute(select(Queue).where(
        #         Queue.master_id == master_id,
        #         extract('month', Queue.starts_at) >= datetime.today().month,
        #         extract('year', Queue.starts_at) >= datetime.today().year,
        #         extract('day', Queue.starts_at) >= datetime.today().day
        #     ))
        #     return list(result.scalars())

    async def is_exist(db: Session, id: int) -> bool:  # move to masters
        is_exist = await db.execute(
            select(LiveQueue).where(
                (LiveQueue.id == id)
            )
        )
        is_exist = is_exist.first()

        return True if is_exist else False

        # async def is_free(db: Session, master_id: int, time: datetime) -> bool:
        #     result = await db.execute(
        #         select(Queue).where(
        #             (Queue.master_id == master_id) &
        #             (Queue.starts_at > check_timedelta_before(time=time)) &
        #             (Queue.starts_at < check_timedelta_after(time=time))
        #         )
        #     )
        #     result = result.first()
        #     print(f'{result=}')
        #     return False if result else True

    async def stats(db: Session) -> Any:  # move to masters
        queue = await db.execute(
            select(LiveQueue)
        )

        queue = list(queue.scalars())
        print(f"{queue=}")
        times = []

        for el in queue:
            if el.deleted_at is not None:
                times.append(int((el.deleted_at - el.created_at).seconds)//60)
        print(f"{times=}")
        return sum(times) / len(times)
