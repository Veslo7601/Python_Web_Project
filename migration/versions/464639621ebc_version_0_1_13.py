"""Version_0.1.13

Revision ID: 464639621ebc
Revises: 10ba77c99fe4
Create Date: 2024-06-28 23:57:26.415418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '464639621ebc'
down_revision: Union[str, None] = '10ba77c99fe4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('comments', sa.Column('updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'updated_at')
    op.drop_column('comments', 'created_at')
    # ### end Alembic commands ###
