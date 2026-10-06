import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

logger = logging.getLogger("smarterp.database")

def get_engine():
    db_url = settings.DATABASE_URL
    # If explicitly postgresql, test or handle gracefully
    if db_url.startswith("postgresql"):
        try:
            test_engine = create_engine(db_url, pool_pre_ping=True, connect_args={"connect_timeout": 3})
            # Try connecting
            with test_engine.connect():
                pass
            logger.info("Successfully connected to PostgreSQL database.")
            return test_engine
        except Exception as e:
            logger.warning(
                f"PostgreSQL connection to {db_url} failed ({e}). "
                f"Falling back to SQLite for local development: {settings.SQLITE_FALLBACK_URL}"
            )
            return create_engine(
                settings.SQLITE_FALLBACK_URL, 
                connect_args={"check_same_thread": False}
            )
    elif db_url.startswith("sqlite"):
        return create_engine(
            db_url, 
            connect_args={"check_same_thread": False}
        )
    return create_engine(db_url)

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
