from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Tables(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer)
    capacity = Column(Integer)

    orders = relationship('Orders', backref='table')
    bookings = relationship('Bookings', backref='table')
