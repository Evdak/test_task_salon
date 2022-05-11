from db.db import Base
from sqlalchemy import Column, Text, Integer, DateTime, String, ForeignKey, Boolean, Float, DefaultClause, text
from sqlalchemy.orm import relationship
from models import User


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(Integer, ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User')
    barber_id = Column(Integer, ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    barber = relationship('User')
    rate = Column(Integer, nullable=False)
