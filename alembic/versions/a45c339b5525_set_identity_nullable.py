"""set identity nullable

Revision ID: a45c339b5525
Revises: 9b2648fa4a8a
Create Date: 2024-10-19 11:20:53.000896

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a45c339b5525'
down_revision: Union[str, None] = '9b2648fa4a8a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'identity_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'identity_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
