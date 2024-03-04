import scrapy
import logging
from database.database import get_db
from database.models import Book, Author, Category, books_author, books_category
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from scrapy.exceptions import DropItem

class FeedbookDbPipeline():
    def __init__(self):
        self.engine = get_db()
        self.encountered_authors = set()
        self.encountered_categories = set()
    
    def process_item(self, item, spider):
        try:
            with self.engine.connect() as connection:
                trans = connection.begin()
                try:

                    prepared_book, authors, categories = self.prepare_item(item)
                    self.insert_categories(connection, categories)
                    self.insert_authors(connection, authors)
                    self.insert_book(connection, prepared_book)
                    trans.commit()
                    self.insert_book_categories(connection, prepared_book['book_id'], categories)
                    self.insert_book_authors(connection, prepared_book['book_id'], authors)
                    trans.commit()
                except Exception as e:
                    trans.rollback()
                    logging.error(f"Failed to add item to database: {e}")
                    raise DropItem(f"Failed to add item to database: {e}")
                
                # conn = connection.begin()
                # conn.commit()
        except Exception as e:
            logging.error(f"Failed to add item to database: {e}")
            raise DropItem(f"Failed to add item to database: {e}")
        return item
    
    @staticmethod
    def prepare_item(item):
        authors = [{'author_name': author_name} for author_name in item['authors']]
        categories = [{'category_name': category_name} for category_name in item['categories']]
        filtered_item = {k: v for k, v in item.items() if k not in ['authors', 'categories']}

        return filtered_item, authors, categories
    
    def insert_categories(self, connection, categories):
        if categories is None:
            return
        
        for category in categories:
            category_name = category['category_name']
            if category_name not in self.encountered_categories:
                try:
                    ins_category = insert(Category).values(category=category_name)
                    connection.execute(ins_category)
                    self.encountered_categories.add(category_name)
                except IntegrityError:
                    pass

    def insert_authors(self, connection, authors):
        if authors is None:
            return
        
        for author in authors:
            author_name = author['author_name']
            if author_name not in self.encountered_authors:
                try:
                    ins_author = insert(Author).values(author_name=author_name)
                    connection.execute(ins_author)
                    self.encountered_authors.add(author_name)
                except IntegrityError:
                    pass

    # def insert_list_unique(self, connection, collection, obj_key: str, table):
    #     for obj in collection:
    #         value = obj[obj_key]
    #         if value not in self.encountered_authors:
    #             try:
    #                 ins = insert(table).values(value)
    #                 connection.execute(ins)
    #                 self.encountered_authors.add(value)
    #             except IntegrityError:
    #                 pass

    def insert_book(self, connection, book):
        ins_book = insert(Book).values(**book)
        connection.execute(ins_book)

    def insert_book_categories(self, connection, book_id, categories):
        if categories:
            for category in categories:
                ins_book_category = insert(books_category).values(book_id=book_id, category=category['category_name'])
                connection.execute(ins_book_category)

    def insert_book_authors(self, connection, book_id, authors):
        if authors:
            for author in authors:
                ins_book_author = insert(books_author).values(book_id=book_id, author_name=author['author_name'])
                connection.execute(ins_book_author)