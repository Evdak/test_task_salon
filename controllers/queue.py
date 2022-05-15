from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.db import User, get_async_session
from typing import List, Optional
from schemas.queue import QueueBase, QueueCreate, QueueInDBBase, QueueUpdate, QueueUpdateEnd
from models.queue import Queue as QueueModel
from sqlalchemy.orm import Session
from repositories.queue import QueueRepository
from repositories.masters import MasterRepository
from .users import current_active_user
from utils import *


router = APIRouter()


@router.get('/all', response_model=List[QueueBase])
async def get_all_queue(
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return await QueueRepository.get_all(db)


@router.get('/all/today', response_model=List[QueueBase])
async def get_all_queue_for_today(
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return await QueueRepository.get_all_today(db)


@router.get('/{master_id}', response_model=List[QueueInDBBase])
async def get_queue_for_master(
        master_id: UUID_ID,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if not await MasterRepository.is_exist_master(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")
    return await QueueRepository.get_by_master_id(db=db, master_id=master_id)


@router.get('/{master_id}/today', response_model=List[QueueInDBBase])
async def get_queue_for_master_for_today(
        master_id: UUID_ID,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if not await MasterRepository.is_exist_master(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")
    return await QueueRepository.get_by_master_id_today(db=db, master_id=master_id)


@router.post('/book', response_model=QueueCreate)
async def book(queue: QueueCreate,
               db: Session = Depends(get_async_session),
               user: User = Depends(current_active_user)):

    if user.role != 'client':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await MasterRepository.is_exist_master(master_id=queue.master_id, db=db)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Master is not exist")

    is_free = await QueueRepository.is_free(master_id=queue.master_id, time=queue.starts_at, db=db)
    if not is_free:
        raise HTTPException(status_code=400, detail="Master is busy")

    return await QueueRepository.create(q=queue, db=db, user=user)


@router.put('/mark_as_started', response_model=QueueBase)
async def mark_as_started(queue: QueueUpdate,
                          db: Session = Depends(get_async_session),
                          user: User = Depends(current_active_user)):

    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await QueueRepository.is_exist(db=db, id=queue.id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Not found by id")

    return await QueueRepository.mark_as_started(q=queue, db=db)


@router.put('/mark_as_ended', response_model=QueueBase)
async def mark_as_ended(queue: QueueUpdateEnd,
                        db: Session = Depends(get_async_session),
                        user: User = Depends(current_active_user)):

    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await QueueRepository.is_exist(db=db, id=queue.id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Not found by id")

    return await QueueRepository.mark_as_ended(q=queue, db=db)


@router.delete('/{id}')
async def delete_by_id(id: int,
                       db: Session = Depends(get_async_session),
                       user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await QueueRepository.is_exist(db=db, id=id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Not found by id")

    return await QueueRepository.delete(id=id, db=db)
