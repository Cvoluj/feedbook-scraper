"""initial migration

Revision ID: d0e94b34e3e8
Revises: 
Create Date: 2024-03-03 17:01:33.401621

"""
import sqlalchemy as sa
from alembic import op

from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd0e94b34e3e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('author_name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('author_name'),
    sa.UniqueConstraint('author_name')
    )
    op.create_table('books',
    sa.Column('book_id', sa.String(length=20), nullable=False),
    sa.Column('book_url', sa.String(length=768), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('translators', sa.JSON(), nullable=True),
    sa.Column('series', sa.String(length=255), nullable=True),
    sa.Column('series_number', sa.BIGINT(), nullable=True),
    sa.Column('series_link', sa.String(length=768), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('publication_date', sa.DateTime(), nullable=False),
    sa.Column('publisher', sa.String(length=255), nullable=True),
    sa.Column('epub_isbn', sa.String(length=20), nullable=True),
    sa.Column('paper_isbn', sa.String(length=20), nullable=True),
    sa.Column('language', sa.String(length=70), nullable=True),
    sa.Column('page_count', sa.BIGINT(), nullable=True),
    sa.Column('format_ebook', sa.String(length=255), nullable=True),
    sa.Column('ebook_size', sa.String(length=255), nullable=True),
    sa.Column('protection', sa.String(length=255), nullable=True),
    sa.Column('price', sa.String(length=10), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=True),
    sa.Column('image_link', sa.String(length=768), nullable=True),
    sa.Column('image_name', sa.String(length=255), nullable=True),
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('book_id')
    )
    op.create_index(op.f('ix_books_updated_at'), 'books', ['updated_at'], unique=False)
    op.create_table('categories',
    sa.Column('category', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('category'),
    sa.UniqueConstraint('category')
    )
    op.create_table('books_author',
    sa.Column('book_id', sa.String(length=20), nullable=True),
    sa.Column('author_name', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['author_name'], ['authors.author_name'], ),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], )
    )
    op.create_table('books_category',
    sa.Column('book_id', sa.String(length=20), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.book_id'], ),
    sa.ForeignKeyConstraint(['category'], ['categories.category'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books_category')
    op.drop_table('books_author')
    op.drop_table('categories')
    op.drop_index(op.f('ix_books_updated_at'), table_name='books')
    op.drop_table('books')
    op.drop_table('authors')
    # ### end Alembic commands ###
