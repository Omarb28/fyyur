"""Adding created_at columns for the bonus challenge

Revision ID: b0698a08afd2
Revises: 24cac1076030
Create Date: 2020-05-08 20:52:34.061434

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0698a08afd2'
down_revision = '24cac1076030'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('Show', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('Venue', sa.Column('created_at', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'created_at')
    op.drop_column('Show', 'created_at')
    op.drop_column('Artist', 'created_at')
    # ### end Alembic commands ###
