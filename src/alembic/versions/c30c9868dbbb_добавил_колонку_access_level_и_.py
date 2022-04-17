"""Добавил колонку access_level и дефолтное значение колонке access_level таблице apikeys

Revision ID: c30c9868dbbb
Revises: b6df821a4d85
Create Date: 2022-04-16 21:47:42.118575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c30c9868dbbb'
down_revision = 'b6df821a4d85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apikeys', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('apikeys', 'name')
    # ### end Alembic commands ###
