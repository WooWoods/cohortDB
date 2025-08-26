import os
from peewee import SqliteDatabase
from dotenv import load_dotenv

load_dotenv()

# Construct an absolute path to the database file
# This assumes the script is run from the project root or the 'backend' directory
DATABASE_URL = os.getenv("DATABASE_URL", "backend/cohort.db")
DB_PATH = os.path.abspath(DATABASE_URL)

# Ensure the directory for the database exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

db = SqliteDatabase(DB_PATH)
