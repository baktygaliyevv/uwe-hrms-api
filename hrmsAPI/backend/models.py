from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///mydatabase.db')  # вот тут нужен урл нашей дб

# вот тут будут модели

Base.metadata.create_all(engine)
