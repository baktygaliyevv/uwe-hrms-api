from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Order(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    table_id = Column(Integer)
    complete = Column(Boolean)

engine = create_engine('sqlite:///mydatabase.db')  # вот тут нужен урл нашей дб

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
