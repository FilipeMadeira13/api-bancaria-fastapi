"""verificar mudanças

Revision ID: 741005f0acd1
Revises: 329a768dde2b
Create Date: 2025-07-20 04:07:49.991162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '741005f0acd1'
down_revision: Union[str, Sequence[str], None] = '329a768dde2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
