from flask import render_template, request, url_for
from app import app, db
import pandas as pd
from app.models import Artist, SpotifyTrack, TidalTrack

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artists_overview', methods=['GET'])
def artists_overview():
    # Get the current page number from the query string (default to 1 if not provided)
    page = request.args.get('page', 1, type=int)
    per_page = 30  # Set the number of artists to display per page

    search = request.args.get('search', '')

    if search:
        # Filter artists by name using the search term
        query = Artist.query.filter(Artist.artist_name.ilike(f'%{search}%'))
    else:
        # Show all artists if no search term is provided
        query = Artist.query

    # Paginate the query
    artists = Artist.query.filter_by(hide=False).order_by(Artist.order).all()
    artists_pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    artists = artists_pagination.items  # Get the artists for the current page
    # Pass the artists and the pagination object to the template
    return render_template('artists_overview.html', artists=artists, pagination=artists_pagination)

@app.route('/tidal_overview', methods=['GET'])
def tidal_overview():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    if search:
        # Filter tidal tracks by track name or artist name using the search term
        tracks = TidalTrack.query.filter(
            TidalTrack.track_name.ilike(f'%{search}%') | 
            TidalTrack.artist_name.ilike(f'%{search}%')
        ).paginate(page=page, per_page=10)
    else:
        # Show all tidal tracks if no search term is provided
        tracks = TidalTrack.query.paginate(page=page, per_page=10)

    return render_template('tidal_tracks.html', tracks=tracks.items, pagination=tracks, search=search)

@app.route('/update_artist', methods=['POST'])
def update_artist():
    artist_name = request.form.get('artist_name')
    need_to_explore = request.form.get('need_to_explore') == 'on'
    looked_at = request.form.get('looked_at') == 'on'
    artist_playlist = request.form.get('artist_playlist') == 'on'

    artist = Artist.query.filter_by(artist_name=artist_name).first()
    if artist:
        artist.need_to_explore = need_to_explore
        artist.looked_at = looked_at
        artist.artist_playlist = artist_playlist
        db.session.commit()
        print(f"Updated artist: {artist_name}")
    
    return '', 204

@app.route('/edit_field/<int:artist_id>/<string:field>', methods=['GET'])
def edit_field(artist_id, field):
    artist = Artist.query.get_or_404(artist_id)
    value = getattr(artist, field)
    return render_template('edit_field.html', artist=artist, field_name=field, value=value)

@app.route('/artist/<int:artist_id>/tracks', methods=['GET'])
def artist_tracks(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    sort_by = request.args.get('sort', 'album_name')  # Default sort by album name
    order = request.args.get('order', 'asc')  # Default order is ascending

    # Fetching sorted Spotify tracks
    if sort_by == 'album_name':
        if order == 'asc':
            spotify_tracks = SpotifyTrack.query.filter_by(artist_name=artist.artist_name).order_by(SpotifyTrack.album_name.asc()).all()
            tidal_tracks = TidalTrack.query.filter_by(artist_name=artist.artist_name).order_by(TidalTrack.album_name.asc()).all()
        else:
            spotify_tracks = SpotifyTrack.query.filter_by(artist_name=artist.artist_name).order_by(SpotifyTrack.album_name.desc()).all()
            tidal_tracks = TidalTrack.query.filter_by(artist_name=artist.artist_name).order_by(TidalTrack.album_name.desc()).all()

    # Identifying common and unique tracks
    spotify_track_names = {track.track_name for track in spotify_tracks}
    tidal_track_names = {track.track_name for track in tidal_tracks}

    common_tracks = spotify_track_names & tidal_track_names  # Intersection
    unique_spotify_tracks = spotify_track_names - tidal_track_names  # Spotify only
    unique_tidal_tracks = tidal_track_names - spotify_track_names  # Tidal only

    return render_template('artist_tracks.html', 
                           artist=artist, 
                           spotify_tracks=spotify_tracks, 
                           tidal_tracks=tidal_tracks,
                           common_tracks=common_tracks,
                           unique_spotify_tracks=unique_spotify_tracks,
                           unique_tidal_tracks=unique_tidal_tracks,
                           sort_by=sort_by, 
                           order=order)

@app.route('/reorder_artists', methods=['POST'])
def reorder_artists():
    order = request.json.get('order', [])
    for index, artist_id in enumerate(order):
        artist = Artist.query.get(int(artist_id))
        if artist:
            artist.order = index + 1  # Assuming you have an 'order' column in your model
    db.session.commit()
    return '', 204

@app.route('/hide_artist', methods=['POST'])
def hide_artist():
    data = request.get_json()
    artist_id = data.get('artist_id')
    artist = Artist.query.get_or_404(artist_id)
    
    artist.hide = True  # Set the hide flag to True
    db.session.commit()
    return '', 204

@app.route('/save_field/<int:artist_id>/<string:field>', methods=['POST'])
def save_field(artist_id, field):
    artist = Artist.query.get_or_404(artist_id)
    new_value = request.form['value']
    print(f"Received new value for {field}: {new_value}") 
    setattr(artist, field, new_value)
    print(artist, field, new_value)
    db.session.commit()
    # return f"<span hx-get=\"{url_for('edit_field', artist_id=artist.id, field=field)}\" hx-trigger=\"click\" hx-swap=\"outerHTML\">{new_value}</span>"
    return f"",204

@app.route('/spotify_overview', methods=['GET'])
def spotify_overview():
    # Get the current page number from the query string (default to 1 if not provided)
    page = request.args.get('page', 1, type=int)
    per_page = 50  # Set the number of tracks to display per page

    search = request.args.get('search', '')

    if search:
        # Filter tracks by name or artist using the search term
        query = SpotifyTrack.query.filter(
            (SpotifyTrack.track_name.ilike(f'%{search}%')) |
            (SpotifyTrack.artist_name.ilike(f'%{search}%'))
        )
    else:
        # Show all tracks if no search term is provided
        query = SpotifyTrack.query

    # Paginate the query
    tracks_pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tracks = tracks_pagination.items  # Get the tracks for the current page

    # Pass the tracks and the pagination object to the template
    return render_template('spotify_overview.html', tracks=tracks, pagination=tracks_pagination)

def load_data():
    file_path = 'artists.csv'
    data = pd.read_csv(file_path)
    
    for _, row in data.iterrows():
        artist = Artist(
            artist_name=row['Artist Name(s)'],
            need_to_explore=row['Need to Explore'],
            looked_at=row['Looked At'],
            artist_playlist=row['Artist Playlist'],
            one_of_each=row.get('One of Each', ''),
            notes=row.get('Notes', '')
        )
        db.session.add(artist)
    db.session.commit()

def load_tidal_data():
    file_path = 'tidal.csv'  # Update this to the path of your CSV file
    data = pd.read_csv(file_path)

    for _, row in data.iterrows():
        tidal_track = TidalTrack(
            track_name=row['Track name'],
            artist_name=row['Artist name'],
            album_name=row['Album'],
            playlist_name=row['Playlist name'],
            type=row['Type'],
            isrc=row['ISRC'],
            tidal_id=row['Tidal - id']
        )
        db.session.add(tidal_track)
    
    try:
        db.session.commit()
        print("Tidal data successfully loaded.")
    except Exception as e:
        db.session.rollback()
        print(f"Error loading Tidal data: {e}")

def load_spotify_data():
    file_path = 'spotify.csv'
    # Load the data
    data = pd.read_csv(file_path)
    
    for index, row in data.iterrows():
        try:
            # Manually extract each field
            spotify_id = row['Spotify ID']
            artist_ids = row['Artist IDs']
            track_name = row['Track Name']
            album_name = row['Album Name']
            helper = row['Helper']
            artist_name = row['Artist Name(s)']
            release_date = row['Release Date']
            duration_ms = int(row['Duration (ms)'])
            popularity = int(row['Popularity'])
            added_by = row['Added By']
            added_at = row['Added At']
            genres = row['Genres']
            danceability = float(row['Danceability'])
            energy = float(row['Energy'])
            key = int(row['Key'])
            loudness = float(row['Loudness'])
            mode = int(row['Mode'])
            speechiness = float(row['Speechiness'])
            acousticness = float(row['Acousticness'])
            instrumentalness = float(row['Instrumentalness'])
            liveness = float(row['Liveness'])
            valence = float(row['Valence'])
            tempo = float(row['Tempo'])
            time_signature = int(row['Time Signature'])

            # Create the SpotifyTrack object
            track = SpotifyTrack(
                spotify_id=spotify_id,
                artist_ids=artist_ids,
                track_name=track_name,
                album_name=album_name,
                helper=helper,
                artist_name=artist_name,
                release_date=release_date,
                duration_ms=duration_ms,
                popularity=popularity,
                added_by=added_by,
                added_at=added_at,
                genres=genres,
                danceability=danceability,
                energy=energy,
                key=key,
                loudness=loudness,
                mode=mode,
                speechiness=speechiness,
                acousticness=acousticness,
                instrumentalness=instrumentalness,
                liveness=liveness,
                valence=valence,
                tempo=tempo,
                time_signature=time_signature
            )
            db.session.add(track)

        except ValueError as e:
            # Print out the row causing the error and the error message
            print(f"Error in row {index}: {row}")
            print(f"Error: {e}")
            continue

    # Try to commit the session
    try:
        db.session.commit()
    except Exception as commit_error:
        print(f"Commit error: {commit_error}")
        db.session.rollback()