import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load .env file from project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "olist_ecommerce")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Global engine instance
engine = create_engine(DATABASE_URL)


def get_engine():
    """Returns the SQLAlchemy engine for PostgreSQL database connection."""
    return engine


def test_connection():
    """Tests the database connection and prints the status."""
    try:
        with engine.connect() as conn:
            print("Connected successfully to PostgreSQL database!")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


if __name__ == "__main__":
    test_connection()