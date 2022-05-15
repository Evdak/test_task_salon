from fastapi_users_db_sqlalchemy import GUID
from db.db import Base
from sqlalchemy import Column, Text, Integer, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models import User


class Queue(Base):
    __tablename__ = "e_queue"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(GUID, ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    # user = relationship('User')
    master_id = Column(GUID, ForeignKey(
        "masters.master_id", ondelete='CASCADE'), nullable=False)
    # master = relationship('Master')
    is_started = Column(Boolean, nullable=False)
    starts_at = Column(DateTime, nullable=True)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
