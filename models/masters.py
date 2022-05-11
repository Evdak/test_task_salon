from db.db import Base
from sqlalchemy import Column, Text, Integer, DateTime, String, ForeignKey, Boolean, Float, DefaultClause, text
from sqlalchemy.orm import relationship
from models import User


class Master(Base):
    __tablename__ = "masters"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    barber_id = Column(Integer, ForeignKey(
        "user.id", ondelete='CASCADE'), nullable=False)
    barber = relationship('User')
    rating = Column(Float, server_default=text("0.0"))
    rate_count = Column(Integer, server_default=text("0"))
