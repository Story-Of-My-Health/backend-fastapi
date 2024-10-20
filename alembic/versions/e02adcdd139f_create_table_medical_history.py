"""create table medical history

Revision ID: e02adcdd139f
Revises: f8a27366ebfa
Create Date: 2024-10-20 19:35:44.589609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e02adcdd139f'
down_revision: Union[str, None] = 'f8a27366ebfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('medical_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('symptoms', sa.String(length=500), nullable=False),
    sa.Column('treatment', sa.String(length=500), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['patient_id'], ['identity.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medical_history')
    # ### end Alembic commands ###
