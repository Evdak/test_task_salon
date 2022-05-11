from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime


# Shared properties
class FeedbackBase(BaseModel):
    user_id: int
    barber_id: int
    rate: int

    @validator('rate')
    def five_star_rating(cls, v):
        if not (1 <= v and v <= 5):
            raise ValueError('Rate 1 to 5')
        return v


# Properties to receive on Feedback creation
class FeedbackCreate(FeedbackBase):
    user_id: int
    barber_id: int
    rate: int


# Properties to receive on Feedback update
class FeedbackUpdate(FeedbackBase):
    rate: int


# Properties shared by models stored in DB
class FeedbackInDBBase(FeedbackBase):
    user_id: int
    barber_id: int
    rate: int

    class Config:
        orm_mode = True


# Properties to return to client
class Feedback(FeedbackInDBBase):
    pass


# Properties properties stored in DB
class FeedbackInDB(FeedbackInDBBase):
    pass
