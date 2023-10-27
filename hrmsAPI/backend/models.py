from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    orders = relationship('Orders', backref='user')
    bookings = relationship('Bookings', backref='user')

class Tables(Base):
    __tablename__ = 'tables'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer)
    capacity = Column(Integer)

    orders = relationship('Orders', backref='table')
    bookings = relationship('Bookings', backref='table')

class Orders(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    table_id = Column(Integer, ForeignKey('Tables.id'))
    complete = Column(Boolean)

class Bookings(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    table_id = Column(Integer, ForeignKey('Tables.id'))
    persons = Column(Integer)
    date = Column(DateTime)
    comment = Column(Text)

#Артемка и дальше по накатанной делаешь все по красоте


engine = create_engine('sqlite:///mydatabase.db')  # вот тут нужен урл нашей дб

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
