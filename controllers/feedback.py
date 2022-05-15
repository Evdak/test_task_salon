from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from db.db import User, get_async_session
from typing import List, Optional
from repositories.users import UserRepository
from schemas.feedback import FeedbackBase, FeedbackCreate, FeedbackUpdate
from models.feedback import Feedback as FeedbackModel
from sqlalchemy.orm import Session
from repositories.feedback import FeedbackRepository
from repositories.masters import MasterRepository
from .users import current_active_user
from utils import *


router = APIRouter()


@router.get('/all', response_model=List[FeedbackBase], responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    }
})
async def get_all_feedback(
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return await FeedbackRepository.get_all(db)


@router.get('/user/{user_id}', response_model=List[FeedbackBase], responses={
    404: {
        "description": "User is not exist",
        "detail": "User is not exist"
    },
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    }
})
async def get_feedback_for_user(
        user_id: UUID_ID,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    if not await UserRepository.is_exist(id=user_id, db=db):
        raise HTTPException(status_code=404, detail="User is not exist")
    return await FeedbackRepository.get_by_user_id(db=db, user_id=user_id)


@router.get('/master/{master_id}', response_model=List[FeedbackBase], responses={
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    },
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    }
})
async def get_feedback_for_master(
        master_id: UUID_ID,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    if not await MasterRepository.is_exist_master(master_id=master_id, db=db):
        raise HTTPException(status_code=404, detail="Master is not exist")

    return await FeedbackRepository.get_by_master_id(db=db, master_id=master_id)


@router.get('/id/{id}', response_model=List[FeedbackBase], responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    },
    404: {
        "description": "Not found by id",
        "detail": "Not found by id"
    }
})
async def get_feedback_by_id(
        id: int,
        db: Session = Depends(get_async_session),
        user: User = Depends(current_active_user)):
    if user.role != 'admin':
        raise HTTPException(status_code=400, detail="Not enough permissions")
    is_exist = await FeedbackRepository.is_exist(db=db, id=id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Not found by id")

    return await FeedbackRepository.get_by_id(db=db, id=id)


@router.post('/create', response_model=FeedbackCreate, responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    },
    404: {
        "description": "Master is not exist",
        "detail": "Master is not exist"
    }
})
async def create(feedback: FeedbackCreate,
                 db: Session = Depends(get_async_session),
                 user: User = Depends(current_active_user)):

    if user.role != 'client':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await MasterRepository.is_exist_master(master_id=feedback.master_id, db=db)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Master is not exist")

    result = await FeedbackRepository.create(f=feedback, db=db, user=user)
    await MasterRepository.rate(master_id=result.master_id, rate=result.rate, db=db)
    return result


@router.put('/update', response_model=FeedbackBase, responses={
    400: {
        "description": "Not enough permissions",
        "detail": "Not enough permissions"
    },
    404: {
        "description": "Not found by id",
        "detail": "Not found by id"
    },
    400: {
        "description": "It is not your's feedback",
        "detail": "It is not your's feedback"
    }
})
async def update(feedback: FeedbackUpdate,
                 db: Session = Depends(get_async_session),
                 user: User = Depends(current_active_user)):

    if user.role != 'client':
        raise HTTPException(status_code=400, detail="Not enough permissions")

    is_exist = await FeedbackRepository.is_exist(db=db, id=feedback.id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Not found by id")

    is_by_user = await FeedbackRepository.is_by_user(db=db, id=feedback.id, user_id=user.id)
    if not is_exist:
        raise HTTPException(
            status_code=400, detail="It is not your's feedback")

    return await FeedbackRepository.update(f=feedback, db=db)


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

    is_exist = await FeedbackRepository.is_exist(db=db, id=id)
    if not is_exist:
        raise HTTPException(status_code=404, detail="Not found by id")

    return await FeedbackRepository.delete(id=id, db=db)
