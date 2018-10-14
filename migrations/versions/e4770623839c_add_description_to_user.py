"""add description to user

Revision ID: e4770623839c
Revises: ba917f81dd73
Create Date: 2018-10-14 18:09:47.453817

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4770623839c'
down_revision = 'ba917f81dd73'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'description')
    # ### end Alembic commands ###