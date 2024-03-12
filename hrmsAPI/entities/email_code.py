from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.mysql import ENUM, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class EmailCode(Base):
    __tablename__ = 'email_codes'

    code = Column(String(32, 'utf8mb3_unicode_ci'), primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    expiration_date = Column(DateTime, nullable=False)

    user = relationship('User')