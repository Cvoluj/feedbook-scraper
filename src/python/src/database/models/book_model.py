from sqlalchemy import Column, Integer, String, Text, DateTime, Float

from database.models.mixins import MysqlTimestampsMixin
from database.models.base import Base

class book_model(Base, MysqlTimestampsMixin):
    __tablename__ = 'books'

    id = Column(String(768), primary_key=True, unique=True, nullable=False)
    detail_page_url = Column(String(768), nullable=False)
    title = Column(String(255), nullable=False)
    authors = Column(String(255), nullable=False)
    translators = Column(String(255))
    series = Column(String(255))
    series_number = Column(Integer)
    categories = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    publication_date = Column(DateTime, nullable=False)
    publisher = Column(String(255), nullable=False)
    isbn = Column(String(255), nullable=False)
    language = Column(String(255), nullable=False)
    page_count = Column(Integer, nullable=False)
    electronic_format = Column(String(255), nullable=False)
    electronic_size = Column(String(255), nullable=False)
    protection_method = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(255), nullable=False)
    image_url = Column(String(768), nullable=False)
    image_filename = Column(String(255), nullable=False)
