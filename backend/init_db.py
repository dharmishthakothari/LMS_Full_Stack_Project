import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base
import app.models  # Ensure all models are registered with Base

def init_database():
    print("Connecting to database and creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Successfully created all tables in database!")

    # Verify tables
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Total tables created ({len(tables)}):")
    for t in sorted(tables):
        print(f" - {t}")

if __name__ == "__main__":
    init_database()
