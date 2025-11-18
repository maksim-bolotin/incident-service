"""
Подключение к базе данных PostgreSQL.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.models import Base

# Настройка подключения к БД
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://incidents_user:incidents_password@localhost:5432/incidents_db"
)

# Создаём подключение к БД
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db() -> None:
    """
    Создаёт все таблицы в БД. Вызывается при старте приложения.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Генератор сессий БД дляиспользования в эндпоинтах.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
