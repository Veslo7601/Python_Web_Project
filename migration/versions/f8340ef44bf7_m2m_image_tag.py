"""m2m_image_tag

Revision ID: f8340ef44bf7
Revises: 2104e64f89cf
Create Date: 2024-07-01 11:03:38.371958

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f8340ef44bf7'
down_revision: Union[str, None] = '2104e64f89cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image_m2m_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_id', sa.Integer(), nullable=True),
    sa.Column('tag_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['image_id'], ['images.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('comments', 'updated_at')
    op.drop_column('comments', 'description')
    op.drop_column('comments', 'created_at')
    op.drop_constraint('tags_images_id_fkey', 'tags', type_='foreignkey')
    op.drop_column('tags', 'images_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tags', sa.Column('images_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('tags_images_id_fkey', 'tags', 'images', ['images_id'], ['id'])
    op.add_column('comments', sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.add_column('comments', sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('comments', sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    op.drop_table('image_m2m_tag')
    # ### end Alembic commands ###
