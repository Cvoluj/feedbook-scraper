from sqlalchemy import Column, Integer, String, ForeignKey, Table
from database.models.base import Base


books_author = Table("books_author", 
                    Base.metadata,
                    Column('book_id', ForeignKey('books.book_id')),
                    Column('author_name', ForeignKey('authors.author_name')),
)
