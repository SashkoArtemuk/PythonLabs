"""empty message

Revision ID: 73652dd7e4a3
Revises: 83101c292061
Create Date: 2020-12-08 17:07:30.602832

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73652dd7e4a3'
down_revision = '83101c292061'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('amount', sa.Integer(), nullable=True))
    op.drop_column('transactions', 'amoung')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('amoung', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('transactions', 'amount')
    # ### end Alembic commands ###
