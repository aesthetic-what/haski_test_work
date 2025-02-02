"""empty message

Revision ID: dfbf8b2a0b63
Revises: 69bfd19c80f7
Create Date: 2025-01-29 22:12:21.110832

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dfbf8b2a0b63'
down_revision: Union[str, None] = '69bfd19c80f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'token')
    # ### end Alembic commands ###
