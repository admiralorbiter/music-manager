from app import app, db
from app.models import Artist

def update_main_artist():
    with app.app_context():
        try:
            # Update all records where main_artist is NULL
            db.session.execute(db.text("UPDATE artist SET main_artist = artist_name WHERE main_artist IS NULL"))
            db.session.commit()
            print("Successfully updated main_artist for all records where it was NULL.")

            # Verify the update
            null_count = db.session.query(Artist).filter(Artist.main_artist == None).count()
            print(f"Number of records with NULL main_artist after update: {null_count}")

        except Exception as e:
            db.session.rollback()
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    update_main_artist()
