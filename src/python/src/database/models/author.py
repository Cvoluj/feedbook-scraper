from sqlalchemy import Column, String
from database.models.base import Base

class Author(Base):
    __tablename__ = 'authors'

    author_name = Column(String(255), primary_key=True, unique=True)