from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Table(Base):
    __tablename__ = 'tables'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(ForeignKey('restaurants.id'), nullable=False, index=True)
    capacity = Column(Integer, nullable=False)

    restaurant = relationship('Restaurant')
