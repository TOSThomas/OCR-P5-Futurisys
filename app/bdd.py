
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.engine import URL

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# Je vérifie que la base existe, sinon je la crée
url_projet = URL.create(
    "postgresql+psycopg2",
    username=user,
    password=password,
    host=host,
    port=port,
    database=database
)

try:
    engine = create_engine(url_projet)
    inspector = inspect(engine)
    
except Exception:
    engine = create_engine(URL.create(
        "postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=port,
        database="postgres"
    ))
    
    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(text(f'CREATE DATABASE "{database}"'))

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()