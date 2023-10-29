from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class RestaurantProduct(Base):
    __tablename__ = 'restaurant_products'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(ForeignKey('restaurants.id'), nullable=False, index=True)
    product_id = Column(ForeignKey('products.id'), nullable=False, index=True)
    count = Column(Integer, nullable=False)

    product = relationship('Product')
    restaurant = relationship('Restaurant')

