"""Version_0.1.12

Revision ID: 10ba77c99fe4
Revises: 5354ef7b8b8a
Create Date: 2024-06-28 23:47:21.159328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10ba77c99fe4'
down_revision: Union[str, None] = '5354ef7b8b8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('description', sa.String(length=255), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'description')
    # ### end Alembic commands ###