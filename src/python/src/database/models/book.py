from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, BIGINT
from sqlalchemy.orm import relationship
from database.models.mixins import MysqlTimestampsMixin
from database.models.base import Base


class Book(Base, MysqlTimestampsMixin):
    __tablename__ = 'books'
    
    book_id = Column(String(20), primary_key=True)
    book_url = Column(String(768))
    title = Column(String(255))
    translators = Column(JSON, nullable=True)
    series = Column(String(255), nullable=True)
    series_number = Column(BIGINT, nullable=True)
    series_link = Column(String(768), nullable=True) 
    description = Column(Text, nullable=True)
    publication_date = Column(DateTime, nullable=False)
    publisher = Column(String(255), nullable=True)
    epub_isbn = Column(String(20), nullable=True) 
    paper_isbn = Column(String(20), nullable=True)  
    language = Column(String(70), nullable=True)
    page_count = Column(BIGINT, nullable=True)
    format_ebook = Column(String(255), nullable=True)
    ebook_size = Column(String(255), nullable=True) 
    protection = Column(String(255), nullable=True)
    price = Column(String(10), nullable=False)
    currency = Column(String(3), nullable=True)
    image_link = Column(String(768), nullable=True)
    image_name = Column(String(255), nullable=True)
