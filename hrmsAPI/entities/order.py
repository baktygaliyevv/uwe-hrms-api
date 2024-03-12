from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), index=True)
    table_id = Column(ForeignKey('tables.id'), nullable=False, index=True)
    promocode_id = Column(ForeignKey('promocodes.id'), index=True)
    created_at = Column(DateTime, nullable=False)
    complete_at = Column(DateTime)

    promocode = relationship('Promocode')
    table = relationship('Table')
    user = relationship('User')
