from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# Shared properties
class QueueBase(BaseModel):
    barber_id: int


# Properties to receive on Queue creation
class QueueCreate(QueueBase):
    barber_id: int
    rating: float
    rate_count: int


# Properties to receive on Queue update
class QueueUpdate(QueueBase):
    rating: float
    rate_count: int


# Properties shared by models stored in DB
class QueueInDBBase(QueueBase):
    barber_id: int
    rating: float
    rate_count: int

    class Config:
        orm_mode = True


# Properties to return to client
class Queue(QueueInDBBase):
    pass


# Properties properties stored in DB
class QueueInDB(QueueInDBBase):
    pass
