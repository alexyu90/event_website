"""empty message

Revision ID: 65251b2b7cda
Revises: 87ce53df37fd
Create Date: 2021-01-25 18:16:41.985914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65251b2b7cda'
down_revision = '87ce53df37fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'seeking_venue')
    # ### end Alembic commands ###
