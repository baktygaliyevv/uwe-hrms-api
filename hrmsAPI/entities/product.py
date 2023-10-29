from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50, 'utf8mb3_unicode_ci'), nullable=False)
    vegan = Column(TINYINT(1), nullable=False)
    vegetarian = Column(TINYINT(1), nullable=False)
    gluten_free = Column(TINYINT(1), nullable=False)
