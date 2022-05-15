from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from utils import UUID_ID


# Shared properties
class MasterBase(BaseModel):
    master_id: UUID_ID
    rating: float
    rate_count: int

    class Config:
        orm_mode = True

# Properties to receive on Master creation


class MasterCreate(BaseModel):
    master_id: UUID_ID


# Properties to receive on Master update
class MasterUpdate(BaseModel):
    rating: float
    rate_count: int


# Properties shared by models stored in DB
class MasterInDBBase(MasterBase):
    master_id: UUID_ID
    rating: float
    rate_count: int

    class Config:
        orm_mode = True


# Properties to return to client
class Master(MasterInDBBase):
    pass


# Properties properties stored in DB
class MasterInDB(MasterInDBBase):
    pass
