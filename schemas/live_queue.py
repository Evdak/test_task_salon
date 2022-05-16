from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from utils import UUID_ID


# Shared properties
class LiveQueueBase(BaseModel):
    id: int
    master_id: UUID_ID
    user_id: UUID_ID
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# Properties to receive on Queue creation
class LiveQueueCreate(BaseModel):
    master_id: UUID_ID
    # created_at: datetime

    class Config:
        orm_mode = True


# Properties to receive on Queue update
class LiveQueueUpdate(BaseModel):
    master_id: UUID_ID

    class Config:
        orm_mode = True


# Properties shared by models stored in DB
class LiveQueueInDBBase(LiveQueueBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class LiveQueue(LiveQueueInDBBase):
    pass


# Properties properties stored in DB
class LiveQueueInDB(LiveQueueInDBBase):
    pass
