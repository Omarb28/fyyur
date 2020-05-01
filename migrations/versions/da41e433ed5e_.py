"""Created Genre Model

Revision ID: da41e433ed5e
Revises: f9ec8245f7ca
Create Date: 2020-05-01 13:34:33.064097

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da41e433ed5e'
down_revision = 'f9ec8245f7ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Genre',
    sa.Column('genre', sa.String(length=120), nullable=False),
    sa.PrimaryKeyConstraint('genre')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Genre')
    # ### end Alembic commands ###