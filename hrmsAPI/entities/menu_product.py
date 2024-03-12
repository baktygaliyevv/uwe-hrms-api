from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, text
from sqlalchemy.dialects.mysql import ENUM, TEXT, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

t_menu_products = Table(
    'menu_products', metadata,
    Column('menu_id', ForeignKey('menu.id'), nullable=False, index=True),
    Column('product_id', ForeignKey('products.id'), nullable=False, index=True)
)

