from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bookings
import orders
import tables
import users

Base = declarative_base()

#Артемка и дальше по накатанной делаешь все по красоте


engine = create_engine('sqlite:///mydatabase.db')  # вот тут нужен урл нашей дб

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
