"""add discounts table

Revision ID: 5febce13adbf
Revises: 467c7ece2b69
Create Date: 2025-02-05 23:26:15.027608

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5febce13adbf'
down_revision: Union[str, None] = '467c7ece2b69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'discounts',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('miner_id', sa.Integer(), sa.ForeignKey('miner_items.id'), nullable=True),
        sa.Column('applies_to_electricity', sa.Boolean(), default=False),
        sa.Column('discount_percentage', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('expiration_date', sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('discounts')
