"""set identity nullable false

Revision ID: 9b2648fa4a8a
Revises: 07c1d09cded0
Create Date: 2024-10-19 11:19:07.200012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9b2648fa4a8a'
down_revision: Union[str, None] = '07c1d09cded0'
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
