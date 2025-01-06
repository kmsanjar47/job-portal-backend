"""migrations

Revision ID: a5c189739676
Revises: fb1c9f1584ba
Create Date: 2025-01-06 21:54:24.361014

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a5c189739676'
down_revision: Union[str, None] = 'fb1c9f1584ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_profile', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user_profile', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user_profile', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('user_profile', 'graduation_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('user_profile', 'department',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user_profile', 'department',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user_profile', 'graduation_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('user_profile', 'phone_number',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user_profile', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('user_profile', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###
