from database import Base
from sqlalchemy import Column, String, DateTime, Integer

class User(Base):
    __tablename__ = "Users"
    id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    token = Column(String)
    user_type = Column(String)
    age = Column(Integer)
    refresh_token = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)