from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class MenuProduct(Base):
    __tablename__ = 'menu_products'

    id = Column(Integer, primary_key=True)
    menu_id = Column(ForeignKey('menu.id'), nullable=False, index=True)
    product_id = Column(ForeignKey('products.id'), nullable=False, index=True)

    menu = relationship('Menu')
    product = relationship('Product')

