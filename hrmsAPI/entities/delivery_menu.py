from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.mysql import ENUM, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DeliveryMenu(Base):
    __tablename__ = 'delivery_menu'

    id = Column(Integer, primary_key=True)
    delivery_id = Column(ForeignKey('deliveries.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    menu_id = Column(ForeignKey('menu.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)

    delivery = relationship('Delivery')
    menu = relationship('Menu')
