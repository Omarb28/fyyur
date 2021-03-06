"""Created Show Model

Revision ID: 09fcfec03460
Revises: 6302864b4376
Create Date: 2020-05-02 09:49:42.761212

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09fcfec03460'
down_revision = '6302864b4376'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Show')
    # ### end Alembic commands ###
