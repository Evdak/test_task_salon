from fastapi import APIRouter, Depends
from db.db import get_async_session
from sqlalchemy.orm import Session
from config import *

router = APIRouter()


@router.get('/info')
async def get_info():
    result = {
        "name": NAME,
        "opening_time": OPEN_TIME,
        "close_time": CLOSE_TIME,
        "destination": DESTINATION,
        "phone_number": PHONE_NUMBER
    }
    return result
