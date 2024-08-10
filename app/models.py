from app import db

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(120), nullable=False)
    need_to_explore = db.Column(db.Boolean, nullable=False)
    looked_at = db.Column(db.Boolean, nullable=False)
    artist_playlist = db.Column(db.Boolean, nullable=False)
    one_of_each = db.Column(db.String(120), nullable=True)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Artist {self.artist_name}>'

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