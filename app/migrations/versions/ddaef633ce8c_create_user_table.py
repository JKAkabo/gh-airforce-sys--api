"""Create user table

Revision ID: ddaef633ce8c
Revises: 
Create Date: 2021-04-28 16:42:12.851693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ddaef633ce8c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('rank', sa.String(), nullable=True))
    op.add_column('users', sa.Column('wing', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'wing')
    op.drop_column('users', 'rank')
    # ### end Alembic commands ###
