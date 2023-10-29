from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100, 'utf8mb3_unicode_ci'), nullable=False)
    phone = Column(VARCHAR(10), nullable=False)
    hash = Column(String(40, 'utf8mb3_unicode_ci'))
    salt = Column(String(32, 'utf8mb3_unicode_ci'))
    role = Column(ENUM('admin', 'manager', 'chef', 'staff', 'courier', 'client'), nullable=False, server_default=text("'client'"))
