from db.db import Base
from sqlalchemy import Column, Text, Integer, DateTime, String, ForeignKey, Boolean, Float, DefaultClause, text
from sqlalchemy.orm import relationship
from models import User
from fastapi_users_db_sqlalchemy.generics import GUID


class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    user_id = Column(GUID, ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User')
    master_id = Column(GUID, ForeignKey(
        "masters.master_id", ondelete='CASCADE'), nullable=False)
    master = relationship('Master')
    rate = Column(Integer, nullable=False)
