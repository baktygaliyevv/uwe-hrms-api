from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True)
    menu_category_id = Column(ForeignKey('menu_categories.id'), nullable=False, index=True)
    name = Column(TEXT, nullable=False)
    price = Column(Integer, nullable=False)

    menu_category = relationship('MenuCategory')
    products = relationship('Product', secondary='menu_products')
