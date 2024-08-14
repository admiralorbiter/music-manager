from app import db

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(120), nullable=False)
    need_to_explore = db.Column(db.Boolean, nullable=False)
    looked_at = db.Column(db.Boolean, nullable=False)
    artist_playlist = db.Column(db.Boolean, nullable=False)
    one_of_each = db.Column(db.String(120), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, nullable=False, default=0)
    hide = db.Column(db.Boolean, nullable=False, default=False)
    musicbrainz_id = db.Column(db.String(36), nullable=True)
    musicbrainz_data = db.relationship('MusicBrainzAlbum', backref='artist', lazy=True)

    def __repr__(self):
        return f'<Artist {self.artist_name}>'

class MusicBrainzAlbum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    album_name = db.Column(db.String(255), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    tracks = db.relationship('MusicBrainzTrack', backref='album', lazy=True)

    def __repr__(self):
        return f'<MusicBrainzAlbum {self.album_name}>'


class MusicBrainzTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(255), nullable=False)
    track_order = db.Column(db.Integer, nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('music_brainz_album.id'), nullable=False)
    playlists = db.relationship('PlaylistTracks', back_populates='track')

    def __repr__(self):
        return f'<MusicBrainzTrack {self.track_name} - Order {self.track_order}>'

class TidalTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(255))
    artist_name = db.Column(db.String(255))
    album_name = db.Column(db.String(255))
    playlist_name = db.Column(db.String(255))
    type = db.Column(db.String(50))
    isrc = db.Column(db.String(20))
    tidal_id = db.Column(db.String(50))

    def __repr__(self):
        return f'<TidalTrack {self.track_name} by {self.artist_name}>'

class SpotifyTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    spotify_id = db.Column(db.String(255))
    artist_ids = db.Column(db.String(255))
    track_name = db.Column(db.String(255))
    album_name = db.Column(db.String(255))
    helper = db.Column(db.String(255))
    artist_name = db.Column(db.String(255))
    release_date = db.Column(db.String(255))
    duration_ms = db.Column(db.Integer)
    popularity = db.Column(db.Integer)
    added_by = db.Column(db.String(255))
    added_at = db.Column(db.String(255))
    genres = db.Column(db.String(1000))
    danceability = db.Column(db.Float)
    energy = db.Column(db.Float)
    key = db.Column(db.Integer)
    loudness = db.Column(db.Float)
    mode = db.Column(db.Integer)
    speechiness = db.Column(db.Float)
    acousticness = db.Column(db.Float)
    instrumentalness = db.Column(db.Float)
    liveness = db.Column(db.Float)
    valence = db.Column(db.Float)
    tempo = db.Column(db.Float)
    time_signature = db.Column(db.Integer)

    def __repr__(self):
        return f'<SpotifyTrack {self.track_name} by {self.artist_name}>'

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_uri = db.Column(db.String(100), nullable=False, unique=True)
    track_name = db.Column(db.String(200))
    artist_uri = db.Column(db.String(200))
    artist_name = db.Column(db.String(200))
    album_uri = db.Column(db.String(200))
    album_name = db.Column(db.String(200))
    album_artist_uri = db.Column(db.String(200))
    album_artist_name = db.Column(db.String(200))
    album_release_date = db.Column(db.String(100))
    album_image_url = db.Column(db.String(300))
    disc_number = db.Column(db.Integer)
    track_number = db.Column(db.Integer)
    track_duration_ms = db.Column(db.Integer)
    track_preview_url = db.Column(db.String(300))
    explicit = db.Column(db.Boolean)
    popularity = db.Column(db.Integer)
    isrc = db.Column(db.String(50))
    added_by = db.Column(db.String(100))
    added_at = db.Column(db.String(100))
    comment = db.Column(db.String(500))

    def __repr__(self):
        return f"<Track {self.track_name} by {self.artist_name}>"
    
class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    tracks = db.relationship('PlaylistTracks', back_populates='playlist')

class PlaylistTracks(db.Model):
    __tablename__ = 'playlist_tracks'
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('music_brainz_track.id'), primary_key=True)

    playlist = db.relationship('Playlist', back_populates='tracks')
    track = db.relationship('MusicBrainzTrack', back_populates='playlists')