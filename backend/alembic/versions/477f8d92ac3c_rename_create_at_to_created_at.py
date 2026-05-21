"""rename create_at to created_at

Revision ID: 477f8d92ac3c
Revises: f27cbd892d2d
Create Date: 2026-05-22 01:00:21.260441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '477f8d92ac3c'
down_revision: Union[str, Sequence[str], None] = 'f27cbd892d2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Safely rename the column in the users table
    op.alter_column('users', 'create_at', new_column_name='created_at')
    
    # Safely rename the column in the books table
    op.alter_column('books', 'create_at', new_column_name='created_at')

def downgrade() -> None:
    # Reverse the process if we ever need to rollback
    op.alter_column('users', 'created_at', new_column_name='create_at')
    op.alter_column('books', 'created_at', new_column_name='create_at')
