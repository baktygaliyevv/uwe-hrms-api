from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class UserToken(Base):
    __tablename__ = 'user_tokens'

    token = Column(String(64), primary_key=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey('users.id')) 
    expiration_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="tokens")
