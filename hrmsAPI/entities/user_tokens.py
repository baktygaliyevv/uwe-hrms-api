from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.mysql import ENUM, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserToken(Base):
    __tablename__ = 'user_tokens'

    token = Column(VARCHAR(64), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    expiration_date = Column(DateTime, nullable=False)

    user = relationship('User')
