"""add rate_limit_entries table for persistent DB-backed rate limiting

Revision ID: a1b2c3d4e5f6
Revises: 089938b20d55
Create Date: 2026-11-26 02:35:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '089938b20d55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'rate_limit_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('client_key', sa.String(length=128), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_rate_limit_entries_id'), 'rate_limit_entries', ['id'], unique=False)
    op.create_index(op.f('ix_rate_limit_entries_client_key'), 'rate_limit_entries', ['client_key'], unique=False)
    op.create_index(op.f('ix_rate_limit_entries_created_at'), 'rate_limit_entries', ['created_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_rate_limit_entries_created_at'), table_name='rate_limit_entries')
    op.drop_index(op.f('ix_rate_limit_entries_client_key'), table_name='rate_limit_entries')
    op.drop_index(op.f('ix_rate_limit_entries_id'), table_name='rate_limit_entries')
    op.drop_table('rate_limit_entries')
