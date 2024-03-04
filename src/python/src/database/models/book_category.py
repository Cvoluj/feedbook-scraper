from sqlalchemy import Column, ForeignKey, Table
from database.models.base import Base


books_category = Table("books_category", 
                    Base.metadata,
                    Column('book_id', ForeignKey('books.book_id')),
                    Column('category', ForeignKey('categories.category')),
)
