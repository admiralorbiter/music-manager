"""Update Artist model

Revision ID: 792997a6c3dd
Revises: f63e8edef2c2
Create Date: 2023-05-10 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector


# revision identifiers, used by Alembic.
revision = '792997a6c3dd'
down_revision = 'f63e8edef2c2'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    columns = [c['name'] for c in inspector.get_columns('artist')]

    # Add main_artist column if it doesn't exist
    if 'main_artist' not in columns:
        op.add_column('artist', sa.Column('main_artist', sa.String(length=120), nullable=True))
        
        # Update existing rows to set main_artist equal to artist_name
        op.execute('UPDATE artist SET main_artist = artist_name')
        
        # Make main_artist non-nullable
        with op.batch_alter_table('artist') as batch_op:
            batch_op.alter_column('main_artist', nullable=False)
    
    # Add genres column if it doesn't exist
    if 'genres' not in columns:
        op.add_column('artist', sa.Column('genres', sa.String(length=255), nullable=True))
    
    # Check if main_artist_id column exists in music_brainz_track
    columns = [c['name'] for c in inspector.get_columns('music_brainz_track')]
    if 'main_artist_id' not in columns:
        # Add main_artist_id column to music_brainz_track
        op.add_column('music_brainz_track', sa.Column('main_artist_id', sa.Integer(), nullable=True))
        
        # Add foreign key constraint
        with op.batch_alter_table('music_brainz_track') as batch_op:
            batch_op.create_foreign_key('fk_track_main_artist', 'artist', ['main_artist_id'], ['id'])


def downgrade():
    # Remove foreign key constraint
    with op.batch_alter_table('music_brainz_track') as batch_op:
        batch_op.drop_constraint('fk_track_main_artist', type_='foreignkey')
    
    # Remove columns
    op.drop_column('music_brainz_track', 'main_artist_id')
    op.drop_column('artist', 'genres')
    op.drop_column('artist', 'main_artist')
