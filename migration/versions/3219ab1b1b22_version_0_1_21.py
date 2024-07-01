"""Version_0.1.21

Revision ID: 3219ab1b1b22
Revises: 84cafad57a32
Create Date: 2024-07-02 00:02:52.359963

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3219ab1b1b22'
down_revision: Union[str, None] = '84cafad57a32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('description', sa.String(length=255), nullable=False))
    op.add_column('comments', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('comments', sa.Column('updated_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'updated_at')
    op.drop_column('comments', 'created_at')
    op.drop_column('comments', 'description')
    # ### end Alembic commands ###
