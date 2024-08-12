from flask_migrate import Migrate, upgrade, migrate, init
from app import app, db
import os

migrate_obj = Migrate(app, db)  # Initialize the Migrate object

with app.app_context():
    # Check if the migrations directory exists
    migrations_path = os.path.join(os.path.dirname(__file__), 'migrations')
    if not os.path.exists(migrations_path):
        init()  # Initialize the migrations directory

    # Generate migration scripts
    migrate()

    # Apply the migrations
    upgrade()

    print("Migration and upgrade complete.")
