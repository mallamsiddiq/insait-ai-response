"""Initial migration

Revision ID: 1366232ff0f6
Revises: 
Create Date: 2025-03-03 15:41:51.776310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '1366232ff0f6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('generated_text')
    # op.drop_table('user')
    # ### end Alembic commands ###
    ""


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('user_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    sa.Column('password', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='user_pkey'),
    sa.UniqueConstraint('username', name='user_username_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('generated_text',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('prompt', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('response', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('timestamp', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='generated_text_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='generated_text_pkey')
    )
    # ### end Alembic commands ###
