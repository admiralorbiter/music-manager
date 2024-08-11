"""Automated migration: Adding 'order' column to Artist model

Revision ID: fc395f8068cf
Revises: fd38be486d2e
Create Date: 2024-08-11 15:38:04.791433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc395f8068cf'
down_revision = 'fd38be486d2e'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('artist') as batch_op:
        batch_op.add_column(sa.Column('order', sa.Integer(), nullable=False, server_default='0'))

    # Set the 'order' column to be the same as the ID for existing records
    op.execute("UPDATE artist SET \"order\" = id")

    # Remove the server default if you don't want new records to have a default value automatically
    with op.batch_alter_table('artist') as batch_op:
        batch_op.alter_column('order', server_default=None)


def downgrade():
    with op.batch_alter_table('artist') as batch_op:
        batch_op.drop_column('order')
