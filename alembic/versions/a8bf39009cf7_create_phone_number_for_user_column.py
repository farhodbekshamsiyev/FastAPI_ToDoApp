"""create phone number for user column

Revision ID: a8bf39009cf7
Revises: 
Create Date: 2024-07-12 00:41:05.760848

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a8bf39009cf7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=12), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
