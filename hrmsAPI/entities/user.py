from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(TEXT, nullable=False)
    last_name = Column(TEXT, nullable=False)
    email = Column(TEXT, nullable=False)
    hash = Column(VARCHAR(64))
    salt = Column(VARCHAR(32))
    role = Column(ENUM('admin', 'manager', 'chef', 'staff', 'courier', 'client'), nullable=False, server_default=text("'client'"))
    verified = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
