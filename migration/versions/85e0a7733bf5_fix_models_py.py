"""Fix models.py

Revision ID: 85e0a7733bf5
Revises: d696c3cd41f4
Create Date: 2024-06-24 01:56:47.192288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85e0a7733bf5'
down_revision: Union[str, None] = 'd696c3cd41f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###