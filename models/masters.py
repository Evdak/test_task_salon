from fastapi_users_db_sqlalchemy import GUID
from db.db import Base
from sqlalchemy import Column, Text, Integer, DateTime, String, ForeignKey, Boolean, Float, DefaultClause, text
from sqlalchemy.orm import relationship
from models import User


class Master(Base):
    __tablename__ = "masters"
    id = Column(Integer, primary_key=True, unique=True)
    master_id = Column(GUID, ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False, index=True, unique=True)
    master = relationship('User')
    rating = Column(Float, server_default=text("0.0"))
    rate_count = Column(Integer, server_default=text("0"))
