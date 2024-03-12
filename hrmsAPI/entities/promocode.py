from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Promocode(Base):
    __tablename__ = 'promocodes'

    id = Column(VARCHAR(50), primary_key=True)
    discount = Column(Integer, nullable=False)
    valid_till = Column(DateTime, nullable=False)
