"""alter description from string to text

Revision ID: 17e782e83f49
Revises: e4770623839c
Create Date: 2018-10-14 18:41:15.728446

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17e782e83f49'
down_revision = 'e4770623839c'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('users', 'description',
                    existing_type=sa.String(), type_=sa.Text())


def downgrade():
    op.alter_column('users', 'size', existing_type=sa.Text(),
                    type_=sa.String())
