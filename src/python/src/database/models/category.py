from sqlalchemy import Column, String
from database.models.base import Base

class Category(Base):
    __tablename__ = 'categories'
    category = Column(String(255), primary_key=True, unique=True)
