"""Database connection utilities."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://appuser:apppass123@localhost:5432/platform_db",
)

_engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
_SessionFactory = sessionmaker(bind=_engine)


def get_db_session() -> Session:
    """Return a new database session."""
    return _SessionFactory()
