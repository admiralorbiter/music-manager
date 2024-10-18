from flask_migrate import Migrate, upgrade, revision, current, init
from app import app, db
import os
from sqlalchemy.exc import OperationalError

migrate_obj = Migrate(app, db)  # Initialize the Migrate object

with app.app_context():
    # Check if the migrations directory exists
    migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_path):
        print("Initializing migrations directory...")
        init()  # Initialize the migrations directory

    # Check if there are any migrations to apply
    current_head = current()
    if current_head is None:
        print("No migrations found. Creating initial migration...")
        revision()
        print("Applying initial migration...")
    else:
        # Generate migration scripts
        print("Generating migration script...")
        revision()

    # Apply the migrations
    print("Applying migrations...")
    try:
        upgrade()
        print("Migration and upgrade complete.")
    except OperationalError as e:
        print(f"An error occurred during migration: {e}")
        print("You may need to manually adjust your database schema or migration scripts.")
