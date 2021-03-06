"""empty message

Revision ID: d51568212029
Revises: 1f8b25fdc8ce
Create Date: 2021-01-26 12:16:28.831766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd51568212029'
down_revision = '1f8b25fdc8ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'Artist', ['name'])
    op.create_unique_constraint(None, 'Venue', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue', type_='unique')
    op.drop_constraint(None, 'Artist', type_='unique')
    # ### end Alembic commands ###
