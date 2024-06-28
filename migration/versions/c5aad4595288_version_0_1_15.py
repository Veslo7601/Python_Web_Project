"""Version_0.1.15

Revision ID: c5aad4595288
Revises: ae38162a2259
Create Date: 2024-06-29 00:02:08.609258

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5aad4595288'
down_revision: Union[str, None] = 'ae38162a2259'
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
