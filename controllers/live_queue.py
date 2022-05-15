from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.db import User, get_async_session
from typing import List, Optional
from schemas.live_queue import LiveQueueBase, LiveQueueCreate, LiveQueueUpdate
from models.live_queue import LiveQueue as LiveQueueModel
from schemas.queue import QueueBase
from sqlalchemy.orm import Session
from repositories.live_queue import LiveQueueRepository
from repositories.masters import MasterRepository
from repositories.queue import QueueRepository
from .users import current_active_user
from utils import *

router = APIRouter()


@router.get('/all', response_model=List[LiveQueueBase])
async def get_all_live_queue(
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return await LiveQueueRepository.get_all(db)


@router.get('/all/today', response_model=List[LiveQueueBase])
async def get_all_live_queue_for_today(
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return await LiveQueueRepository.get_all_today(db)


@router.get('/{master_id}', response_model=List[LiveQueueBase])
async def get_live_queue_for_master(
        master_id: UUID_ID,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if not await MasterRepository.is_exist(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")
    return await LiveQueueRepository.get_by_master_id(db=db, master_id=master_id)


@router.get('/{master_id}/today', response_model=List[LiveQueueBase])
async def get_live_queue_for_master_for_today(
        master_id: UUID_ID,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if not await MasterRepository.is_exist(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")
    return await LiveQueueRepository.get_by_master_id_today(db=db, master_id=master_id)


@router.post('/book', response_model=int)
async def live_book(queue: LiveQueueCreate,
                    db: Session = Depends(get_async_session),
                    user: User = Depends(current_active_user)):

    if user.role != 'client':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await MasterRepository.is_exist(master_id=queue.master_id, db=db)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Master is not exist")

    is_booking_avaliable = await LiveQueueRepository.is_booking_avaliable(master_id=queue.master_id, db=db)
    if not is_booking_avaliable:
        raise HTTPException(status_code=400, detail="Not enough time")

    await LiveQueueRepository.create(q=queue, db=db, user=user)
    return await LiveQueueRepository.get_queue_number(master_id=queue.master_id, db=db)


@router.put('/call_a_client/{master_id}', response_model=QueueBase)
async def call_a_client_from_live_queue(master_id: UUID_ID,
                                        db: Session = Depends(
                                            get_async_session),
                                        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await MasterRepository.is_exist(master_id=master_id, db=db)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Master is not exist")

    count = await LiveQueueRepository.get_queue_count(master_id=master_id, db=db)
    if count == 0:
        raise HTTPException(status_code=400, detail="Live queue is empty")

    result = await LiveQueueRepository.call_a_client(master_id=master_id, db=db)
    result = await QueueRepository.create_from_live_queue(
        q=result, user_id=result.user_id, db=db)

    return result


@router.get('/count/{master_id}', response_model=int)
async def get_live_queue_count(master_id: UUID_ID,
                               db: Session = Depends(get_async_session),
                               user: User = Depends(current_active_user)):

    if user.role != 'owner':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await MasterRepository.is_exist(master_id=master_id, db=db)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Master is not exist")

    return await LiveQueueRepository.get_queue_count(master_id=master_id, db=db)
