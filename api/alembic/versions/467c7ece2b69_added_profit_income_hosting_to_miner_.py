"""added profit income hosting to miner item

Revision ID: 467c7ece2b69
Revises: 5775661d755b
Create Date: 2025-01-15 23:29:03.167272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '467c7ece2b69'
down_revision: Union[str, None] = '5775661d755b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('miner_items', sa.Column('income', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('miner_items', sa.Column('profit', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('miner_items', sa.Column('hosting', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    op.drop_column('miner_items', 'income')
    op.drop_column('miner_items', 'profit')
    op.drop_column('miner_items', 'hosting')
