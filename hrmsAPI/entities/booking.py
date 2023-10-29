from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text
from sqlalchemy.dialects.mysql import ENUM, TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False, index=True)
    table_id = Column(ForeignKey('tables.id'), nullable=False, index=True)
    persons = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False)
    comment = Column(Text(collation='utf8mb3_unicode_ci'), nullable=False)

    table = relationship('Table')
    user = relationship('User')

