"""empty message

Revision ID: a3b0dffdf29a
Revises: 
Create Date: 2020-12-08 15:02:12.910515

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3b0dffdf29a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('login', sa.String(), nullable=True),
    sa.Column('psw', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('wallets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('currency', sa.String(), nullable=True),
    sa.Column('ballance', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('transactions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_wallet_id', sa.Integer(), nullable=True),
    sa.Column('recevier_wallet_id', sa.Integer(), nullable=True),
    sa.Column('amoung', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['recevier_wallet_id'], ['wallets.id'], ),
    sa.ForeignKeyConstraint(['sender_wallet_id'], ['wallets.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transactions')
    op.drop_table('wallets')
    op.drop_table('users')
    # ### end Alembic commands ###