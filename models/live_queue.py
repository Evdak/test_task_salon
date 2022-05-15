from datetime import datetime
from doctest import master

from fastapi_users_db_sqlalchemy import GUID
from db.db import Base
from sqlalchemy import Column, Text, Integer, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models import User


class LiveQueue(Base):
    __tablename__ = "live_queue"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(GUID, ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User')
    master_id = Column(GUID, ForeignKey(
        "masters.id", ondelete='CASCADE'), nullable=False)
    user = relationship('Master')
    created_at = Column(DateTime, default=datetime.now())
    deleted_at = Column(DateTime, nullable=True)
