"""initial migration

Revision ID: 161f7c41de71
Revises: 89a8cf96c355
Create Date: 2017-04-29 13:50:48.086000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '161f7c41de71'
down_revision = '89a8cf96c355'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('disabled', sa.Boolean(), nullable=True))
    op.drop_column('comments', 'disable')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('disable', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('comments', 'disabled')
    # ### end Alembic commands ###
