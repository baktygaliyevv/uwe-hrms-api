from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class OrderDelivery(Base):
    __tablename__ = 'order_deliveries'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False, index=True)
    address = Column(Text(collation='utf8mb3_unicode_ci'), nullable=False)
    status = Column(ENUM('new', 'delivering', 'complete', ''), nullable=False)

    order = relationship('Order')

