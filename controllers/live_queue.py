from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
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


@router.get('/all', response_model=List[LiveQueueBase], responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    }
})
async def get_all_live_queue(
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return await LiveQueueRepository.get_all(db)


@router.get('/all/today', response_model=List[LiveQueueBase], responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    }
})
async def get_all_live_queue_for_today(
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return await LiveQueueRepository.get_all_today(db)


@router.get('/master/{master_id}', response_model=List[LiveQueueBase], responses={
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    }
})
async def get_live_queue_for_master(
        master_id: UUID_ID,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if not await MasterRepository.is_exist_master(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")
    return await LiveQueueRepository.get_by_master_id(db=db, master_id=master_id)


@router.get('/master/{master_id}/today', response_model=List[LiveQueueBase], responses={
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    }
})
async def get_live_queue_for_master_for_today(
        master_id: UUID_ID,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if not await MasterRepository.is_exist_master(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")
    return await LiveQueueRepository.get_by_master_id_today(db=db, master_id=master_id)


@router.post('/book', response_model=int, responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    },
    400: {
        "description": "Not enough time",
        "detail": "Not enough time"
    },
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    }
})
async def live_book(queue: LiveQueueCreate,
                    db: Session = Depends(get_async_session),
                    user: User = Depends(current_active_user)):

    if user.role != 'client':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await MasterRepository.is_exist_master(master_id=queue.master_id, db=db)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Master is not exist")

    is_booking_avaliable = await LiveQueueRepository.is_booking_avaliable(master_id=queue.master_id, db=db)
    if not is_booking_avaliable:
        raise HTTPException(status_code=400, detail="Not enough time")

    await LiveQueueRepository.create(q=queue, db=db, user=user)
    return await LiveQueueRepository.get_queue_number(master_id=queue.master_id, db=db)


@router.put('/call_a_client/{master_id}', response_model=QueueBase, responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    },
    400: {
        "description": "Live queue is empty",
        "detail": "Live queue is empty"
    },
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    }
})
async def call_a_client_from_live_queue(master_id: UUID_ID,
                                        db: Session = Depends(
                                            get_async_session),
                                        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await MasterRepository.is_exist_master(master_id=master_id, db=db)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Master is not exist")

    count = await LiveQueueRepository.get_queue_count(master_id=master_id, db=db)
    if count == 0:
        raise HTTPException(status_code=400, detail="Live queue is empty")

    result = await LiveQueueRepository.call_a_client(master_id=master_id, db=db)
    result = await QueueRepository.create_from_live_queue(
        q=result, user_id=result.user_id, db=db)

    return result


@router.get('/count/{master_id}', response_model=int, responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    },
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    }
})
async def get_live_queue_count(master_id: UUID_ID,
                               db: Session = Depends(get_async_session),
                               user: User = Depends(current_active_user)):

    if user.role != 'owner':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await MasterRepository.is_exist_master(master_id=master_id, db=db)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Master is not exist")

    return await LiveQueueRepository.get_queue_count(master_id=master_id, db=db)


@ router.delete('/delete/{id}', responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    },
    404: {
        "description": "Not found by id",
        "detail": "Not found by id"
    }
})
async def delete_by_id(id: int,
                       db: Session = Depends(get_async_session),
                       user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await LiveQueueRepository.is_exist(db=db, id=id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Not found by id")

    return await LiveQueueRepository.delete(id=id, db=db)


@ router.get('/statistics', response_model=str, responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    }
})
async def get_statistics(db: Session = Depends(get_async_session),
                         user: User = Depends(current_active_user)):

    if user.role != 'owner':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    result = await LiveQueueRepository.stats(db=db)
    return {'average_time': result}
