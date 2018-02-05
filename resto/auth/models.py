import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    username = Column(String(80),nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(100))
    password = Column(String(124),nullable=False)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)