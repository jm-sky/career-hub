"""Add projects table

Revision ID: c835a82da87a
Revises: 0282962e9baa
Create Date: 2025-10-08 12:59:18.145952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c835a82da87a'
down_revision: Union[str, Sequence[str], None] = '0282962e9baa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('profile_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'STAGING', 'ARCHIVED', name='projectstatus'), nullable=False),
        sa.Column('category', sa.Enum('DEMO', 'INTERNAL', 'PRODUCTION', name='projectcategory'), nullable=False),
        sa.Column('scale', sa.Enum('SMALL', 'MEDIUM', 'LARGE', 'ENTERPRISE', name='projectscale'), nullable=False),
        sa.Column('start_date', sa.String(length=7), nullable=True),
        sa.Column('end_date', sa.String(length=7), nullable=True),
        sa.Column('client', sa.String(length=200), nullable=True),
        sa.Column('technologies', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('achievements', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('challenges', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('display_order', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ondelete='CASCADE'),
    )
    op.create_index(op.f('ix_projects_profile_id'), 'projects', ['profile_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_projects_profile_id'), table_name='projects')
    op.drop_table('projects')
    op.execute('DROP TYPE IF EXISTS projectstatus')
    op.execute('DROP TYPE IF EXISTS projectcategory')
    op.execute('DROP TYPE IF EXISTS projectscale')
