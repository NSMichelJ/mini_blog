"""empty message

Revision ID: 37bd61514e88
Revises: 853036cb509f
Create Date: 2021-12-23 18:23:06.357924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37bd61514e88'
down_revision = '853036cb509f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('confirmed', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('confirmed_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'confirmed_on')
    op.drop_column('user', 'confirmed')
    # ### end Alembic commands ###
