"""initial migration

Revision ID: f8c4ce01c4a0
Revises: 
Create Date: 2024-02-27 20:16:45.384796

"""
import sqlalchemy as sa
from alembic import op

from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f8c4ce01c4a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('created_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', mysql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('id', sa.String(length=768), nullable=False),
    sa.Column('detail_page_url', sa.String(length=768), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('authors', sa.String(length=255), nullable=False),
    sa.Column('translators', sa.String(length=255), nullable=True),
    sa.Column('series', sa.String(length=255), nullable=True),
    sa.Column('series_number', sa.Integer(), nullable=True),
    sa.Column('categories', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('publication_date', sa.DateTime(), nullable=True),
    sa.Column('publisher', sa.String(length=255), nullable=True),
    sa.Column('isbn', sa.String(length=255), nullable=True),
    sa.Column('language', sa.String(length=255), nullable=True),
    sa.Column('page_count', sa.Integer(), nullable=True),
    sa.Column('electronic_format', sa.String(length=255), nullable=True),
    sa.Column('electronic_size', sa.String(length=255), nullable=True),
    sa.Column('protection_method', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('currency', sa.String(length=255), nullable=True),
    sa.Column('image_url', sa.String(length=768), nullable=True),
    sa.Column('image_filename', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_books_updated_at'), 'books', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_books_updated_at'), table_name='books')
    op.drop_table('books')
    # ### end Alembic commands ###
