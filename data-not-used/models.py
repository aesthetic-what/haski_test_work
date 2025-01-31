from sqlalchemy import Column, String, Integer, Boolean
from data.database import Base


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    white_list = Column(Boolean, default=False)
    token = Column(String)