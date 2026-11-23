import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import (create_engine, text, Integer, Float, DateTime, JSON, func)
from sqlalchemy.engine import URL
from sqlalchemy.orm import (DeclarativeBase, Mapped, mapped_column, sessionmaker)

load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")
sslmode = os.getenv("DB_SSLMODE", "prefer")

url_projet = URL.create(
    "postgresql+psycopg2",
    username=user,
    password=password,
    host=host,
    port=int(port) if port else 5432,
    database=database,
    query={"sslmode": sslmode},
)

engine = create_engine(
    url_projet,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass

class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    date_prediction: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    prediction: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    probabilite_depart: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    probabilite_rester: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    donnees_salarie: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
    )

def create_database_if_not_exists():
    if not database:
        raise ValueError("DB_NAME absent")

    url_admin = URL.create(
        "postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=int(port) if port else 5432,
        database="postgres",
        query={"sslmode": sslmode},
    )

    admin_engine = create_engine(
        url_admin,
        isolation_level="AUTOCOMMIT",
    )

    try:
        with admin_engine.connect() as connection:

            result = connection.execute(text("SELECT 1 FROM pg_database WHERE datname = :database"), {"database": database})

            if result.scalar() is None:
                quoted_database = (admin_engine.dialect.identifier_preparer.quote(database))
                connection.execute(text(f"CREATE DATABASE {quoted_database}"))
                print(f"BDD créée.")

    finally:
        admin_engine.dispose()

def init_db():
    Base.metadata.create_all(bind=engine)

def setup_database():
    create_database_if_not_exists()
    init_db()

def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.scalar()