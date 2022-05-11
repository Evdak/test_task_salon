from db.db import Base
from sqlalchemy import Column, Text, Integer, DateTime, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models import User


class Queue(Base):
    __tablename__ = "e_queue"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    barber_id = Column(Integer, ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    barber = relationship('User')
    is_started = Column(Boolean, nullable=False)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
