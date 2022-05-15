from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.db import User, get_async_session
from typing import List, Optional
from schemas.masters import MasterBase, MasterCreate
from models.masters import Master as MasterModel
from sqlalchemy.orm import Session
from repositories.queue import QueueRepository
from repositories.masters import MasterRepository
from .users import current_active_user
from utils import *


router = APIRouter()


@router.get('/all', response_model=List[MasterBase])
async def get_all_masters(
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'owner':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return await MasterRepository.get_all(db)


# @router.get('/get_queue_for_master', response_model=List[QueueBase])
# async def get_queue_for_master(
#         master_id: UUID_ID,
#         db: Session = Depends(get_async_session),
#         user: User = Depends(current_active_user)):
#     if not await MasterRepository.is_exist_master(master_id=master_id, db=db):
#         raise HTTPException(status_code=404, detail="Master is not exist")
#     return await QueueRepository.get_master(db=db, user=user, master_id=master_id)


@router.post('/register_as_master', response_model=MasterBase, responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    },
    400: {
        "description": "Master is already exist",
        "detail": "Master is already exist"
    }
})
async def register_as_master(db: Session = Depends(get_async_session),
                             user: User = Depends(current_active_user)):

    if user.role != 'master':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if await MasterRepository.is_exist_master(master_id=user.id, db=db):
        raise HTTPException(status_code=400, detail="Master is already exist")

    return await MasterRepository.create(db=db, user=user)


@router.get('/is_free/{master_id}', response_model=bool, responses={
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    }
})
async def is_free(master_id: UUID_ID,
                  db: Session = Depends(get_async_session)):
    if not await MasterRepository.is_exist_master(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")
    return await QueueRepository.is_free(master_id=master_id, time=datetime.now(tz=utc), db=db)


@router.get('/{master_id}', response_model=MasterBase, responses={
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    }
})
async def get_master_by_id(master_id: UUID_ID,
                           db: Session = Depends(get_async_session),
                           user: User = Depends(current_active_user)):
    if not await MasterRepository.is_exist_master(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")
    return await MasterRepository.get_master(master_id=master_id, db=db)


@router.delete('/{id}', responses={
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

    is_exist = await MasterRepository.is_exist(db=db, id=id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Not found by id")

    return await MasterRepository.delete(id=id, db=db)
