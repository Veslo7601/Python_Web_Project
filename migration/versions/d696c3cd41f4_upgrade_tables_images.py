"""UPGRADE tables Images

Revision ID: d696c3cd41f4
Revises: 840c952f33cb
Create Date: 2024-06-24 01:44:24.856205

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd696c3cd41f4'
down_revision: Union[str, None] = '840c952f33cb'
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