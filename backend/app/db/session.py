import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load the .env file (assuming session.py is run from a place that can see the root)
# A robust way is to point directly to the backend folder like we did in Alembic:
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Read the vault
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from the .env file!")

# The engine manages the database connections.
# echo=True prints all generated SQL to the console.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=False
)

# The session factory generates Session objects.
# autoflush=False ensures SQLAlchemy doesn't prematurely push uncommitted changes to the DB.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency to inject the session into my application (e.g., FastAPI endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()