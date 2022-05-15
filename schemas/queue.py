from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime
from utils import *


# Shared properties
class QueueBase(BaseModel):
    id: int
    user_id: UUID_ID
    master_id: UUID_ID
    is_started: bool
    starts_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Properties to receive on Queue creation
class QueueCreate(BaseModel):
    master_id: UUID_ID
    starts_at: datetime

    @validator('starts_at')
    def check_date(cls, v):
        if v < datetime.now(tz=utc):
            raise ValueError("Date or time is wrong")
        if not (get_open_datetime() <= v <= get_close_datetime()):
            raise ValueError("Baebershop is not working at this time")
        return v

    class Config:
        orm_mode = True


class QueueUpdate(BaseModel):
    id: int
    is_started: bool
    started_at: datetime
    # ended_at: Optional[datetime] = None


class QueueUpdateEnd(BaseModel):
    id: int
    ended_at: datetime


# Properties shared by models stored in DB
class QueueInDBBase(BaseModel):
    id: int
    user_id: UUID_ID
    master_id: UUID_ID
    is_started: bool
    starts_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Queue(QueueInDBBase):
    pass


# Properties properties stored in DB
class QueueInDB(QueueInDBBase):
    pass
