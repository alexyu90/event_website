"""empty message

Revision ID: 902d58f8f644
Revises: 65251b2b7cda
Create Date: 2021-01-25 18:26:46.224180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '902d58f8f644'
down_revision = '65251b2b7cda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_talent')
    # ### end Alembic commands ###
