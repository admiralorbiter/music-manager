from flask import Flask
from flask_migrate import Migrate, upgrade
from app import app, db
import os

# Initialize Flask-Migrate
migrate = Migrate(app, db)

def run_migrations():
    with app.app_context():
        # Apply the migrations
        upgrade()

        print("Migration and upgrade complete.")

if __name__ == '__main__':
    run_migrations()  # This will run the migrations
    app.run()  # Then run the app if needed
