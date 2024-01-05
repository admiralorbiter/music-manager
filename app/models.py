from app import db

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

    def __repr__(self):
        return f"<Track {self.track_name} by {self.artist_name}>"