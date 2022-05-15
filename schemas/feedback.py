from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime
from utils import UUID_ID


# Shared properties
class FeedbackBase(BaseModel):
    user_id: UUID_ID
    master_id: UUID_ID
    rate: int
    text: Optional[str] = None

    @validator('rate')
    def five_star_rating(cls, v):
        if not (1 <= v and v <= 5):
            raise ValueError('Rate 1 to 5')
        return v

    class Config:
        orm_mode = True


# Properties to receive on Feedback creation
class FeedbackCreate(BaseModel):
    master_id: UUID_ID
    rate: int
    text: Optional[str] = None

    @validator('rate')
    def five_star_rating(cls, v):
        if not (1 <= v and v <= 5):
            raise ValueError('Rate 1 to 5')
        return v

    class Config:
        orm_mode = True


# Properties to receive on Feedback update
class FeedbackUpdate(BaseModel):
    id: int
    rate: int
    text: Optional[str] = None

    @validator('rate')
    def five_star_rating(cls, v):
        if not (1 <= v and v <= 5):
            raise ValueError('Rate 1 to 5')
        return v

    class Config:
        orm_mode = True


# Properties shared by models stored in DB
class FeedbackInDBBase(FeedbackBase):
    user_id: UUID_ID
    master_id: UUID_ID
    rate: int
    text: Optional[str] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Feedback(FeedbackInDBBase):
    pass


# Properties properties stored in DB
class FeedbackInDB(FeedbackInDBBase):
    pass
