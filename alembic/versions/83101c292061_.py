"""empty message

Revision ID: 83101c292061
Revises: 60e373423a5c
Create Date: 2020-12-08 16:59:46.638887

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83101c292061'
down_revision = '60e373423a5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('wallets', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('wallets', 'name')
    # ### end Alembic commands ###