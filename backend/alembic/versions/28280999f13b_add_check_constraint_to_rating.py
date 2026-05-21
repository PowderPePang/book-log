"""add check constraint to rating

Revision ID: 28280999f13b
Revises: ccc1627c6b8e
Create Date: 2026-05-21 23:10:25.385754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28280999f13b'
down_revision: Union[str, Sequence[str], None] = 'ccc1627c6b8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Tell PostgreSQL to add the check constraint to the books table
    op.create_check_constraint(
        'check_rating_1_to_5',      # The name of the constraint
        'books',                    # The table it belongs to
        'rating >= 1 AND rating <= 5' # The actual SQL rule
    )

def downgrade() -> None:
    # If we ever need to undo this, tell PostgreSQL to drop the constraint
    op.drop_constraint('check_rating_1_to_5', 'books', type_='check')
