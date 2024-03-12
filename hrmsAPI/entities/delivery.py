from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.mysql import ENUM, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Delivery(Base):
    __tablename__ = 'deliveries'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    restaurant_id = Column(ForeignKey('restaurants.id'), nullable=False, index=True)
    promocode_id = Column(ForeignKey('promocodes.id'), index=True)
    address = Column(TEXT, nullable=False)
    created_at = Column(DateTime, nullable=False)
    status = Column(ENUM('new', 'delivering', 'complete'), nullable=False)

    promocode = relationship('Promocode')
    restaurant = relationship('Restaurant')
    user = relationship('User')