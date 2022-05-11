from typing import Optional
from pydantic import BaseModel
from datetime import datetime


# Shared properties
class MasterBase(BaseModel):
    barber_id: int
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


# Properties to receive on Master creation
class MasterCreate(MasterBase):
    pass


# Properties to receive on Master update
class MasterUpdate(MasterBase):
    is_started: bool
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None


# Properties shared by models stored in DB
class MasterInDBBase(MasterBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Master(MasterInDBBase):
    pass


# Properties properties stored in DB
class MasterInDB(MasterInDBBase):
    pass
