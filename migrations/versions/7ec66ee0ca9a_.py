"""empty message

Revision ID: 7ec66ee0ca9a
Revises: fc395f8068cf
Create Date: 2024-08-11 16:18:53.147112

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ec66ee0ca9a'
down_revision = 'fc395f8068cf'
branch_labels = None
depends_on = None


def upgrade():
    # Add the 'hide' column to the 'artist' table
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hide', sa.Boolean(), nullable=False, server_default='0'))

def downgrade():
    # Remove the 'hide' column in case of downgrade
    with op.batch_alter_table('artist', schema=None) as batch_op:
        batch_op.drop_column('hide')

    # ### end Alembic commands ###
